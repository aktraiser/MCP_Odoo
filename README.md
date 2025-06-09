# Odoo MCP Server

Un serveur MCP (Model Context Protocol) pour l'intégration avec Odoo ERP, permettant aux assistants IA d'interagir avec les données et fonctionnalités Odoo via XML-RPC.

## Fonctionnalités

* **Intégration Odoo complète** : Accès complet aux modèles, enregistrements et méthodes Odoo
* **Communication XML-RPC** : Connexion sécurisée aux instances Odoo via XML-RPC
* **Configuration flexible** : Support des fichiers de configuration et variables d'environnement
* **Système de ressources** : Accès basé sur URI aux structures de données Odoo
* **Gestion d'erreurs** : Messages d'erreur clairs pour les problèmes API Odoo courants
* **Opérations sans état** : Cycle requête/réponse propre pour une intégration fiable

## Outils

* **test_odoo_connection**
  * Teste la connexion au serveur Odoo
  * Retourne : Dictionnaire avec le statut de la connexion et les informations du serveur

* **execute_method**
  * Exécute une méthode personnalisée sur un modèle Odoo
  * Paramètres :
    * `model` (string) : Le nom du modèle (ex: 'res.partner')
    * `method` (string) : Nom de la méthode à exécuter
    * `args` (array optionnel) : Arguments positionnels
    * `kwargs` (object optionnel) : Arguments nommés
  * Retourne : Dictionnaire avec le résultat de la méthode et indicateur de succès

* **search_employee**
  * Recherche des employés par nom
  * Paramètres :
    * `name` (string) : Le nom (ou partie du nom) à rechercher
    * `limit` (number optionnel) : Nombre maximum de résultats (défaut 20)
  * Retourne : Objet contenant l'indicateur de succès, liste des employés trouvés et message d'erreur

* **search_holidays**
  * Recherche des congés dans une période spécifiée
  * Paramètres :
    * `start_date` (string) : Date de début au format YYYY-MM-DD
    * `end_date` (string) : Date de fin au format YYYY-MM-DD
    * `employee_id` (number optionnel) : ID employé optionnel pour filtrer
  * Retourne : Objet contenant l'indicateur de succès, liste des congés trouvés et message d'erreur

* **get_leads_statistics**
  * Récupère les statistiques complètes des leads CRM
  * Retourne : Dictionnaire avec les statistiques CRM (total, leads chauds, CA espéré, etc.)

* **server_status**
  * Obtient le statut général du serveur MCP-Odoo
  * Retourne : Dictionnaire avec le statut complet du serveur et la configuration

## Ressources

* **odoo://models**
  * Liste tous les modèles disponibles dans le système Odoo
  * Retourne : Array JSON des informations de modèles

* **odoo://model/{model_name}**
  * Obtient des informations sur un modèle spécifique incluant les champs
  * Exemple : `odoo://model/res.partner`
  * Retourne : Objet JSON avec métadonnées du modèle et définitions des champs

* **odoo://record/{model_name}/{record_id}**
  * Récupère un enregistrement spécifique par ID
  * Exemple : `odoo://record/res.partner/1`
  * Retourne : Objet JSON avec les données de l'enregistrement

## Fonctionnalités d'indexation avec LlamaIndex

Le serveur MCP-Odoo intègre LlamaIndex pour permettre l'indexation et la recherche sémantique des données Odoo. Cette fonctionnalité optionnelle ajoute des capacités d'IA pour la recherche et l'analyse des données.

### Outils d'indexation

* **index_leads**
  * Indexe les leads CRM pour la recherche sémantique
  * Paramètres :
    * `limit` (number optionnel) : Nombre maximum de leads à indexer (défaut 100)
    * `domain` (array optionnel) : Domaine de recherche Odoo
  * Retourne : Dictionnaire avec le nombre de documents indexés et statut de réussite

