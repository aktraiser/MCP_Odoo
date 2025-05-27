#!/usr/bin/env python3
"""
Tests pour l'application Agent CRM MCP Server
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock

# Ajouter le répertoire parent au path pour importer app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestAgentCRMMCP(unittest.TestCase):
    """Tests pour les fonctions MCP du CRM"""
    
    def setUp(self):
        """Configuration des tests"""
        # Mock des variables d'environnement
        self.env_patcher = patch.dict(os.environ, {
            'ODOO_URL': 'test.odoo.com',
            'ODOO_DB': 'test_db',
            'ODOO_LOGIN': 'test_user',
            'ODOO_PASSWORD': 'test_pass',
            'OPENAI_API_KEY': 'test_key'
        })
        self.env_patcher.start()
        
        # Mock d'odoorpc
        self.odoo_patcher = patch('odoorpc.ODOO')
        self.mock_odoo_class = self.odoo_patcher.start()
        self.mock_odoo = Mock()
        self.mock_odoo_class.return_value = self.mock_odoo
        
        # Mock d'openai
        self.openai_patcher = patch('openai.ChatCompletion.create')
        self.mock_openai = self.openai_patcher.start()
        
    def tearDown(self):
        """Nettoyage après les tests"""
        self.env_patcher.stop()
        self.odoo_patcher.stop()
        self.openai_patcher.stop()
    
    def test_environment_variables(self):
        """Test que les variables d'environnement sont correctement chargées"""
        self.assertEqual(os.getenv('ODOO_URL'), 'test.odoo.com')
        self.assertEqual(os.getenv('ODOO_DB'), 'test_db')
        self.assertEqual(os.getenv('OPENAI_API_KEY'), 'test_key')
    
    def test_ingest_prospects(self):
        """Test de la fonction ingest_prospects"""
        # Import après le mock
        from app import ingest_prospects
        
        # Configuration du mock
        self.mock_odoo.env = {'crm.lead': Mock()}
        self.mock_odoo.env['crm.lead'].create.side_effect = [1, 2, 3]
        
        # Test data
        test_records = [
            {'name': 'Test Lead 1', 'email_from': 'test1@example.com'},
            {'name': 'Test Lead 2', 'email_from': 'test2@example.com'},
            {'name': 'Test Lead 3', 'email_from': 'test3@example.com'}
        ]
        
        # Exécution
        result = ingest_prospects(test_records)
        
        # Vérifications
        self.assertEqual(result, {'created_ids': [1, 2, 3]})
        self.assertEqual(self.mock_odoo.env['crm.lead'].create.call_count, 3)
    
    def test_qualify_lead(self):
        """Test de la fonction qualify_lead"""
        from app import qualify_lead
        
        # Configuration du mock Odoo
        mock_lead_data = [{
            'name': 'Test Lead',
            'email_from': 'test@example.com',
            'description': 'Test description'
        }]
        self.mock_odoo.env = {'crm.lead': Mock()}
        self.mock_odoo.env['crm.lead'].read.return_value = mock_lead_data
        
        # Configuration du mock OpenAI
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test summary with score: 85/100"
        self.mock_openai.return_value = mock_response
        
        # Exécution
        result = qualify_lead(1)
        
        # Vérifications
        self.assertEqual(result, "Test summary with score: 85/100")
        self.mock_odoo.env['crm.lead'].read.assert_called_once_with([1], ['name', 'email_from', 'description'])
        self.mock_openai.assert_called_once()
    
    def test_generate_offer(self):
        """Test de la fonction generate_offer"""
        from app import generate_offer
        
        # Configuration du mock Odoo
        mock_lead_data = [{
            'name': 'Test Lead',
            'company_id': [1, 'Test Company']
        }]
        self.mock_odoo.env = {'crm.lead': Mock(), 'res.partner': Mock()}
        self.mock_odoo.env['crm.lead'].read.return_value = mock_lead_data
        
        mock_company = Mock()
        mock_company.name = 'Test Company'
        self.mock_odoo.env['res.partner'].browse.return_value = mock_company
        
        # Configuration du mock OpenAI
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test proposal email"
        self.mock_openai.return_value = mock_response
        
        # Exécution
        result = generate_offer(1, 'formel')
        
        # Vérifications
        self.assertEqual(result, "Test proposal email")
        self.mock_openai.assert_called_once()
    
    def test_summarize_opportunity(self):
        """Test de la fonction summarize_opportunity"""
        from app import summarize_opportunity
        
        # Configuration du mock
        mock_opp_data = [{
            'name': 'Test Opportunity',
            'probability': 75,
            'stage_id': [1, 'Qualified']
        }]
        self.mock_odoo.env = {'crm.lead': Mock()}
        self.mock_odoo.env['crm.lead'].read.return_value = mock_opp_data
        
        # Exécution
        result = summarize_opportunity(1)
        
        # Vérifications
        expected = "Opportunity 'Test Opportunity', stage: Qualified, probability: 75%."
        self.assertEqual(result, expected)

def run_tests():
    """Fonction pour exécuter tous les tests"""
    print("🧪 Lancement des tests...")
    
    # Créer la suite de tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAgentCRMMCP)
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Afficher le résultat
    if result.wasSuccessful():
        print("✅ Tous les tests sont passés avec succès!")
        return True
    else:
        print("❌ Certains tests ont échoué.")
        return False

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1) 