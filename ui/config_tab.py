"""
Onglet de configuration pour l'interface Gradio
"""
import gradio as gr
from config.settings import config
from ui.utils import validate_url, update_config

def create_config_tab():
    """Créer l'onglet de configuration"""
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
                value=config.odoo_url or "",
                info="Ne pas inclure https:// - sera ajouté automatiquement"
            )
            url_validation = gr.Textbox(label="Validation URL", interactive=False, visible=False)
            
            odoo_db_input = gr.Textbox(
                label="Base de données Odoo", 
                placeholder="ma-entreprise-db",
                value=config.odoo_db or "",
                info="Nom de votre base de données Odoo"
            )
            odoo_login_input = gr.Textbox(
                label="Login Odoo", 
                placeholder="admin@exemple.com",
                value=config.odoo_login or "",
                info="Votre email de connexion Odoo"
            )
            odoo_password_input = gr.Textbox(
                label="Mot de passe Odoo", 
                type="password",
                placeholder="Votre mot de passe",
                value=config.odoo_password or ""
            )
            openai_key_input = gr.Textbox(
                label="Clé API OpenAI (optionnel)", 
                type="password",
                placeholder="sk-...",
                value=config.openai_api_key or "",
                info="Nécessaire pour les fonctions IA (qualification, génération d'offres)"
            )
            
            update_btn = gr.Button("Mettre à jour la configuration", variant="primary", size="lg")
            config_status = gr.Textbox(label="Statut", interactive=False, lines=3)
            
            # Validation d'URL lors du changement
            odoo_url_input.change(validate_url, inputs=odoo_url_input, outputs=url_validation)
            
            update_btn.click(
                update_config,
                inputs=[odoo_url_input, odoo_db_input, odoo_login_input, odoo_password_input, openai_key_input],
                outputs=config_status
            ) 