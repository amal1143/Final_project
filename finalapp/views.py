from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from datetime import date
from django.contrib.admin.views.decorators import staff_member_required
import razorpay
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import now

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

from .models import FarmerModel,CustomerModel,Product,Order,PickupBooking,Market



# ---------------- AUTH ----------------
def register(request):
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_home')
            elif FarmerModel.objects.filter(user=user).exists():
                return redirect('farmer_home')
            else:
                return redirect('customer_home')
        messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name
        )

        if role == "farmer":
            FarmerModel.objects.create(user=user)
        else:
            CustomerModel.objects.create(user=user)

        return redirect('login')

    return render(request, 'register.html')


# ---------------- ADMIN ----------------
@staff_member_required
def admin_home(request):
    pending_count = Product.objects.filter(is_approved=False).count()
    return render(request, 'admin_home.html', {'pending_count': pending_count})


@staff_member_required
def admin_products(request):
    products = Product.objects.filter(is_approved=False)
    return render(request, 'admin_products.html', {'products': products})


@staff_member_required
def approve_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_approved = True
    product.save()
    return redirect('admin_products')


@staff_member_required
def reject_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin_products')

# ---------------- FARMER ----------------
@login_required
def farmer_home(request):
    farmer = get_object_or_404(FarmerModel, user=request.user)
    today = timezone.now().date()

    today_sales = Order.objects.filter(
        product__farmer=farmer,
        status="CONFIRMED",
        created_at__date=today
    ).aggregate(total=Sum("total_amount"))["total"] or 0

    context = {
        "farmer": farmer,
        "active_products": Product.objects.filter(farmer=farmer, is_approved=True).count(),
        "pending_orders": Order.objects.filter(product__farmer=farmer, status="CONFIRMED").count(),
        "pickup_bookings": PickupBooking.objects.filter(farmer=farmer, status="pending").count(),
        "today_sales": today_sales,
    }
    return render(request, "farmer_home.html", context)


@login_required
def add(request):
    return render(request, 'add_product.html')


@login_required
def addproduct(request):
    farmer = get_object_or_404(FarmerModel, user=request.user)

    if not farmer.market:
        messages.error(request, "Market not assigned. Contact admin.")
        return redirect('farmer_home')

    if request.method == "POST":
        Product.objects.create(
            farmer=farmer,
            product_name=request.POST.get('product_name'),
            category=request.POST.get('category'),
            price=int(request.POST.get('price')),
            quantity=int(request.POST.get('quantity')),
            description=request.POST.get('description'),
            image=request.FILES.get('image'),
            is_approved=False
        )
        messages.success(request, "Product added successfully")
        return redirect('view_products')

    return render(request, 'add_product.html')


@login_required
def view_products(request):
    farmer = get_object_or_404(FarmerModel, user=request.user)
    products = Product.objects.filter(farmer=farmer)
    return render(request, 'view_products.html', {'products': products})



@login_required
def edit_product(request, id):
    farmer = get_object_or_404(FarmerModel, user=request.user)
    product = get_object_or_404(Product, id=id, farmer=farmer)

    if request.method == "POST":
        product.product_name = request.POST.get('product_name')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.description = request.POST.get('description')
        product.is_approved = False  
        product.save()
        return redirect('view_products')

    return render(request, 'edit_product.html', {'product': product})


@login_required
def delete_product(request, id):
    farmer = get_object_or_404(FarmerModel, user=request.user)
    product = get_object_or_404(Product, id=id, farmer=farmer)
    product.delete()
    return redirect('view_products')


# ---------------- CUSTOMER ----------------
@login_required
def customer_home(request):
    return render(request, 'customer_home.html')


@login_required
def profile(request):
    if request.method == "POST":
        request.user.first_name = request.POST.get('full_name')
        request.user.email = request.POST.get('email')
        request.user.save()

    return render(request, 'profile.html')


