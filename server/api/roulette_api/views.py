import json
import os
from decimal import Decimal, InvalidOperation
from pathlib import Path
from random import randint

import environ
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.middleware import csrf
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.views import TokenObtainPairView

from roulette_api.roulette import Bet, BetFactory, InvalidBet

from .models import Transaction, Wallet
from .serializers import TransactionSerializer, UserSerializer, WalletSerializer


BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
env = environ.Env()

BETS_PATH = Path(__file__).resolve().parent / "data" / "bets.json"
MONEY_QUANTIZER = Decimal("0.01")


class UserCreateView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: UserSerializer, 400: "Bad Request"},
        operation_description="Create a new user.",
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    @swagger_auto_schema(
        responses={200: "Logout successful", 400: "Token not provided", 401: "Invalid token"},
        operation_description="Logout user and remove auth cookies.",
    )
    def post(self, request):
        access_token = request.COOKIES.get("access_token")
        result = token_validation(access_token)
        if result == 401:
            return Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        if result == 400:
            return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class IsAuthenticatedView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="User is authenticated",
                examples={"application/json": {"isAuthenticated": True}},
            ),
            400: openapi.Response(
                description="Token not provided",
                examples={"application/json": {"error": "Token not provided"}},
            ),
            401: openapi.Response(
                description="Invalid token",
                examples={"application/json": {"error": "Invalid token"}},
            ),
        },
        operation_description="Check if the user is authenticated",
    )
    def get(self, request):
        access_token = request.COOKIES.get("access_token")
        result = token_validation(access_token)
        if result == 401:
            return Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        if result == 400:
            return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"isAuthenticated": True}, status=status.HTTP_200_OK)


def token_validation(access_token):
    if not access_token:
        return 400

    try:
        untyped_token = UntypedToken(access_token)
        return untyped_token.payload
    except Exception:
        return 401


class BetApiView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Successful retrieval of bets"),
            400: "Token not provided",
            401: "Invalid token",
            500: "Bets file not found",
        },
        operation_description="Retrieve available bets",
    )
    def get(self, request, *args, **kwargs):
        access_token = request.COOKIES.get("access_token")
        result = token_validation(access_token)
        if result == 401:
            return Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        if result == 400:
            return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with open(BETS_PATH, "r", encoding="utf-8") as bets_json:
                bets = json.load(bets_json)
            return Response(bets, status=status.HTTP_200_OK)
        except FileNotFoundError:
            return Response({"bets": ["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WalletView(APIView):
    @swagger_auto_schema(
        responses={
            200: "Wallet loaded",
            400: "Token not provided",
            401: "Invalid token",
            404: "Wallet not found",
        },
        operation_description="Get current wallet balance and latest transactions.",
    )
    def get(self, request):
        user, error_response = get_user_from_cookie(request)
        if error_response is not None:
            return error_response

        wallet = Wallet.objects.filter(user=user).first()
        if wallet is None:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)

        limit = request.query_params.get("limit", 20)
        try:
            limit = max(1, min(int(limit), 100))
        except (TypeError, ValueError):
            limit = 20

        transactions = wallet.transactions.order_by("-timestamp")[:limit]
        return Response(
            {
                "wallet": WalletSerializer(wallet).data,
                "transactions": TransactionSerializer(transactions, many=True).data,
            },
            status=status.HTTP_200_OK,
        )


class WalletDepositView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"amount": openapi.Schema(type=openapi.TYPE_NUMBER)},
            required=["amount"],
            example={"amount": 500},
        ),
        responses={
            200: "Deposit created",
            400: "Invalid amount",
            401: "Invalid token",
            404: "Wallet not found",
        },
        operation_description="Deposit virtual coins in wallet.",
    )
    def post(self, request):
        user, error_response = get_user_from_cookie(request)
        if error_response is not None:
            return error_response

        wallet = Wallet.objects.filter(user=user).first()
        if wallet is None:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)

        amount = parse_money(request.data.get("amount"))
        if amount is None or amount <= 0:
            return Response(
                {"error": "Invalid amount. Provide a positive number."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            description=f"Deposit of {amount} coins",
        )
        wallet.refresh_from_db()
        return Response(
            {
                "message": "Deposit successful",
                "amount": str(amount),
                "new_balance": str(wallet.balance),
            },
            status=status.HTTP_200_OK,
        )


class TransactionListView(APIView):
    @swagger_auto_schema(
        responses={200: "Transactions loaded", 400: "Token not provided", 401: "Invalid token"},
        operation_description=(
            "List wallet transactions with pagination. "
            "Query params: limit (1-200), offset (>=0), q (search by description/amount)."
        ),
    )
    def get(self, request):
        user, error_response = get_user_from_cookie(request)
        if error_response is not None:
            return error_response

        wallet = Wallet.objects.filter(user=user).first()
        if wallet is None:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)

        limit = request.query_params.get("limit", 30)
        try:
            limit = max(1, min(int(limit), 200))
        except (TypeError, ValueError):
            limit = 30

        offset = request.query_params.get("offset", 0)
        try:
            offset = max(0, int(offset))
        except (TypeError, ValueError):
            offset = 0

        q = (request.query_params.get("q") or "").strip()
        transactions_qs = wallet.transactions.all()
        if q:
            query = Q(description__icontains=q)
            parsed_amount = parse_money(q)
            if parsed_amount is not None:
                query |= Q(amount=parsed_amount)
            transactions_qs = transactions_qs.filter(query)

        transactions_qs = transactions_qs.order_by("-timestamp", "-id")
        total = transactions_qs.count()
        sliced_transactions = list(transactions_qs[offset : offset + limit])

        next_offset = offset + len(sliced_transactions)
        has_next = next_offset < total

        return Response(
            {
                "results": TransactionSerializer(sliced_transactions, many=True).data,
                "pagination": {
                    "offset": offset,
                    "limit": limit,
                    "next_offset": next_offset,
                    "has_next": has_next,
                    "total": total,
                },
                "filters": {"q": q},
            },
            status=status.HTTP_200_OK,
        )


