"""
Application Gradio pour MCP Odoo CRM
Point d'entrée principal pour Hugging Face Spaces
"""

import gradio as gr
import sys
import os
import json
from typing import List, Dict, Any

# Ajouter le répertoire racine au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Activer le serveur MCP via variable d'environnement
os.environ["GRADIO_MCP_SERVER"] = "True"

from config.settings import config
from odoo_connector.connection import odoo_connector

def diagnose_odoo_connection():
    """
    Diagnostiquer la connexion Odoo et afficher des informations détaillées
    
    Returns:
        str: Statut de la connexion et diagnostic
    """
    try:
        # Vérifier la configuration
        if not config.is_odoo_configured():
            missing_vars = config.get_missing_odoo_vars()
            error_msg = f"Configuration Odoo incomplète. Variables manquantes: {', '.join(missing_vars)}\n"
            error_msg += "Configurez vos informations Odoo dans l'interface."
            return error_msg
        
        # Vérifier la connexion
        connection_status = odoo_connector.get_status()
        odoo_instance = odoo_connector.get_odoo_instance()
        
        if not odoo_instance:
            # Tenter une reconnexion
            reconnect_success = odoo_connector.reconnect()
            if reconnect_success:
                analysis = f"✅ Reconnexion réussie !\nStatut: {odoo_connector.get_status()}"
                return analysis
            else:
                error_msg = f"❌ Connexion Odoo échouée\nStatut: {connection_status}\n"
                error_msg += f"URL configurée: {config.odoo_url}\n"
                error_msg += f"Base de données: {config.odoo_db}\n"
                error_msg += f"Utilisateur: {config.odoo_login}"
                return error_msg
        
        # Tester l'accès aux leads
        try:
            lead_count = odoo_instance.env['crm.lead'].search_count([])
            analysis = f"✅ Connexion Odoo active\n"
            analysis += f"Statut: {connection_status}\n"
            analysis += f"Nombre de leads dans la base: {lead_count}\n"
            analysis += f"URL: {config.odoo_url}\n"
            analysis += f"Base de données: {config.odoo_db}\n"
            analysis += f"Utilisateur: {config.odoo_login}"
            return analysis
        except Exception as e:
            error_msg = f"❌ Connexion établie mais erreur d'accès aux données\n"
            error_msg += f"Erreur: {str(e)}\n"
            error_msg += "Vérifiez les droits d'accès de l'utilisateur"
            return error_msg
            
    except Exception as e:
        return f"Erreur de diagnostic: {str(e)}"

def create_lead(name: str, partner_name: str = "", email_from: str = "", phone: str = "", description: str = ""):
    """
    Créer un nouveau lead dans le CRM Odoo
    
    Args:
        name: Nom du lead (requis)
        partner_name: Nom de l'entreprise
        email_from: Email du contact
        phone: Téléphone du contact
        description: Description du lead
        
    Returns:
        str: Résultat de la création
    """
    # Vérifier la configuration Odoo
    if not config.is_odoo_configured():
        missing_vars = config.get_missing_odoo_vars()
        return f"Configuration Odoo incomplète. Variables manquantes: {', '.join(missing_vars)}"
    
    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        # Tenter une reconnexion
        reconnect_success = odoo_connector.reconnect()
        if not reconnect_success:
            return f"Connexion Odoo échouée. Statut: {odoo_connector.get_status()}"
        odoo = odoo_connector.get_odoo_instance()
    
    try:
        # Préparer les données du lead
        lead_data = {"name": name}
        if partner_name: lead_data["partner_name"] = partner_name
        if email_from: lead_data["email_from"] = email_from
        if phone: lead_data["phone"] = phone
        if description: lead_data["description"] = description
        
        # Créer le lead dans Odoo
        lead_id = odoo.env['crm.lead'].create(lead_data)
        
        # Vérifier que le lead a bien été créé
        created_lead = odoo.env['crm.lead'].read([lead_id], ['name'])
        if not created_lead:
            return "Lead créé mais non trouvé lors de la vérification"
        
        return f"✅ Lead créé avec succès ! ID: {lead_id}"
        
    except Exception as e:
        return f"Erreur lors de la création du lead: {str(e)}"

