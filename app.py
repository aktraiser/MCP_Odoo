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
        connection_status = "❌ Variables d'environnement manquantes"
        return False
    
    try:
        odoo = odoorpc.ODOO(ODOO_URL, protocol='jsonrpc+ssl')
        odoo.login(ODOO_DB, ODOO_LOGIN, ODOO_PASSWORD)
        connection_status = "✅ Connecté à Odoo"
        return True
    except Exception as e:
        connection_status = f"❌ Erreur de connexion: {str(e)}"
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

# Build Gradio Interfaces as MCP tools
with gr.Blocks(title="Agent CRM MCP Server") as mcp_app:
    gr.Markdown("# Agent CRM MCP Tools")
    
    # Connection Status
    with gr.Row():
        status_display = gr.Textbox(label="Statut de connexion", value=connection_status, interactive=False)
        test_btn = gr.Button("Tester la connexion")
        test_btn.click(test_connection, outputs=status_display)
    
    gr.Markdown("## Configuration requise")
    gr.Markdown("""
    Pour utiliser cette application, configurez les variables d'environnement suivantes dans les Settings de votre Space :
    - `ODOO_URL` : URL de votre instance Odoo
    - `ODOO_DB` : Nom de votre base de données
    - `ODOO_LOGIN` : Nom d'utilisateur Odoo
    - `ODOO_PASSWORD` : Mot de passe Odoo
    - `OPENAI_API_KEY` : Votre clé API OpenAI
    """)
    
    # Ingest Prospects
    gr.Interface(
        fn=ingest_prospects,
        inputs=gr.JSON(label="Leads (list of records)"),
        outputs=gr.JSON(label="Created Lead IDs"),
        title="Ingest Prospects",
    )
    # Qualify Lead
    gr.Interface(
        fn=qualify_lead,
        inputs=gr.Number(label="Lead ID", precision=0),
        outputs=gr.Text(label="Summary & Score"),
        title="Qualify Lead",
    )
    # Generate Offer
    gr.Interface(
        fn=generate_offer,
        inputs=[
            gr.Number(label="Lead ID", precision=0),
            gr.Dropdown(label="Tone", choices=["formel", "vendeur", "technique"], value="formel")
        ],
        outputs=gr.Text(label="Proposal Email"),
        title="Generate Offer",
    )
    # Summarize Opportunity
    gr.Interface(
        fn=summarize_opportunity,
        inputs=gr.Number(label="Lead ID", precision=0),
        outputs=gr.Text(label="Opportunity Summary"),
        title="Summarize Opportunity",
    )

# Launch as MCP Server
if __name__ == "__main__":
    mcp_app.launch() 