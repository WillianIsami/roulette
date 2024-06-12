from django.test import TestCase
from django.contrib.auth.models import User
from roulette_api.models import Wallet

class WalletModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_wallet_creation(self):
        wallet = Wallet.objects.get(user=self.user)
        self.assertIsInstance(wallet, Wallet)
        self.assertEqual(wallet.balance, 0.00)
