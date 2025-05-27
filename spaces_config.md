# Configuration Hugging Face Spaces

## Étapes de déploiement sur Hugging Face Spaces

### 1. Créer un nouveau Space

1. Allez sur https://huggingface.co/spaces
2. Cliquez sur "Create new Space"
3. Choisissez :
   - **Space name** : `agent-crm-mcp-server` (ou votre nom préféré)
   - **License** : MIT
   - **SDK** : Gradio
   - **Hardware** : CPU basic (gratuit) ou GPU selon vos besoins

### 2. Uploader les fichiers

Uploadez ces fichiers dans votre Space :
- `app.py`
- `requirements.txt`

### 3. Configurer les variables d'environnement

Dans les paramètres de votre Space, ajoutez ces variables d'environnement :

| Variable | Valeur | Description |
|----------|--------|-------------|
| `ODOO_URL` | `votre-instance.odoo.com` | URL de votre instance Odoo |
| `ODOO_DB` | `votre-db` | Nom de votre base de données |
| `ODOO_LOGIN` | `votre-login` | Nom d'utilisateur Odoo |
| `ODOO_PASSWORD` | `votre-password` | Mot de passe Odoo |
| `OPENAI_API_KEY` | `sk-...` | Votre clé API OpenAI |

### 4. Déployer

1. Cliquez sur "Commit changes"
2. Le Space va automatiquement se construire et se déployer
3. Une fois prêt, vous aurez une URL publique pour votre serveur MCP

### 5. Utilisation

Votre serveur MCP sera accessible via l'URL de votre Space et pourra être utilisé par des clients MCP compatibles.

## Sécurité

⚠️ **Important** : 
- Ne jamais exposer vos credentials dans le code
- Utilisez uniquement les variables d'environnement de Spaces
- Considérez créer un utilisateur Odoo dédié avec permissions limitées
- Surveillez l'utilisation de votre clé OpenAI

## Support

Pour toute question sur le déploiement, consultez la documentation Hugging Face Spaces : https://huggingface.co/docs/hub/spaces 