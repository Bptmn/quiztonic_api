# QuizTonic API Contract

This document describes the API contract for QuizTonic API. This contract defines the request/response formats, error handling, and versioning policy.

## 📡 Base URL

### Production
```
https://{lambda-url}.lambda-url.{region}.on.aws/
```

### Development
```
http://localhost:5050
```

## 🔄 API Versioning

- **Current Version**: `v1.0.0`
- **Versioning Strategy**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Breaking Changes**: Will result in new MAJOR version
- **Backward Compatibility**: Minor and patch versions maintain backward compatibility

## 📨 Request Format

### Endpoint
```
POST /
```

### Headers
```
Content-Type: application/json
```

### Request Body

```json
{
  "data": {
    "text_content": "string (optional)",
    "url": "string (optional)",
    "pdf_file": "string (base64 encoded, optional)",
    "num_questions": "number (required)",
    "num_choices": "number (required)",
    "generate_flashcards": "boolean (optional, default: false)"
  }
}
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text_content` | string | No* | Raw text content for quiz generation |
| `url` | string | No* | URL of web page to process |
| `pdf_file` | string (base64) | No* | Base64 encoded PDF file |
| `num_questions` | number | Yes | Number of questions to generate (min: 1, max: 50) |
| `num_choices` | number | Yes | Number of answer choices per question (min: 2, max: 6) |
| `generate_flashcards` | boolean | No | Whether to generate flashcards (default: false) |

*At least one of `text_content`, `url`, or `pdf_file` must be provided.

### Example Request

```json
{
  "data": {
    "text_content": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without explicit programming.",
    "num_questions": 5,
    "num_choices": 4,
    "generate_flashcards": true
  }
}
```

## 📤 Response Format

### Success Response (200 OK)

```json
{
  "quizName": "string",
  "questionCards": [
    {
      "questionText": "string",
      "questionChoices": ["string"],
      "questionAnswerIndex": "number",
      "answerExplanation": "string"
    }
  ],
  "flashcards": [
    {
      "front": "string",
      "back": "string"
    }
  ],
  "quizContext": {
    "contentSource": "string",
    "contentLanguage": "string",
    "contentLanguageCode": "string",
    "contentLength": "number",
    "chunkSize": "number",
    "chunkOverlap": "number",
    "nbChunks": "number",
    "generationModelName": "string",
    "embeddingModelName": "string",
    "hasEmbeddedChunks": "boolean",
    "tokens": {
      "prompts": "number",
      "responses": "number",
      "embeddings": "number",
      "total": "number"
    },
    "costs": {
      "prompts": "string ($)",
      "responses": "string ($)",
      "embeddings": "string ($)",
      "total": "string ($)"
    }
  }
}
```

### Response Fields

#### Quiz Data
- `quizName`: Generated name for the quiz
- `questionCards`: Array of multiple-choice questions
  - `questionText`: The question text
  - `questionChoices`: Array of answer choices
  - `questionAnswerIndex`: Index of the correct answer (0-based)
  - `answerExplanation`: Explanation of the correct answer
- `flashcards`: Array of flashcards (if requested)
  - `front`: Front side of the flashcard
  - `back`: Back side of the flashcard

#### Context Data
- `contentSource`: Source type ("text", "web_page", "pdf_file")
- `contentLanguage`: Human-readable language name
- `contentLanguageCode`: Language code (e.g., "en", "fr")
- `contentLength`: Total character count of input content
- `chunkSize`: Text chunk size used for processing
- `chunkOverlap`: Overlap between chunks
- `nbChunks`: Number of text chunks created
- `generationModelName`: LLM model used (e.g., "gpt-4o-mini")
- `embeddingModelName`: Embedding model used (e.g., "text-embedding-3-small")
- `hasEmbeddedChunks`: Whether vector embeddings were used
- `tokens`: Token usage statistics
- `costs`: Estimated cost breakdown

### Example Response

