"""
Application Gradio pour MCP Odoo CRM
Point d'entrée principal pour Hugging Face Spaces
"""

import gradio as gr
import sys
import os

# Ajouter le répertoire racine au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.gradio_app import create_gradio_interface

def main():
    """Point d'entrée principal pour Hugging Face Spaces"""
    print("🚀 Lancement de l'application MCP Odoo CRM...")
    
    # Créer l'interface Gradio
    app = create_gradio_interface()
    
    # Lancer l'application
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=False
    )

if __name__ == "__main__":
    main() 