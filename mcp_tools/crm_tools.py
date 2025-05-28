"""
Outils MCP pour la gestion CRM
"""
import openai
from odoo_connector.connection import odoo_connector
from config.settings import config

def ingest_prospects(records: list[dict]) -> dict:
    """
    Créer des leads dans Odoo CRM à partir d'une liste d'enregistrements.
    
    Args:
        records: liste de dictionnaires avec des clés correspondant aux champs 'crm.lead'
    
    Returns:
        dict: {'created_ids': [id1, id2, ...]} ou {'error': 'message d'erreur'}
    """
    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        return {"error": "Connexion Odoo non disponible. Configurez les variables d'environnement."}
    
    try:
        created = []
        for rec in records:
            lead_id = odoo.env['crm.lead'].create(rec)
            created.append(lead_id)
        return {"created_ids": created}
    except Exception as e:
        return {"error": f"Erreur lors de la création: {str(e)}"}


def qualify_lead(lead_id: int) -> str:
    """
    Générer un résumé et un score d'intérêt pour un lead.
    
    Args:
        lead_id: ID du lead à analyser
    
    Returns:
        str: Analyse du lead avec score d'intérêt
    """
    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        return "❌ Connexion Odoo non disponible. Configurez les variables d'environnement."
    
    if not config.is_openai_configured():
        return "❌ Clé OpenAI non configurée."
    
    try:
        lead = odoo.env['crm.lead'].read([lead_id], ['name', 'email_from', 'description'])[0]
        prompt = (
            f"Informations du Lead:\nNom: {lead['name']}\nEmail: {lead.get('email_from','N/A')}\n"
            f"Notes: {lead.get('description','')}\n"
            "Fournissez un résumé court et un score d'intérêt (0-100)."
        )
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur: {str(e)}"


def generate_offer(lead_id: int, tone: str) -> str:
    """
    Générer une proposition commerciale basée sur le contexte du lead.
    
    Args:
        lead_id: ID du lead
        tone: 'formel', 'vendeur', ou 'technique'
    
    Returns:
        str: Proposition commerciale générée
    """
    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        return "❌ Connexion Odoo non disponible. Configurez les variables d'environnement."
    
    if not config.is_openai_configured():
        return "❌ Clé OpenAI non configurée."
    
    try:
        lead = odoo.env['crm.lead'].read([lead_id], ['name', 'company_id'])[0]
        company = odoo.env['res.partner'].browse(lead['company_id'][0]).name if lead.get('company_id') else "Entreprise"
        prompt = (
            f"Générez un email de proposition {tone} pour le lead {lead['name']} chez {company}."
        )
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur: {str(e)}"


def summarize_opportunity(lead_id: int) -> str:
    """
    Retourner un résumé bref du statut de l'opportunité.
    
    Args:
        lead_id: ID du lead/opportunité
    
    Returns:
        str: Résumé de l'opportunité
    """
    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        return "❌ Connexion Odoo non disponible. Configurez les variables d'environnement."
    
    try:
        opp = odoo.env['crm.lead'].read([lead_id], ['name', 'probability', 'stage_id'])[0]
        return (
            f"Opportunité '{opp['name']}', étape: {opp['stage_id'][1]}, "
            f"probabilité: {opp['probability']}%."
        )
    except Exception as e:
        return f"❌ Erreur: {str(e)}" 