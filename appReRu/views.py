from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import json
import datetime
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            return redirect("login_user")
    return render(request, "files/register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful! 🎉  😁")
            return redirect("shop")
        else:

            messages.error(request, "Invalid Credentials  😞 ")
    return render(request, "files/login.html")


def logout_user(request):
    logout(request)
    return redirect("shop")


@login_required
def Account_User(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]
    # Retrieve the user's complete orders
    user_orders = Order.objects.filter(
        customer=request.user, complete=True, status="unfulfilled"
    ).order_by("-date_ordered")

    # Create an empty dictionary to store order items for each order
    orders_with_items = {}

    # Fetch order items for each complete order
    for order in user_orders:
        order_items = OrderItem.objects.filter(order=order)
        orders_with_items[order] = order_items

    completed_fulfilled_orders = Order.objects.filter(
        customer=customer, complete=True, status="fulfilled"
    )

    fulfilled_orders_with_items = {}
    for completed_fulfilled_order in completed_fulfilled_orders:
        order_items = OrderItem.objects.filter(order=completed_fulfilled_order)
        fulfilled_orders_with_items[completed_fulfilled_order] = order_items

    # Check for success message
    if messages.get_messages(request):
        success_message = "Refund request submitted successfully."
    else:
        success_message = None

    # footer
    social = OurSocials.objects.filter().first()
    privacy = PrivacyPolicy.objects.filter().first()
    term = TermsAndConditions.objects.filter().first()
    return_policy = ReturnPolicy.objects.filter().first()
    help = FaqsHelp.objects.filter().first()
    contact = Contact.objects.filter().first()
    new_messages_count = UserInbox.objects.filter(user=request.user).count()

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "orders_with_items": orders_with_items,
        "social": social,
        "privacy": privacy,
        "term": term,
        "return_policy": return_policy,
        "help": help,
        "contact": contact,
        "completed_fulfilled_orders": completed_fulfilled_orders,
        "fulfilled_orders_with_items": fulfilled_orders_with_items,
        "new_messages_count": new_messages_count,
        "success_message": success_message,
    }

    return render(request, "files/account_user.html", context)


@login_required
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    # footer

    ad = (
        Advertisement.objects.first()
    )  # Change this according to your Advertisement model
    social = OurSocials.objects.filter().first()
    privacy = PrivacyPolicy.objects.filter().first()
    term = TermsAndConditions.objects.filter().first()
    return_policy = ReturnPolicy.objects.filter().first()
    help = FaqsHelp.objects.filter().first()
    contact = Contact.objects.filter().first()

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "social": social,
        "privacy": privacy,
        "term": term,
        "return_policy": return_policy,
        "help": help,
        "contact": contact,
        "ad": ad,
    }
    return render(request, "files/cart.html", context)


@login_required
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    # footer
    social = OurSocials.objects.filter().first()
    privacy = PrivacyPolicy.objects.filter().first()
    term = TermsAndConditions.objects.filter().first()
    return_policy = ReturnPolicy.objects.filter().first()
    help = FaqsHelp.objects.filter().first()
    contact = Contact.objects.filter().first()

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "social": social,
        "privacy": privacy,
        "term": term,
        "return_policy": return_policy,
        "help": help,
        "contact": contact,
    }
    return render(request, "files/chackout.html", context)


@login_required
def contact(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    if request.method == "POST":
        # If the request method is POST, it means the form has been submitted
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        # Create a new Review object with the submitted data
        contact = ContactUs.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
        )
    # footer
    social = OurSocials.objects.filter().first()
    privacy = PrivacyPolicy.objects.filter().first()
    term = TermsAndConditions.objects.filter().first()
    return_policy = ReturnPolicy.objects.filter().first()
    help = FaqsHelp.objects.filter().first()
    contact = Contact.objects.filter().first()

    context = {
        "social": social,
        "privacy": privacy,
        "term": term,
        "return_policy": return_policy,
        "help": help,
        "contact": contact,
        "items": items,
        "order": order,
        "cartItems": cartItems,
    }

    return render(request, "files/contact.html", context)


