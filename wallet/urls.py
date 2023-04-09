from django.urls import path
from .views import WalletCreateView, TransferView

urlpatterns = [
    path('api/v1/wallets/', WalletCreateView.as_view(), name='wallet-create'),
    path('api/v1/transactions/', TransferView.as_view(), name='transfer'),
]
