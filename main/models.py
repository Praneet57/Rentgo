from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    CATEGORY_CHOICES = [
        ('physical', 'Physical Asset'),
        ('digital', 'Digital Asset'),
    ]
    PHYSICAL_TYPES = [
        ('car', 'Car'),
        ('land', 'Land'),
    ]
    DIGITAL_TYPES = [
        ('ott', 'OTT Platform'),
        ('nft', 'NFT'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    asset_type = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    owner_name = models.CharField(max_length=100, default="Unknown")
    owner_contact = models.CharField(max_length=15)
    owner_wallet = models.CharField(max_length=100)
    image = models.ImageField(upload_to='assets/', null=True, blank=True)

    def __str__(self):
        return self.name


class Rental(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    customer_contact = models.CharField(max_length=15)
    customer_proof = models.FileField(upload_to='customer_proofs/')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Calculate total price based on rental days
        if self.start_date and self.end_date:
            days = (self.end_date - self.start_date).days + 1
            self.total_price = days * self.asset.price_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.username} renting {self.asset.name}"
