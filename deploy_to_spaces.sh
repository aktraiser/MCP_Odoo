#!/bin/bash

# Script de déploiement vers Hugging Face Spaces
# Usage: ./deploy_to_spaces.sh <username/space-name>
# Exemple: ./deploy_to_spaces.sh aktraiser/MCP_Odoo

if [ $# -eq 0 ]; then
    echo "Usage: $0 <username/space-name>"
    echo "Exemple: $0 Aktraiser/MCP_Odoo"
    exit 1
fi

SPACE_NAME=$1
HF_REPO="https://huggingface.co/spaces/${SPACE_NAME}.git"

echo "🚀 Déploiement vers Hugging Face Spaces: ${SPACE_NAME}"

# Vérifier si le remote 'huggingface' existe déjà
if git remote get-url huggingface >/dev/null 2>&1; then
    echo "✅ Remote 'huggingface' existe déjà, mise à jour de l'URL"
    git remote set-url huggingface "${HF_REPO}"
else
    echo "➕ Ajout du remote 'huggingface' -> ${HF_REPO}"
    git remote add huggingface "${HF_REPO}"
fi

# Copier le README spécifique pour Spaces
if [ -f "README_SPACES.md" ]; then
    cp README_SPACES.md README.md
    echo "📝 README mis à jour pour Spaces"
fi

# Commit et push vers Hugging Face
echo "📤 Push vers Hugging Face Spaces..."
git add .
git commit -m "Deploy to Hugging Face Spaces" || echo "Rien à committer"
git push huggingface main

echo "✅ Déploiement terminé !"
echo "🌐 Votre Space est disponible sur: https://huggingface.co/spaces/${SPACE_NAME}"