```json
{
  "quizName": "Machine Learning Fundamentals",
  "questionCards": [
    {
      "questionText": "What is machine learning?",
      "questionChoices": [
        "A subset of AI that enables computers to learn from data",
        "A programming language for AI",
        "A database system for AI",
        "A hardware component for AI"
      ],
      "questionAnswerIndex": 0,
      "answerExplanation": "Machine learning is indeed a subset of artificial intelligence that enables computers to learn and make decisions from data without explicit programming."
    }
  ],
  "flashcards": [
    {
      "front": "Machine Learning",
      "back": "A subset of artificial intelligence that enables computers to learn and make decisions from data without explicit programming."
    }
  ],
  "quizContext": {
    "contentSource": "text",
    "contentLanguage": "English",
    "contentLanguageCode": "en",
    "contentLength": 150,
    "chunkSize": 2000,
    "chunkOverlap": 100,
    "nbChunks": 1,
    "generationModelName": "gpt-4o-mini",
    "embeddingModelName": "text-embedding-3-small",
    "hasEmbeddedChunks": false,
    "tokens": {
      "prompts": 250,
      "responses": 180,
      "embeddings": 0,
      "total": 430
    },
    "costs": {
      "prompts": "0.000019 $",
      "responses": "0.000108 $",
      "embeddings": "0.000000 $",
      "total": "0.000127 $"
    }
  }
}
```

## ❌ Error Responses

### 400 Bad Request

```json
{
  "message": "string",
  "status_code": 400,
  "stack_trace": "string (optional)"
}
```

**Common Causes:**
- Missing required parameters
- Invalid parameter values
- No content source provided
- Content too short (< 500 characters)

### 422 Unprocessable Entity

```json
{
  "message": "string",
  "status_code": 422,
  "stack_trace": "string (optional)"
}
```

**Common Causes:**
- Invalid URL format
- Unsupported file format
- Content parsing errors

### 500 Internal Server Error

```json
{
  "message": "string",
  "status_code": 500,
  "stack_trace": "string (optional)"
}
```

**Common Causes:**
- OpenAI API errors
- Vector store errors
- Unexpected system errors

### Example Error Response

```json
{
  "message": "Must provide at least one data source argument (text_content, url, or pdf_file)",
  "status_code": 400
}
```

## 🔒 CORS Configuration

The API supports CORS for web applications:

```
Allow-Origin: *
Allow-Methods: POST, OPTIONS
Allow-Headers: Content-Type
```

## 📊 Rate Limiting

Currently, no rate limiting is enforced. However, it's recommended to:
- Implement client-side rate limiting
- Use exponential backoff for retries
- Monitor API usage and costs

## 🔐 Authentication

Currently, no authentication is required. For production deployments:
- Consider implementing API keys
- Use AWS API Gateway for additional security
- Implement request signing for sensitive operations

## 🧪 Testing

### cURL Example

```bash
curl -X POST https://{lambda-url}.lambda-url.{region}.on.aws/ \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "text_content": "Your content here",
      "num_questions": 5,
      "num_choices": 4,
      "generate_flashcards": true
    }
  }'
```

### Python Example

```python
import requests
import json

url = "https://{lambda-url}.lambda-url.{region}.on.aws/"
payload = {
    "data": {
        "text_content": "Your content here",
        "num_questions": 5,
        "num_choices": 4,
        "generate_flashcards": True
    }
}

response = requests.post(url, json=payload)
result = response.json()
print(json.dumps(result, indent=2))
```

### Dart/Flutter Example

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<Map<String, dynamic>> generateQuiz({
  required String textContent,
  int numQuestions = 5,
  int numChoices = 4,
  bool generateFlashcards = true,
}) async {
  final url = Uri.parse('https://{lambda-url}.lambda-url.{region}.on.aws/');
  final response = await http.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: json.encode({
      'data': {
        'text_content': textContent,
        'num_questions': numQuestions,
        'num_choices': numChoices,
        'generate_flashcards': generateFlashcards,
      }
    }),
  );

  if (response.statusCode == 200) {
    return json.decode(response.body);
  } else {
    throw Exception('API Error: ${response.statusCode}');
  }
}
```

## 📝 Changelog

### v1.0.0 (Current)
- Initial API release
- Support for text, URL, and PDF content
- Quiz and flashcard generation
- Multi-language support (English, French)
- Cost tracking and token monitoring

## 🔗 Related Documentation

- [QuizTonic API README](README.md)
- [Deployment Guide](RAQAM_LAMBDA_DEPLOYMENT_GUIDE.md)
- [QuizTonic Mobile App](https://github.com/Bptmn/quiztonic)