* **index_quotes**
  * Indexe les devis/commandes de vente pour la recherche sémantique
  * Paramètres :
    * `limit` (number optionnel) : Nombre maximum de devis à indexer (défaut 100)
    * `domain` (array optionnel) : Domaine de recherche Odoo
  * Retourne : Dictionnaire avec le nombre de documents indexés et statut de réussite

* **index_products**
  * Indexe les produits pour la recherche sémantique
  * Paramètres :
    * `limit` (number optionnel) : Nombre maximum de produits à indexer (défaut 100)
    * `domain` (array optionnel) : Domaine de recherche Odoo (défaut: produits actifs)
  * Retourne : Dictionnaire avec le nombre de documents indexés et statut de réussite

* **semantic_search**
  * Effectue une recherche sémantique dans une collection indexée
  * Paramètres :
    * `query` (string) : Requête en langage naturel
    * `collection_type` (string) : Type de collection (leads, quotes, products)
    * `top_k` (number optionnel) : Nombre de résultats à retourner (défaut 5)
  * Retourne : Dictionnaire avec la réponse IA et les sources associées

* **get_index_stats**
  * Récupère les statistiques d'une collection indexée
  * Paramètres :
    * `collection_type` (string) : Type de collection (leads, quotes, products)
  * Retourne : Dictionnaire avec le nombre de documents et informations de stockage

* **delete_index**
  * Supprime complètement une collection indexée
  * Paramètres :
    * `collection_type` (string) : Type de collection (leads, quotes, products)
  * Retourne : Dictionnaire avec le statut de suppression

### Configuration pour l'indexation

#### Dépendances requises

```bash
pip install llama-index llama-index-embeddings-openai llama-index-vector-stores-chroma chromadb
```

#### Variables d'environnement optionnelles

* `LLAMA_CLOUD_API_KEY` : Clé API LlamaCloud pour utiliser les embeddings premium LlamaCloud (recommandé)
* `OPENAI_API_KEY` : Clé API OpenAI pour utiliser les embeddings OpenAI (alternatif)
  * Si aucune des deux n'est définie, utilise les embeddings HuggingFace (gratuit mais moins performant)

**Ordre de priorité des embeddings :**
1. **LlamaCloud** (premium) - si `LLAMA_CLOUD_API_KEY` est définie
2. **OpenAI** (premium) - si `OPENAI_API_KEY` est définie  
3. **HuggingFace** (gratuit) - fallback automatique

#### Stockage des données

Les données indexées sont stockées dans ChromaDB :
* Chemin par défaut : `./chroma_db/`
* Collections automatiques :
  - `odoo_leads` : Données des leads CRM
  - `odoo_quotes` : Données des devis
  - `odoo_products` : Données des produits

### Exemples d'utilisation

#### Indexation des données

```python
# Indexer 50 leads récents
index_leads(limit=50)

# Indexer les produits vendables uniquement
index_products(limit=100, domain=[["sale_ok", "=", True]])

# Indexer tous les devis de cette année
index_quotes(domain=[["create_date", ">=", "2024-01-01"]])
```

#### Recherche sémantique

```python
# Rechercher des leads avec un certain profil
semantic_search(
    query="entreprise technologie startup investissement", 
    collection_type="leads",
    top_k=5
)

# Trouver des produits similaires
semantic_search(
    query="ordinateur portable professionnel", 
    collection_type="products",
    top_k=3
)

# Analyser les devis par montant
semantic_search(
    query="devis important montant élevé client premium", 
    collection_type="quotes"
)
```

#### Gestion des collections

```python
# Voir les statistiques
get_index_stats("leads")

# Nettoyer une collection
delete_index("products")
```

### Test des fonctionnalités d'indexation

Un script de test est disponible pour vérifier le bon fonctionnement :

```bash
python test_indexing.py
```

Ce script :
1. Vérifie la disponibilité de LlamaIndex
2. Teste la connexion Odoo
3. Indexe un échantillon de données
4. Effectue des recherches sémantiques
5. Affiche les statistiques

## Configuration

### Configuration de la connexion Odoo

