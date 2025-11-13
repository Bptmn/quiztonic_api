#!/bin/bash

# Script de configuration de l'environnement de développement local
# Utilise exactement les mêmes contraintes que l'environnement de production

set -e

echo "🚀 Configuration de l'environnement de développement RAQAM-API"
echo "================================================================"

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "requirements.txt" ] || [ ! -f "constraints.txt" ]; then
    echo "❌ Erreur: Les fichiers requirements.txt et constraints.txt doivent être présents"
    exit 1
fi

# Vérifier la version Python disponible
echo "🔍 Vérification de la version Python..."
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo "✅ Python 3.11 trouvé"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    if [[ "$PYTHON_VERSION" == "3.11" ]]; then
        PYTHON_CMD="python3"
        echo "✅ Python 3.11 trouvé (python3)"
    else
        echo "⚠️  Python 3.11 non trouvé, utilisation de $PYTHON_VERSION"
        echo "   Pour une compatibilité parfaite, installez Python 3.11"
        PYTHON_CMD="python3"
    fi
else
    echo "❌ Python 3 non trouvé"
    exit 1
fi

# Créer un environnement virtuel
echo "📦 Création de l'environnement virtuel avec $PYTHON_CMD..."
$PYTHON_CMD -m venv venv

# Activer l'environnement virtuel
echo "🔌 Activation de l'environnement virtuel..."
source venv/bin/activate

# Mettre à jour pip
echo "⬆️  Mise à jour de pip..."
pip install --upgrade pip

# Installer les dépendances avec les mêmes contraintes que la production
echo "📥 Installation des dépendances avec les contraintes de production..."
pip install -r requirements.txt --constraint constraints.txt

# Vérifier les dépendances
echo "✅ Vérification des dépendances..."
pip check

echo ""
echo "================================================================"
echo "✅ Environnement de développement configuré avec succès!"
echo ""
echo "🔌 Pour activer l'environnement virtuel:"
echo "   source venv/bin/activate"
echo ""
echo "🧪 Pour tester votre code:"
echo "   python -m pytest"
echo "   # ou"
echo "   python api/api.py"
echo ""
echo "🔌 Pour désactiver l'environnement:"
echo "   deactivate"
echo ""
echo "⚠️  Cet environnement utilise EXACTEMENT les mêmes versions"
echo "   que l'environnement de production (contrôlé par constraints.txt)"
echo "================================================================"
