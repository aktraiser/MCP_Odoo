# Guide d'utilisation - Agent CRM MCP Tools

## 🎯 Comment injecter des leads

### 1. **Onglet "Outils CRM" > Section "Ingest Prospects"**

Dans le champ "Leads (list of records)", copiez-collez le JSON suivant :

```json
[
  {
    "name": "Prospect - Entreprise TechCorp",
    "partner_name": "TechCorp Solutions",
    "email_from": "contact@techcorp.com",
    "phone": "+33 1 23 45 67 89",
    "description": "Entreprise de 50 employés spécialisée dans le développement logiciel. Intéressée par nos solutions CRM pour améliorer leur gestion commerciale.",
    "expected_revenue": 15000.0,
    "probability": 60,
    "tag_ids": [[6, 0, []]],
    "user_id": 1
  },
  {
    "name": "Lead - Startup InnovateLab",
    "partner_name": "InnovateLab",
    "email_from": "ceo@innovatelab.fr",
    "phone": "+33 6 78 90 12 34",
    "description": "Startup en phase de croissance (15 employés) dans l'IoT. Recherche une solution CRM intégrée pour gérer leurs prospects internationaux.",
    "expected_revenue": 8500.0,
    "probability": 40,
    "tag_ids": [[6, 0, []]],
    "user_id": 1
  }
]
```

### 2. **Cliquez sur "Submit"**

Le système va créer les leads dans Odoo et vous retourner les IDs créés.

## 🔍 Comment qualifier un lead

### 1. **Section "Qualify Lead"**
- Entrez l'ID d'un lead créé (par exemple : 1, 2, 3...)
- Cliquez sur "Submit"
- L'IA analysera le lead et donnera un score d'intérêt

## 📧 Comment générer une offre

### 1. **Section "Generate Offer"**
- Entrez l'ID du lead
- Choisissez le tone : "formel", "vendeur", ou "technique"
- Cliquez sur "Submit"
- L'IA générera un email de proposition personnalisé

## 📊 Comment résumer une opportunité

### 1. **Section "Summarize Opportunity"**
- Entrez l'ID du lead/opportunité
- Cliquez sur "Submit"
- Obtenez un résumé du statut de l'opportunité

## 📋 Structure des champs pour les leads

### Champs obligatoires :
- `name` : Nom du lead/prospect
- `partner_name` : Nom de l'entreprise
- `email_from` : Email de contact

### Champs optionnels :
- `phone` : Téléphone
- `description` : Description détaillée
- `expected_revenue` : Chiffre d'affaires attendu
- `probability` : Probabilité de conversion (0-100)
- `user_id` : ID de l'utilisateur assigné (1 par défaut)
- `tag_ids` : Tags (format Odoo : [[6, 0, []]])

## 🎯 Conseils d'utilisation

1. **Commencez par injecter quelques leads** pour tester
2. **Notez les IDs retournés** pour les utiliser dans les autres outils
3. **Testez la qualification** sur un lead avec une description détaillée
4. **Générez des offres** avec différents tons pour voir les variations
5. **Vérifiez dans Odoo** que les leads sont bien créés

## 🔧 Dépannage

- **Erreur de connexion** : Vérifiez l'onglet Configuration
- **Lead non trouvé** : Vérifiez que l'ID existe dans la réponse d'injection
- **Erreur OpenAI** : Vérifiez que la clé API est configurée pour les fonctions IA 