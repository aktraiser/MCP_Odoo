#!/usr/bin/env python3
"""
Test final de l'application MCP Odoo CRM
Valide que l'interface web et le serveur MCP fonctionnent correctement
"""

import requests
import json
import time

def test_gradio_app():
    """Test de l'interface Gradio"""
    print("🧪 Test de l'interface Gradio...")
    
    try:
        response = requests.get("http://localhost:7860", timeout=5)
        if response.status_code == 200:
            print("✅ Interface Gradio accessible")
            return True
        else:
            print(f"❌ Interface Gradio inaccessible (code: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test Gradio: {e}")
        return False

def test_mcp_endpoint():
    """Test de l'endpoint MCP SSE"""
    print("🧪 Test de l'endpoint MCP SSE...")
    
    try:
        response = requests.head("http://localhost:7860/gradio_api/mcp/sse", timeout=5)
        if response.status_code == 200:
            print("✅ Endpoint MCP SSE accessible")
            return True
        else:
            print(f"❌ Endpoint MCP SSE inaccessible (code: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test MCP: {e}")
        return False

def test_gradio_api():
    """Test de l'API Gradio"""
    print("🧪 Test de l'API Gradio...")
    
    try:
        response = requests.get("http://localhost:7860/info", timeout=5)
        if response.status_code == 200:
            info = response.json()
            print(f"✅ API Gradio accessible - Version: {info.get('version', 'inconnue')}")
            return True
        else:
            print(f"❌ API Gradio inaccessible (code: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test API: {e}")
        return False

def main():
    """Test principal"""
    print("🚀 Tests finaux de l'application MCP Odoo CRM")
    print("=" * 50)
    
    # Attendre que l'application soit prête
    print("⏳ Attente du démarrage de l'application...")
    time.sleep(3)
    
    tests = [
        test_gradio_app,
        test_mcp_endpoint,
        test_gradio_api
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    print("=" * 50)
    print("📊 Résultats des tests:")
    
    if all(results):
        print("🎉 Tous les tests sont passés avec succès !")
        print("✅ L'application est prête pour le déploiement")
        print()
        print("🔗 URLs disponibles:")
        print("   - Interface web: http://localhost:7860")
        print("   - Serveur MCP: http://localhost:7860/gradio_api/mcp/sse")
        print()
        print("📝 Configuration pour Claude Desktop:")
        print(json.dumps({
            "mcpServers": {
                "odoo-crm": {
                    "url": "http://localhost:7860/gradio_api/mcp/sse"
                }
            }
        }, indent=2))
    else:
        print("❌ Certains tests ont échoué")
        print("🔧 Vérifiez que l'application est bien lancée")

if __name__ == "__main__":
    main() 