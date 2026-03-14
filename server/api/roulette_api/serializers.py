from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Wallet, Transaction


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=3,
        error_messages={
            'blank': 'Username is required.',
            'min_length': 'Username must contain at least 3 characters.',
        },
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False,
        error_messages={
            'blank': 'Password is required.',
            'min_length': 'Password must contain at least 8 characters.',
        },
    )

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate_username(self, value):
        normalized = value.strip()
        if len(normalized) < 3:
            raise serializers.ValidationError('Username must contain at least 3 characters.')
        return normalized

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as err:
            raise serializers.ValidationError(err.messages) from err
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'wallet',
            'amount',
            'description',
            'description_key',
            'description_context',
            'timestamp',
        ]
