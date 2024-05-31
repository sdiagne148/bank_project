from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Account
from .serializers import AccountSerializer
from decimal import Decimal, InvalidOperation

class AccountListCreate(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

@api_view(['POST'])
def deposit(request, pk):
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    amount = request.data.get("amount")
    if not amount:
        return Response({"error": "No amount provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        amount = Decimal(amount)
    except InvalidOperation:
        return Response({"error": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)

    account.balance += amount
    account.save()
    return Response(AccountSerializer(account).data)

@api_view(['POST'])
def withdraw(request, pk):
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    amount = request.data.get("amount")
    if not amount:
        return Response({"error": "No amount provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        amount = Decimal(amount)
    except InvalidOperation:
        return Response({"error": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)

    if account.balance < amount:
        return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

    account.balance -= amount
    account.save()
    return Response(AccountSerializer(account).data)

@api_view(['POST'])
def transfer(request):
    from_account_code = request.data.get("from_account")
    to_account_code = request.data.get("to_account")
    amount = request.data.get("amount")

    if not from_account_code or not to_account_code or not amount:
        return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        from_account = Account.objects.get(code=from_account_code)
        to_account = Account.objects.get(code=to_account_code)
    except Account.DoesNotExist:
        return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        amount = Decimal(amount)
    except InvalidOperation:
        return Response({"error": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)

    if from_account.balance < amount:
        return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

    from_account.balance -= amount
    to_account.balance += amount
    from_account.save()
    to_account.save()
    return Response({
        "from_account": AccountSerializer(from_account).data,
        "to_account": AccountSerializer(to_account).data
    })