def ingest_prospects_from_json(prospects_json: str):
    """
    Ingérer plusieurs prospects dans le CRM Odoo à partir d'un JSON
    
    Args:
        prospects_json: JSON contenant la liste des prospects
        
    Returns:
        str: Résultat de l'ingestion
    """
    # Vérifier la configuration Odoo
    if not config.is_odoo_configured():
        missing_vars = config.get_missing_odoo_vars()
        return f"Configuration Odoo incomplète. Variables manquantes: {', '.join(missing_vars)}"
    
    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        # Tenter une reconnexion
        reconnect_success = odoo_connector.reconnect()
        if not reconnect_success:
            return f"Connexion Odoo échouée. Statut: {odoo_connector.get_status()}"
        odoo = odoo_connector.get_odoo_instance()
    
    try:
        # Parser le JSON
        prospects = json.loads(prospects_json)
        if not isinstance(prospects, list):
            return "Le JSON doit contenir une liste de prospects"
        
        if not prospects:
            return "Aucun prospect fourni"
        
        created_ids = []
        errors = []
        
        for i, prospect in enumerate(prospects):
            try:
                # Nettoyer les données du prospect
                cleaned_prospect = clean_prospect_data(prospect)
                
                # Créer le lead dans Odoo
                lead_id = odoo.env['crm.lead'].create(cleaned_prospect)
                
                # Vérifier que le lead a bien été créé
                created_lead = odoo.env['crm.lead'].read([lead_id], ['name'])
                if created_lead:
                    created_ids.append(lead_id)
                else:
                    errors.append(f"Prospect {i+1} créé mais non trouvé lors de la vérification")
                
            except Exception as e:
                errors.append(f"Prospect {i+1} ('{prospect.get('name', 'Sans nom')}'): {str(e)}")
        
        result = f"✅ {len(created_ids)} prospects créés avec succès ! IDs: {created_ids}"
        if errors:
            result += f"\n\n❌ Erreurs rencontrées:\n" + "\n".join(errors)
        
        return result
        
    except json.JSONDecodeError as e:
        return f"Erreur: JSON invalide - {str(e)}"
    except Exception as e:
        return f"Erreur générale: {str(e)}"

def configure_odoo(url: str, db: str, login: str, password: str):
    """
    Configurer la connexion Odoo
    
    Args:
        url: URL de l'instance Odoo
        db: Nom de la base de données
        login: Login utilisateur
        password: Mot de passe
        
    Returns:
        str: Résultat de la configuration
    """
    try:
        config.update_odoo_config(url, db, login, password)
        
        # Tester la connexion
        reconnect_success = odoo_connector.reconnect()
        if reconnect_success:
            return f"✅ Configuration Odoo mise à jour et connexion réussie !"
        else:
            return f"❌ Configuration mise à jour mais connexion échouée. Vérifiez vos paramètres."
            
    except Exception as e:
        return f"Erreur lors de la configuration: {str(e)}"

