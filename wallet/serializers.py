from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Wallet
        fields = ('currency', 'user')

    def create(self, validated_data):
        currency = validated_data.get('currency')
        if currency != 'ETH':
            raise serializers.ValidationError("Можем принимать только ETH")
        return super().create(validated_data)


class TransferSerializer(serializers.Serializer):
    sender = serializers.CharField()
    recipient = serializers.CharField()
    amount = serializers.FloatField()