class SpinRouletteView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            additional_properties=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
            ),
            example={
                "32": [5, "straight-up", [7]],
                "57": [5, "split", [13, 14]],
                "2nd 12": [5, "2nd 12", [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]],
            },
        ),
        responses={
            200: "Successful spin",
            400: "Invalid bet or insufficient funds",
            401: "Invalid token",
        },
        operation_description="Spin roulette and apply winnings/losses to wallet.",
    )
    def post(self, request, *args, **kwargs):
        user, error_response = get_user_from_cookie(request)
        if error_response is not None:
            return error_response

        wallet = Wallet.objects.filter(user=user).first()
        if wallet is None:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            parsed_bets = self.parse_bets(request.data)
        except ValueError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

        total_stake = sum((bet["value"] for bet in parsed_bets), Decimal("0.00")).quantize(MONEY_QUANTIZER)
        wallet.refresh_from_db()
        if wallet.balance < total_stake:
            return Response(
                {
                    "error": "Insufficient balance.",
                    "required": str(total_stake),
                    "current_balance": str(wallet.balance),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        drawn_number = randint(0, 36)
        total_winnings = Decimal("0.00")
        net_result = Decimal("0.00")
        resolved_bets = []

        for bet_data in parsed_bets:
            bet_value = bet_data["value"]
            bet_numbers = bet_data["numbers"]
            bet_type = bet_data["type"]

            won = drawn_number in bet_numbers
            if won:
                profit = self.calculate_profit(bet_value, len(bet_numbers))
                total_winnings += profit
                net_change = profit
                description = (
                    f"Win on {bet_type}: numbers {bet_numbers}, drawn {drawn_number}, "
                    f"profit {profit}"
                )
            else:
                net_change = -bet_value
                description = (
                    f"Loss on {bet_type}: numbers {bet_numbers}, drawn {drawn_number}, "
                    f"stake {-net_change}"
                )

            net_result += net_change
            Transaction.objects.create(wallet=wallet, amount=net_change, description=description)
            resolved_bets.append(
                {
                    "type": bet_type,
                    "value": str(bet_value),
                    "numbers": bet_numbers,
                    "won": won,
                    "net_change": str(net_change.quantize(MONEY_QUANTIZER)),
                }
            )

        wallet.refresh_from_db()
        return Response(
            {
                "drawn_number": drawn_number,
                "total_bet": str(total_stake),
                "total_winnings": str(total_winnings.quantize(MONEY_QUANTIZER)),
                "net_result": str(net_result.quantize(MONEY_QUANTIZER)),
                "new_balance": str(wallet.balance),
                "resolved_bets": resolved_bets,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def calculate_profit(bet_value, covered_numbers_count):
        payout = (Decimal(36) / Decimal(covered_numbers_count)) * bet_value
        return (payout - bet_value).quantize(MONEY_QUANTIZER)

    def parse_bets(self, raw_bets):
        if not isinstance(raw_bets, dict) or not raw_bets:
            raise ValueError("At least one bet is required.")

        parsed_bets = []
        for _, raw_bet in raw_bets.items():
            if not isinstance(raw_bet, list) or len(raw_bet) != 3:
                raise ValueError("Each bet must follow format [value, type, numbers].")

            bet_value = parse_money(raw_bet[0])
            if bet_value is None or bet_value <= 0:
                raise ValueError("Bet value must be a positive number.")

            bet_type = self.normalize_bet_type(raw_bet[1])
            try:
                bet_numbers = [int(number) for number in raw_bet[2]]
            except (TypeError, ValueError):
                raise ValueError("Bet numbers must be an array of integers.")

            self.bet_is_valid(bet_value, bet_type, bet_numbers)
            parsed_bets.append({"value": bet_value, "type": bet_type, "numbers": bet_numbers})

        return parsed_bets

    @staticmethod
    def normalize_bet_type(raw_type):
        if not isinstance(raw_type, str):
            raise ValueError("Bet type must be a string.")

        normalized = raw_type.strip().lower().replace("-", " ").replace("_", " ")

        mapping = {
            "straight up": "straight-up",
            "split": "split",
            "street": "street",
            "two street": "two_street",
            "corner": "corner",
            "line1": "line1",
            "line 1": "line1",
            "line2": "line2",
            "line 2": "line2",
            "line3": "line3",
            "line 3": "line3",
            "1st 12": "1st 12",
            "1st12": "1st 12",
            "2nd 12": "2nd 12",
            "2nd12": "2nd 12",
            "3rd 12": "3rd 12",
            "3rd12": "3rd 12",
            "1 18": "1-18",
            "1-18": "1-18",
            "even": "even",
            "red": "red",
            "black": "black",
            "odd": "odd",
            "19 36": "19-36",
            "19-36": "19-36",
            "zero bets": "zero_bets",
            "zero_bets": "zero_bets",
        }

        if normalized not in mapping:
            raise ValueError(f"Unknown bet type: {raw_type}")
        return mapping[normalized]

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

        if bet_type not in bet_dict:
            raise ValueError(f"Unknown bet type: {bet_type}")

        try:
            if bet_type in {"straight-up", "split"}:
                result_bet = bet_dict[bet_type](bet_value, ",".join(str(n) for n in bet_numbers))
            elif bet_type in {"street", "two_street", "corner", "zero_bets"}:
                result_bet = bet_dict[bet_type](bet_value, bet_numbers)
            else:
                result_bet = bet_dict[bet_type](bet_value)

            if set(bet.numbers) != result_bet.numbers:
                raise InvalidBet
            return True
        except InvalidBet as exc:
            raise ValueError("Bet not found") from exc


def parse_money(raw_value):
    try:
        return Decimal(str(raw_value)).quantize(MONEY_QUANTIZER)
    except (InvalidOperation, TypeError, ValueError):
        return None


def get_user_from_cookie(request):
    access_token = request.COOKIES.get("access_token")
    result = token_validation(access_token)
    if result == 401:
        return None, Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
    if result == 400:
        return None, Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

    user_id = result.get("user_id")
    if user_id is None:
        return None, Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

    user = User.objects.filter(id=user_id).first()
    if user is None:
        return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    return user, None


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


class CookieTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password"),
            },
            required=["username", "password"],
            example={"username": "yourusername", "password": "yourpassword"},
        ),
        responses={200: "Login successful", 400: "Invalid credentials", 404: "Account not found"},
        operation_description="Obtain JWT pair and set cookies",
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({"Not Found": "Account Not Found"}, status=status.HTTP_404_NOT_FOUND)

        data = get_tokens_for_user(user)
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=data["access"],
            expires=60 * 60,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        response.set_cookie(
            key="refresh_token",
            value=data["refresh"],
            expires=60 * 60 * 24,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        csrf.get_token(request)
        response.data = {"Success": "Login successfully", "data": data}
        return response


class CookieTokenRefreshView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Token refreshed successfully"),
            400: openapi.Response(description="No refresh token provided"),
            401: openapi.Response(description="Invalid or expired token"),
        },
        operation_description="Refresh JWT cookies using refresh token cookie",
    )
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"Error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            data = {"refresh": str(refresh), "access": str(refresh.access_token)}
            response = Response(data, status=status.HTTP_200_OK)
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=data["access"],
                expires=60 * 60,
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            response.set_cookie(
                key="refresh_token",
                value=data["refresh"],
                expires=60 * 60 * 24,
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            return response
        except Exception:
            return Response({"Error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)
