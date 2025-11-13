#!/usr/bin/env python3
"""
Script de test pour Lambda Function URL RAQAM
Teste l'API via l'URL publique de la Lambda
"""
import requests
import json
import time
from datetime import datetime

def test_lambda_function_url(function_url):
    """Teste la Lambda Function URL RAQAM"""
    
    print(f"🧪 Test de la Lambda Function URL: {function_url}")
    print("=" * 70)
    
    # Tests à effectuer
    test_cases = [
        {
            "name": "Test Wikipedia Anglais",
            "payload": {
                "data": {
                    "url": "https://en.wikipedia.org/wiki/Machine_learning",
                    "num_questions": 4,
                    "num_choices": 4,
                    "generate_flashcards": True
                }
            },
            "expected_language": "English"
        },
        {
            "name": "Test Wikipedia Français",
            "payload": {
                "data": {
                    "url": "https://fr.wikipedia.org/wiki/Bordeaux",
                    "num_questions": 3,
                    "num_choices": 4,
                    "generate_flashcards": True
                }
            },
            "expected_language": "French"
        },
        {
            "name": "Test Contenu Texte Français",
            "payload": {
                "data": {
                    "text_content": """
                    L'intelligence artificielle est un domaine de l'informatique qui vise à créer 
                    des systèmes capables d'effectuer des tâches qui nécessitent normalement 
                    l'intelligence humaine. Elle comprend l'apprentissage automatique, le 
                    traitement du langage naturel et la vision par ordinateur.
                    """,
                    "num_questions": 3,
                    "num_choices": 4,
                    "generate_flashcards": True
                }
            },
            "expected_language": "French"
        },
        {
            "name": "Test Contenu Texte Anglais",
            "payload": {
                "data": {
                    "text_content": """
                    Machine learning is a subset of artificial intelligence that focuses on 
                    algorithms that can learn from data. It includes supervised learning, 
                    unsupervised learning, and reinforcement learning techniques.
                    """,
                    "num_questions": 3,
                    "num_choices": 4,
                    "generate_flashcards": True
                }
            },
            "expected_language": "English"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['name']}")
        print("-" * 50)
        
        try:
            # Appeler l'API
            start_time = time.time()
            response = requests.post(
                function_url,
                json=test_case['payload'],
                headers={'Content-Type': 'application/json'},
                timeout=60
            )
            end_time = time.time()
            
            duration = end_time - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                # Vérifier la structure de la réponse
                if 'quizName' in result:
                    print(f"✅ Quiz généré: {result['quizName']}")
                else:
                    print("⚠️  Pas de quiz généré")
                
                if 'flashCards' in result:
                    flashcard_count = len(result['flashCards'])
                    print(f"✅ Flashcards générées: {flashcard_count}")
                else:
                    print("⚠️  Pas de flashcards générées")
                
                # Vérifier la langue détectée
                if 'quizContext' in result:
                    detected_language = result['quizContext'].get('contentLanguage', 'Unknown')
                    print(f"🌍 Langue détectée: {detected_language}")
                    
                    if detected_language == test_case['expected_language']:
                        print("✅ Langue correcte!")
                    else:
                        print(f"❌ Langue incorrecte (attendu: {test_case['expected_language']})")
                else:
                    print("⚠️  Pas d'information de langue")
                
                # Afficher les métriques
                print(f"⏱️  Durée: {duration:.2f}s")
                
                if 'quizContext' in result:
                    context = result['quizContext']
                    if 'tokens' in context:
                        tokens = context['tokens']
                        print(f"🔢 Tokens: {tokens.get('total', 'N/A')}")
                    
                    if 'costs' in context:
                        costs = context['costs']
                        print(f"💰 Coût: {costs.get('total', 'N/A')}")
                
                results.append({
                    "test": test_case['name'],
                    "status": "SUCCESS",
                    "duration": duration,
                    "language": detected_language if 'quizContext' in result else "Unknown"
                })
                
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                print(f"📄 Réponse: {response.text}")
                results.append({
                    "test": test_case['name'],
                    "status": "HTTP_ERROR",
                    "error": f"HTTP {response.status_code}: {response.text}"
                })
                
        except requests.exceptions.Timeout:
            print("❌ Timeout - La requête a pris trop de temps")
            results.append({
                "test": test_case['name'],
                "status": "TIMEOUT",
                "error": "Request timeout"
            })
            
        except requests.exceptions.ConnectionError:
            print("❌ Erreur de connexion - Vérifiez l'URL")
            results.append({
                "test": test_case['name'],
                "status": "CONNECTION_ERROR",
                "error": "Connection error"
            })
            
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            results.append({
                "test": test_case['name'],
                "status": "EXCEPTION",
                "error": str(e)
            })
    
    # Résumé des résultats
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
    total_count = len(results)
    
    print(f"✅ Tests réussis: {success_count}/{total_count}")
    print(f"📈 Taux de réussite: {success_count/total_count*100:.1f}%")
    
    for result in results:
        status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
        print(f"{status_icon} {result['test']}: {result['status']}")
        if result['status'] == 'SUCCESS':
            print(f"   ⏱️  Durée: {result['duration']:.2f}s")
            print(f"   🌍 Langue: {result['language']}")
        elif 'error' in result:
            print(f"   ❌ Erreur: {result['error']}")
    
    print("\n🎯 Recommandations:")
    if success_count == total_count:
        print("✅ Tous les tests sont passés! Votre Lambda Function URL fonctionne parfaitement.")
        print("📱 Vous pouvez maintenant intégrer cette URL dans votre app:")
        print(f"   {function_url}")
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les logs CloudWatch.")
        print("📊 Console CloudWatch: https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups")
    
    return results

def test_cors(function_url):
    """Teste la configuration CORS"""
    print(f"\n🔍 Test de la configuration CORS")
    print("-" * 40)
    
    try:
        # Test OPTIONS request (preflight)
        response = requests.options(
            function_url,
            headers={
                'Origin': 'https://example.com',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
        )
        
        print(f"📡 OPTIONS request: {response.status_code}")
        
        # Vérifier les headers CORS
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        
        print("🔧 Headers CORS:")
        for header, value in cors_headers.items():
            if value:
                print(f"   ✅ {header}: {value}")
            else:
                print(f"   ❌ {header}: Non défini")
        
        if all(cors_headers.values()):
            print("✅ Configuration CORS correcte!")
        else:
            print("⚠️  Configuration CORS incomplète")
            
    except Exception as e:
        print(f"❌ Erreur CORS: {str(e)}")

def test_performance(function_url):
    """Teste les performances de l'API"""
    print(f"\n⚡ Test de performance")
    print("-" * 40)
    
    test_payload = {
        "data": {
            "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
            "num_questions": 2,
            "num_choices": 4,
            "generate_flashcards": False
        }
    }
    
    times = []
    
    for i in range(3):
        try:
            start_time = time.time()
            response = requests.post(
                function_url,
                json=test_payload,
                headers={'Content-Type': 'application/json'},
                timeout=60
            )
            end_time = time.time()
            
            duration = end_time - start_time
            times.append(duration)
            
            print(f"   Test {i+1}: {duration:.2f}s (Status: {response.status_code})")
            
        except Exception as e:
            print(f"   Test {i+1}: Erreur - {str(e)}")
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n📊 Statistiques:")
        print(f"   ⏱️  Temps moyen: {avg_time:.2f}s")
        print(f"   🚀 Temps minimum: {min_time:.2f}s")
        print(f"   🐌 Temps maximum: {max_time:.2f}s")
        
        if avg_time < 30:
            print("✅ Performance excellente!")
        elif avg_time < 60:
            print("✅ Performance correcte")
        else:
            print("⚠️  Performance à améliorer")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python test_lambda_url.py <function_url>")
        print("Example: python test_lambda_url.py https://abc123.lambda-url.us-east-1.on.aws/")
        sys.exit(1)
    
    function_url = sys.argv[1]
    
    # Test de l'API
    results = test_lambda_function_url(function_url)
    
    # Test CORS
    test_cors(function_url)
    
    # Test de performance
    test_performance(function_url)
    
    print(f"\n🎉 Tests terminés!")
    print(f"🌐 URL de votre API: {function_url}")
    print(f"📱 Intégrez cette URL dans votre app pour remplacer l'ancienne API")
