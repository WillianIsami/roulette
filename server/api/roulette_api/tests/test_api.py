from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import patch, mock_open
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from roulette_api.views import SpinRouletteView
from roulette_api.tests.test_roulette import all_two
import json

class UserCreateViewTests(APITestCase):
    def test_create_user_success(self):
        url = reverse('user_create')
        data = {
            'username': 'newuser',
            'password': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_create_user_invalid_data(self):
        url = reverse('user_create')
        data = {
            'username': '',
            'password': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

class LogoutViewTests(APITestCase):
    def test_logout_success(self):
        with patch('roulette_api.views.token_validation') as mock_token_validation:
            mock_token_validation.return_value = {"user_id": 1}
            url = reverse('logout')
            response = self.client.post(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue('access_token' in response.cookies)
            self.assertEqual(response.cookies['access_token'].value, '')
            self.assertEqual(response.data['detail'], 'Logout successful')

    def test_logout_invalid_token(self):
        with patch('roulette_api.views.token_validation') as mock_token_validation:
            mock_token_validation.return_value = 401
            url = reverse('logout')
            response = self.client.post(url)

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertIn('error', response.data)
            self.assertEqual(response.data['error'], 'Invalid token.')

    def test_logout_token_not_provided(self):
        with patch('roulette_api.views.token_validation') as mock_token_validation:
            mock_token_validation.return_value = 400
            url = reverse('logout')
            response = self.client.post(url)
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('error', response.data)
            self.assertEqual(response.data['error'], 'Token not provided')

class IsAuthenticatedViewTests(APITestCase):
    @patch('roulette_api.views.token_validation')
    def test_authenticated_user(self, mock_token_validation):
        mock_token_validation.return_value = {'user_id': 1}
        url = reverse('is_authenticated')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['isAuthenticated'])

    @patch('roulette_api.views.token_validation')
    def test_invalid_token(self, mock_token_validation):
        mock_token_validation.return_value = 401
        url = reverse('is_authenticated')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid token.')

    @patch('roulette_api.views.token_validation')
    def test_token_not_provided(self, mock_token_validation):
        mock_token_validation.return_value = 400
        url = reverse('is_authenticated')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Token not provided')


class IsAuthenticatedViewTests(APITestCase):
    @patch('roulette_api.views.token_validation')
    def test_authenticated_user(self, mock_token_validation):
        mock_token_validation.return_value = {'user_id': 1}
        url = reverse('is_authenticated')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['isAuthenticated'])

    @patch('roulette_api.views.token_validation')
    def test_invalid_token(self, mock_token_validation):
        mock_token_validation.return_value = 401
        url = reverse('is_authenticated')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid token.')

    @patch('roulette_api.views.token_validation')
    def test_token_not_provided(self, mock_token_validation):
        mock_token_validation.return_value = 400
        url = reverse('is_authenticated')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Token not provided')


class BetApiViewTests(APITestCase):
    @patch('roulette_api.views.token_validation')
    def test_get_bets_with_valid_token(self, mock_token_validation):
        mock_token_validation.return_value = {'user_id': 1}
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
                "19-36"
            ]
        }
        with patch('builtins.open', new_callable=mock_open, read_data=json.dumps(mock_bets_content)):
            url = reverse('bet_api')
            response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, mock_bets_content)

    @patch('roulette_api.views.token_validation')
    def test_get_bets_with_invalid_token(self, mock_token_validation):
        mock_token_validation.return_value = 401
        url = reverse('bet_api')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid token.')

    @patch('roulette_api.views.token_validation')
    def test_get_bets_without_token(self, mock_token_validation):
        mock_token_validation.return_value = 400
        url = reverse('bet_api')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Token not provided')

    @patch('roulette_api.views.token_validation')
    def test_get_bets_file_not_found(self, mock_token_validation):
        mock_token_validation.return_value = {'user_id': 1}
        with patch('builtins.open', side_effect=FileNotFoundError):
            url = reverse('bet_api')
            response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('bets', response.data)
        self.assertEqual(response.data['bets'], ['error'])

