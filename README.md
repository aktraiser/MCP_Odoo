---
title: MCP Odoo CRM
emoji: 🏢
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# MCP Odoo CRM 🏢

Une application **Model Context Protocol (MCP)** pour intégrer et gérer un système CRM Odoo via une interface Gradio moderne.

## 🚀 Fonctionnalités

### 🔧 Serveur MCP
- **Connexion Odoo** : Diagnostic et gestion de la connexion à votre instance Odoo
- **Gestion des Leads** : Création et ingestion de prospects en lot
- **Qualification IA** : Analyse automatique des leads avec OpenAI
- **Propositions commerciales** : Génération d'emails personnalisés
- **Ressources MCP** : Accès aux données CRM via le protocole MCP

### 🎨 Interface Gradio
- **Configuration intuitive** : Paramétrage facile de la connexion Odoo
- **Tableau de bord CRM** : Visualisation et gestion des leads
- **Import en lot** : Chargement de fichiers CSV/Excel
- **Génération de contenu** : Outils IA intégrés

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