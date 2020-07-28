import unittest
import json
from flaskr import create_app
from models import Account

class BankTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

    def tearDown(self):
        pass

    def test_get_index_page(self):
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

    def test_create_account(self):
        res = self.client().post('/accounts/create', json={
            'first_name': 'Test_f',
            'last_name': 'Test_l',
            'balance': '55555',
            'password': '444'
        })

        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(data['first_name'])
        self.assertTrue(data['last_name'])
        self.assertTrue(data['balance'])

    def test_400_create_account(self):
        res = self.client().post('/accounts/create', json={
            'first_name': 'Test_f',
            'last_name': 'Test_l',
            'balance': '55555',
            'password': ''
        })

        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
        self.assertTrue(data['message'])
    
if __name__ == '__main__':
    unittest.main()