@login_required
def shop_detail(request, pk):
    if request.method == "POST":
        # If the request method is POST, it means the form has been submitted
        name = request.POST.get("name")
        email = request.POST.get("email")
        review_text = request.POST.get("review")

        # Assuming 'pk' is the primary key of the product being reviewed
        product = get_object_or_404(Product, pk=pk)

        # Create a new Review object with the submitted data
        review = Review.objects.create(
            product=product, name=name, email=email, review=review_text
        )

        # Redirect to the same product detail page after submitting the review
        return redirect("shop_detail", pk=pk)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    # Retrieve the product with the given primary key or return a 404 error if not found
    product = get_object_or_404(Product, pk=pk)
    # Retrieve all reviews related to the product
    reviews = Review.objects.filter(product=product)

    # Retrieve featured products from the same category (if any)
    featured_products = (
        Product.objects.filter(categories=product.categories)
        .exclude(pk=pk)
        .order_by("-created")[:6]
    )

    # Retrieve all ads related to the product
    ad = (
        Advertisement.objects.first()
    )  # Change this according to your Advertisement model

    # Footer content

    ad1 = Advertisement1.objects.first()
    social = OurSocials.objects.first()
    privacy = PrivacyPolicy.objects.first()
    term = TermsAndConditions.objects.first()
    return_policy = ReturnPolicy.objects.first()
    help = FaqsHelp.objects.first()
    contact = Contact.objects.first()

    context = {
        "product": product,
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "reviews": reviews,
        "featured_products": featured_products,
        "ad": ad,
        "social": social,
        "privacy": privacy,
        "term": term,
        "return_policy": return_policy,
        "help": help,
        "contact": contact,
        "ad1": ad1,
    }
    return render(request, "files/shop-detail.html", context)


