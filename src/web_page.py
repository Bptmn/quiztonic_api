import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin
import time

from src.exception import WebPageException
from src.utils import is_content_rich

class WebPage():
    def __init__(self,
                 url):
        """
        Web page for which to extract text content         
        """
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

    def _is_valid_url(self, url):
        """Check if URL is valid and accessible"""
        try:
            parsed = urlparse(url)
            return all([parsed.scheme, parsed.netloc])
        except:
            return False

    def _make_request_with_retry(self, url, max_retries=3, timeout=10):
        """Make HTTP request with retry logic and better error handling"""
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    url, 
                    headers=self.headers, 
                    timeout=timeout,
                    allow_redirects=True,
                    verify=True
                )
                
                # Handle different status codes
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:  # Rate limited
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                elif response.status_code in [403, 404, 500, 502, 503, 504]:
                    raise WebPageException(message=f"Server error: {response.status_code} - {response.reason}")
                else:
                    raise WebPageException(message=f"HTTP error: {response.status_code} - {response.reason}")
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise WebPageException(message="Request timeout after multiple attempts")
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise WebPageException(message="Connection error - unable to reach the server")
            except requests.exceptions.RequestException as e:
                raise WebPageException(message=f"Request failed: {str(e)}")
        
        raise WebPageException(message="Max retries exceeded")

    def _remove_irrelevant_content(self, soup):
        """Remove navigation, advertising, and other irrelevant content"""
        # Remove script and style elements
        for element in soup(["script", "style", "noscript"]):
            element.decompose()
        
        # Remove navigation elements (but be more selective for educational sites)
        nav_selectors = [
            "header", "footer", 
            "[role='banner']", "[role='contentinfo']",
            "[role='complementary']", "[role='search']"
        ]
        
        for selector in nav_selectors:
            for element in soup.select(selector):
                element.decompose()
        
        # Remove common advertising and social media elements
        # Be more specific to avoid removing legitimate content
        ad_selectors = [
            "[class*='advertisement']", "[class*='banner']",
            "[class*='social-media']", "[class*='share-buttons']", 
            "[class*='follow-us']", "[class*='subscribe']", "[class*='newsletter']",
            "[id*='advertisement']", "[id*='banner']",
            "[id*='social-media']", "[id*='share-buttons']", 
            "[id*='follow-us']", "[id*='subscribe']", "[id*='newsletter']"
        ]
        
        for selector in ad_selectors:
            for element in soup.select(selector):
                element.decompose()
        
        # Remove forms (contact forms, search forms, etc.)
        for form in soup.find_all("form"):
            form.decompose()
        
        # Remove navigation bars and menus (but preserve main content)
        for nav in soup.find_all("nav"):
            nav.decompose()
        
        # Remove aside elements (sidebars, but be careful with Wikipedia infoboxes)
        for aside in soup.find_all("aside"):
            # For Wikipedia, preserve infoboxes which are in aside elements
            if not (aside.get("class") and any("infobox" in cls.lower() for cls in aside.get("class", []))):
                aside.decompose()
        
        # Remove elements with very little text content (likely navigation or ads)
        # But be more lenient for educational content
        for element in soup.find_all(["div", "span", "p"]):
            text = element.get_text(strip=True)
            if text and len(text) < 10:  # Reduced threshold
                # Check if it contains mostly links or navigation-like content
                links = element.find_all("a")
                if len(links) > len(text.split()) * 0.7:  # More lenient threshold
                    element.decompose()

    def _extract_main_content(self, soup):
        """Extract main content using multiple strategies"""
        # Strategy 1: Look for semantic HTML5 elements
        semantic_selectors = [
            "article", "main", "[role='main']",
            "[id='content']", "[id='main']", "[id='article']",
            "[class*='content']", "[class*='main']", "[class*='article']",
            "[class*='post']", "[class*='entry']"
        ]
        
        for selector in semantic_selectors:
            elements = soup.select(selector)
            if elements:
                # Return the largest semantic element
                main_element = max(elements, key=lambda x: len(x.get_text(strip=True)))
                return main_element
        
        # Strategy 2: Look for Wikipedia-specific content
        # Wikipedia has specific patterns we can target
        wikipedia_selectors = [
            "[id='mw-content-text']",  # Wikipedia main content
            "[class*='mw-content']",   # Wikipedia content classes
            "[class*='mw-parser']"    # Wikipedia parser output
        ]
        
        for selector in wikipedia_selectors:
            elements = soup.select(selector)
            if elements:
                main_element = max(elements, key=lambda x: len(x.get_text(strip=True)))
                if len(main_element.get_text(strip=True)) > 200:  # Ensure substantial content
                    return main_element
        
        # Strategy 3: Find the div with the most text content
        divs = soup.find_all("div")
        if divs:
            # Filter out divs that are likely navigation or ads
            content_divs = []
            for div in divs:
                text = div.get_text(strip=True)
                if len(text) > 100:  # Minimum content length
                    # Check if it's not mostly links
                    links = div.find_all("a")
                    link_text_ratio = sum(len(link.get_text(strip=True)) for link in links) / len(text) if text else 0
                    if link_text_ratio < 0.4:  # Less than 40% links (more lenient)
                        content_divs.append(div)
            
            if content_divs:
                return max(content_divs, key=lambda x: len(x.get_text(strip=True)))
        
        # Strategy 4: Fallback to body content
        return soup.find("body") or soup

    def _clean_text(self, text):
        """Clean and normalize extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common web artifacts
        text = re.sub(r'Cookie\s+Policy|Privacy\s+Policy|Terms\s+of\s+Service', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Skip\s+to\s+content|Skip\s+to\s+main', '', text, flags=re.IGNORECASE)
        
        # Remove email patterns and phone numbers (likely contact info)
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        return text.strip()

    def extract_text(self):
        """
        Extracts the text from a web page by scraping page and parsing html
        content to get relevant text        
        """
        # Validate URL
        if not self._is_valid_url(self.url):
            raise WebPageException(message="Invalid URL format")
        
        try:
            # Make request with retry logic
            response = self._make_request_with_retry(self.url)
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Remove irrelevant content
            self._remove_irrelevant_content(soup)
            
            # Extract main content
            main_content = self._extract_main_content(soup)
            
            if not main_content:
                raise WebPageException(message="No main content found on the page")
            
            # Extract and clean text
            text = main_content.get_text(separator="\n", strip=True)
            text = self._clean_text(text)
            
            # Validate content quality
            if not is_content_rich(text, min_length=200, min_sentences=3):
                raise WebPageException(message="Insufficient quality content extracted from the page. The page may contain mostly navigation, ads, or other non-educational content.")
            
            return text
            
        except WebPageException:
            raise
        except Exception as e:
            raise WebPageException(message=f"Unexpected error during content extraction: {str(e)}")

