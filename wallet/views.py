from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet
from .serializers import WalletSerializer, TransferSerializer
from .utilities import create_eth_account


class WalletCreateView(generics.ListCreateAPIView):
    """Create a wallet for the user"""
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [
            {
                'id': wallet.id, 'currency': wallet.currency,
                'public_key': wallet.public_key, 'balance': wallet.balance
            }
            for wallet in queryset]
        return Response(data)

    def perform_create(self, serializer):
        private_key, public_key = create_eth_account()
        public_key_value = f"{public_key}"
        private_key_value = f"{private_key}"
        instance = serializer.save(public_key=public_key_value, private_key=private_key_value)
        self.created_instance = instance

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        wallet = self.created_instance
        response.data = {
            'id': wallet.id,
            'currency': wallet.currency,
            'public_key': wallet.public_key
        }
        return response


class TransferView(APIView):
    """Transfer money from one wallet to another"""
    serializer_class = TransferSerializer

    def post(self, request):
        sender = request.data.get('sender')
        recipient = request.data.get('recipient')
        amount = request.data.get('amount')

        # Check the presence of purses in the system
        if not Wallet.objects.filter(public_key=sender).exists():
            return Response({'error': 'No sender found'}, status=400)
        if not Wallet.objects.filter(public_key=recipient).exists():
            return Response({'error': 'No recipient found'}, status=400)

        # Balance check of sender’s wallet
        sender_wallet = Wallet.objects.get(public_key=sender)
        if sender_wallet.balance < float(amount):
            return Response({'error': 'Insufficient funds'}, status=400)

        # Funds transfer execution
        with transaction.atomic():  # If an exception occurs during translation, the changes will be undone
            sender_wallet.balance -= float(amount)
            sender_wallet.save()
            recipient_wallet = Wallet.objects.get(public_key=recipient)
            recipient_wallet.balance += float(amount)
            recipient_wallet.save()

        return Response({'status': 'success'})
