#!/usr/bin/env python3
"""
Vérifier les leads créés dans Odoo
"""

import odoorpc

def verify_leads():
    """Vérifier les derniers leads créés dans Odoo"""
    
    # Connexion à Odoo
    odoo = odoorpc.ODOO('dasein.odoo.com', protocol='jsonrpc+ssl', port=443)
    odoo.login('dasein', 'lbometon@hotmail.fr', 'bupzEw-kasdy2-nubmoc')

    # Vérifier les derniers leads créés
    recent_leads = odoo.env['crm.lead'].search_read(
        [], 
        ['name', 'partner_name', 'email_from', 'create_date'], 
        order='create_date desc', 
        limit=10
    )

    print('=== DERNIERS LEADS DANS ODOO ===')
    for lead in recent_leads:
        print(f'ID {lead["id"]}: {lead["name"]} - {lead["partner_name"]} - {lead["create_date"]}')
    
    # Compter le total
    total_leads = odoo.env['crm.lead'].search_count([])
    print(f'\n✅ Total des leads dans Odoo: {total_leads}')

if __name__ == "__main__":
    verify_leads() 