class SpinRouletteViewTests(APITestCase):

    # @patch('roulette_api.views.token_validation')
    # @patch('roulette_api.views.User.objects.get')
    # @patch('roulette_api.views.Wallet.objects.get')
    # @patch('roulette_api.views.Transaction.objects.create')
    # def test_spin_roulette_with_valid_token_and_valid_bets(self, mock_create_transaction, mock_get_wallet, mock_get_user, mock_token_validation):
    #     bets_data = {
    #         "80": [5,"straight-up",[19]]
    #     }
    #     url = reverse('spin_roulette')
    #     response = self.client.post(url, bets_data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    @patch('roulette_api.views.token_validation')
    def test_spin_roulette_with_invalid_token(self, mock_token_validation):
        mock_token_validation.return_value = 401
        url = reverse('spin_roulette')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    @patch('roulette_api.views.token_validation')
    def test_spin_roulette_without_token(self, mock_token_validation):
        mock_token_validation.return_value = 400
        url = reverse('spin_roulette')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    # @patch('roulette_api.views.token_validation')
    # def test_spin_roulette_with_invalid_bet(self, mock_token_validation):
    #     mock_token_validation.return_value = {"user_id": 1}
    #     invalid_bets_data = {
    #         "invalid_bet": [10, "invalid_bet_type", [1]]
    #     }
    #     url = reverse('spin_roulette')
    #     response = self.client.post(url, invalid_bets_data)
        
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.data['error'], 'Bet not found')


class SpinBetVerification(TestCase):
    def setUp(self):
        self.obj = SpinRouletteView()
    
    def test_straight_up_bet_valid(self):
        bet_value = 5
        bet_type = "straight-up"
        for i in range(0,37):
            bet_numbers = [i]
            self.assertTrue(self.obj.bet_is_valid(bet_value, bet_type, bet_numbers))
    
    def test_split_bet_valid(self):
        bet_value = 10
        bet_type = "split"
        for numbers in all_two():
            self.assertTrue(self.obj.bet_is_valid(bet_value, bet_type, list(numbers)))
    
    def test_street_bet_valid(self):
        bet_value = 10
        bet_type = "street"
        for numbers in range(1,13):
            self.assertTrue(self.obj.bet_is_valid(bet_value, bet_type, list(map(lambda it: numbers*3+it, [-2,-1,0]))))
    
    def test_street_bet_invalid(self):
        bet_value = 10
        bet_type = "corner"
        expected_data = Response({"error": "Bet not found"}, status=status.HTTP_404_NOT_FOUND)
        response = self.obj.bet_is_valid(bet_value, bet_type, [0,0,0])
        self.assertEqual(response.data, expected_data.data)
        # for numbers in range(1,13):
        #     response = self.obj.bet_is_valid(bet_value, bet_type, list(map(lambda it: numbers*3+it, [0,0,0])))
        #     self.assertEqual(response.data, expected_data.data)
    
    def test_two_street_bet_valid(self):
        bet_value = 10
        bet_type = "two street"
        for numbers in range(1,7):
            self.assertTrue(self.obj.bet_is_valid(bet_value, bet_type, list(map(lambda it: numbers*3+it, [-2,-1,0,1,2,3]))))

    def test_invalid_bet(self):
        bet_value = 5
        bet_type = "invalid_bet_type"
        bet_numbers = [1, 2, 3]
        expected_data = Response({"error": "Bet not found"}, status=status.HTTP_404_NOT_FOUND)
        response = self.obj.bet_is_valid(bet_value, bet_type, bet_numbers)
        self.assertEqual(response.data, expected_data.data)

class CookieTokenObtainPairViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'testuser'
        self.password = 'testpass'
        self.active_user = User.objects.create_user(username=self.username, password=self.password, is_active=True)

    def test_generate_tokens(self):
        refresh = RefreshToken.for_user(self.active_user)
        self.assertNotEqual('', refresh)
        self.assertNotEqual('', refresh.access_token)
