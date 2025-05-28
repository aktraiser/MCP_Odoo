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

# Agent CRM MCP Server

Serveur MCP (Model Context Protocol) pour l'intégration avec Odoo CRM, offrant des outils d'automatisation et d'intelligence artificielle pour la gestion des prospects et opportunités.

## 🏗️ Architecture

Le projet est maintenant structuré de manière modulaire :

```
MCP_Odoo/
├── config/                 # Configuration et variables d'environnement
│   ├── __init__.py
│   └── settings.py
├── odoo_connector/         # Gestion de la connexion Odoo
│   ├── __init__.py
│   └── connection.py
├── mcp_tools/             # Outils MCP (ancienne version)
│   ├── __init__.py
│   └── crm_tools.py
├── ui/                    # Interface utilisateur Gradio
│   ├── __init__.py
│   ├── utils.py
│   ├── config_tab.py
│   ├── crm_tab.py
│   └── gradio_app.py
├── mcp_server.py          # Serveur MCP principal (FastMCP)
├── mcp_config.json        # Configuration MCP
├── app.py                 # Point d'entrée principal
└── requirements.txt       # Dépendances Python
```

## 🚀 Modes de fonctionnement

### 1. Interface Gradio (Mode par défaut)
Interface web conviviale pour tester et utiliser les outils CRM :

```bash
python app.py
# ou
python app.py --mode gradio
```

### 2. Serveur MCP
Serveur MCP compatible avec les clients MCP (Claude Desktop, etc.) :

```bash
python app.py --mode mcp
```

## 🛠️ Outils MCP disponibles

### Ressources
- `odoo://crm/leads` - Liste tous les leads CRM
- `odoo://crm/lead/{lead_id}` - Détails d'un lead spécifique
- `odoo://crm/stages` - Liste des étapes CRM

### Outils
- `create_lead` - Créer un nouveau lead
- `ingest_prospects` - Ingérer plusieurs prospects en lot
- `qualify_lead` - Analyser un lead avec l'IA
- `generate_offer` - Générer une proposition commerciale
- `summarize_opportunity` - Résumer le statut d'une opportunité

## 📋 Configuration

### Variables d'environnement
Créez un fichier `.env` avec :

```env
ODOO_URL=votre-instance.odoo.com
ODOO_DB=votre-base-de-donnees
ODOO_LOGIN=votre-email@exemple.com
ODOO_PASSWORD=votre-mot-de-passe
OPENAI_API_KEY=sk-votre-cle-openai
```

### Configuration MCP
Modifiez `mcp_config.json` pour configurer le serveur MCP :

```json
{
  "mcpServers": {
    "odoo-crm": {
      "command": "python",
      "args": ["mcp_server.py"],
      "env": {
        "ODOO_URL": "votre-instance.odoo.com",
        "ODOO_DB": "votre-base-de-donnees",
        "ODOO_LOGIN": "votre-email@exemple.com",
        "ODOO_PASSWORD": "votre-mot-de-passe",
        "OPENAI_API_KEY": "sk-votre-cle-openai"
      }
    }
  }
}
```

## 🔧 Installation

1. **Cloner le repository**
```bash
git clone <repository-url>
cd MCP_Odoo
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer les variables d'environnement**
```bash
cp env.example .env
# Éditer .env avec vos paramètres
```

4. **Lancer l'application**
```bash
# Interface Gradio
python app.py

# Serveur MCP
python app.py --mode mcp
```

## 🧪 Utilisation avec Claude Desktop

Pour utiliser le serveur MCP avec Claude Desktop :

1. Ajoutez la configuration dans votre fichier de configuration Claude Desktop
2. Redémarrez Claude Desktop
3. Le serveur "odoo-crm" sera disponible avec tous ses outils

## 📚 Exemples d'utilisation

### Créer un lead
```python
# Via l'outil MCP create_lead
{
  "name": "Prospect TechCorp",
  "partner_name": "TechCorp Solutions",
  "email_from": "contact@techcorp.com",
  "phone": "+33 1 23 45 67 89",
  "description": "Entreprise intéressée par nos solutions",
  "expected_revenue": 15000.0,
  "probability": 60
}
```

### Ingérer plusieurs prospects
```python
# Via l'outil MCP ingest_prospects
[
  {
    "name": "Lead 1",
    "partner_name": "Entreprise 1",
    "email_from": "contact1@exemple.com"
  },
  {
    "name": "Lead 2", 
    "partner_name": "Entreprise 2",
    "email_from": "contact2@exemple.com"
  }
]
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez suivre la structure modulaire existante.

## 📄 Licence

[Votre licence ici] 