def shop(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    # footer
    social = OurSocials.objects.filter().first()
    privacy = PrivacyPolicy.objects.filter().first()
    term = TermsAndConditions.objects.filter().first()
    return_policy = ReturnPolicy.objects.filter().first()
    help = FaqsHelp.objects.filter().first()
    contact = Contact.objects.filter().first()

    # Retrieve all products
    all_products = Product.objects.all().order_by("-created")
    categories = Category.objects.all()

    # Pagination
    paginator = Paginator(all_products, 6)  # Show 6 products per page
    page_number = request.GET.get("page")

    # Ensure page number is valid
    try:
        page_number = int(page_number)
    except (TypeError, ValueError):
        page_number = 1

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        products = paginator.page(paginator.num_pages)

    # Calculate page range
    current_page = products.number
    start_page = max(current_page - 2, 1)
    end_page = min(current_page + 2, paginator.num_pages)
    page_range = range(start_page, end_page + 1)

    context = {
        "products": products,
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "page_range": page_range,
        "current_page": current_page,
        "social": social,
        "privacy": privacy,
        "term": term,
        "return_policy": return_policy,
        "help": help,
        "contact": contact,
        "categories": categories,
    }
    return render(request, "files/shop.html", context)


@login_required
def search_view(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    query = request.GET.get("query")
    if query is None:
        return redirect("shop")
    else:
        results = Product.objects.filter(
            Q(name__icontains=query)
            | Q(price__icontains=query)
            | Q(categories__name__icontains=query)
        )

    # footer
    social = OurSocials.objects.filter().first()
    privacy = PrivacyPolicy.objects.filter().first()
    term = TermsAndConditions.objects.filter().first()
    return_policy = ReturnPolicy.objects.filter().first()
    help = FaqsHelp.objects.filter().first()
    contact = Contact.objects.filter().first()

    return render(
        request,
        "files/search_results.html",
        {
            "results": results,
            "items": items,
            "order": order,
            "cartItems": cartItems,
            "social": social,
            "privacy": privacy,
            "term": term,
            "return_policy": return_policy,
            "help": help,
            "contact": contact,
        },
    )


def error(request):
    return render(request, "files/404.html")


@login_required
def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    print("Action:", action)
    print("Product:", productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    # Call the update_product_availability function to update the product availability status
    update_product_availability(product)

    return JsonResponse("Item was added", safe=False)


def update_product_availability(product):
    print("Updating product availability for:", product.name)  # Debug statement

    # Fetch all active orders
    active_orders = Order.objects.all()

    # Sum up the quantity of the product in all active orders
    total_ordered_quantity = OrderItem.objects.filter(
        order__in=active_orders, product=product
    ).aggregate(total_quantity=Sum("quantity"))["total_quantity"]

    if total_ordered_quantity is None:
        total_ordered_quantity = 0

    # Calculate the remaining quantity in stock
    remaining_quantity = product.quantity - total_ordered_quantity

    # Update product availability status
    if remaining_quantity <= 0:
        product.availability_status = "sold_out"
    else:
        product.availability_status = "available"

    # Save the updated product
    product.save()


@login_required
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        return JsonResponse("User not authenticated", safe=False)

    total = float(data["shipping"]["total"])
    payment_method = data["shipping"].get("payment_method", "Pay Now")

    # Handle payment verification based on payment method
    if payment_method == "Pay Now":
        if total == order.get_cart_total:
            order.complete = True
    elif payment_method == "Pay on Delivery":
        order.complete = True

    # Append payment method to transaction_id
    order.transaction_id = f"{transaction_id} ({payment_method})"

    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            mobile=data["shipping"]["mobile"],
            firstname=data["shipping"]["firstname"],
            lastname=data["shipping"]["lastname"],
            email=data["shipping"]["email"],
            order_notes=data["shipping"]["order_notes"],
        )

    return JsonResponse("Order processed successfully", safe=False)


@login_required
def User_Profile(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    # Retrieve the user's profile information
    user_profile = request.user

    # Footer content
    social = OurSocials.objects.filter().first()
    privacy = PrivacyPolicy.objects.filter().first()
    term = TermsAndConditions.objects.filter().first()
    return_policy = ReturnPolicy.objects.filter().first()
    help = FaqsHelp.objects.filter().first()
    contact = Contact.objects.filter().first()

    context = {
        "user_profile": user_profile,
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "social": social,
        "privacy": privacy,
        "term": term,
        "return_policy": return_policy,
        "help": help,
        "contact": contact,
    }

    return render(request, "files/user_profile.html", context)


def refund_request(request, pk):
    if request.method == "POST":
        # Get data from the request
        user = request.user
        fulfilled_order_id = pk  # Use the ID passed in the URL
        reason = request.POST.get("reason")

        # Retrieve the FulfilledOrder instance using fulfilled_order_id
        fulfilled_order = get_object_or_404(
            FulfilledOrder, transaction_id=fulfilled_order_id
        )

        # Check if the order was fulfilled within the last 3 days
        three_days_ago = timezone.now() - timezone.timedelta(days=3)
        if fulfilled_order.date_ordered <= three_days_ago:
            # Check if there is already a refund request related to this fulfilled order
            existing_refund_request = RefundRequest.objects.filter(
                fulfilled_order=fulfilled_order
            ).exists()
            if not existing_refund_request:
                # Create a RefundRequest object and save it to the database
                RefundRequest.objects.create(
                    user=user, fulfilled_order=fulfilled_order, reason=reason
                )

                # Add a success message
                messages.success(
                    request,
                    "Refund request submitted successfully. Check your email for regular updates on your request. It will take not more than 3 business days to fulfill your request. Thank you for being a loyal customer",
                )

                # Redirect to 'acc' page
                return redirect("acc")
            else:
                # Add a warning message if there is already a refund request
                messages.warning(
                    request,
                    "A refund request for this order already exists. Check your email please!!",
                )
        else:
            # Add a warning message if the order is not within the last 3 days
            messages.warning(
                request,
                "Refund requests can only be submitted for orders placed within the last 3 days.",
            )

    return render(request, "files/refund_request_form.html")


@login_required
def inbox(request):
    # Mark all unread messages as read when the user visits the inbox
    UserInbox.objects.filter(user=request.user, read=False).update(read=True)

    # Retrieve inbox messages
    user_inbox = UserInbox.objects.filter(user=request.user).order_by("-sent_at")

    return render(request, "files/inbox.html", {"user_inbox": user_inbox})