# ---------------- MARKET MANAGEMENT ----------------
@staff_member_required
def view_farmers(request):
    farmers = FarmerModel.objects.select_related('market', 'user')
    markets = Market.objects.all()

    if request.method == "POST":
        farmer_id = request.POST.get("farmer_id")
        market_id = request.POST.get("market_id")

        farmer = get_object_or_404(FarmerModel, id=farmer_id)
        market = get_object_or_404(Market, id=market_id)

        farmer.market = market
        farmer.save()

        messages.success(request, "Market assigned successfully")

        return redirect('view_farmers')

    return render(request, 'view_farmers.html', {
        "farmers": farmers,
        "markets": markets
    })



@staff_member_required
def manage_markets(request):
    markets = Market.objects.all()

    if request.method == "POST":
        Market.objects.create(
            name=request.POST.get('name'),
            location=request.POST.get('location')
        )
        return redirect('manage_markets')

    return render(request, 'manage_markets.html', {
        'markets': markets
    })


@staff_member_required
def delete_market(request, market_id):
    if request.method == "POST":
        market = get_object_or_404(Market, id=market_id)
        market.delete()
        return redirect('manage_markets')

    return redirect('manage_markets')


@login_required
def farmer_markets(request):
    farmer = FarmerModel.objects.select_related('market').filter(
        user=request.user
    ).first()

    return render(request, 'farmer_markets.html', {
        'market': farmer.market if farmer else None
    })




@staff_member_required
def view_customers(request):
    customers = CustomerModel.objects.select_related('user')
    return render(request, 'view_customers.html', {
        'customers': customers
    })


@login_required
def customer_markets(request):
    markets = Market.objects.all()
    return render(request, 'customer_markets.html', {
        'markets': markets
    })

@login_required
def market_products(request, market_id):
    market = get_object_or_404(Market, id=market_id)

    products = Product.objects.filter(
        farmer__market=market,
        is_approved=True
    )

    return render(request, 'market_products.html', {
        'market': market,
        'products': products
    })

@login_required
def place_order(request, product_id):
    customer = CustomerModel.objects.get(user=request.user)
    product = Product.objects.get(id=product_id)

    quantity = int(request.POST.get("quantity"))
    total = quantity * product.price

    order = Order.objects.create(
        customer=customer,
        product=product,
        quantity=quantity,
        total_amount=total,
        status="PENDING",
        payment_status="PENDING"
    )

         
    return redirect("confirm_order", order_id=order.id)

    

@login_required
def razorpay_checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)

    if not order.total_amount or order.total_amount < 1:
        messages.error(request, "Invalid payment amount")
        return redirect("my_orders")

    if order.razorpay_order_id:
        return render(request, "razorpay_checkout.html", {
            "order": order,
            "razorpay_key": settings.RAZORPAY_KEY_ID
        })

    try:
        razorpay_order = razorpay_client.order.create({
            "amount": int(order.total_amount) * 100,
            "currency": "INR",
            "payment_capture": 1
        })
    except razorpay.errors.BadRequestError as e:
        print("RAZORPAY ERROR:", e)
        messages.error(request, "Razorpay error. Check amount & keys.")
        return redirect("my_orders")

    order.razorpay_order_id = razorpay_order["id"]
    order.save()

    return render(request, "razorpay_checkout.html", {
        "order": order,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })

@login_required
def razorpay_success(request):
    if request.method == "POST":

        razorpay_order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("razorpay_payment_id")

        order = Order.objects.filter(
            razorpay_order_id=razorpay_order_id
        ).first()

        if not order:
            messages.error(request, "Order not found")
            return redirect("my_orders")

        # Stop duplicate payment
        if order.payment_status == Order.PAYMENT_PAID:
            return redirect("my_orders")

        order.payment_method = "ONLINE"
        order.payment_status = Order.PAYMENT_PAID
        order.status = Order.STATUS_CONFIRMED
        order.razorpay_payment_id = payment_id
        order.save()

        # Reduce stock safely
        product = order.product
        if product.quantity >= order.quantity:
            product.quantity -= order.quantity
            product.save()

        # Create pickup only once
        PickupBooking.objects.get_or_create(
            order=order,
            defaults={
                "farmer": product.farmer,
                "customer": order.customer,
                "pickup_date": now().date()
            }
        )

        messages.success(request, "Payment successful 🎉")
        return redirect("my_orders")


