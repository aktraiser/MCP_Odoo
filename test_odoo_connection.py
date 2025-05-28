#!/usr/bin/env python3
"""
Script de test pour diagnostiquer la connexion Odoo et la création de leads
"""

from odoo_connector.connection import odoo_connector
from config.settings import config

def test_odoo_connection():
    """Tester la connexion et la création de leads Odoo"""
    
    print('=== DIAGNOSTIC CONNEXION ODOO ===')
    print(f'Statut: {odoo_connector.get_status()}')
    print(f'Connecté: {odoo_connector.is_connected}')
    print(f'URL: {config.odoo_url}')
    print(f'DB: {config.odoo_db}')
    print(f'Login: {config.odoo_login}')

    if not odoo_connector.is_connected:
        print('❌ Pas de connexion Odoo')
        return False

    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        print('❌ Instance Odoo non disponible')
        return False

    try:
        # Tester l'accès aux leads
        lead_count = odoo.env['crm.lead'].search_count([])
        print(f'✅ Nombre de leads existants: {lead_count}')
        
        # Tester la création d'un lead simple
        print('\n=== TEST CRÉATION LEAD ===')
        test_lead_data = {
            'name': 'Test Lead Diagnostic',
            'partner_name': 'Test Company',
            'email_from': 'test@example.com'
        }
        
        print(f'Données du lead: {test_lead_data}')
        lead_id = odoo.env['crm.lead'].create(test_lead_data)
        print(f'✅ Lead créé avec ID: {lead_id}')
        
        # Vérifier que le lead existe
        created_lead = odoo.env['crm.lead'].read([lead_id], ['name', 'partner_name', 'email_from'])
        print(f'✅ Lead vérifié: {created_lead}')
        
        # Compter à nouveau
        new_count = odoo.env['crm.lead'].search_count([])
        print(f'✅ Nouveau nombre de leads: {new_count}')
        
        # Lister les derniers leads créés
        recent_leads = odoo.env['crm.lead'].search_read(
            [], 
            ['name', 'partner_name', 'create_date'], 
            order='create_date desc', 
            limit=5
        )
        print(f'\n=== DERNIERS LEADS CRÉÉS ===')
        for lead in recent_leads:
            print(f"ID {lead['id']}: {lead['name']} - {lead['partner_name']} - {lead['create_date']}")
        
        return True
        
    except Exception as e:
        print(f'❌ Erreur lors du test: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_odoo_connection() 