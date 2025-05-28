#!/usr/bin/env python3
"""
Test complet du serveur MCP Odoo
"""

import asyncio
from mcp_server import mcp, LeadData

async def test_mcp_server():
    """Tester le serveur MCP complet"""
    
    print('=== TEST SERVEUR MCP ODOO ===')
    
    # Test du diagnostic
    print('\n1. Test du diagnostic de connexion...')
    try:
        # Simuler un appel d'outil MCP
        from fastmcp import Context
        
        class FakeContext:
            pass
        
        # Importer les fonctions directement
        from mcp_server import diagnose_odoo_connection
        
        result = diagnose_odoo_connection(FakeContext())
        print(f'✅ Diagnostic: {result.success}')
        if result.success:
            print(f'   Statut: {result.analysis[:100]}...')
        else:
            print(f'   Erreur: {result.error}')
            
    except Exception as e:
        print(f'❌ Erreur diagnostic: {e}')
    
    # Test de création de lead
    print('\n2. Test de création de lead...')
    try:
        from mcp_server import create_lead
        
        lead_data = LeadData(
            name="Test MCP Server",
            partner_name="Test Company MCP Server",
            email_from="test-server@example.com",
            description="Lead créé via test du serveur MCP complet"
        )
        
        result = create_lead(FakeContext(), lead_data)
        print(f'✅ Création lead: {result.success}')
        if result.success:
            print(f'   Lead ID: {result.lead_id}')
        else:
            print(f'   Erreur: {result.error}')
            
    except Exception as e:
        print(f'❌ Erreur création lead: {e}')
    
    # Test d'ingestion multiple
    print('\n3. Test d\'ingestion multiple...')
    try:
        from mcp_server import ingest_prospects
        
        prospects = [
            LeadData(
                name="Prospect MCP 1",
                partner_name="Company MCP 1",
                email_from="prospect1-mcp@example.com"
            ),
            LeadData(
                name="Prospect MCP 2",
                partner_name="Company MCP 2", 
                email_from="prospect2-mcp@example.com"
            )
        ]
        
        result = ingest_prospects(FakeContext(), prospects)
        print(f'✅ Ingestion: {result.success}')
        if result.success:
            print(f'   IDs créés: {result.created_ids}')
            print(f'   Nombre: {result.count}')
        else:
            print(f'   Erreur: {result.error}')
            
    except Exception as e:
        print(f'❌ Erreur ingestion: {e}')
    
    print('\n=== FIN DES TESTS ===')

if __name__ == "__main__":
    asyncio.run(test_mcp_server()) 