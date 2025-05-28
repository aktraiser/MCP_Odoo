#!/usr/bin/env python3
"""
Test de création de leads via le serveur MCP
"""

from mcp_server import create_lead, ingest_prospects, LeadData
from fastmcp import Context
import asyncio

async def test_lead_creation():
    """Tester la création de leads via le serveur MCP"""
    
    # Créer un contexte factice pour le test
    class FakeContext:
        pass
    
    print('=== TEST CRÉATION LEAD UNIQUE ===')
    try:
        # Test de création d'un lead unique
        lead_data = LeadData(
            name="Test Lead MCP",
            partner_name="Test Company MCP",
            email_from="test-mcp@example.com",
            phone="+33123456789",
            description="Lead créé via le serveur MCP"
        )
        
        result = create_lead(FakeContext(), lead_data)
        print(f'Succès: {result.success}')
        if result.success:
            print(f'Lead créé avec ID: {result.lead_id}')
        else:
            print(f'Erreur: {result.error}')
            
    except Exception as e:
        print(f'Erreur lors du test: {e}')
        import traceback
        traceback.print_exc()
    
    print('\n=== TEST INGESTION MULTIPLE ===')
    try:
        # Test d'ingestion de plusieurs prospects
        prospects = [
            LeadData(
                name="Prospect 1 MCP",
                partner_name="Company 1 MCP",
                email_from="prospect1@example.com"
            ),
            LeadData(
                name="Prospect 2 MCP", 
                partner_name="Company 2 MCP",
                email_from="prospect2@example.com"
            ),
            LeadData(
                name="Prospect 3 MCP",
                partner_name="Company 3 MCP", 
                email_from="prospect3@example.com"
            )
        ]
        
        result = ingest_prospects(FakeContext(), prospects)
        print(f'Succès: {result.success}')
        if result.success:
            print(f'Leads créés: {result.created_ids}')
            print(f'Nombre total: {result.count}')
        else:
            print(f'Erreur: {result.error}')
            
    except Exception as e:
        print(f'Erreur lors du test: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_lead_creation()) 