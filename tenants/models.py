from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

class Client(TenantMixin):
    company_name = models.CharField(max_length=100)
    company_email = models.EmailField(unique=True)
    company_phone = models.CharField(max_length=15)
    created_on = models.DateTimeField(auto_now_add=True)

    # Specify schema name explicitly
    auto_create_schema = True
    auto_drop_schema = True

class Domain(DomainMixin):
    pass
