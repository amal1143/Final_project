# from django.urls import path
# from . import views

# urlpatterns = [

#     path('', views.homepage, name='homepage'),

#     # ========= AUTH =========
#     path('about/', views.about, name='about'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('register/', views.register, name='register'),

#     # Farmer
#     path('farmer/', views.farmer_home, name='farmer_home'),
#     path('add/', views.add, name='add'),
#     path('add-product/', views.addproduct, name='addproduct'),
#     path('products/', views.view_products, name='view_products'),
#     path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
#     path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
#     path('farmer/orders/', views.farmer_orders, name='farmer_orders'),

#     # Farmer dashboard extra pages
#     path("farmer/active-products/", views.farmer_active_products, name="farmer_active_products"),
#     path("farmer/pending-orders/", views.farmer_pending_orders, name="farmer_pending_orders"),
#     path("farmer/pickup-bookings/", views.farmer_pickup_bookings, name="farmer_pickup_bookings"),
#     path("farmer/confirm-pickup/<int:booking_id>/",views.confirm_pickup,name="confirm_pickup"),


#     # Admin
#     path('admin-home/', views.admin_home, name='admin_home'),
#     path('admin-products/', views.admin_products, name='admin_products'),
#     path('approve/<int:product_id>/', views.approve_product, name='approve_product'),
#     path('reject/<int:product_id>/', views.reject_product, name='reject_product'),
#     path('view-farmers/', views.view_farmers, name='view_farmers'),
#     path('manage-markets/', views.manage_markets, name='manage_markets'),
#     path('delete-market/<int:market_id>/', views.delete_market, name='delete_market'),
#     path('admin_customers/', views.view_customers, name='view_customers'),
#     path('admin-reports/', views.admin_reports, name='admin_reports'),


#     # Customer
#     path('customer/', views.customer_home, name='customer_home'),
#     path('customer/markets/', views.customer_markets, name='customer_markets'),
#     path('market/<int:market_id>/', views.market_products, name='market_products'),
#     path('place-order/<int:product_id>/', views.place_order, name='place_order'),
#     path('orders/', views.my_orders, name='my_orders'),
#     path('confirm-order/<int:order_id>/',views.confirm_order, name='confirm_order'),
#     path('razorpay/<int:order_id>/', views.razorpay_checkout, name='razorpay_checkout'),
#     path("razorpay-success/", views.razorpay_success, name="razorpay_success"),
#     path("cod/<int:order_id>/", views.cash_on_delivery, name="cash_on_delivery"),
#     path("order/delete/<int:order_id>/", views.delete_order, name="delete_order"),
#     path("pickup-bookings/", views.customer_pickup_bookings, name="customer_pickup_bookings"),
        
#     path('customer/browse-products/',views.browse_products,name='browse_products'),
#      path('order/details/<int:product_id>/', views.add_order_details, name='add_order_details'),
# path('confirm-orders/<int:order_id>/', views.confirm_orders, name='confirm_orders'),
# path('pay-now/<int:order_id>/', views.pay_now, name='pay_now'),
#     path('cod-confirm/<int:order_id>/', views.cod_confirm, name='cod_confirm'),


   
#     # Profile
#     path('profile/', views.profile, name='profile'),
# ]

# from django.urls import path
# from . import views

# urlpatterns = [

#     # Home
#     path('', views.homepage, name='homepage'),

#     # ========= AUTH =========
#     path('about/', views.about, name='about'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('register/', views.register, name='register'),

#     # ========= FARMER =========
#     path('farmer/', views.farmer_home, name='farmer_home'),
#     path('add/', views.add, name='add'),
#     path('add-product/', views.addproduct, name='addproduct'),
#     path('products/', views.view_products, name='view_products'),
#     path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
#     path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
#     path('farmer/orders/', views.farmer_orders, name='farmer_orders'),
#     path('farmer/market/', views.farmer_markets, name='farmer_markets'),


#     # Farmer extra pages
#     path('farmer/active-products/', views.farmer_active_products, name='farmer_active_products'),
#     path('farmer/pending-orders/', views.farmer_pending_orders, name='farmer_pending_orders'),
#     path('farmer/pickup-bookings/', views.farmer_pickup_bookings, name='farmer_pickup_bookings'),
#     path('farmer/confirm-pickup/<int:booking_id>/', views.confirm_pickup, name='confirm_pickup'),

#     # ========= ADMIN =========
#     path('admin-home/', views.admin_home, name='admin_home'),
#     path('admin-products/', views.admin_products, name='admin_products'),
#     path('approve/<int:product_id>/', views.approve_product, name='approve_product'),
#     path('reject/<int:product_id>/', views.reject_product, name='reject_product'),
#     path('dashboard/farmers/', views.view_farmers, name='view_farmers'),
#     path('manage-markets/', views.manage_markets, name='manage_markets'),
#     path('delete-market/<int:market_id>/', views.delete_market, name='delete_market'),
#     path('admin-customers/', views.view_customers, name='view_customers'),
#     path('admin-reports/', views.admin_reports, name='admin_reports'),
#      path('confirm-order/<int:order_id>/',views.confirm_order, name='confirm_order'),

