#!/bin/bash

# Script de déploiement pour Agent CRM MCP Server

echo "🚀 Déploiement Agent CRM MCP Server"

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si le fichier .env existe
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env non trouvé. Copie de env.example vers .env"
    cp env.example .env
    echo "📝 Veuillez éditer le fichier .env avec vos configurations avant de continuer."
    echo "   Variables requises: ODOO_URL, ODOO_DB, ODOO_LOGIN, ODOO_PASSWORD, OPENAI_API_KEY"
    exit 1
fi

# Construire l'image Docker
echo "🔨 Construction de l'image Docker..."
docker build -t agent-crm-mcp .

# Lancer le conteneur
echo "🚀 Lancement du conteneur..."
docker-compose up -d

echo "✅ Déploiement terminé!"
echo "🌐 L'application est accessible sur: http://localhost:7860"
echo "📊 Pour voir les logs: docker-compose logs -f"
echo "🛑 Pour arrêter: docker-compose down" 