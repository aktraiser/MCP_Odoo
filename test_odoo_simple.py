#!/usr/bin/env python3
"""
Script de test simple pour diagnostiquer la création de leads Odoo
"""

import odoorpc

def test_odoo_direct():
    """Tester directement la connexion et création de leads"""
    
    # Configuration directe (remplacez par vos vraies valeurs)
    ODOO_URL = "dasein.odoo.com"
    ODOO_DB = "dasein"
    ODOO_LOGIN = input("Entrez votre login Odoo: ")
    ODOO_PASSWORD = input("Entrez votre mot de passe Odoo: ")
    
    print('=== TEST CONNEXION ODOO DIRECTE ===')
    
    try:
        # Connexion HTTPS
        odoo = odoorpc.ODOO(ODOO_URL, protocol='jsonrpc+ssl', port=443)
        odoo.login(ODOO_DB, ODOO_LOGIN, ODOO_PASSWORD)
        print(f'✅ Connexion réussie à {ODOO_URL}')
        
        # Tester l'accès aux leads
        lead_count = odoo.env['crm.lead'].search_count([])
        print(f'✅ Nombre de leads existants: {lead_count}')
        
        # Tester la création d'un lead simple
        print('\n=== TEST CRÉATION LEAD ===')
        test_lead_data = {
            'name': 'Test Lead Diagnostic Direct',
            'partner_name': 'Test Company Direct',
            'email_from': 'test-direct@example.com'
        }
        
        print(f'Données du lead: {test_lead_data}')
        lead_id = odoo.env['crm.lead'].create(test_lead_data)
        print(f'✅ Lead créé avec ID: {lead_id}')
        print(f'Type de lead_id: {type(lead_id)}')
        
        # Vérifier que le lead existe
        created_lead = odoo.env['crm.lead'].read([lead_id], ['name', 'partner_name', 'email_from'])
        print(f'✅ Lead vérifié: {created_lead}')
        
        # Compter à nouveau
        new_count = odoo.env['crm.lead'].search_count([])
        print(f'✅ Nouveau nombre de leads: {new_count}')
        print(f'✅ Différence: {new_count - lead_count}')
        
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
    test_odoo_direct() 