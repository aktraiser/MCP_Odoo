"""
Serveur MCP basé sur Gradio pour Agent CRM
Point d'entrée principal de l'application
"""

import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Agent CRM - Serveur MCP et Interface Gradio")
    parser.add_argument(
        "--mode", 
        choices=["gradio", "mcp"], 
        default="gradio",
        help="Mode de lancement: 'gradio' pour l'interface web, 'mcp' pour le serveur MCP"
    )
    
    args = parser.parse_args()
    
    if args.mode == "mcp":
        # Lancer le serveur MCP
        print("🚀 Lancement du serveur MCP...")
        from mcp_server import mcp
        mcp.run()
    else:
        # Lancer l'interface Gradio (mode par défaut)
        print("🚀 Lancement de l'interface Gradio...")
        from ui.gradio_app import launch_app
        launch_app()

if __name__ == "__main__":
    main() 