#     # ========= CUSTOMER =========
#     path('customer/', views.customer_home, name='customer_home'),
#     path('customer/markets/', views.customer_markets, name='customer_markets'),
#     path('market/<int:market_id>/', views.market_products, name='market_products'),
#     path('place-order/<int:product_id>/', views.place_order, name='place_order'),
#     path('orders/', views.my_orders, name='my_orders'),
#         path('confirm-orders/<int:order_id>/', views.confirm_orders, name='confirm_orders'),

#     # Order flow
#     path('confirm-orders/<int:order_id>/', views.confirm_orders, name='confirm_orders'),
#     path('razorpay/<int:order_id>/', views.razorpay_checkout, name='razorpay_checkout'),
#     path('razorpay-success/', views.razorpay_success, name='razorpay_success'),
#     path('cod/<int:order_id>/', views.cash_on_delivery, name='cash_on_delivery'),
#     path('pay-now/<int:order_id>/', views.pay_now, name='pay_now'),
#     path('cod-confirm/<int:order_id>/', views.cod_confirm, name='cod_confirm'),
#     path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),

#     # Pickup
#     path('pickup-bookings/', views.customer_pickup_bookings, name='customer_pickup_bookings'),

#     # Browse
#     path('customer/browse-products/', views.browse_products, name='browse_products'),
#     path('order/details/<int:product_id>/', views.add_order_details, name='add_order_details'),

#     # Profile
#     path('profile/', views.profile, name='profile'),
# ]

from django.urls import path
from . import views

urlpatterns = [

    # ---------------- HOME ----------------
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),

    # ---------------- AUTH ----------------
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # ---------------- FARMER ----------------
    path('farmer/', views.farmer_home, name='farmer_home'),
    path('add-product/', views.addproduct, name='addproduct'),
    path('products/', views.view_products, name='view_products'),
    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
path('add/', views.add, name='add'),
    path('farmer/orders/', views.farmer_orders, name='farmer_orders'),
    path('farmer/market/', views.farmer_markets, name='farmer_markets'),

    # Farmer extra pages
    path('farmer/active-products/', views.farmer_active_products, name='farmer_active_products'),
    path('farmer/pending-orders/', views.farmer_pending_orders, name='farmer_pending_orders'),
    path('farmer/pickup-bookings/', views.farmer_pickup_bookings, name='farmer_pickup_bookings'),
    path('farmer/confirm-pickup/<int:booking_id>/', views.confirm_pickup, name='confirm_pickup'),
     path('confirm-order/<int:order_id>/',views.confirm_order, name='confirm_order'),

    # ---------------- ADMIN ----------------
    path('admin-home/', views.admin_home, name='admin_home'),
    path('admin-products/', views.admin_products, name='admin_products'),
    path('approve/<int:product_id>/', views.approve_product, name='approve_product'),
    path('reject/<int:product_id>/', views.reject_product, name='reject_product'),
    path('dashboard/farmers/', views.view_farmers, name='view_farmers'),
    path('manage-markets/', views.manage_markets, name='manage_markets'),
    path('delete-market/<int:market_id>/', views.delete_market, name='delete_market'),
    path('admin-customers/', views.view_customers, name='view_customers'),
    path('admin-reports/', views.admin_reports, name='admin_reports'),

    # ---------------- CUSTOMER ----------------
    path('customer/', views.customer_home, name='customer_home'),
    path('customer/markets/', views.customer_markets, name='customer_markets'),
    path('market/<int:market_id>/', views.market_products, name='market_products'),
    path('place-order/<int:product_id>/', views.place_order, name='place_order'),
    path('orders/', views.my_orders, name='my_orders'),
    path('confirm-orders/<int:order_id>/', views.confirm_orders, name='confirm_orders'),


    path('razorpay/<int:order_id>/', views.razorpay_checkout, name='razorpay_checkout'),
    path('razorpay-success/', views.razorpay_success, name='razorpay_success'),
    path('cod/<int:order_id>/', views.cash_on_delivery, name='cash_on_delivery'),
    path('pay-now/<int:order_id>/', views.pay_now, name='pay_now'),
    path('cod-confirm/<int:order_id>/', views.cod_confirm, name='cod_confirm'),
    path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),
path('farmer/pending-orders/', views.farmer_pending_orders, name='farmer_pending_orders'),
path('complete-order/<int:order_id>/', views.complete_order, name='complete_order'),

    # ---------------- PICKUP ----------------
    path('pickup-bookings/', views.customer_pickup_bookings, name='customer_pickup_bookings'),

    # ---------------- BROWSE ----------------
    path('customer/browse-products/', views.browse_products, name='browse_products'),
    path('order/details/<int:product_id>/', views.add_order_details, name='add_order_details'),

    # ---------------- PROFILE ----------------
    path('profile/', views.profile, name='profile'),
]
