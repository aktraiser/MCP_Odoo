"""
Configuration et gestion des variables d'environnement
"""
import os
from dotenv import load_dotenv
import openai

# Charger les variables d'environnement
load_dotenv()

class Config:
    """Classe de configuration centralisée"""
    
    def __init__(self):
        # Configuration Odoo avec valeurs par défaut pour les tests et déploiement
        self.odoo_url = os.getenv("ODOO_URL", "dasein.odoo.com")
        self.odoo_db = os.getenv("ODOO_DB", "dasein")
        self.odoo_login = os.getenv("ODOO_LOGIN", "lbometon@hotmail.fr")
        self.odoo_password = os.getenv("ODOO_PASSWORD", "bupzEw-kasdy2-nubmoc")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Configurer OpenAI si la clé est disponible
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def update_odoo_config(self, url, db, login, password):
        """Mettre à jour la configuration Odoo"""
        self.odoo_url = url.strip() if url else None
        self.odoo_db = db.strip() if db else None
        self.odoo_login = login.strip() if login else None
        self.odoo_password = password
    
    def update_openai_config(self, api_key):
        """Mettre à jour la configuration OpenAI"""
        self.openai_api_key = api_key.strip() if api_key else None
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def is_odoo_configured(self):
        """Vérifier si la configuration Odoo est complète"""
        return all([self.odoo_url, self.odoo_db, self.odoo_login, self.odoo_password])
    
    def is_openai_configured(self):
        """Vérifier si OpenAI est configuré"""
        return bool(self.openai_api_key)
    
    def get_missing_odoo_vars(self):
        """Retourner la liste des variables Odoo manquantes"""
        missing = []
        if not self.odoo_url: missing.append("ODOO_URL")
        if not self.odoo_db: missing.append("ODOO_DB")
        if not self.odoo_login: missing.append("ODOO_LOGIN")
        if not self.odoo_password: missing.append("ODOO_PASSWORD")
        return missing

# Instance globale de configuration
config = Config() 