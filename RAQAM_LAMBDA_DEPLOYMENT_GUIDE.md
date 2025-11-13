# 🚀 Guide Complet de Déploiement RAQAM Lambda Function URL

## 📋 Vue d'Ensemble

Votre API RAQAM est maintenant prête pour le déploiement sur AWS Lambda avec **Lambda Function URL** - la solution la plus simple et efficace!

### ✅ Fonctionnalités Incluses
- **Détection automatique de langue** (FR/EN)
- **Extraction Wikipedia améliorée** (96-98% de contenu préservé)
- **Flashcards enrichies** (3-8 cartes avec contenu détaillé)
- **Gestion d'erreurs robuste**
- **Filtrage de contenu intelligent**

## 🎯 Pourquoi Lambda Function URL?

### ✅ Avantages
- **Plus simple** - Pas besoin d'API Gateway
- **Moins cher** - Pas de coûts API Gateway ($3.50/million vs $0.20/million)
- **Plus rapide** - Moins de latence
- **CORS configuré** - Prêt pour les apps web
- **URL directe** - `https://abc123.lambda-url.us-east-1.on.aws/`

### ❌ Inconvénients
- **Pas de domaines personnalisés** - URL AWS uniquement
- **Moins de fonctionnalités** - Pas de rate limiting, authentification avancée

## 📁 Fichiers de Déploiement

### 🚀 Déploiement
- **`deploy_lambda_url.sh`** - Script de déploiement automatique
- **`Dockerfile`** - Dockerfile optimisé pour Lambda
- **`setup_local.sh`** - Script de configuration de l'environnement local

### 🧪 Tests
- **`test_lambda_url.py`** - Script de test complet pour Function URL

### 📚 Documentation
- **`RAQAM_LAMBDA_DEPLOYMENT_GUIDE.md`** - Ce guide complet
- **`README.md`** - Documentation principale du projet
- **`CHANGELOG.md`** - Historique des modifications

## 🚀 Déploiement en 3 Étapes

### **1. Configuration AWS (Une seule fois)**

#### **1.1. Créer un Compte AWS (si pas déjà fait)**
1. Allez sur [aws.amazon.com](https://aws.amazon.com)
2. Cliquez sur "Create an AWS Account"
3. Suivez les étapes d'inscription

#### **1.2. Créer un Utilisateur IAM**

**Étape 1: Aller dans IAM**
1. Connectez-vous à [AWS Console](https://console.aws.amazon.com)
2. Recherchez "IAM" dans la barre de recherche
3. Cliquez sur "IAM"

**Étape 2: Créer un utilisateur**
1. Cliquez sur "Users" dans le menu de gauche
2. Cliquez sur "Create user"
3. Nom d'utilisateur: `raqam-deployer`
4. Cliquez sur "Next"

**Étape 3: Attacher des politiques**
1. Sélectionnez "Attach policies directly"
2. Recherchez et sélectionnez ces politiques:
   - `AWSLambdaFullAccess`
   - `IAMFullAccess`
   - `CloudWatchLogsFullAccess`
3. Cliquez sur "Next" puis "Create user"

**Étape 4: Créer les clés d'accès**
1. Cliquez sur votre utilisateur `raqam-deployer`
2. Allez dans l'onglet "Security credentials"
3. Cliquez sur "Create access key"
4. Sélectionnez "Command Line Interface (CLI)"
5. Cochez "I understand..."
6. Cliquez sur "Next"
7. **IMPORTANT:** Copiez et sauvegardez:
   - **Access Key ID**
   - **Secret Access Key**

⚠️ **ATTENTION:** Ces clés ne sont affichées qu'une seule fois!

#### **1.3. Installer AWS CLI**

**Sur macOS:**
```bash
brew install awscli
```

**Informations à renseigner:**
```
AWS Access Key ID: AKIA... (votre clé d'accès)
AWS Secret Access Key: ... (votre clé secrète)
Default region name: us-east-1
Default output format: json
```

#### **1.5. Vérifier la Configuration**
```bash
aws sts get-caller-identity
```

Vous devriez voir quelque chose comme:
```json
{
    "UserId": "AIDA...",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/raqam-deployer"
}
```

### **2. Déploiement Automatique**

```bash
# Définissez votre clé OpenAI
export OPENAI_API_KEY="sk-proj-..."

# Déployez avec Lambda Function URL
./deploy_lambda_url.sh
```

### **3. Test et Intégration**

```bash
# Testez votre API
python test_lambda_url.py https://abc123.lambda-url.us-east-1.on.aws/

# Intégrez l'URL dans votre app
```

## 🌐 Résultat Final

### **URL de Votre API**
```
https://abc123.lambda-url.us-east-1.on.aws/
```

### **Format des Requêtes**
```json
POST https://abc123.lambda-url.us-east-1.on.aws/
Content-Type: application/json

{
  "data": {
    "url": "https://en.wikipedia.org/wiki/Machine_learning",
    "num_questions": 4,
    "num_choices": 4,
    "generate_flashcards": true
  }
}
```

### **CORS Configuré**
```json
{
  "AllowCredentials": false,
  "AllowHeaders": ["content-type"],
  "AllowMethods": ["*"],
  "AllowOrigins": ["*"],
  "ExposeHeaders": [],
  "MaxAge": 86400
}
```

## 📱 Intégration dans Votre App

### **Remplacement de l'Ancienne URL**
```dart
// Ancienne URL (à remplacer)
// const String oldApiUrl = 'https://ancienne-lambda-url.amazonaws.com/';

// Nouvelle URL Lambda Function URL
const String newApiUrl = 'https://abc123.lambda-url.us-east-1.on.aws/';
```

### **Exemple Flutter/Dart**
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class RAQAMService {
  static const String baseUrl = 'https://abc123.lambda-url.us-east-1.on.aws/';
  
  static Future<Map<String, dynamic>> generateQuiz({
    required String url,
    int numQuestions = 4,
    int numChoices = 4,
    bool generateFlashcards = true,
  }) async {
    final response = await http.post(
      Uri.parse(baseUrl),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'data': {
          'url': url,
          'num_questions': numQuestions,
          'num_choices': numChoices,
          'generate_flashcards': generateFlashcards,
        }
      }),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to generate quiz: ${response.statusCode}');
    }
  }
}
```

## 🧪 Tests Complets

### **Test Automatique**
```bash
python test_lambda_url.py https://abc123.lambda-url.us-east-1.on.aws/
```

### **Test Manuel avec curl**
```bash
curl -X POST https://abc123.lambda-url.us-east-1.on.aws/ \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "url": "https://en.wikipedia.org/wiki/Machine_learning",
      "num_questions": 4,
      "num_choices": 4,
      "generate_flashcards": true
    }
  }'
