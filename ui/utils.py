"""
Utilitaires pour l'interface utilisateur
"""
import json
from config.settings import config
from odoo_connector.connection import odoo_connector

def validate_url(url):
    """Valider et suggérer le format d'URL"""
    if not url:
        return "❌ URL vide"
    
    url = url.strip()
    
    # Modèles d'URL courants pour Odoo
    suggestions = []
    
    if not url.endswith('.odoo.com') and not url.endswith('.com') and not '.' in url:
        suggestions.append(f"Essayez: {url}.odoo.com")
    
    if url.startswith('www.'):
        suggestions.append(f"Essayez sans 'www.': {url[4:]}")
    
    if suggestions:
        return f"💡 Suggestions: {' ou '.join(suggestions)}"
    
    return "✅ Format d'URL valide"

def update_config(odoo_url, odoo_db, odoo_login, odoo_password, openai_key):
    """Mettre à jour la configuration et tester la connexion"""
    # Valider les entrées
    if not odoo_url or not odoo_db or not odoo_login or not odoo_password:
        return "❌ Tous les champs Odoo sont obligatoires"
    
    # Mettre à jour la configuration
    config.update_odoo_config(odoo_url, odoo_db, odoo_login, odoo_password)
    config.update_openai_config(openai_key)
    
    # Tester la connexion Odoo
    result = odoo_connector.update_config_and_reconnect(odoo_url, odoo_db, odoo_login, odoo_password)
    
    return result

def get_connection_status():
    """Retourner le statut de connexion actuel"""
    return odoo_connector.get_status()

def test_connection():
    """Tester et réinitialiser la connexion"""
    odoo_connector.reconnect()
    return odoo_connector.get_status()

def load_example_leads():
    """Charger un exemple de leads JSON"""
    return '''[
  {
    "name": "Prospect - Entreprise TechCorp",
    "partner_name": "TechCorp Solutions",
    "email_from": "contact@techcorp.com",
    "phone": "+33 1 23 45 67 89",
    "description": "Entreprise de 50 employés spécialisée dans le développement logiciel.",
    "expected_revenue": 15000.0,
    "probability": 60,
    "user_id": 1
  },
  {
    "name": "Lead - Startup InnovateLab",
    "partner_name": "InnovateLab",
    "email_from": "ceo@innovatelab.fr",
    "phone": "+33 6 78 90 12 34",
    "description": "Startup en phase de croissance dans l'IoT.",
    "expected_revenue": 8500.0,
    "probability": 40,
    "user_id": 1
  }
]'''

def process_leads(leads_json):
    """Traiter les leads JSON et les créer dans Odoo"""
    try:
        from mcp_tools.crm_tools import ingest_prospects
        leads_data = json.loads(leads_json) if isinstance(leads_json, str) else leads_json
        return ingest_prospects(leads_data)
    except json.JSONDecodeError:
        return {"error": "Format JSON invalide"}
    except Exception as e:
        return {"error": f"Erreur: {str(e)}"} 