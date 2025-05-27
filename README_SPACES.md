---
title: MCP Odoo Server
emoji: 🏢
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

# MCP Odoo Server

Serveur MCP (Model Context Protocol) pour l'intégration avec Odoo ERP.

## Fonctionnalités

- Connexion sécurisée à Odoo via OdooRPC
- Interface Gradio pour les tests
- Support des opérations CRUD sur les modèles Odoo
- Intégration avec OpenAI pour l'assistance IA

## Configuration

Configurez les variables d'environnement suivantes dans les paramètres de votre Space :

- `ODOO_URL` : URL de votre instance Odoo
- `ODOO_DB` : Nom de votre base de données
- `ODOO_LOGIN` : Nom d'utilisateur Odoo
- `ODOO_PASSWORD` : Mot de passe Odoo
- `OPENAI_API_KEY` : Votre clé API OpenAI

## Utilisation

Une fois déployé, ce Space fournit un serveur MCP accessible via l'interface Gradio pour tester les fonctionnalités d'intégration Odoo. 