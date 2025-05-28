---
title: MCP Odoo CRM Server
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "4.44.0"
app_file: app.py
pinned: false
license: mit
---

# 🚀 MCP Odoo CRM Server

Un serveur MCP (Model Context Protocol) avec Gradio pour la gestion CRM Odoo.

## 🎯 Fonctionnalités

Ce serveur MCP expose 4 outils pour interagir avec Odoo CRM :

- **`test_odoo_connection`** - Teste et établit la connexion à Odoo
- **`create_odoo_lead`** - Crée un nouveau lead dans Odoo CRM  
- **`get_odoo_leads`** - Récupère la liste des leads depuis Odoo
- **`get_connection_status`** - Vérifie le statut de la connexion

## 🔗 Utilisation avec les Clients MCP

### Endpoint MCP SSE
```
https://votre-space.hf.space/gradio_api/mcp/sse
```

### Configuration pour Cursor
```json
{
  "mcpServers": {
    "odoo-crm": {
      "url": "https://votre-space.hf.space/gradio_api/mcp/sse"
    }
  }
}
```

### Configuration pour Claude Desktop
```json
{
  "mcpServers": {
    "odoo-crm": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://votre-space.hf.space/gradio_api/mcp/sse",
        "--transport",
        "sse-only"
      ]
    }
  }
}
```

## 📖 Exemples d'utilisation

Une fois configuré dans votre client MCP :

1. **Connecter à Odoo** :
   ```
   Connecte-toi à mon instance Odoo avec l'URL https://mon-odoo.com, 
   base de données "production", utilisateur "admin" et mot de passe "monmotdepasse"
   ```

2. **Créer un lead** :
   ```
   Crée un lead pour l'entreprise "TechCorp" avec le contact "Jean Dupont", 
   email "jean@techcorp.com" et revenus attendus de 5000€
   ```

3. **Lister les leads** :
   ```
   Récupère les 10 derniers leads de mon CRM Odoo
   ```

## 🛠️ Développement Local

```bash
git clone https://huggingface.co/spaces/votre-username/mcp-odoo-crm
cd mcp-odoo-crm
pip install -r requirements.txt
python app.py
```

## 📚 Documentation

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Documentation Gradio MCP](https://www.gradio.app/guides/building-mcp-server-with-gradio)
- [API Odoo](https://www.odoo.com/documentation/17.0/developer/reference/external_api.html)

## 🛠️ Technologies

- **FastMCP** : Serveur MCP moderne et performant
- **Gradio** : Interface web interactive
- **OdooRPC** : Connexion native à Odoo
- **OpenAI** : Intelligence artificielle pour la qualification
- **Pydantic** : Validation des données

## 📋 Configuration

### Variables d'environnement (optionnelles)

```bash
ODOO_URL=votre-instance.odoo.com
ODOO_DB=nom-de-votre-base
ODOO_LOGIN=votre-email
ODOO_PASSWORD=votre-mot-de-passe
OPENAI_API_KEY=votre-clé-openai
```

### Configuration via l'interface

1. Ouvrez l'onglet **Configuration**
2. Saisissez vos informations de connexion Odoo
3. Testez la connexion
4. (Optionnel) Ajoutez votre clé OpenAI pour les fonctionnalités IA

## 🎯 Utilisation

### Création de leads
1. Allez dans l'onglet **CRM**
2. Remplissez le formulaire de création de lead
3. Cliquez sur "Créer le Lead"

### Import en lot
1. Préparez un fichier CSV avec les colonnes : `name`, `partner_name`, `email_from`, `phone`, `description`
2. Uploadez le fichier dans l'interface
3. Lancez l'import

### Qualification IA
1. Sélectionnez un lead existant
2. Utilisez l'outil de qualification pour obtenir une analyse automatique
3. Générez des propositions commerciales personnalisées

## 🔗 Intégration MCP

Ce serveur peut être utilisé comme un serveur MCP standard :

```bash
# Lancer le serveur MCP
python mcp_server.py

# Ou via l'interface
python app.py --mode mcp
```

## 📊 Structure du projet

```
MCP_Odoo/
├── app.py                 # Point d'entrée Gradio
├── mcp_server.py         # Serveur MCP principal
├── config/
│   └── settings.py       # Configuration
├── odoo_connector/
│   └── connection.py     # Connexion Odoo
├── ui/
│   ├── gradio_app.py     # Interface principale
│   ├── config_tab.py     # Onglet configuration
│   ├── crm_tab.py        # Onglet CRM
│   └── utils.py          # Utilitaires UI
└── requirements.txt      # Dépendances

```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

---

**Développé avec ❤️ pour simplifier la gestion CRM avec Odoo** 