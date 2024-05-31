from django.urls import path
from .views import AccountListCreate, AccountDetail, deposit, withdraw, transfer

urlpatterns = [
    path('accounts/', AccountListCreate.as_view(), name='account-list'),
    path('accounts/<int:pk>/', AccountDetail.as_view(), name='account-detail'),
    path('accounts/<int:pk>/deposit/', deposit, name='account-deposit'),
    path('accounts/<int:pk>/withdraw/', withdraw, name='account-withdraw'),
    path('accounts/transfer/', transfer, name='account-transfer'),
]
