import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Wallet


@pytest.mark.django_db
class TestWalletCreateView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_wallets(self):
        self.user = User.objects.create(username='testuser')
        wallet1 = Wallet.objects.create(user=self.user, currency="ETH", balance=100)
        wallet2 = Wallet.objects.create(user=self.user, currency="ETH", balance=50)
        response = self.client.get('/api/v1/wallets/')

        assert response.status_code == 200
        assert response.data == [
            {
                'id': wallet1.id,
                'currency': wallet1.currency,
                'public_key': wallet1.public_key,
                'balance': wallet1.balance
            },
            {
                'id': wallet2.id,
                'currency': wallet2.currency,
                'public_key': wallet2.public_key,
                'balance': wallet2.balance
            }
        ]

    def test_create_wallet(self):
        self.user = User.objects.create(username='testuser')
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/wallets/', {'currency': 'ETH'})
        assert response.status_code == 201
        assert 'currency' in response.data
        wallet = Wallet.objects.get(public_key=response.data['public_key'])
        assert wallet.balance == 0


@pytest.mark.django_db
class TestTransferView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser')
        self.sender_wallet = Wallet.objects.create(user=self.user, balance=100, public_key="test_key_sender")
        self.recipient_wallet = Wallet.objects.create(user=self.user, balance=50, public_key="test_key_recipient")

    def test_successful_transfer(self):
        response = self.client.post('/api/v1/transactions/', {
            'sender': self.sender_wallet.public_key,
            'recipient': self.recipient_wallet.public_key,
            'amount': 50
        })
        assert response.status_code == 200
        assert response.data == {'status': 'success'}
        self.sender_wallet.refresh_from_db()
        self.recipient_wallet.refresh_from_db()
        assert self.sender_wallet.balance == 50
        assert self.recipient_wallet.balance == 100

    def test_insufficient_funds(self):
        response = self.client.post('/api/v1/transactions/', {
            'sender': self.sender_wallet.public_key,
            'recipient': self.recipient_wallet.public_key,
            'amount': 150
        })
        assert response.status_code == 400
        assert response.data == {'error': 'Insufficient funds'}
        self.sender_wallet.refresh_from_db()
        self.recipient_wallet.refresh_from_db()
        assert self.sender_wallet.balance == 100
        assert self.recipient_wallet.balance == 50

    def test_sender_not_found(self):
        response = self.client.post('/api/v1/transactions/', {
            'sender': 999,
            'recipient': self.recipient_wallet.public_key,
            'amount': 10
        })
        assert response.status_code == 400
        assert response.data == {'error': 'No sender found'}

    def test_recipient_not_found(self):
        response = self.client.post('/api/v1/transactions/', {
            'sender': self.sender_wallet.public_key,
            'recipient': 999,
            'amount': 50
        })
        assert response.status_code == 400
        assert response.data == {'error': 'No recipient found'}