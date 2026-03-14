import json
from unittest.mock import mock_open, patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from roulette_api.models import Transaction, Wallet
from roulette_api.tests.test_roulette import all_two
from roulette_api.views import SpinRouletteView


class UserCreateViewTests(APITestCase):
    def test_create_user_success(self):
        url = reverse("user_create")
        data = {"username": "newuser", "password": "newpassword123"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "newuser")
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_create_user_invalid_data(self):
        url = reverse("user_create")
        data = {"username": "", "password": "newpassword123"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_create_user_with_short_username(self):
        url = reverse("user_create")
        data = {"username": "ab", "password": "newpassword123"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_create_user_with_weak_password(self):
        url = reverse("user_create")
        data = {"username": "secure-user", "password": "12345"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)


class LogoutViewTests(APITestCase):
    def test_logout_success(self):
        with patch("roulette_api.views.token_validation") as mock_token_validation:
            mock_token_validation.return_value = {"user_id": 1}
            url = reverse("logout")
            response = self.client.post(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["detail"], "Logout successful")
            self.assertIn("access_token", response.cookies)

    def test_logout_invalid_token(self):
        with patch("roulette_api.views.token_validation") as mock_token_validation:
            mock_token_validation.return_value = 401
            url = reverse("logout")
            response = self.client.post(url)

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.data["error"], "Invalid token.")

    def test_logout_token_not_provided(self):
        with patch("roulette_api.views.token_validation") as mock_token_validation:
            mock_token_validation.return_value = 400
            url = reverse("logout")
            response = self.client.post(url)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data["error"], "Token not provided")


class IsAuthenticatedViewTests(APITestCase):
    @patch("roulette_api.views.token_validation")
    def test_authenticated_user(self, mock_token_validation):
        mock_token_validation.return_value = {"user_id": 1}
        url = reverse("is_authenticated")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["isAuthenticated"])

    @patch("roulette_api.views.token_validation")
    def test_invalid_token(self, mock_token_validation):
        mock_token_validation.return_value = 401
        url = reverse("is_authenticated")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid token.")

    @patch("roulette_api.views.token_validation")
    def test_token_not_provided(self, mock_token_validation):
        mock_token_validation.return_value = 400
        url = reverse("is_authenticated")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Token not provided")


class BetApiViewTests(APITestCase):
    @patch("roulette_api.views.token_validation")
    def test_get_bets_with_valid_token(self, mock_token_validation):
        mock_token_validation.return_value = {"user_id": 1}
        mock_bets_content = {
            "bets": [
                "straight-up",
                "split",
                "street",
                "two street",
                "corner",
                "line",
                "1st 12",
                "2nd 12",
                "3rd 12",
                "1-18",
                "even",
                "red",
                "black",
                "odd",
                "19-36",
            ]
        }

        with patch("builtins.open", new_callable=mock_open, read_data=json.dumps(mock_bets_content)):
            url = reverse("bet_api")
            response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, mock_bets_content)

    @patch("roulette_api.views.token_validation")
    def test_get_bets_with_invalid_token(self, mock_token_validation):
        mock_token_validation.return_value = 401
        url = reverse("bet_api")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid token.")

    @patch("roulette_api.views.token_validation")
    def test_get_bets_without_token(self, mock_token_validation):
        mock_token_validation.return_value = 400
        url = reverse("bet_api")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Token not provided")

    @patch("roulette_api.views.token_validation")
    def test_get_bets_file_not_found(self, mock_token_validation):
        mock_token_validation.return_value = {"user_id": 1}
        with patch("builtins.open", side_effect=FileNotFoundError):
            url = reverse("bet_api")
            response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["bets"], ["error"])


class SpinRouletteViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="spin-user", password="123")
        self.wallet = Wallet.objects.get(user=self.user)

    @patch("roulette_api.views.token_validation")
    def test_spin_roulette_with_invalid_token(self, mock_token_validation):
        mock_token_validation.return_value = 401
        url = reverse("spin_roulette")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch("roulette_api.views.token_validation")
    def test_spin_roulette_without_token(self, mock_token_validation):
        mock_token_validation.return_value = 400
        url = reverse("spin_roulette")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("roulette_api.views.token_validation")
    def test_spin_roulette_with_insufficient_balance(self, mock_token_validation):
        mock_token_validation.return_value = {"user_id": self.user.id}
        bets_data = {"b1": [5, "straight-up", [19]]}

        url = reverse("spin_roulette")
        response = self.client.post(url, bets_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Insufficient balance.")

    @patch("roulette_api.views.token_validation")
    @patch("roulette_api.views.randint")
    def test_spin_roulette_with_valid_bet(self, mock_randint, mock_token_validation):
        mock_token_validation.return_value = {"user_id": self.user.id}
        mock_randint.return_value = 19

        Transaction.objects.create(wallet=self.wallet, amount=100, description="deposit")
        bets_data = {"b1": [10, "straight-up", [19]]}

        url = reverse("spin_roulette")
        response = self.client.post(url, bets_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["drawn_number"], 19)
        self.assertEqual(response.data["total_winnings"], "350.00")

        self.wallet.refresh_from_db()
        self.assertEqual(float(self.wallet.balance), 450.0)


class SpinBetVerification(TestCase):
    def setUp(self):
        self.obj = SpinRouletteView()

    def test_straight_up_bet_valid(self):
        for i in range(0, 37):
            self.assertTrue(self.obj.bet_is_valid(5, "straight-up", [i]))

    def test_split_bet_valid(self):
        for numbers in all_two():
            self.assertTrue(self.obj.bet_is_valid(10, "split", list(numbers)))

    def test_street_bet_valid(self):
        for numbers in range(1, 13):
            self.assertTrue(
                self.obj.bet_is_valid(
                    10, "street", list(map(lambda it: numbers * 3 + it, [-2, -1, 0]))
                )
            )

    def test_street_bet_invalid(self):
        with self.assertRaises(ValueError):
            self.obj.bet_is_valid(10, "corner", [0, 0, 0])

    def test_two_street_bet_valid(self):
        for numbers in range(1, 7):
            self.assertTrue(
                self.obj.bet_is_valid(
                    10,
                    "two_street",
                    list(map(lambda it: numbers * 3 + it, [-2, -1, 0, 1, 2, 3])),
                )
            )

    def test_invalid_bet(self):
        with self.assertRaises(ValueError):
            self.obj.bet_is_valid(5, "invalid_bet_type", [1, 2, 3])


class WalletAndTransactionApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="wallet-user", password="123")
        self.wallet = Wallet.objects.get(user=self.user)

    @patch("roulette_api.views.token_validation")
    def test_wallet_deposit_and_wallet_summary(self, mock_token_validation):
        mock_token_validation.return_value = {"user_id": self.user.id}

        deposit_url = reverse("wallet_deposit")
        deposit_response = self.client.post(deposit_url, {"amount": 250}, format="json")
        self.assertEqual(deposit_response.status_code, status.HTTP_200_OK)

        wallet_url = reverse("wallet")
        wallet_response = self.client.get(wallet_url)
        self.assertEqual(wallet_response.status_code, status.HTTP_200_OK)
        self.assertEqual(wallet_response.data["wallet"]["balance"], "250.00")

    @patch("roulette_api.views.token_validation")
    def test_transaction_list(self, mock_token_validation):
        mock_token_validation.return_value = {"user_id": self.user.id}
        Transaction.objects.create(wallet=self.wallet, amount=100, description="deposit")

        url = reverse("transaction_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("pagination", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["description"], "deposit")
        self.assertEqual(response.data["pagination"]["total"], 1)

    @patch("roulette_api.views.token_validation")
    def test_transaction_list_with_search_and_offset(self, mock_token_validation):
        mock_token_validation.return_value = {"user_id": self.user.id}
        Transaction.objects.create(wallet=self.wallet, amount=100, description="deposit")
        Transaction.objects.create(wallet=self.wallet, amount=-20, description="Loss on red")
        Transaction.objects.create(wallet=self.wallet, amount=35, description="Win on split")

        url = reverse("transaction_list")
        response = self.client.get(url, {"q": "loss", "limit": 1, "offset": 0})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pagination"]["total"], 1)
        self.assertEqual(response.data["pagination"]["has_next"], False)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIn("Loss", response.data["results"][0]["description"])


class CookieTokenObtainPairViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "testuser"
        self.password = "testpass"
        self.active_user = User.objects.create_user(
            username=self.username,
            password=self.password,
            is_active=True,
        )

    def test_generate_tokens(self):
        refresh = RefreshToken.for_user(self.active_user)
        self.assertNotEqual("", refresh)
        self.assertNotEqual("", refresh.access_token)
