# Gradio-based MCP Server for Agent CRM
import os
from dotenv import load_dotenv
import odoorpc
import openai
import pandas as pd
from io import StringIO
import gradio as gr

# Load environment variables
load_dotenv()
ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_LOGIN = os.getenv("ODOO_LOGIN")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Odoo RPC client with error handling
odoo = None
connection_status = "❌ Non connecté"

def init_odoo_connection():
    """Initialize Odoo connection with proper error handling"""
    global odoo, connection_status
    
    if not all([ODOO_URL, ODOO_DB, ODOO_LOGIN, ODOO_PASSWORD]):
        missing = []
        if not ODOO_URL: missing.append("ODOO_URL")
        if not ODOO_DB: missing.append("ODOO_DB") 
        if not ODOO_LOGIN: missing.append("ODOO_LOGIN")
        if not ODOO_PASSWORD: missing.append("ODOO_PASSWORD")
        connection_status = f"❌ Variables manquantes: {', '.join(missing)}"
        return False
    
    try:
        # Clean and validate URL
        url = ODOO_URL.strip()
        
        # Remove protocol if present (odoorpc will add it)
        if url.startswith('https://'):
            url = url[8:]
        elif url.startswith('http://'):
            url = url[7:]
        
        # Remove trailing slash
        url = url.rstrip('/')
        
        connection_status = f"🔄 Tentative de connexion à {url}..."
        
        # Try HTTPS first (most common for Odoo online)
        try:
            odoo = odoorpc.ODOO(url, protocol='jsonrpc+ssl', port=443)
            odoo.login(ODOO_DB, ODOO_LOGIN, ODOO_PASSWORD)
            connection_status = f"✅ Connecté à {url} (HTTPS)"
            return True
        except Exception as ssl_error:
            # If HTTPS fails, try HTTP
            try:
                odoo = odoorpc.ODOO(url, protocol='jsonrpc', port=8069)
                odoo.login(ODOO_DB, ODOO_LOGIN, ODOO_PASSWORD)
                connection_status = f"✅ Connecté à {url} (HTTP)"
                return True
            except Exception as http_error:
                # Both failed, return detailed error
                connection_status = f"❌ Échec HTTPS: {str(ssl_error)[:100]}... | HTTP: {str(http_error)[:100]}..."
                return False
                
    except Exception as e:
        connection_status = f"❌ Erreur générale: {str(e)}"
        return False

# Try to initialize connection
init_odoo_connection()

# Configure OpenAI
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# MCP tool implementations

def ingest_prospects(records: list[dict]) -> dict:
    """
    Create leads in Odoo CRM from a list of records.
    records: list of dicts with keys matching 'crm.lead' fields
    Returns: {'created_ids': [id1, id2, ...]}
    """
    if not odoo:
        return {"error": "Connexion Odoo non disponible. Configurez les variables d'environnement."}
    
    try:
        created = []
        for rec in records:
            lead_id = odoo.env['crm.lead'].create(rec)
            created.append(lead_id)
        return {"created_ids": created}
    except Exception as e:
        return {"error": f"Erreur lors de la création: {str(e)}"}


def qualify_lead(lead_id: int) -> str:
    """
    Generate a summary and interest score for a lead.
    """
    if not odoo:
        return "❌ Connexion Odoo non disponible. Configurez les variables d'environnement."
    
    if not OPENAI_API_KEY:
        return "❌ Clé OpenAI non configurée."
    
    try:
        lead = odoo.env['crm.lead'].read([lead_id], ['name', 'email_from', 'description'])[0]
        prompt = (
            f"Lead Info:\nName: {lead['name']}\nEmail: {lead.get('email_from','N/A')}\n"
            f"Notes: {lead.get('description','')}\n"
            "Provide a short summary and an interest score (0-100)."
        )
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur: {str(e)}"


def generate_offer(lead_id: int, tone: str) -> str:
    """
    Generate a proposal email or quote based on lead context.
    tone: 'formel', 'vendeur', or 'technique'
    """
    if not odoo:
        return "❌ Connexion Odoo non disponible. Configurez les variables d'environnement."
    
    if not OPENAI_API_KEY:
        return "❌ Clé OpenAI non configurée."
    
    try:
        lead = odoo.env['crm.lead'].read([lead_id], ['name', 'company_id'])[0]
        company = odoo.env['res.partner'].browse(lead['company_id'][0]).name
        prompt = (
            f"Generate a {tone} proposal email for lead {lead['name']} at {company}."
        )
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur: {str(e)}"