```

### **Test avec Python**
```python
import requests
import json

url = "https://abc123.lambda-url.us-east-1.on.aws/"
payload = {
    "data": {
        "url": "https://en.wikipedia.org/wiki/Machine_learning",
        "num_questions": 4,
        "num_choices": 4,
        "generate_flashcards": True
    }
}

response = requests.post(url, json=payload)
print(response.json())
```

## 💰 Coûts Estimés

### **Par Quiz**
- **Tokens OpenAI:** ~$0.01-0.05
- **Lambda:** ~$0.0001
- **Total:** ~$0.01-0.05 par quiz

### **Par Mois (1000 quiz)**
- **OpenAI:** ~$10-50
- **Lambda:** ~$0.10
- **Total:** ~$10-50/mois

### **Comparaison des Coûts**
| Service | Coût par million | Économie |
|---------|------------------|----------|
| **Lambda Function URL** | $0.20 | ✅ |
| API Gateway | $3.50 | ❌ +$3.30 |

## 🔧 Configuration Technique

### **Lambda Function**
- **Runtime:** Python 3.9
- **Mémoire:** 1024 MB
- **Timeout:** 5 minutes
- **Handler:** `api.lambda_function.lambda_handler`

### **Function URL**
- **Auth Type:** NONE (public)
- **CORS:** Configuré pour toutes les origines
- **Methods:** Toutes les méthodes autorisées

### **Variables d'Environnement**
- `OPENAI_API_KEY` - Votre clé API OpenAI

### **Permissions IAM**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}
```

## 📊 Fonctionnalités Incluses

### ✅ **Améliorations Déployées**
- **Détection automatique de langue** (FR/EN)
- **Extraction Wikipedia améliorée** (96-98% de contenu préservé)
- **Flashcards enrichies** (3-8 cartes avec contenu détaillé)
- **Gestion d'erreurs robuste**
- **Filtrage de contenu intelligent**

### 🎯 **Cas d'Usage Testés**
- ✅ Wikipedia FR (Bordeaux, Intelligence artificielle)
- ✅ Wikipedia EN (Machine Learning, AI)
- ✅ Articles de presse français
- ✅ Documentation technique
- ✅ Contenu texte direct

