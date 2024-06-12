from django.test import TestCase
from django.contrib.auth.models import User
from roulette_api.models import Wallet, Transaction

class TransactionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.wallet = Wallet.objects.get(user=self.user)

    def test_transaction_creation(self):
        transaction = Transaction.objects.create(wallet=self.wallet, amount=50.00)
        self.wallet.refresh_from_db()
        
        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(transaction.amount, 50.00)
        self.assertEqual(self.wallet.balance, 50.00)