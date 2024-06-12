import json
import environ
import os
from random import randint
from pathlib import Path

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken

from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf
from django.contrib.auth.models import User

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import UserSerializer
from .models import Wallet, Transaction
from roulette_api.roulette import Bet, InvalidBet, BetFactory


BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
env = environ.Env()

class UserCreateView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: 'Bad Request'
        },
        operation_description='Create a new user.'
    )

    def post(self, request):
        """
        Creates a new user.

        Returns a 201 status code and the created user data if successful.
        Returns a 400 status code if there are validation errors.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    @swagger_auto_schema(
        responses={
            200: 'Logout successful',
            400: 'Token not provided',
            401: 'Invalid token'
        },
        operation_description="Logout the user by deleting the access token cookie."
    )
    def post(self, request):
        """
        Logs out the user.

        The access token must be provided via an HttpOnly cookie named `access_token`.
        Deletes the access token cookie and returns a 200 status code if successful.
        Returns a 400 status code if the token is not provided.
        Returns a 401 status code if the token is invalid.
        """
        access_token = request.COOKIES.get('access_token')
        result = token_validation(access_token)
        if result != 400 and result != 401:
            response = Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
            response.delete_cookie('access_token')
            return response
        elif result == 401:
            return Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

class IsAuthenticatedView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="User is authenticated",
                examples={
                    "application/json": {
                        "isAuthenticated": True
                    }
                }
            ),
            400: openapi.Response(
                description="Token not provided",
                examples={
                    "application/json": {
                        "error": "Token not provided"
                    }
                }
            ),
            401: openapi.Response(
                description="Invalid token",
                examples={
                    "application/json": {
                        "error": "Invalid token"
                    }
                }
            )
        },
        operation_description="Check if the user is authenticated"
    )
    def get(self, request):
        """
        Check if the user is authenticated

        - The access token must be provided via an HttpOnly cookie named `access_token`.
        - Returns a 200 status code with `isAuthenticated: True` if the token is valid.
        - Returns a 401 status code with an error message if the token is invalid.
        - Returns a 400 status code with an error message if the token is not provided.
        """
        access_token = request.COOKIES.get('access_token')
        result = token_validation(access_token)
        if result != 400 and result != 401:
            response = Response({'isAuthenticated': True}, status=status.HTTP_200_OK)
            return response
        elif result == 401:
            return Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

def token_validation(access_token):
    if access_token:
        try:
            untyped_token = UntypedToken(access_token)
            decoded = untyped_token.payload
            return decoded
        except:
            return 401
    return 400

class BetApiView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Successful retrieval of bets",
                examples={
                    "application/json": {
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
                }
            ),
            400: openapi.Response(
                description="Token not provided",
                examples={
                    "application/json": {
                        "error": "Token not provided"
                    }
                }
            ),
            401: openapi.Response(
                description="Invalid token",
                examples={
                    "application/json": {
                        "error": "Invalid token"
                    }
                }
            )
        },
        operation_description="Retrieve available bets"
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve available bets.

        - The access token must be provided via an HttpOnly cookie named `access_token`.
        - Returns a 200 status code with the bets data if the token is valid.
        - Returns a 401 status code with an error message if the token is invalid.
        - Returns a 400 status code with an error message if the token is not provided.
        """
        access_token = request.COOKIES.get('access_token')
        result = token_validation(access_token)
        if result != 400 and result != 401:
            try:
                with open('./roulette_api/data/bets.json', 'r') as bets_json:
                    bets = json.load(bets_json)
                return Response(bets, status=status.HTTP_200_OK)
            except FileNotFoundError:
                return Response({ "bets": ["error"] }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif result == 401:
            return Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

class SpinRouletteView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            additional_properties=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_STRING
                )
            ),

            example={
                "32": [5, "straight-up", [7]],
                "57": [5, "split", [13,14]],
                "2nd 12": [5,"2nd 12",[13,14,15,16,17,18,19,20,21,22,23,24]],
            }
        ),
        responses={
            200: openapi.Response(
                description="Successful Spin",
                examples={
                    "aplication/json": {
                        "drawn_number": 17,
                        "total_winnings": 150,
                        "new_balance": 1050
                    }
                }
            ),
            400: "Token not provided",
            401: "Invalid token"
        },
        operation_description="Spin the roulette wheel and process bets"
    )
    def post(self, request, *args, **kwargs):
        """
        Spin the roulette wheel and process the bets

        - The access token must be provided via an HttpOnly cookie named `access_token`.
        - If the token is valid, it processes the bets and returns the result of the spin.
        - If the token is invalid, it returns a 401 Unauthorized error.
        - If the token is not provided, it returns a 400 Bad Request error.
        """
        access_token = request.COOKIES.get('access_token')
        result = token_validation(access_token)
        if result != 400 and result != 401:
            user_id = result.get("user_id")
            user = User.objects.get(id=user_id)
            wallet = Wallet.objects.get(user=user)
            bets = request.data
            drawn_number = randint(0, 36)
            total_winnings = 0
            
            for bet_data in bets.values():
                bet_value, bet_type, bet_numbers = bet_data[0], bet_data[1], bet_data[2]
                bet_type = bet_type.strip().lower()
                self.bet_is_valid(bet_value, bet_type, bet_numbers)   
                if drawn_number in bet_numbers:
                    winning = (36 / len(bet_numbers)) * bet_value - bet_value
                    total_winnings += winning

                    Transaction.objects.create(
                        wallet=wallet,
                        amount=winning,
                        description=f"Win: Bet on {bet_numbers} with drawn number {drawn_number}"
                    )
                else:
                    Transaction.objects.create(
                        wallet=wallet,
                        amount=-bet_value,
                        description=f"Lose: Bet on {bet_numbers} with draw number {drawn_number}"
                    )
            wallet.refresh_from_db()

            return (
                Response({
                    "drawn_number": drawn_number,
                    "total_winnigs": total_winnings,
                    "new_balance": wallet.balance
                }, status.HTTP_200_OK)
            )
        elif result == 401:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

    def bet_is_valid(self, bet_value, bet_type, bet_numbers):
        factory = BetFactory()
        bet = Bet(bet_value, bet_numbers)
        bet_dict = {
            "straight-up": factory.create_from_str,
            "split": factory.create_from_str,
            "street": bet.create_street,
            "two_street": bet.create_two_street,
            "corner": bet.create_corner,
            "line1": bet.create_line_one,
            "line2": bet.create_line_two,
            "line3": bet.create_line_three,
            "1st 12": bet.create_first_dozen,
            "2nd 12": bet.create_second_dozen,
            "3rd 12": bet.create_third_dozen,
            "1-18": bet.create_low,
            "even": bet.create_even,
            "red": bet.create_red,
            "black": bet.create_black,
            "odd": bet.create_odd,
            "19-36": bet.create_high,
            "zero_bets": bet.create_zero_bets,
        }
        try:
            bet_types_custom = ["straight-up", "split"]
            bet_types_value_list = ["street", "two street", "corner", "zero_bets"]
            if bet_type in bet_types_custom: 
                result_bet = bet_dict[bet_type](0, ','.join(str(n) for n in bet_numbers))
            elif bet_type in bet_types_value_list:
                result_bet = bet_dict[bet_type](bet_value, bet_numbers)
            else:
                result_bet = bet_dict[bet_type](bet_value)
            if set(bet.numbers) == result_bet.numbers:
                return True
            return Response({"error": "Bet not found"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"error": "Bet not found"}, status=status.HTTP_404_NOT_FOUND)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class CookieTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password')
            },
            required=['username', 'password'],
            example={
                'username': 'yourusername',
                'password': 'yourpassword'
            }
        ),
        responses={
            200: openapi.Response(
                description="Login successfully",
                examples={
                    "application/json": {
                        "Success": "Login successfully",
                        "data": {
                            "refresh": "token_refresh",
                            "access": "token_access"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid credentials",
                examples={
                    "application/json": {
                        "message": "Invalid credentials"
                    }
                }
            ),
            404: openapi.Response(
                description="Account Not Found",
                examples={
                    "application/json": {
                        "Not Found": "Account Not Found!"
                    }
                }
            ),
        },
        operation_description="Obtain a pair of JWT tokens and set an access token cookie"
    )
    def post(self, request, *args, **kwargs):
        """
        Obtain a pair of JWT tokens and set an access token cookie.

        - The access token must be provided via an HttpOnly cookie named `access_token`.
        - Returns a 200 status code with tokens if the login is successful.
        - Returns a 400 status code with an error message if the credentials are invalid.
        - Returns a 404 status code with an error message if the account is not active.
        """
        response = super().post(request, *args, **kwargs)
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value = data["access"],
                    expires=60*60*1,
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                response.data = {"Success": "Login successfully", "data": data}
                return response
            else:
                return Response({"Not Found" : "Account Not Found"}, status=status.HTTP_404_NOT_FOUND)
        else: 
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class CookieTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Token refreshed successfully",
                examples={
                    "application/json": {
                        "access": "new_access_token",
                        "refresh": "new_refresh_token"
                    }
                }
            ),
            400: openapi.Response(
                description="No refresh token provided",
                examples={
                    "application/json": {
                        "Error": "No refresh token provided"
                    }
                }
            ),
            401: openapi.Response(
                description="Invalid or expired token",
                examples={
                    "application/json": {
                        "error": "Invalid or expired token"
                    }
                }
            )
        },
        operation_description="Refresh JWT tokens and set a new access token cookie"
    )
    def post(self, request, *args, **kwargs):
        """
        Refresh JWT tokens and set a new access token cookie.

        - Returns a 200 status code with new tokens if the refresh is successful.
        - Returns a 400 status code with an error message if the token is invalid, expired, or not provided.
        """
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                access_token = refresh.access_token
                response = super().post(request, *args, **kwargs)

                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value = str(access_token),
                    expires=60*60*24,
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                return response
            except Exception as e: 
                return Response({"Error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"Error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)