1. **Fichier de configuration** `odoo_config.json` :

```json
{
  "url": "https://your-odoo-instance.com",
  "db": "your-database-name",
  "username": "your-username",
  "password": "your-password-or-api-key",
  "timeout": 30,
  "verify_ssl": true
}
```

2. **Variables d'environnement** (alternative) :
   * `ODOO_URL` : URL de votre serveur Odoo
   * `ODOO_DB` : Nom de la base de données
   * `ODOO_USERNAME` : Nom d'utilisateur de connexion
   * `ODOO_PASSWORD` : Mot de passe ou clé API
   * `ODOO_TIMEOUT` : Timeout de connexion en secondes (défaut: 30)
   * `ODOO_VERIFY_SSL` : Vérification des certificats SSL (défaut: true)

### Utilisation avec Claude Desktop

Ajoutez ceci à votre `claude_desktop_config.json` :

```json
{
  "mcpServers": {
    "odoo": {
      "command": "python",
      "args": ["run_server.py"],
      "env": {
        "ODOO_URL": "https://your-odoo-instance.com",
        "ODOO_DB": "your-database-name",
        "ODOO_USERNAME": "your-username",
        "ODOO_PASSWORD": "your-password-or-api-key"
      }
    }
  }
}
```

### Utilisation avec Docker

```json
{
  "mcpServers": {
    "odoo": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "ODOO_URL",
        "-e", "ODOO_DB", 
        "-e", "ODOO_USERNAME",
        "-e", "ODOO_PASSWORD",
        "mcp/odoo"
      ],
      "env": {
        "ODOO_URL": "https://your-odoo-instance.com",
        "ODOO_DB": "your-database-name",
        "ODOO_USERNAME": "your-username",
        "ODOO_PASSWORD": "your-password-or-api-key"
      }
    }
  }
}
```

## Installation

### Package Python

```bash
pip install -e .
```

### Lancement du serveur

```bash
# Utilisation du script de lancement
python run_server.py

# Utilisation directe du module
python -m odoo_mcp.server

# Avec les outils de développement MCP
mcp dev src/odoo_mcp/server.py
```

### Construction Docker

```bash
docker build -t mcp/odoo:latest .
```

## Développement

### Structure du projet

```
├── src/
│   └── odoo_mcp/
│       ├── __init__.py
│       ├── server.py       # Serveur MCP principal
│       ├── client.py       # Client Odoo XML-RPC
│       └── config.py       # Configuration
├── run_server.py           # Script de lancement
├── pyproject.toml          # Configuration du package
├── odoo_config.json.example # Exemple de configuration
└── README.md
```

### Tests

```bash
# Lancer les tests
python -m pytest

# Test de connexion simple
export ODOO_PASSWORD='your-password'
python run_server.py --debug
```

## Directives de formatage des paramètres

Lors de l'utilisation des outils MCP pour Odoo, respectez ces directives :

1. **Paramètre Domain** :
   * Formats supportés :
     * Format liste : `[["field", "operator", value], ...]`
     * Format objet : `{"conditions": [{"field": "...", "operator": "...", "value": "..."}]}`
     * Chaîne JSON de l'un ou l'autre format
   * Exemples :
     * Format liste : `[["is_company", "=", true]]`
     * Format objet : `{"conditions": [{"field": "date_order", "operator": ">=", "value": "2025-03-01"}]}`
     * Conditions multiples : `[["date_order", ">=", "2025-03-01"], ["date_order", "<=", "2025-03-31"]]`

2. **Paramètre Fields** :
   * Doit être un array de noms de champs : `["name", "email", "phone"]`
   * Le serveur tentera d'analyser les entrées string comme JSON

## Licence

Ce serveur MCP est sous licence MIT.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir des issues ou soumettre des pull requests.

## Références

Inspiré par le projet [mcp-odoo de tuanle96](https://github.com/tuanle96/mcp-odoo) avec des améliorations pour la robustesse et la facilité d'utilisation. 