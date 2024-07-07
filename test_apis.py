import unittest
from unittest.mock import patch, Mock
import requests

from api1 import StatementAnalyzer
from api2 import EndpointChecker
from api3 import PDFComparator

class TestAPIs(unittest.TestCase):
    
    def setUp(self):
        self.statement_analyzer = StatementAnalyzer()
        self.endpoint_checker = EndpointChecker('https://www.google.com')
        self.pdf_comparator = PDFComparator('version1.pdf', 'version2.pdf')
    
    def test_statement_analyzer(self):
        text = "some stupid and shit incorect spelling logikal bad room paris london."
        result = self.statement_analyzer.analyze(text)
        
        self.assertIn('incorect', result['incorrect_spellings'])
        self.assertIn('stupid', result['profanity_words'])
        self.assertEqual(result['nouns'], sorted(result['nouns'], key=len))
    
    @patch('requests.get')
    def test_endpoint_checker(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        status = self.endpoint_checker.check_status()
        
        self.assertEqual(status['ResponseCode'], 200)
        self.assertTrue(status['IsAlive'])
    
    @patch.object(PDFComparator, 'read_pdf', side_effect=[
        "Paragraph one. Paragraph two.",
        "Paragraph one. Changed paragraph two."
    ])
    def test_pdf_comparator(self, mock_read_pdf):
        result = self.pdf_comparator.compare_pdfs()
        
        expected_changes = [
            '- Paragraph two.',
            '+ Changed paragraph two.'
        ]
        
        self.assertTrue(any(change for change in result['changes'] if '- Paragraph two.' in change and '+ Changed paragraph two.' in change))

if __name__ == '__main__':
    unittest.main()
