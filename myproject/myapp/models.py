from django.db import models


class Product(models.Model):

    CATEGORY_CHOICES = [
        ('Paneer Specials', 'Paneer Specials'),
        ('Veg Biryani', 'Veg Biryani'),
        ('Veg Pizza', 'Veg Pizza'),
        ('Veg Burger', 'Veg Burger'),
        ('South Indian', 'South Indian'),
        ('Veg Thali', 'Veg Thali'),
        ('Veg Snacks', 'Veg Snacks'),
        ('Desserts', 'Desserts'),
        ('Non-Veg', 'Non-Veg'),
    ]

    name = models.CharField(max_length=100)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    image = models.URLField(max_length=500)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name