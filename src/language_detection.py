"""
Language detection and prompt localization for RAQAM
"""
import re
from collections import Counter

def detect_language(text):
    """
    Detect the language of the text content.
    Returns: 'fr' for French, 'en' for English, or 'en' as default
    
    @param text: Text content to analyze
    """
    # Remove common punctuation and numbers
    words = re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text.lower())
    
    if not words or len(words) < 20:
        return 'en'  # Default to English if not enough words
    
    # French-specific indicators
    french_indicators = {
        # Common French words
        'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'et', 'est', 'sont',
        'dans', 'pour', 'avec', 'par', 'sur', 'cette', 'ces', 'son', 'sa', 'ses',
        'qui', 'que', 'où', 'dont', 'nous', 'vous', 'ils', 'elles', 'leur', 'leurs',
        'être', 'avoir', 'faire', 'dire', 'aller', 'voir', 'savoir', 'pouvoir',
        'très', 'plus', 'aussi', 'mais', 'donc', 'ou', 'car', 'alors', 'ainsi',
        'à', 'été', 'fait', 'dit', 'peut', 'comme', 'tout', 'tous', 'toute', 'toutes'
    }
    
    # English-specific indicators
    english_indicators = {
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
        'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
        'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
        'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
        'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me'
    }
    
    # Count matches
    french_count = sum(1 for word in words if word in french_indicators)
    english_count = sum(1 for word in words if word in english_indicators)
    
    # Calculate ratios
    total_words = len(words)
    french_ratio = french_count / total_words if total_words > 0 else 0
    english_ratio = english_count / total_words if total_words > 0 else 0
    
    # Additional French-specific patterns
    french_patterns = [
        r'\bqu\'', r'\bd\'', r'\bl\'', r'\bm\'', r'\bt\'', r'\bs\'',  # French elision
        r'é|è|ê|ë|à|â|ù|û|ô|î|ï|ç',  # French accents
        r'\b(?:tion|sion|ment)\b'  # Common French endings
    ]
    
    french_pattern_matches = sum(len(re.findall(pattern, text.lower())) for pattern in french_patterns)
    
    # Decision logic
    if french_ratio > english_ratio * 1.2 or french_pattern_matches > 10:
        return 'fr'
    elif english_ratio > french_ratio * 1.2:
        return 'en'
    else:
        # If unclear, check for accented characters which are more common in French
        accent_count = len(re.findall(r'[éèêëàâäùûüôöîïç]', text.lower()))
        if accent_count > len(text) * 0.01:  # More than 1% accented chars
            return 'fr'
        return 'en'

def get_language_name(lang_code):
    """
    Get the full language name from code
    
    @param lang_code: Language code ('en' or 'fr')
    """
    language_names = {
        'en': 'English',
        'fr': 'French'
    }
    return language_names.get(lang_code, 'English')

def get_localized_prompts(language='en'):
    """
    Get localized prompt templates based on detected language
    
    @param language: Language code ('en' or 'fr')
    """
    if language == 'fr':
        question_prompt = """
Vous êtes un assistant pédagogique expert. En vous basant sur le contenu suivant, générez {num_questions} questions à choix multiples détaillées qui testent la compréhension du matériel.

Contenu:
{content}

Assurez-vous que les questions sont spécifiques et directement liées au contenu fourni. Incluez pour chaque question:
- Une question claire et précise
- Quatre choix de réponse (une correcte et trois distracteurs plausibles)
- La réponse correcte
- Une explication détaillée

IMPORTANT: Générez TOUT le contenu (questions, choix, explications) EN FRANÇAIS.

Fournissez également un nom général pour ce quiz en français.
"""

        flashcards_prompt = """
Vous êtes un créateur de contenu éducatif expert. En vous basant sur le contenu suivant, générez des fiches d'étude (flashcards) complètes qui capturent les concepts, termes et idées les plus importants.

Contenu:
{content}

Générez 3-8 fiches d'étude de haute qualité (selon la longueur du contenu) qui couvrent:
- La terminologie clé et les définitions
- Les concepts et principes importants
- Les faits et données critiques
- Les processus et procédures
- Les relations et connexions entre les idées

Pour chaque fiche, créez:
- Recto: Un terme, concept ou question clair et concis
- Verso: Une explication détaillée et informative qui fournit du contexte, des exemples et des informations supplémentaires

IMPORTANT: Générez TOUT le contenu (termes, définitions, explications) EN FRANÇAIS.

Assurez-vous que les fiches sont éducatives et complètes, et qu'elles seraient précieuses pour étudier et comprendre le matériel.
"""

        retrieval_query = """
Extraire un contenu détaillé et spécifique du document pour générer des questions.
"""

    else:  # Default to English
        question_prompt = """
You are a helpful assistant. Based on the following content, generate {num_questions} detailed multiple-choice questions that tests understanding of the material.

Content:
{content}

Make the questions specific and ensure it relates directly to the provided material. Include:
- A question
- Four choices (one correct and three plausible distractors)
- The correct answer
- An explanation

IMPORTANT: Generate ALL content (questions, choices, explanations) in ENGLISH.

Provide a general quiz name about this content.
"""

        flashcards_prompt = """
You are an expert educational content creator. Based on the following content, generate comprehensive flashcards that capture the most important concepts, terms, and ideas.

Content:
{content}

Generate 3-8 high-quality flashcards (according to the length of the content) that cover:
- Key terminology and definitions
- Important concepts and principles
- Critical facts and data points
- Processes and procedures
- Relationships and connections between ideas

For each flashcard, create:
- Front: A clear, concise term, concept, or question
- Back: A detailed, informative explanation that provides context, examples, and additional insights

IMPORTANT: Generate ALL content (terms, definitions, explanations) in ENGLISH.

Make the flashcards educational and comprehensive, ensuring they would be valuable for studying and understanding the material.
"""

        retrieval_query = """
Extract detailed and specific content from the document to generate questions.
"""

    return {
        'question_prompt': question_prompt,
        'flashcards_prompt': flashcards_prompt,
        'retrieval_query': retrieval_query
    }