def summarize_opportunity(lead_id: int) -> str:
    """
    Return a brief summary of the opportunity status.
    """
    if not odoo:
        return "❌ Connexion Odoo non disponible. Configurez les variables d'environnement."
    
    try:
        opp = odoo.env['crm.lead'].read([lead_id], ['name', 'probability', 'stage_id'])[0]
        return (
            f"Opportunity '{opp['name']}', stage: {opp['stage_id'][1]}, "
            f"probability: {opp['probability']}%."
        )
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

def get_connection_status():
    """Return current connection status"""
    return connection_status

def test_connection():
    """Test and reinitialize connection"""
    success = init_odoo_connection()
    return connection_status

# Function to update environment variables and reconnect
def update_config(odoo_url, odoo_db, odoo_login, odoo_password, openai_key):
    """Update configuration and test connection"""
    global ODOO_URL, ODOO_DB, ODOO_LOGIN, ODOO_PASSWORD, OPENAI_API_KEY
    
    # Validate inputs
    if not odoo_url or not odoo_db or not odoo_login or not odoo_password:
        return "❌ Tous les champs Odoo sont obligatoires"
    
    # Update global variables
    ODOO_URL = odoo_url.strip()
    ODOO_DB = odoo_db.strip()
    ODOO_LOGIN = odoo_login.strip()
    ODOO_PASSWORD = odoo_password
    OPENAI_API_KEY = openai_key.strip() if openai_key else None
    
    # Update OpenAI API key
    if openai_key:
        openai.api_key = openai_key
    
    # Test Odoo connection
    success = init_odoo_connection()
    
    if success:
        return "✅ Configuration mise à jour et connexion réussie !"
    else:
        return f"❌ Configuration mise à jour mais connexion échouée :\n{connection_status}"

def validate_url(url):
    """Validate and suggest URL format"""
    if not url:
        return "❌ URL vide"
    
    url = url.strip()
    
    # Common URL patterns for Odoo
    suggestions = []
    
    if not url.endswith('.odoo.com') and not url.endswith('.com') and not '.' in url:
        suggestions.append(f"Essayez: {url}.odoo.com")
    
    if url.startswith('www.'):
        suggestions.append(f"Essayez sans 'www.': {url[4:]}")
    
    if suggestions:
        return f"💡 Suggestions: {' ou '.join(suggestions)}"
    
    return "✅ Format d'URL valide"

