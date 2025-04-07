
import unittest
from app import app

class SecureCommunicationsTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Secure Communications", response.get_json()["message"])

    def test_analyze_message(self):
        response = self.app.post('/analyze_message', json={"message": "This is urgent."})
        self.assertEqual(response.status_code, 200)
        self.assertIn("analysis", response.get_json())

    def test_secure_message(self):
        message_data = {"peer_public_key": "abcd1234", "message": "Test secure message"}
        response = self.app.post('/secure_message', json=message_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("encrypted_message", response.get_json())

if __name__ == '__main__':
    unittest.main()
