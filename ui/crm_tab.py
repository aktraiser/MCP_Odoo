"""
Onglet des outils CRM pour l'interface Gradio
"""
import gradio as gr
from ui.utils import get_connection_status, test_connection, load_example_leads, process_leads
from mcp_tools.crm_tools import qualify_lead, generate_offer, summarize_opportunity

def create_crm_tab():
    """Créer l'onglet des outils CRM"""
    with gr.Tab("Outils CRM"):
        # Statut de connexion
        with gr.Row():
            status_display = gr.Textbox(
                label="Statut de connexion", 
                value=get_connection_status(), 
                interactive=False
            )
            test_btn = gr.Button("Tester la connexion")
            test_btn.click(test_connection, outputs=status_display)
        
        gr.Markdown("## Outils disponibles")
        gr.Markdown("Utilisez les outils ci-dessous une fois la connexion établie.")
        
        # Ingest Prospects
        with gr.Group():
            gr.Markdown("### 📥 Ingest Prospects")
            gr.Markdown("Créer des leads dans Odoo à partir d'une liste de prospects")
            gr.Markdown("**Format attendu :** `[{\"name\": \"Prospect Test\", \"partner_name\": \"Entreprise Test\", \"email_from\": \"test@exemple.com\"}]`")
            
            leads_input = gr.Code(
                label="Leads (JSON format)",
                language="json",
                lines=10,
                interactive=True
            )
            
            with gr.Row():
                clear_leads_btn = gr.Button("Effacer", variant="secondary")
                submit_leads_btn = gr.Button("Créer les leads", variant="primary")
            
            leads_output = gr.JSON(label="IDs des leads créés")
            
            # Bouton d'exemple
            example_leads_btn = gr.Button("📋 Charger un exemple", variant="secondary")
            
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