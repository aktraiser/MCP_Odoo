"""
Gestion de la connexion Odoo RPC
"""
import odoorpc
from config.settings import config

class OdooConnector:
    """Gestionnaire de connexion Odoo"""
    
    def __init__(self):
        self.odoo = None
        self.connection_status = "❌ Non connecté"
        self.is_connected = False
        
        # Tentative de connexion initiale
        self.connect()
    
    def connect(self):
        """Initialiser la connexion Odoo avec gestion d'erreurs"""
        if not config.is_odoo_configured():
            missing = config.get_missing_odoo_vars()
            self.connection_status = f"❌ Variables manquantes: {', '.join(missing)}"
            self.is_connected = False
            return False
        
        try:
            # Nettoyer et valider l'URL
            url = config.odoo_url.strip()
            
            # Supprimer le protocole si présent (odoorpc l'ajoutera)
            if url.startswith('https://'):
                url = url[8:]
            elif url.startswith('http://'):
                url = url[7:]
            
            # Supprimer le slash final
            url = url.rstrip('/')
            
            self.connection_status = f"🔄 Tentative de connexion à {url}..."
            
            # Essayer HTTPS d'abord (plus courant pour Odoo online)
            try:
                self.odoo = odoorpc.ODOO(url, protocol='jsonrpc+ssl', port=443)
                self.odoo.login(config.odoo_db, config.odoo_login, config.odoo_password)
                self.connection_status = f"✅ Connecté à {url} (HTTPS)"
                self.is_connected = True
                return True
            except Exception as ssl_error:
                # Si HTTPS échoue, essayer HTTP
                try:
                    self.odoo = odoorpc.ODOO(url, protocol='jsonrpc', port=8069)
                    self.odoo.login(config.odoo_db, config.odoo_login, config.odoo_password)
                    self.connection_status = f"✅ Connecté à {url} (HTTP)"
                    self.is_connected = True
                    return True
                except Exception as http_error:
                    # Les deux ont échoué, retourner l'erreur détaillée
                    self.connection_status = f"❌ Échec HTTPS: {str(ssl_error)[:100]}... | HTTP: {str(http_error)[:100]}..."
                    self.is_connected = False
                    return False
                    
        except Exception as e:
            self.connection_status = f"❌ Erreur générale: {str(e)}"
            self.is_connected = False
            return False
    
    def reconnect(self):
        """Reconnecter avec la configuration actuelle"""
        return self.connect()
    
    def get_status(self):
        """Retourner le statut de connexion actuel"""
        return self.connection_status
    
    def get_odoo_instance(self):
        """Retourner l'instance Odoo si connectée"""
        if self.is_connected and self.odoo:
            return self.odoo
        return None
    
    def update_config_and_reconnect(self, url, db, login, password):
        """Mettre à jour la configuration et reconnecter"""
        # Valider les entrées
        if not url or not db or not login or not password:
            return "❌ Tous les champs Odoo sont obligatoires"
        
        # Mettre à jour la configuration
        config.update_odoo_config(url, db, login, password)
        
        # Tester la connexion Odoo
        success = self.connect()
        
        if success:
            return "✅ Configuration mise à jour et connexion réussie !"
        else:
            return f"❌ Configuration mise à jour mais connexion échouée :\n{self.connection_status}"

# Instance globale du connecteur
odoo_connector = OdooConnector() 