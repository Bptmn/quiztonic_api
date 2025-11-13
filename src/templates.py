# OBSOLÈTE: Ces templates sont maintenant gérés dynamiquement par src/language_detection.py
# Ce fichier est conservé pour la compatibilité avec l'ancien code mais n'est plus utilisé.

question_prompt_template = """
You are a helpful assistant. Based on the following content, generate {num_questions} detailed multiple-choice questions that tests understanding of the material. 

Content:
{content}

Make the questions specific and ensure it relates directly to the provided material. Include:
- A question
- Four choices (one correct and three plausible distractors)
- The correct answer
- An explanation

IMPORTANT: Generate ALL content (questions, choices, explanations) in ENGLISH.

Provide a general quiz name about this content
"""

flashcards_prompt_template = """
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