#!/usr/bin/env python3
"""
Point d'entrée pour Hugging Face Spaces
Lance le serveur MCP Odoo CRM
"""

import os
import sys

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importer et lancer le serveur MCP
from mcp_odoo_server import demo

if __name__ == "__main__":
    print("🚀 Lancement du serveur MCP Odoo CRM sur Hugging Face Spaces...")
    
    # Configuration pour Hugging Face Spaces
    demo.launch(
        mcp_server=True,  # Active le serveur MCP
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Pas besoin de share sur HF Spaces
        debug=False,
        show_error=True
    ) 