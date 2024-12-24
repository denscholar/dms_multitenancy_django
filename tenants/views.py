from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection


from accounts.models import CustomUser
from tenants.models import Client
from tenants.serializers import TenantSignupSerializer

class TenantSignupView(APIView):
    def post(self, request):
        serializer = TenantSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Tenant and superuser created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TenantUsersView(APIView):
    def get(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
            users = CustomUser.objects.filter(client=client)
            return Response({"users": users}, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

class CurrentTenantUsersView(APIView):
    def get(self, request):
        tenant_schema = connection.schema_name  # Current tenant schema
        users = CustomUser.objects.all()  # Scoped to the tenant by schema
        user_data = [{"email": user.email, "is_staff": user.is_staff} for user in users]
        return Response({"users": user_data}, status=status.HTTP_200_OK)