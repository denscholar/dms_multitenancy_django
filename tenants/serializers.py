from rest_framework import serializers
from tenants.models import Client
from accounts.models import CustomUser

class TenantSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Client
        fields = ['company_name', 'company_email', 'company_phone', 'password', 'confirm_password']

    def validate(self, data):
        # Validate passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Extract password
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')

        # Create the tenant (Client)
        client = Client.objects.create(**validated_data)
        client.create_schema()  # Automatically create the schema for the tenant

        # Create the tenant's superuser
        CustomUser.objects.create_superuser(
            email=validated_data['company_email'],
            password=password,
            client=client  # Link the superuser to the created tenant
        )
        return client