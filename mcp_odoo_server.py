#!/usr/bin/env python3
"""
Serveur MCP Gradio pour Odoo CRM
Basé sur la documentation officielle Gradio MCP
"""

import gradio as gr
import os
import logging
from typing import Optional, Dict, Any, List
import json
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import des modules locaux avec fallback
try:
    from odoo_connector.connection import OdooConnector
    from config.settings import get_odoo_config
except ImportError as e:
    logger.warning(f"Import error: {e}")
    
    class OdooConnector:
        def __init__(self, *args, **kwargs):
            self.connected = False
        
        def test_connection(self):
            return False, "Module Odoo non disponible"
        
        def create_lead(self, *args, **kwargs):
            return False, "Module Odoo non disponible"
        
        def get_leads(self, *args, **kwargs):
            return False, "Module Odoo non disponible"
    
    def get_odoo_config():
        return {
            'url': '',
            'db': '',
            'username': '',
            'password': ''
        }

# Variables globales pour la connexion Odoo
odoo_connector = None
connection_status = "❌ Non connecté"

def test_odoo_connection(url: str, db: str, username: str, password: str) -> str:
    """
    Test la connexion à Odoo et retourne le statut.
    
    Args:
        url (str): URL de l'instance Odoo
        db (str): Nom de la base de données
        username (str): Nom d'utilisateur
        password (str): Mot de passe
    
    Returns:
        str: Message de statut de la connexion
    """
    global odoo_connector, connection_status
    
    try:
        if not all([url, db, username, password]):
            connection_status = "❌ Erreur"
            return "❌ Tous les champs sont requis"
        
        odoo_connector = OdooConnector(url, db, username, password)
        success, message = odoo_connector.test_connection()
        
        if success:
            connection_status = "✅ Connecté"
            return f"✅ Connexion réussie à {db}"
        else:
            connection_status = "❌ Erreur de connexion"
            return f"❌ Échec de connexion: {message}"
            
    except Exception as e:
        connection_status = "❌ Erreur"
        return f"❌ Erreur: {str(e)}"

def create_odoo_lead(name: str, partner_name: str = "", email: str = "", 
                    phone: str = "", description: str = "", 
                    expected_revenue: str = "0") -> str:
    """
    Crée un lead dans Odoo CRM.
    
    Args:
        name (str): Nom du lead (requis)
        partner_name (str): Nom de l'entreprise
        email (str): Email du contact
        phone (str): Téléphone du contact
        description (str): Description du lead
        expected_revenue (str): Revenus attendus en euros
    
    Returns:
        str: Message de confirmation ou d'erreur
    """
    global odoo_connector
    
    try:
        if not odoo_connector:
            return "❌ Pas de connexion Odoo active. Veuillez d'abord vous connecter."
        
        if not name.strip():
            return "❌ Le nom du lead est requis"
        
        # Conversion du revenu attendu
        try:
            revenue = float(expected_revenue) if expected_revenue else 0.0
        except ValueError:
            revenue = 0.0
        
        lead_data = {
            'name': name.strip(),
            'partner_name': partner_name.strip() if partner_name else "",
            'email_from': email.strip() if email else "",
            'phone': phone.strip() if phone else "",
            'description': description.strip() if description else "",
            'expected_revenue': revenue
        }
        
        success, result = odoo_connector.create_lead(lead_data)
        
        if success:
            return f"✅ Lead créé avec succès ! ID: {result}"
        else:
            return f"❌ Échec de création du lead: {result}"
            
    except Exception as e:
        return f"❌ Erreur lors de la création: {str(e)}"

def get_odoo_leads(limit: str = "10") -> str:
    """
    Récupère la liste des leads depuis Odoo CRM.
    
    Args:
        limit (str): Nombre maximum de leads à récupérer
    
    Returns:
        str: Liste des leads au format JSON ou message d'erreur
    """
    global odoo_connector
    
    try:
        if not odoo_connector:
            return "❌ Pas de connexion Odoo active. Veuillez d'abord vous connecter."
        
        # Conversion de la limite
        try:
            limit_int = int(limit) if limit else 10
            limit_int = max(1, min(limit_int, 100))  # Entre 1 et 100
        except ValueError:
            limit_int = 10
        
        success, leads = odoo_connector.get_leads(limit=limit_int)
        
        if success:
            if leads:
                return f"✅ {len(leads)} leads récupérés:\n" + json.dumps(leads, indent=2, ensure_ascii=False)
            else:
                return "✅ Aucun lead trouvé dans Odoo"
        else:
            return f"❌ Erreur lors de la récupération: {leads}"
            
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

def get_connection_status() -> str:
    """
    Retourne le statut actuel de la connexion Odoo.
    
    Returns:
        str: Statut de la connexion
    """
    return connection_status

# Interface Gradio avec les outils MCP
demo = gr.TabbedInterface(
    [
        gr.Interface(
            fn=test_odoo_connection,
            inputs=[
                gr.Textbox(label="URL Odoo", placeholder="https://votre-instance.odoo.com"),
                gr.Textbox(label="Base de données", placeholder="nom_de_la_db"),
                gr.Textbox(label="Nom d'utilisateur", placeholder="admin"),
                gr.Textbox(label="Mot de passe", type="password")
            ],
            outputs=gr.Textbox(label="Statut de connexion"),
            title="🔗 Connexion Odoo",
            description="Testez et établissez la connexion à votre instance Odoo",
            api_name="test_odoo_connection"
        ),
        gr.Interface(
            fn=create_odoo_lead,
            inputs=[
                gr.Textbox(label="Nom du lead *", placeholder="Nom du prospect"),
                gr.Textbox(label="Nom de l'entreprise", placeholder="Entreprise cliente"),
                gr.Textbox(label="Email", placeholder="contact@entreprise.com"),
                gr.Textbox(label="Téléphone", placeholder="+33 1 23 45 67 89"),
                gr.Textbox(label="Description", lines=3, placeholder="Description du lead..."),
                gr.Textbox(label="Revenus attendus (€)", placeholder="1000")
            ],
            outputs=gr.Textbox(label="Résultat"),
            title="➕ Créer un Lead",
            description="Créez un nouveau lead dans Odoo CRM",
            api_name="create_odoo_lead"
        ),
        gr.Interface(
            fn=get_odoo_leads,
            inputs=[
                gr.Textbox(label="Nombre de leads", placeholder="10", value="10")
            ],
            outputs=gr.Textbox(label="Liste des leads", lines=10),
            title="📋 Lister les Leads",
            description="Récupérez la liste des leads depuis Odoo",
            api_name="get_odoo_leads"
        ),
        gr.Interface(
            fn=get_connection_status,
            inputs=[],
            outputs=gr.Textbox(label="Statut actuel"),
            title="📊 Statut",
            description="Vérifiez le statut de la connexion Odoo",
            api_name="get_connection_status"
        )
    ],
    [
        "Connexion",
        "Créer Lead", 
        "Lister Leads",
        "Statut"
    ],
    title="🚀 MCP Odoo CRM Server"
)

if __name__ == "__main__":
    print("🚀 Lancement du serveur MCP Odoo CRM...")
    
    # Lancer avec le serveur MCP activé
    demo.launch(
        mcp_server=True,  # Active le serveur MCP
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        debug=False
    ) 