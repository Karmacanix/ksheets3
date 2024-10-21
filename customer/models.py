from django.db import models

# Create your models here.
class Customer(models.Model):
    # Basic customer information
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Address fields (may need to be split into components)
    street_address = models.CharField(max_length=255)
    suburb = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    region = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default="New Zealand")

    # Optional additional fields for business customers
    business_name = models.CharField(max_length=255, blank=True, null=True)
    gst_number = models.CharField(max_length=20, blank=True, null=True)

    # Timestamps for record tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name