def process_uploaded_file(file):
    """
    Traiter un fichier JSON uploadé par l'utilisateur
    
    Args:
        file: Objet fichier Gradio uploadé
        
    Returns:
        str: Contenu JSON du fichier ou message d'erreur
    """
    if not file:
        return "Aucun fichier sélectionné"
    
    try:
        with open(file.name, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Valider que c'est du JSON valide
        json.loads(content)
        
        return content
    except json.JSONDecodeError:
        return "Erreur: Le fichier n'est pas un JSON valide"
    except Exception as e:
        return f"Erreur lors de la lecture du fichier: {str(e)}"

def load_example_leads():
    """
    Charger le fichier d'exemple de leads
    
    Returns:
        str: Contenu JSON du fichier d'exemple
    """
    try:
        with open('example_leads.json', 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Erreur lors du chargement du fichier d'exemple: {str(e)}"

def clean_prospect_data(prospect: Dict[str, Any]) -> Dict[str, Any]:
    """
    Nettoyer les données d'un prospect pour éviter les erreurs Odoo
    
    Args:
        prospect: Données brutes du prospect
        
    Returns:
        Dict: Données nettoyées
    """
    # Champs autorisés pour la création de leads
    allowed_fields = {
        'name', 'partner_name', 'email_from', 'phone', 'description', 
        'expected_revenue', 'probability', 'street', 'city', 'zip', 
        'country_id', 'state_id', 'website', 'mobile'
    }
    
    # Filtrer les champs autorisés
    cleaned = {k: v for k, v in prospect.items() if k in allowed_fields}
    
    # S'assurer que le nom est présent
    if 'name' not in cleaned or not cleaned['name']:
        cleaned['name'] = f"Lead importé - {cleaned.get('partner_name', 'Sans nom')}"
    
    return cleaned

# Créer l'interface Gradio avec les outils MCP
with gr.Blocks(title="MCP Odoo CRM", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏢 MCP Odoo CRM")
    gr.Markdown("Interface Gradio avec serveur MCP intégré pour la gestion CRM Odoo")
    
    with gr.Tab("🔧 Configuration"):
        gr.Markdown("### Configuration de la connexion Odoo")
        with gr.Row():
            url_input = gr.Textbox(label="URL Odoo", value="dasein.odoo.com", placeholder="votre-instance.odoo.com")
            db_input = gr.Textbox(label="Base de données", value="dasein", placeholder="nom-de-votre-base")
        with gr.Row():
            login_input = gr.Textbox(label="Login", value="lbometon@hotmail.fr", placeholder="votre-email")
            password_input = gr.Textbox(label="Mot de passe", type="password", value="bupzEw-kasdy2-nubmoc")
        
        config_btn = gr.Button("Configurer Odoo", variant="primary")
        config_output = gr.Textbox(label="Résultat", lines=3)
        
        config_btn.click(
            configure_odoo,
            inputs=[url_input, db_input, login_input, password_input],
            outputs=config_output
        )
    
    with gr.Tab("📊 Diagnostic"):
        gr.Markdown("### Diagnostic de la connexion Odoo")
        diag_btn = gr.Button("Diagnostiquer la connexion", variant="primary")
        diag_output = gr.Textbox(label="Diagnostic", lines=10)
        
        diag_btn.click(diagnose_odoo_connection, outputs=diag_output)
    
    with gr.Tab("➕ Créer Lead"):
        gr.Markdown("### Créer un nouveau lead")
        with gr.Row():
            lead_name = gr.Textbox(label="Nom du lead *", placeholder="Prospect TechCorp")
            lead_company = gr.Textbox(label="Entreprise", placeholder="TechCorp Solutions")
        with gr.Row():
            lead_email = gr.Textbox(label="Email", placeholder="contact@techcorp.com")
            lead_phone = gr.Textbox(label="Téléphone", placeholder="+33 1 23 45 67 89")
        lead_desc = gr.Textbox(label="Description", lines=3, placeholder="Description du lead...")
        
        create_btn = gr.Button("Créer le Lead", variant="primary")
        create_output = gr.Textbox(label="Résultat", lines=2)
        
        create_btn.click(
            create_lead,
            inputs=[lead_name, lead_company, lead_email, lead_phone, lead_desc],
            outputs=create_output
        )
    
    with gr.Tab("📥 Import JSON"):
        gr.Markdown("### Importer plusieurs prospects depuis JSON")
        gr.Markdown("**Option 1:** Chargez un fichier JSON depuis votre ordinateur")
        
        with gr.Row():
            file_upload = gr.File(
                label="Fichier JSON", 
                file_types=[".json"],
                file_count="single"
            )
            load_example_btn = gr.Button("📁 Charger l'exemple", variant="secondary")
        
        gr.Markdown("**Option 2:** Collez directement le JSON dans la zone de texte")
        gr.Markdown("Format attendu: `[{\"name\": \"Lead 1\", \"partner_name\": \"Company 1\", \"email_from\": \"email1@example.com\"}, ...]`")
        
        json_input = gr.Textbox(
            label="JSON des prospects", 
            lines=15,
            placeholder='[{"name": "Lead 1", "partner_name": "Company 1", "email_from": "email1@example.com"}]'
        )
        
        import_btn = gr.Button("Importer les prospects", variant="primary")
        import_output = gr.Textbox(label="Résultat", lines=8)
        
        # Connecter les événements
        file_upload.upload(
            process_uploaded_file,
            inputs=file_upload,
            outputs=json_input
        )
        
        load_example_btn.click(
            load_example_leads,
            outputs=json_input
        )
        
        import_btn.click(
            ingest_prospects_from_json,
            inputs=json_input,
            outputs=import_output
        )
    
    gr.Markdown("---")
    gr.Markdown("### 🔗 Serveur MCP")
    gr.Markdown("Cette application expose automatiquement un serveur MCP. L'URL du serveur sera affichée dans les logs au démarrage.")

def main():
    """Point d'entrée principal pour Hugging Face Spaces"""
    print("🚀 Lancement de l'application MCP Odoo CRM...")
    
    # Lancer l'application (le serveur MCP est activé via la variable d'environnement)
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=False
    )

if __name__ == "__main__":
    main() 