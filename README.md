# Agent CRM MCP Server

Serveur MCP (Model Context Protocol) basé sur Gradio pour la gestion CRM avec Odoo et OpenAI.

## Description

Ce projet fournit un serveur MCP qui expose des outils CRM via une interface Gradio. Il permet d'interagir avec Odoo CRM et d'utiliser l'IA d'OpenAI pour automatiser diverses tâches de gestion commerciale.

## Fonctionnalités

- **Ingestion de prospects** : Création automatique de leads dans Odoo CRM
- **Qualification de leads** : Génération de résumés et scores d'intérêt avec IA
- **Génération d'offres** : Création de propositions commerciales personnalisées
- **Résumé d'opportunités** : Synthèse du statut des opportunités commerciales

## Installation

### Prérequis

- Python 3.8+
- Accès à une instance Odoo
- Clé API OpenAI

### Installation locale

1. Clonez le repository :
```bash
git clone <votre-repo-url>
cd MCP_Odoo
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez les variables d'environnement :
```bash
cp env.example .env
# Éditez le fichier .env avec vos configurations
```

4. Lancez l'application :
```bash
python app.py
```

### Déploiement sur Hugging Face Spaces

1. Créez un nouveau Space sur Hugging Face
2. Uploadez les fichiers `app.py` et `requirements.txt`
3. Configurez les variables d'environnement dans les paramètres du Space :
   - `ODOO_URL`
   - `ODOO_DB`
   - `ODOO_LOGIN`
   - `ODOO_PASSWORD`
   - `OPENAI_API_KEY`

## Configuration

### Variables d'environnement

| Variable | Description | Exemple |
|----------|-------------|---------|
| `ODOO_URL` | URL de votre instance Odoo | `mycompany.odoo.com` |
| `ODOO_DB` | Nom de la base de données Odoo | `mycompany_db` |
| `ODOO_LOGIN` | Nom d'utilisateur Odoo | `admin` |
| `ODOO_PASSWORD` | Mot de passe Odoo | `password123` |
| `OPENAI_API_KEY` | Clé API OpenAI | `sk-...` |

## Utilisation

### Outils disponibles

#### 1. Ingest Prospects
Crée des leads dans Odoo CRM à partir d'une liste de données.

**Entrée** : JSON avec liste de records
```json
[
  {
    "name": "Prospect Name",
    "email_from": "prospect@example.com",
    "description": "Notes about the prospect"
  }
]
```

#### 2. Qualify Lead
Génère un résumé et un score d'intérêt pour un lead existant.

**Entrée** : ID du lead (nombre entier)

#### 3. Generate Offer
Génère une proposition commerciale personnalisée.

**Entrées** :
- ID du lead (nombre entier)
- Ton : "formel", "vendeur", ou "technique"

#### 4. Summarize Opportunity
Fournit un résumé de l'état d'une opportunité.

**Entrée** : ID du lead/opportunité (nombre entier)

## Architecture

```
app.py                 # Application principale Gradio MCP
requirements.txt       # Dépendances Python
env.example           # Exemple de configuration
README.md             # Documentation
```

## Sécurité

- Ne jamais commiter le fichier `.env` avec vos vraies credentials
- Utilisez les variables d'environnement de Hugging Face Spaces pour la production
- Assurez-vous que votre utilisateur Odoo a les permissions appropriées

## Support

Pour toute question ou problème, veuillez ouvrir une issue sur le repository.

## Licence

Ce projet est sous licence MIT. 