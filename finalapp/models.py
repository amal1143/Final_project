from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# ---------------- MARKET ----------------
class Market(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.name} - {self.location}"


# ---------------- FARMER ----------------
class FarmerModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username


# ---------------- CUSTOMER ----------------
class CustomerModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
# ---------------- PRODUCT ----------------
class Product(models.Model):
    farmer = models.ForeignKey(FarmerModel, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.product_name


# ---------------- ORDER ----------------
class Order(models.Model):

    # STATUS CONSTANTS
    STATUS_PENDING = "PENDING"
    STATUS_CONFIRMED = "CONFIRMED"
    STATUS_COMPLETED = "COMPLETED"

    # PAYMENT CONSTANTS
    PAYMENT_PENDING = "PENDING"
    PAYMENT_PAID = "PAID"

    customer = models.ForeignKey("CustomerModel", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    quantity = models.IntegerField()
    total_amount = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=[
            (STATUS_PENDING, "Pending"),
            (STATUS_CONFIRMED, "Confirmed"),
            (STATUS_COMPLETED, "Completed"),
        ],
        default=STATUS_PENDING
    )

    payment_status = models.CharField(
        max_length=20,
        choices=[
            (PAYMENT_PENDING, "Pending"),
            (PAYMENT_PAID, "Paid"),
        ],
        default=PAYMENT_PENDING
    )

    created_at = models.DateTimeField(default=now)

    # Razorpay
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.product} - {self.customer}"



# ---------------- PICKUP BOOKING ----------------
class PickupBooking(models.Model):
    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"

    farmer = models.ForeignKey(FarmerModel, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pickup_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[(STATUS_PENDING, "Pending"), (STATUS_COMPLETED, "Completed")],
        default=STATUS_PENDING
    )

    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Pickup #{self.id} - {self.order}"
