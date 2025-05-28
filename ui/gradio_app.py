"""
Application Gradio principale pour le serveur MCP Agent CRM
"""
import gradio as gr
from ui.config_tab import create_config_tab
from ui.crm_tab import create_crm_tab

def create_gradio_app():
    """Créer l'application Gradio complète"""
    with gr.Blocks(title="Agent CRM MCP Server") as app:
        gr.Markdown("# Agent CRM MCP Tools")
        
        # Créer les onglets
        create_config_tab()
        create_crm_tab()
    
    return app

def launch_app():
    """Lancer l'application Gradio"""
    app = create_gradio_app()
    app.launch() 