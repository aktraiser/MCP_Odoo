"""
Serveur MCP pour l'intégration Odoo CRM

Fournit des outils et ressources MCP pour interagir avec les systèmes CRM Odoo
"""

import json
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import Any, AsyncIterator, Dict, List, Optional

from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, Field

from odoo_connector.connection import odoo_connector
from config.settings import config


@dataclass
class AppContext:
    """Contexte d'application pour le serveur MCP"""
    
    odoo_connector: Any


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """
    Cycle de vie de l'application pour l'initialisation et le nettoyage
    """
    # Initialiser le client Odoo au démarrage
    try:
        yield AppContext(odoo_connector=odoo_connector)
    finally:
        # Pas de nettoyage nécessaire pour le client Odoo
        pass


# Créer le serveur MCP
mcp = FastMCP(
    "Odoo CRM MCP Server",
    description="Serveur MCP pour interagir avec les systèmes CRM Odoo",
    dependencies=["odoorpc", "openai"],
    lifespan=app_lifespan,
)


# ----- Ressources MCP -----


@mcp.resource(
    "odoo://crm/leads", 
    description="Liste tous les leads disponibles dans le système CRM Odoo"
)
def get_crm_leads() -> str:
    """Liste tous les leads CRM disponibles"""
    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        return json.dumps({"error": "Connexion Odoo non disponible"}, indent=2)
    
    try:
        leads = odoo.env['crm.lead'].search_read(
            [], 
            ['name', 'partner_name', 'email_from', 'phone', 'stage_id', 'probability'],
            limit=50
        )
        return json.dumps(leads, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.resource(
    "odoo://crm/lead/{lead_id}",
    description="Obtenir des informations détaillées sur un lead spécifique par ID",
)
def get_crm_lead(lead_id: str) -> str:
    """
    Obtenir un lead spécifique par ID

    Parameters:
        lead_id: ID du lead CRM
    """
    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        return json.dumps({"error": "Connexion Odoo non disponible"}, indent=2)
    
    try:
        lead_id_int = int(lead_id)
        lead = odoo.env['crm.lead'].read([lead_id_int])
        if not lead:
            return json.dumps(
                {"error": f"Lead non trouvé: ID {lead_id}"}, indent=2
            )
        return json.dumps(lead[0], indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.resource(
    "odoo://crm/stages",
    description="Liste toutes les étapes CRM disponibles",
)
def get_crm_stages() -> str:
    """Liste toutes les étapes CRM"""
    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        return json.dumps({"error": "Connexion Odoo non disponible"}, indent=2)
    
    try:
        stages = odoo.env['crm.stage'].search_read(
            [], 
            ['name', 'sequence', 'probability', 'fold']
        )
        return json.dumps(stages, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


# ----- Modèles Pydantic pour la sécurité des types -----


class LeadData(BaseModel):
    """Données pour créer un lead CRM"""
    
    name: str = Field(description="Nom du lead (requis)")
    partner_name: Optional[str] = Field(default=None, description="Nom de l'entreprise")
    email_from: Optional[str] = Field(default=None, description="Email du contact")
    phone: Optional[str] = Field(default=None, description="Téléphone du contact")
    description: Optional[str] = Field(default=None, description="Description du lead")
    expected_revenue: Optional[float] = Field(default=None, description="Revenus attendus")
    probability: Optional[float] = Field(default=None, description="Probabilité de succès (0-100)")
    user_id: Optional[int] = Field(default=None, description="ID de l'utilisateur assigné")


class CreateLeadResponse(BaseModel):
    """Réponse pour la création de lead"""
    
    success: bool = Field(description="Indique si la création a réussi")
    lead_id: Optional[int] = Field(default=None, description="ID du lead créé")
    error: Optional[str] = Field(default=None, description="Message d'erreur, le cas échéant")


class IngestProspectsResponse(BaseModel):
    """Réponse pour l'ingestion de prospects"""
    
    success: bool = Field(description="Indique si l'ingestion a réussi")
    created_ids: Optional[List[int]] = Field(default=None, description="Liste des IDs créés")
    count: Optional[int] = Field(default=None, description="Nombre de leads créés")
    error: Optional[str] = Field(default=None, description="Message d'erreur, le cas échéant")


class QualifyLeadResponse(BaseModel):
    """Réponse pour la qualification de lead"""
    
    success: bool = Field(description="Indique si la qualification a réussi")
    analysis: Optional[str] = Field(default=None, description="Analyse du lead")
    error: Optional[str] = Field(default=None, description="Message d'erreur, le cas échéant")


# ----- Outils MCP -----


@mcp.tool(description="Diagnostiquer la connexion Odoo et afficher le statut")
def diagnose_odoo_connection(ctx: Context) -> QualifyLeadResponse:
    """
    Diagnostiquer la connexion Odoo et afficher des informations détaillées

    Returns:
        QualifyLeadResponse: Statut de la connexion et diagnostic
    """
    try:
        # Vérifier la configuration
        if not config.is_odoo_configured():
            missing_vars = config.get_missing_odoo_vars()
            error_msg = f"Configuration Odoo incomplète. Variables manquantes: {', '.join(missing_vars)}\n"
            error_msg += "Créez un fichier .env avec les variables suivantes:\n"
            error_msg += "ODOO_URL=votre-instance-odoo.com\n"
            error_msg += "ODOO_DB=nom-de-votre-base\n"
            error_msg += "ODOO_LOGIN=votre-nom-utilisateur\n"
            error_msg += "ODOO_PASSWORD=votre-mot-de-passe"
            return QualifyLeadResponse(success=False, error=error_msg)
        
        # Vérifier la connexion
        connection_status = odoo_connector.get_status()
        odoo_instance = odoo_connector.get_odoo_instance()
        
        if not odoo_instance:
            # Tenter une reconnexion
            reconnect_success = odoo_connector.reconnect()
            if reconnect_success:
                analysis = f"✅ Reconnexion réussie !\nStatut: {odoo_connector.get_status()}"
                return QualifyLeadResponse(success=True, analysis=analysis)
            else:
                error_msg = f"❌ Connexion Odoo échouée\nStatut: {connection_status}\n"
                error_msg += f"URL configurée: {config.odoo_url}\n"
                error_msg += f"Base de données: {config.odoo_db}\n"
                error_msg += f"Utilisateur: {config.odoo_login}"
                return QualifyLeadResponse(success=False, error=error_msg)
        
        # Tester l'accès aux leads
        try:
            lead_count = odoo_instance.env['crm.lead'].search_count([])
            analysis = f"✅ Connexion Odoo active\n"
            analysis += f"Statut: {connection_status}\n"
            analysis += f"Nombre de leads dans la base: {lead_count}\n"
            analysis += f"URL: {config.odoo_url}\n"
            analysis += f"Base de données: {config.odoo_db}\n"
            analysis += f"Utilisateur: {config.odoo_login}"
            return QualifyLeadResponse(success=True, analysis=analysis)
        except Exception as e:
            error_msg = f"❌ Connexion établie mais erreur d'accès aux données\n"
            error_msg += f"Erreur: {str(e)}\n"
            error_msg += "Vérifiez les droits d'accès de l'utilisateur"
            return QualifyLeadResponse(success=False, error=error_msg)
            
    except Exception as e:
        return QualifyLeadResponse(success=False, error=f"Erreur de diagnostic: {str(e)}")


@mcp.tool(description="Créer un nouveau lead dans le CRM Odoo")
def create_lead(
    ctx: Context,
    lead_data: LeadData,
) -> CreateLeadResponse:
    """
    Créer un nouveau lead dans le CRM Odoo

    Parameters:
        lead_data: Données du lead à créer

    Returns:
        CreateLeadResponse: Résultat de la création
    """
    # Vérifier la configuration Odoo
    if not config.is_odoo_configured():
        missing_vars = config.get_missing_odoo_vars()
        error_msg = f"Configuration Odoo incomplète. Variables manquantes: {', '.join(missing_vars)}"
        return CreateLeadResponse(success=False, error=error_msg)
    
    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        # Tenter une reconnexion
        reconnect_success = odoo_connector.reconnect()
        if not reconnect_success:
            error_msg = f"Connexion Odoo échouée. Statut: {odoo_connector.get_status()}"
            return CreateLeadResponse(success=False, error=error_msg)
        odoo = odoo_connector.get_odoo_instance()
    
    try:
        # Convertir les données Pydantic en dictionnaire
        lead_dict = lead_data.model_dump(exclude_none=True)
        
        # Créer le lead dans Odoo
        lead_id = odoo.env['crm.lead'].create(lead_dict)
        
        # Vérifier que le lead a bien été créé
        created_lead = odoo.env['crm.lead'].read([lead_id], ['name'])
        if not created_lead:
            return CreateLeadResponse(success=False, error="Lead créé mais non trouvé lors de la vérification")
        
        return CreateLeadResponse(success=True, lead_id=lead_id)
        
    except Exception as e:
        error_msg = f"Erreur lors de la création du lead: {str(e)}"
        return CreateLeadResponse(success=False, error=error_msg)


@mcp.tool(description="Ingérer plusieurs prospects dans le CRM Odoo")
def ingest_prospects(
    ctx: Context,
    prospects: List[LeadData],
) -> IngestProspectsResponse:
    """
    Ingérer plusieurs prospects dans le CRM Odoo

    Parameters:
        prospects: Liste des prospects à créer

    Returns:
        IngestProspectsResponse: Résultat de l'ingestion
    """
    # Vérifier la configuration Odoo
    if not config.is_odoo_configured():
        missing_vars = config.get_missing_odoo_vars()
        error_msg = f"Configuration Odoo incomplète. Variables manquantes: {', '.join(missing_vars)}"
        return IngestProspectsResponse(success=False, error=error_msg)
    
    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        # Tenter une reconnexion
        reconnect_success = odoo_connector.reconnect()
        if not reconnect_success:
            error_msg = f"Connexion Odoo échouée. Statut: {odoo_connector.get_status()}"
            return IngestProspectsResponse(success=False, error=error_msg)
        odoo = odoo_connector.get_odoo_instance()
    
    if not prospects:
        return IngestProspectsResponse(success=False, error="Aucun prospect fourni")
    
    try:
        created_ids = []
        
        for i, prospect in enumerate(prospects):
            try:
                # Convertir les données Pydantic en dictionnaire
                prospect_dict = prospect.model_dump(exclude_none=True)
                
                # Créer le lead dans Odoo
                lead_id = odoo.env['crm.lead'].create(prospect_dict)
                
                # Vérifier que le lead a bien été créé
                created_lead = odoo.env['crm.lead'].read([lead_id], ['name'])
                if created_lead:
                    created_ids.append(lead_id)
                else:
                    return IngestProspectsResponse(
                        success=False, 
                        error=f"Prospect {i+1} créé mais non trouvé lors de la vérification"
                    )
                
            except Exception as e:
                return IngestProspectsResponse(
                    success=False, 
                    error=f"Erreur lors de la création du prospect {i+1} ('{prospect.name}'): {str(e)}"
                )
        
        return IngestProspectsResponse(
            success=True, 
            created_ids=created_ids, 
            count=len(created_ids)
        )
        
    except Exception as e:
        return IngestProspectsResponse(success=False, error=f"Erreur générale: {str(e)}")


@mcp.tool(description="Qualifier un lead avec l'IA")
def qualify_lead(
    ctx: Context,
    lead_id: int,
) -> QualifyLeadResponse:
    """
    Qualifier un lead avec l'IA pour obtenir un score d'intérêt

    Parameters:
        lead_id: ID du lead à qualifier

    Returns:
        QualifyLeadResponse: Résultat de la qualification
    """
    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        return QualifyLeadResponse(success=False, error="Connexion Odoo non disponible")
    
    if not config.is_openai_configured():
        return QualifyLeadResponse(success=False, error="Clé OpenAI non configurée")
    
    try:
        # Vérifier que le lead existe
        if not lead_id or lead_id <= 0:
            return QualifyLeadResponse(success=False, error="ID de lead invalide")
            
        lead = odoo.env['crm.lead'].read([lead_id], [
            'name', 'email_from', 'description', 'partner_name', 'phone'
        ])
        
        if not lead:
            return QualifyLeadResponse(
                success=False, 
                error=f"Aucun lead trouvé avec l'ID {lead_id}"
            )
            
        lead = lead[0]
        
        # Préparer le prompt pour l'IA
        prompt = (
            f"Informations du Lead:\n"
            f"Nom: {lead.get('name', 'N/A')}\n"
            f"Entreprise: {lead.get('partner_name', 'N/A')}\n"
            f"Email: {lead.get('email_from', 'N/A')}\n"
            f"Téléphone: {lead.get('phone', 'N/A')}\n"
            f"Notes: {lead.get('description', 'Aucune description')}\n\n"
            "Fournissez un résumé court et un score d'intérêt (0-100) pour ce prospect."
        )
        
        # Appeler l'API OpenAI
        import openai
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        analysis = resp.choices[0].message.content
        
        return QualifyLeadResponse(success=True, analysis=analysis)
        
    except Exception as e:
        return QualifyLeadResponse(success=False, error=str(e))


@mcp.tool(description="Générer une proposition commerciale pour un lead")
def generate_offer(
    ctx: Context,
    lead_id: int,
    tone: str = "formel",
) -> QualifyLeadResponse:
    """
    Générer une proposition commerciale pour un lead

    Parameters:
        lead_id: ID du lead
        tone: Ton de la proposition ('formel', 'vendeur', 'technique')

    Returns:
        QualifyLeadResponse: Proposition générée
    """
    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        return QualifyLeadResponse(success=False, error="Connexion Odoo non disponible")
    
    if not config.is_openai_configured():
        return QualifyLeadResponse(success=False, error="Clé OpenAI non configurée")
    
    try:
        # Vérifier que le lead existe
        if not lead_id or lead_id <= 0:
            return QualifyLeadResponse(success=False, error="ID de lead invalide")
            
        lead = odoo.env['crm.lead'].read([lead_id], [
            'name', 'partner_name', 'email_from', 'description'
        ])
        
        if not lead:
            return QualifyLeadResponse(
                success=False, 
                error=f"Aucun lead trouvé avec l'ID {lead_id}"
            )
            
        lead = lead[0]
        company = lead.get('partner_name', 'votre entreprise')
        
        # Préparer le prompt pour l'IA
        prompt = (
            f"Générez un email de proposition {tone} pour le lead {lead.get('name', 'N/A')} "
            f"chez {company}. "
            f"Contexte: {lead.get('description', 'Aucune information supplémentaire')}"
        )
        
        # Appeler l'API OpenAI
        import openai
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        offer = resp.choices[0].message.content
        
        return QualifyLeadResponse(success=True, analysis=offer)
        
    except Exception as e:
        return QualifyLeadResponse(success=False, error=str(e))


@mcp.tool(description="Résumer le statut d'une opportunité")
def summarize_opportunity(
    ctx: Context,
    lead_id: int,
) -> QualifyLeadResponse:
    """
    Résumer le statut d'une opportunité

    Parameters:
        lead_id: ID du lead/opportunité

    Returns:
        QualifyLeadResponse: Résumé de l'opportunité
    """
    odoo = odoo_connector.get_odoo_instance()
    if not odoo:
        return QualifyLeadResponse(success=False, error="Connexion Odoo non disponible")
    
    try:
        # Vérifier que le lead existe
        if not lead_id or lead_id <= 0:
            return QualifyLeadResponse(success=False, error="ID de lead invalide")
            
        opp = odoo.env['crm.lead'].read([lead_id], [
            'name', 'probability', 'stage_id', 'expected_revenue'
        ])
        
        if not opp:
            return QualifyLeadResponse(
                success=False, 
                error=f"Aucune opportunité trouvée avec l'ID {lead_id}"
            )
            
        opp = opp[0]
        stage_name = opp['stage_id'][1] if opp.get('stage_id') else 'Non définie'
        
        summary = (
            f"Opportunité '{opp.get('name', 'N/A')}'\n"
            f"Étape: {stage_name}\n"
            f"Probabilité: {opp.get('probability', 0)}%\n"
            f"Revenus attendus: {opp.get('expected_revenue', 0)} €"
        )
        
        return QualifyLeadResponse(success=True, analysis=summary)
        
    except Exception as e:
        return QualifyLeadResponse(success=False, error=str(e))


if __name__ == "__main__":
    # Lancer le serveur MCP
    mcp.run() 