# Build Gradio Interfaces as MCP tools
with gr.Blocks(title="Agent CRM MCP Server") as mcp_app:
    gr.Markdown("# Agent CRM MCP Tools")
    
    # Configuration Section
    with gr.Tab("Configuration"):
        gr.Markdown("## Configuration des paramètres de connexion")
        gr.Markdown("Renseignez vos paramètres de connexion ci-dessous :")
        
        with gr.Column():
            gr.Markdown("### 📋 Exemples de configuration")
            gr.Markdown("""
            **URL Odoo :** 
            - Pour Odoo Online: `votre-entreprise.odoo.com`
            - Pour serveur local: `localhost` ou `192.168.1.100`
            - Pour serveur distant: `odoo.votre-domaine.com`
            
            **Base de données :** Le nom de votre base de données (souvent le nom de votre entreprise)
            
            **Login :** Votre adresse email utilisée pour vous connecter à Odoo
            """)
            
            odoo_url_input = gr.Textbox(
                label="URL Odoo", 
                placeholder="votre-entreprise.odoo.com",
                value=ODOO_URL or "",
                info="Ne pas inclure https:// - sera ajouté automatiquement"
            )
            url_validation = gr.Textbox(label="Validation URL", interactive=False, visible=False)
            
            odoo_db_input = gr.Textbox(
                label="Base de données Odoo", 
                placeholder="ma-entreprise-db",
                value=ODOO_DB or "",
                info="Nom de votre base de données Odoo"
            )
            odoo_login_input = gr.Textbox(
                label="Login Odoo", 
                placeholder="admin@exemple.com",
                value=ODOO_LOGIN or "",
                info="Votre email de connexion Odoo"
            )
            odoo_password_input = gr.Textbox(
                label="Mot de passe Odoo", 
                type="password",
                placeholder="Votre mot de passe",
                value=ODOO_PASSWORD or ""
            )
            openai_key_input = gr.Textbox(
                label="Clé API OpenAI (optionnel)", 
                type="password",
                placeholder="sk-...",
                value=OPENAI_API_KEY or "",
                info="Nécessaire pour les fonctions IA (qualification, génération d'offres)"
            )
            
            update_btn = gr.Button("Mettre à jour la configuration", variant="primary", size="lg")
            config_status = gr.Textbox(label="Statut", interactive=False, lines=3)
            
            # URL validation on change
            odoo_url_input.change(validate_url, inputs=odoo_url_input, outputs=url_validation)
            
            update_btn.click(
                update_config,
                inputs=[odoo_url_input, odoo_db_input, odoo_login_input, odoo_password_input, openai_key_input],
                outputs=config_status
            )
    
    # Main Tools Section
    with gr.Tab("Outils CRM"):
        # Connection Status
        with gr.Row():
            status_display = gr.Textbox(label="Statut de connexion", value=connection_status, interactive=False)
            test_btn = gr.Button("Tester la connexion")
            test_btn.click(test_connection, outputs=status_display)
        
        gr.Markdown("## Outils disponibles")
        gr.Markdown("Utilisez les outils ci-dessous une fois la connexion établie.")
        
        # Ingest Prospects
        with gr.Group():
            gr.Markdown("### 📥 Ingest Prospects")
            gr.Markdown("Créer des leads dans Odoo à partir d'une liste de prospects")
            
            leads_input = gr.Code(
                label="Leads (JSON format)",
                language="json",
                placeholder='[{"name": "Prospect Test", "partner_name": "Entreprise Test", "email_from": "test@exemple.com"}]',
                lines=10,
                interactive=True
            )
            
            with gr.Row():
                clear_leads_btn = gr.Button("Effacer", variant="secondary")
                submit_leads_btn = gr.Button("Créer les leads", variant="primary")
            
            leads_output = gr.JSON(label="IDs des leads créés")
            
            # Example button
            example_leads_btn = gr.Button("📋 Charger un exemple", variant="secondary")
            
            def load_example_leads():
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
                try:
                    import json
                    leads_data = json.loads(leads_json) if isinstance(leads_json, str) else leads_json
                    return ingest_prospects(leads_data)
                except json.JSONDecodeError:
                    return {"error": "Format JSON invalide"}
                except Exception as e:
                    return {"error": f"Erreur: {str(e)}"}
            
            example_leads_btn.click(load_example_leads, outputs=leads_input)
            clear_leads_btn.click(lambda: "", outputs=leads_input)
            submit_leads_btn.click(process_leads, inputs=leads_input, outputs=leads_output)
        
        # Qualify Lead
        with gr.Group():
            gr.Markdown("### 🔍 Qualify Lead")
            gr.Markdown("Analyser un lead avec l'IA et obtenir un score d'intérêt")
            
            with gr.Row():
                qualify_lead_id = gr.Number(label="Lead ID", precision=0, value=0)
                qualify_btn = gr.Button("Analyser le lead", variant="primary")
            
            qualify_output = gr.Textbox(label="Analyse et score", lines=5, interactive=False)
            
            qualify_btn.click(qualify_lead, inputs=qualify_lead_id, outputs=qualify_output)
        
        # Generate Offer
        with gr.Group():
            gr.Markdown("### 📧 Generate Offer")
            gr.Markdown("Générer une proposition commerciale personnalisée")
            
            with gr.Row():
                offer_lead_id = gr.Number(label="Lead ID", precision=0, value=0)
                offer_tone = gr.Dropdown(
                    label="Tone", 
                    choices=["formel", "vendeur", "technique"], 
                    value="formel"
                )
                generate_btn = gr.Button("Générer l'offre", variant="primary")
            
            offer_output = gr.Textbox(label="Proposition générée", lines=8, interactive=False)
            
            generate_btn.click(generate_offer, inputs=[offer_lead_id, offer_tone], outputs=offer_output)
        
        # Summarize Opportunity
        with gr.Group():
            gr.Markdown("### 📊 Summarize Opportunity")
            gr.Markdown("Obtenir un résumé de l'état d'une opportunité")
            
            with gr.Row():
                summary_lead_id = gr.Number(label="Lead ID", precision=0, value=0)
                summary_btn = gr.Button("Résumer l'opportunité", variant="primary")
            
            summary_output = gr.Textbox(label="Résumé de l'opportunité", lines=3, interactive=False)
            
            summary_btn.click(summarize_opportunity, inputs=summary_lead_id, outputs=summary_output)

# Launch as MCP Server
if __name__ == "__main__":
    mcp_app.launch() 