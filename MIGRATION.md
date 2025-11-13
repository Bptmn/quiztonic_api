# Migration Guide: RAQAM-API → QuizTonic API

Ce guide explique comment migrer depuis l'ancien projet `RAQAM-API` vers le nouveau projet `quiztonic_api`.

## 📋 Vue d'ensemble

L'API a été séparée du projet principal dans un repository GitHub indépendant pour:
- Meilleure séparation des responsabilités
- Déploiements indépendants
- Gestion de version indépendante
- Sécurité améliorée

## 🔄 Changements Principaux

### Nom du Projet
- **Ancien**: `RAQAM-API`
- **Nouveau**: `quiztonic_api`

### Noms AWS
- **Fonction Lambda**: `raqam-api` → `quiztonic-api`
- **Rôle IAM**: `raqam-lambda-role` → `quiztonic-lambda-role`
- **Profil AWS**: `raqam-deployer` → `quiztonic-deployer`
- **Image Docker**: `raqam-lambda` → `quiztonic-api-lambda`

### Repository GitHub
- **Ancien**: Répertoire `RAQAM-API/` dans le repo principal
- **Nouveau**: Repository GitHub séparé `quiztonic_api`

## 📦 Étapes de Migration

### 1. Créer le Nouveau Repository GitHub

```bash
# Sur GitHub, créer un nouveau repository:
# - Nom: quiztonic_api
# - Description: QuizTonic API - Backend service for quiz and flashcard generation
# - Public/Private selon vos préférences
```

### 2. Initialiser le Repository Local

```bash
cd /Users/baptisteveyrard/Local/GitHub/RAQAM/quiztonic_api

# Initialiser Git
git init
git add .
git commit -m "Initial commit: QuizTonic API separated from main project"

# Ajouter le remote GitHub
git remote add origin https://github.com/Bptmn/quiztonic_api.git
git branch -M main
git push -u origin main
```

### 3. Mettre à Jour la Configuration AWS

Si vous avez déjà déployé l'ancienne version, vous pouvez soit:
- **Option A**: Garder l'ancienne fonction Lambda et mettre à jour le code
- **Option B**: Créer une nouvelle fonction Lambda avec le nouveau nom

#### Option A: Mise à jour de l'existante

```bash
# Modifier deploy_lambda_url.sh temporairement pour utiliser l'ancien nom
FUNCTION_NAME="raqam-api"  # Garder l'ancien nom
```

#### Option B: Nouvelle fonction (recommandé)

```bash
# Configurer le nouveau profil AWS
aws configure --profile quiztonic-deployer

# Déployer avec le nouveau script
./deploy_lambda_url.sh
```

### 4. Mettre à Jour l'Application Flutter

Dans le projet `quiztonic` (application Flutter):

1. **Mettre à jour l'URL de l'API** dans `lib/app_constants.dart` ou où l'URL est définie
2. **Mettre à jour la documentation** pour référencer le nouveau repository
3. **Créer un fichier `API_DEPENDENCIES.md`** pour documenter la dépendance

### 5. Nettoyer l'Ancien Projet

Une fois la migration terminée et testée:

```bash
# Dans le projet principal quiztonic
git rm -r RAQAM-API/
git commit -m "Remove RAQAM-API: migrated to separate repository quiztonic_api"
```

## 🔗 Documentation à Mettre à Jour

- [ ] README.md dans quiztonic_api
- [ ] API_CONTRACT.md (créé dans quiztonic_api)
- [ ] Mise à jour de l'app Flutter avec nouvelle URL
- [ ] Documentation du projet principal quiztonic

## ✅ Checklist de Migration

- [ ] Nouveau repository GitHub créé
- [ ] Code initialisé et pushé
- [ ] Configuration AWS mise à jour
- [ ] Déploiement testé
- [ ] Application Flutter mise à jour
- [ ] Tests de bout en bout réussis
- [ ] Ancien code supprimé du projet principal
- [ ] Documentation mise à jour

## 🆘 Support

En cas de problème:
1. Vérifier que tous les fichiers ont été copiés correctement
2. Vérifier les permissions des scripts (chmod +x)
3. Vérifier la configuration AWS
4. Consulter les logs CloudWatch pour les erreurs Lambda

## 📚 Ressources

- [API Contract Documentation](API_CONTRACT.md)
- [Deployment Guide](RAQAM_LAMBDA_DEPLOYMENT_GUIDE.md)
- [QuizTonic Mobile App](https://github.com/Bptmn/quiztonic)

