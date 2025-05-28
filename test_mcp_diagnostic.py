#!/usr/bin/env python3
"""
Test du diagnostic MCP Odoo
"""

from mcp_server import diagnose_odoo_connection
from fastmcp import Context
import asyncio

async def test_diagnostic():
    """Tester le diagnostic de connexion Odoo dans le serveur MCP"""
    
    # Créer un contexte factice pour le test
    class FakeContext:
        pass
    
    try:
        result = diagnose_odoo_connection(FakeContext())
        print('=== RÉSULTAT DU DIAGNOSTIC MCP ===')
        print(f'Succès: {result.success}')
        if result.success:
            print(f'Analyse: {result.analysis}')
        else:
            print(f'Erreur: {result.error}')
        print('==================================')
        
    except Exception as e:
        print(f'Erreur lors du test: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_diagnostic()) 