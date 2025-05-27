#!/bin/bash

# Script d'initialisation du repository Git pour Agent CRM MCP Server
# Nom du repository: Aktraiser

echo "🚀 Initialisation du repository Git 'Aktraiser'"

# Initialiser le repository git
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit: Agent CRM MCP Server

- Serveur MCP basé sur Gradio pour CRM Odoo
- Intégration OpenAI pour qualification de leads
- Outils: ingest_prospects, qualify_lead, generate_offer, summarize_opportunity
- Support Docker et Hugging Face Spaces
- Documentation complète et tests inclus"

echo "✅ Repository Git initialisé avec succès!"
echo "📝 Pour connecter à un repository distant:"
echo "   git remote add origin https://github.com/votre-username/Aktraiser.git"
echo "   git branch -M main"
echo "   git push -u origin main"

echo ""
echo "📁 Structure du repository:"
tree -a -I '.git' || ls -la 