@login_required
def cash_on_delivery(request, order_id):
    customer = CustomerModel.objects.filter(user=request.user).first()
    order = get_object_or_404(Order, id=order_id, customer=customer)

    if order.status == Order.STATUS_CONFIRMED:
        return redirect("my_orders")

    order.payment_method = "COD"
    order.payment_status = Order.PAYMENT_PENDING
    order.status = Order.STATUS_CONFIRMED
    order.save()

    
    product = order.product
    if product.quantity >= order.quantity:
        product.quantity -= order.quantity
        product.save()

    PickupBooking.objects.get_or_create(
        order=order,
        defaults={
            "farmer": product.farmer,
            "customer": customer,
            "pickup_date": now().date()
        }
    )

    return redirect("my_orders")

@login_required
def my_orders(request):
    try:
        customer = CustomerModel.objects.get(user=request.user)
    except CustomerModel.DoesNotExist:
        return redirect("customer_home")

    orders = Order.objects.filter(
        customer=customer
    ).select_related("product").order_by("-created_at")

    return render(request, "my_orders.html", {
        "orders": orders
    })



@login_required
def confirm_order(request, order_id):
    customer = get_object_or_404(CustomerModel, user=request.user)
    order = get_object_or_404(Order, id=order_id, customer=customer)

    if request.method == "POST":
        # Save to CUSTOMER (not Order)
        customer.user.first_name = request.POST.get("name")
        customer.phone = request.POST.get("phone")
        customer.address = request.POST.get("address")

        customer.user.save()
        customer.save()

        order.status = Order.STATUS_CONFIRMED
        order.save()

        return redirect("razorpay_checkout", order_id=order.id)

    return render(request, "confirm_order.html", {
        "order": order,
        "customer": customer
    })

@login_required
def farmer_orders(request):
    farmer = get_object_or_404(FarmerModel, user=request.user)

    orders = Order.objects.filter(
        product__farmer=farmer,
        status="CONFIRMED"
    ).order_by('-id')

    return render(request, "farmer_orders.html", {
        "orders": orders
    })
# ================= FARMER EXTRA PAGES =================

@login_required
def farmer_active_products(request):
    farmer = get_object_or_404(FarmerModel, user=request.user)

    products = Product.objects.filter(
        farmer=farmer,
        is_approved=True
    )

    return render(request, "active_products.html", {
        "products": products
    })

@login_required
def farmer_pending_orders(request):
    farmer = get_object_or_404(FarmerModel, user=request.user)

    orders = Order.objects.filter(
        product__farmer=farmer,
        status=Order.STATUS_CONFIRMED
    ).select_related("customer", "product")

    return render(request, "pending_orders.html", {
        "orders": orders
    })
    
@login_required
def farmer_pickup_bookings(request):
    farmer = get_object_or_404(FarmerModel, user=request.user)

    bookings = PickupBooking.objects.filter(
        farmer=farmer
    ).select_related("customer", "order")

    return render(request, "pickup_bookings.html", {
        "bookings": bookings
    })

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer__user=request.user
    )

    order.delete()
    return redirect("my_orders")

@login_required
def customer_pickup_bookings(request):
    customer = CustomerModel.objects.get(user=request.user)

    bookings = PickupBooking.objects.filter(
        order__customer=customer
    ).order_by('-pickup_date')

    return render(request, "customer_pickup_bookings.html", {
        "bookings": bookings
    })


@login_required
def confirm_pickup(request, booking_id):
    farmer = get_object_or_404(FarmerModel, user=request.user)

    booking = get_object_or_404(
        PickupBooking,
        id=booking_id,
        farmer=farmer
    )

    booking.status = "completed"
    booking.save()

    return redirect("farmer_pickup_bookings")

@login_required
def browse_products(request):
    products = Product.objects.all()   # FIXED
    return render(request, 'browse_products.html', {
        'products': products
    })


