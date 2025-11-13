from src.raqam import QuizGenerator
from src.quiz_config import QuizConfig
from src.utils import load_config

def main():
    """Exemple d'utilisation de RAQAM avec du contenu texte"""
    config = load_config()
    
    # Exemple de contenu texte
    text_content = """
    L'intelligence artificielle est un domaine de l'informatique qui vise à créer 
    des systèmes capables d'effectuer des tâches qui nécessitent normalement 
    l'intelligence humaine. Elle comprend l'apprentissage automatique, le 
    traitement du langage naturel et la vision par ordinateur.
    """
    
    # Configuration du quiz
    quiz_config = QuizConfig(**config["base_quiz_config"])       
    quiz_config.parse_input_data({
        "text_content": text_content, 
        "num_questions": 4, 
        "num_choices": 4
    }) 
    
    # Génération du quiz
    quiz_generator = QuizGenerator(**quiz_config.__dict__)
    quiz = quiz_generator.generate_quiz()
    quiz_context = quiz_generator.get_context()
    
    print("Quiz généré:")
    print(quiz.json())
    print("\nContexte:")
    print(quiz_context)

if __name__ == "__main__":
    main()
