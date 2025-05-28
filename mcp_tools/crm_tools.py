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
    
    if not records:
        return {"error": "Aucun enregistrement fourni"}
    
    try:
        created = []
        for i, rec in enumerate(records):
            try:
                # Vérifier que le champ 'name' est présent (requis pour crm.lead)
                if not rec.get('name'):
                    return {"error": f"Enregistrement {i+1}: Le champ 'name' est requis"}
                
                # Nettoyer les données - supprimer les clés vides ou None
                clean_rec = {k: v for k, v in rec.items() if v is not None and v != ''}
                
                # Créer le lead
                lead_id = odoo.env['crm.lead'].create(clean_rec)
                created.append(lead_id)
                
            except Exception as e:
                return {"error": f"Erreur lors de la création de l'enregistrement {i+1}: {str(e)}"}
        
        return {"created_ids": created, "count": len(created)}
        
    except Exception as e:
        return {"error": f"Erreur générale lors de la création: {str(e)}"}


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
        # Vérifier que le lead existe
        if not lead_id or lead_id <= 0:
            return "❌ ID de lead invalide"
            
        lead = odoo.env['crm.lead'].read([lead_id], ['name', 'email_from', 'description', 'partner_name', 'phone'])
        
        if not lead:
            return f"❌ Aucun lead trouvé avec l'ID {lead_id}"
            
        lead = lead[0]
        prompt = (
            f"Informations du Lead:\n"
            f"Nom: {lead.get('name', 'N/A')}\n"
            f"Entreprise: {lead.get('partner_name', 'N/A')}\n"
            f"Email: {lead.get('email_from', 'N/A')}\n"
            f"Téléphone: {lead.get('phone', 'N/A')}\n"
            f"Notes: {lead.get('description', 'Aucune description')}\n\n"
            "Fournissez un résumé court et un score d'intérêt (0-100) pour ce prospect."
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
        # Vérifier que le lead existe
        if not lead_id or lead_id <= 0:
            return "❌ ID de lead invalide"
            
        lead = odoo.env['crm.lead'].read([lead_id], ['name', 'partner_name', 'email_from', 'description'])
        
        if not lead:
            return f"❌ Aucun lead trouvé avec l'ID {lead_id}"
            
        lead = lead[0]
        company = lead.get('partner_name', 'votre entreprise')
        
        prompt = (
            f"Générez un email de proposition {tone} pour le lead {lead.get('name', 'N/A')} "
            f"chez {company}. "
            f"Contexte: {lead.get('description', 'Aucune information supplémentaire')}"
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
        # Vérifier que le lead existe
        if not lead_id or lead_id <= 0:
            return "❌ ID de lead invalide"
            
        opp = odoo.env['crm.lead'].read([lead_id], ['name', 'probability', 'stage_id', 'expected_revenue'])
        
        if not opp:
            return f"❌ Aucune opportunité trouvée avec l'ID {lead_id}"
            
        opp = opp[0]
        stage_name = opp['stage_id'][1] if opp.get('stage_id') else 'Non définie'
        
        return (
            f"Opportunité '{opp.get('name', 'N/A')}'\n"
            f"Étape: {stage_name}\n"
            f"Probabilité: {opp.get('probability', 0)}%\n"
            f"Revenus attendus: {opp.get('expected_revenue', 0)} €"
        )
        
    except Exception as e:
        return f"❌ Erreur: {str(e)}" 