@login_required
def add_order_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = CustomerModel.objects.filter(user=request.user).first()

    if not customer:
        messages.error(request, "Customer profile missing")
        return redirect("login")

    if request.method == "POST":
        quantity = int(request.POST.get("quantity"))
        pickup_date = request.POST.get("pickup_date")

        if quantity <= 0 or quantity > product.quantity:
            messages.error(request, "Invalid quantity")
            return redirect("browse_products")

        total = quantity * product.price

        order = Order.objects.create(
            product=product,
            customer=customer,
            quantity=quantity,
            total_amount=total,
            status="PENDING"
        )

        PickupBooking.objects.create(
            farmer=product.farmer,
            customer=customer,
            order=order,
            pickup_date=pickup_date
        )

        return redirect("confirm_orders", order.id)

    return render(request, "add_order_details.html", {"product": product})

@login_required
def confirm_orders(request, order_id):
    
    customer = get_object_or_404(CustomerModel, user=request.user)
    
    order = get_object_or_404(Order, id=order_id, customer=customer)
    
    pickupbooking = PickupBooking.objects.filter(order=order).first()

    return render(request, "confirm_orders.html", {
        "order": order,
        "pickupbooking": pickupbooking
    })




@login_required
def pay_now(request, order_id):
    customer = CustomerModel.objects.filter(user=request.user).first()
    order = get_object_or_404(Order, id=order_id, customer=customer)

    order.payment_method = "ONLINE"
    order.payment_status = "PAID"
    order.status = "CONFIRMED"
    order.save()

    PickupBooking.objects.get_or_create(
        order=order,
        defaults={
            "farmer": order.product.farmer,
            "customer": customer,
            "pickup_date": now().date()
        }
    )

    return redirect("customer_pickup_bookings")



@login_required
def cod_confirm(request, order_id):
    customer = CustomerModel.objects.filter(user=request.user).first()
    order = get_object_or_404(Order, id=order_id, customer=customer)

    if order.status == Order.STATUS_CONFIRMED:
        return redirect("customer_pickup_bookings")

    order.payment_method = "COD"
    order.payment_status = Order.PAYMENT_PENDING
    order.status = Order.STATUS_CONFIRMED
    order.save()

    
    product = order.product
    if product.quantity >= order.quantity:
        product.quantity -= order.quantity
        product.save()

    PickupBooking.objects.get_or_create(
        order=order,
        defaults={
            "farmer": product.farmer,
            "customer": customer,
            "pickup_date": now().date()
        }
    )

    return redirect("customer_pickup_bookings")


@staff_member_required
def admin_reports(request):
    selected_date = request.GET.get("date")

    if selected_date:
        # filter by selected date
        total_sales = Order.objects.filter(
            created_at__date=selected_date,
            status="CONFIRMED"
        ).aggregate(total=Sum("total_amount"))["total"] or 0

        total_orders = Order.objects.filter(
            created_at__date=selected_date
        ).count()

        today_sales = total_sales
    else:
        today = timezone.now().date()

        total_orders = Order.objects.count()

        total_sales = Order.objects.filter(
            status="CONFIRMED"
        ).aggregate(total=Sum("total_amount"))["total"] or 0

        today_sales = Order.objects.filter(
            created_at__date=today,
            status="CONFIRMED"
        ).aggregate(total=Sum("total_amount"))["total"] or 0

    total_farmers = FarmerModel.objects.count()
    total_customers = CustomerModel.objects.count()

    return render(request, "admin_reports.html", {
        "total_orders": total_orders,
        "total_sales": total_sales,
        "today_sales": today_sales,
        "total_farmers": total_farmers,
        "total_customers": total_customers,
        "selected_date": selected_date,
    })

def homepage(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_home')
        elif FarmerModel.objects.filter(user=request.user).exists():
            return redirect('farmer_home')
        else:
            return redirect('customer_home')
    return render(request, 'homepage.html')


def about(request):
    return render(request, 'about.html')

@login_required
def complete_order(request, order_id):
    farmer = get_object_or_404(FarmerModel, user=request.user)

    order = get_object_or_404(
        Order,
        id=order_id,
        product__farmer=farmer
    )

    order.status = Order.STATUS_COMPLETED
    order.save()

    return redirect("farmer_pending_orders")