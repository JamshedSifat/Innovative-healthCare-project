from django.db import models
from django.contrib.auth.models import User

# Model for storing product/accessory information
class Accessory(models.Model):
    p_name = models.CharField(max_length=100, help_text="Product name")
    p_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in Taka")
    p_count = models.IntegerField(help_text="Stock quantity")
    p_description = models.TextField(help_text="Product description")
    p_image = models.ImageField(upload_to='products/', help_text="Product image")
    v_name = models.CharField(max_length=100, help_text="Vendor/Brand name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.p_name

    class Meta:
        ordering = ['-created_at']  # Show newest products first

# Model for storing items in user's shopping cart
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    # Calculate total cost for this cart item
    @property
    def total_cost(self):
        return self.accessory.p_cost * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.accessory.p_name} x {self.quantity}"

    class Meta:
        # Ensure one user can't have duplicate items in cart
        unique_together = ('user', 'accessory')

# Model for storing completed orders/bills
class Bill(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Calculate total bill amount
    @property
    def total_cost(self):
        total = 0
        for item in self.billitem_set.all():
            total += item.total_cost
        return total

    def __str__(self):
        return f"Bill #{self.id} - {self.customer.username}"

# Model for storing individual items in a bill
class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    # Automatically calculate total cost when saving
    def save(self, *args, **kwargs):
        self.total_cost = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.accessory.p_name} x {self.quantity}"