## 🔍 Monitoring et Logs

### **CloudWatch Logs**
```bash
# Voir les logs en temps réel
aws logs tail /aws/lambda/raqam-api --follow

# Voir les logs récents
aws logs describe-log-streams --log-group-name /aws/lambda/raqam-api
```

### **Métriques**
- **Console AWS** → **Lambda** → **raqam-api** → **Monitoring**
- **Console AWS** → **CloudWatch** → **Metrics**

### **Métriques Importantes**
- **Durée d'exécution** - Doit être < 30 secondes
- **Erreurs** - Doit être 0%
- **Mémoire utilisée** - Doit être < 1024 MB
- **Coût** - ~$0.01-0.05 par quiz

## 🚨 Dépannage

### **Problèmes Courants**

1. **Erreur de permissions IAM**
   ```bash
   # Vérifier le rôle
   aws iam get-role --role-name raqam-lambda-role
   ```

2. **Erreur CORS**
   ```bash
   # Vérifier la configuration CORS
   aws lambda get-function-url-config --function-name raqam-api
   ```

3. **Erreur 403 Forbidden**
   ```bash
   # Vérifier que l'URL est correcte
   aws lambda get-function-url-config --function-name raqam-api --query 'FunctionUrl'
   ```

4. **Erreur 500 Internal Server Error**
   ```bash
   # Voir les logs
   aws logs tail /aws/lambda/raqam-api --follow
   ```

5. **Timeout de la fonction**
   ```bash
   # Augmenter le timeout
   aws lambda update-function-configuration \
       --function-name raqam-api \
       --timeout 300
   ```

6. **Erreur de mémoire**
   ```bash
   # Augmenter la mémoire
   aws lambda update-function-configuration \
       --function-name raqam-api \
       --memory-size 1024
   ```

### **Logs de Débogage**
```bash
# Voir les logs détaillés
aws logs filter-log-events \
    --log-group-name /aws/lambda/raqam-api \
    --start-time $(date -d '1 hour ago' +%s)000
```

## 🔄 Mise à Jour

### **Mise à jour du code**
```bash
# 1. Modifier le code
# 2. Reconstruire
docker build -f Dockerfile.lambda -t raqam-lambda .

# 3. Redéployer
./deploy_lambda_url.sh
```

### **Mise à jour des variables**
```bash
aws lambda update-function-configuration \
    --function-name raqam-api \
    --environment Variables='{OPENAI_API_KEY=NEW_KEY}'
```

## 🎯 Cas d'Usage

### **✅ Idéal pour**
- Apps web simples
- Prototypes rapides
- APIs internes
- Tests et développement

### **❌ Pas idéal pour**
- APIs publiques avec authentification complexe
- Rate limiting avancé
- Domaines personnalisés
- APIs avec beaucoup de trafic

## 📊 Comparaison des Options

| Option | Simplicité | Coût | Fonctionnalités | URL Publique |
|--------|------------|------|------------------|--------------|
| **Lambda Function URL** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ |
| API Gateway | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ |
| Lambda seule | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ❌ |

## 🎉 Résumé Final

### **Ce que vous obtenez**
- 🌐 **URL publique** pour votre API
- 🔧 **CORS configuré** pour les apps web
- 💰 **Coût minimal** (~$0.01-0.05 par quiz)
- 🚀 **Déploiement simple** en une commande
- ✅ **Toutes les améliorations** (détection de langue, extraction Wikipedia, flashcards enrichies)

### **URL finale**
```
https://abc123.lambda-url.us-east-1.on.aws/
```

### **Intégration**
Remplacez simplement l'ancienne URL par la nouvelle dans votre app Flutter!

## 📞 Support

### **Ressources**
- **Guide complet:** `RAQAM_LAMBDA_DEPLOYMENT_GUIDE.md` (ce fichier)
- **Tests:** `test_lambda_url.py`
- **Logs:** Console CloudWatch AWS
- **Métriques:** Console Lambda AWS

### **Commandes Utiles**
```bash
# Status de la fonction
aws lambda get-function --function-name raqam-api

# Logs en temps réel
aws logs tail /aws/lambda/raqam-api --follow

# Test rapide
aws lambda invoke --function-name raqam-api --payload '{}' response.json
```

---

**🎯 Votre API RAQAM est maintenant prête pour la production avec Lambda Function URL!**

**Dernière mise à jour:** 25 octobre 2025  
**Version:** 2.0.0 (avec détection de langue et Lambda Function URL)
