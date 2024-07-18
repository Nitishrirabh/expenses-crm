from django.db import models


class DomainDetails(models.Model):
    domain_name = models.CharField(max_length=255)
    expiry_date = models.DateField()
    ssl_expiry_date = models.DateField()
    server_name = models.CharField(max_length=255)
    server_hosted_on = models.CharField(max_length=255)
    server_expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'domain_details'