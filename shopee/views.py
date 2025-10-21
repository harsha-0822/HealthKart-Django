from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Product, Cart, CartItem, Address, Category, Order, OrderItem
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required
def purchase(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)
    
    if not cart_items.exists():
        messages.error(request, 'No items in the cart to order.')
        return redirect('cart_view')
    
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    # Create the order
    order = Order.objects.create(user=user, total_amount=total_amount)
    order_items = []
    for item in cart_items:
        order_item = OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        order_item.total_price = item.product.price * item.quantity
        order_item.save()
        order_items.append(order_item)
    
    # Clear the cart
    cart_items.delete()

    # Send confirmation email
    subject = 'Order Confirmation'
    message = f'Thank you for your purchase!\n\nYour order total is: {total_amount} Rs.\n\n'
    message += 'Your order details:\n'
    for item in order_items:
        message += f'{item.product.name} (Quantity: {item.quantity}) - {item.total_price} Rs\n'
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # Sender's email
            [user.email],  # Recipient's email
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email: {e}")

    # Render the confirmation page
    context = {
        'user': user,
        'order': order,
        'order_items': order_items,
        'total_amount': total_amount,
        
    }
    return render(request, 'shopee/purchase_complete.html', context)



def index(request):
    return render(request, 'shopee/index.html')

def product_list(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category', None)
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '')

    products = Product.objects.all()

    if selected_category:
        products = products.filter(category_id=selected_category)

    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    return render(request, 'shopee/product_list.html', {'products': products, 'categories': categories})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shopee/product_detail.html', {'product': product})

@login_required
def cart_view(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    cart_items = []
    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        # Retrieve product images for cart items
        for item in cart_items:
            item.product.image_url = item.product.image.url
    if not cart_items:
        messages.info(request, 'No items in your cart.')
    
    # Dynamic payment methods
    payment_methods = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
        ('upi', 'UPI'),
        ('cod', 'Cash on Delivery'),
    ]
    
    return render(request, 'shopee/cart.html', {
        'cart_items': cart_items,
        'payment_methods': payment_methods
    })

@login_required
def user_detail(request):
    user = request.user
    address = Address.objects.filter(user=user).first()
    return render(request, 'shopee/user_detail.html', {'user': user, 'address': address})

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, 'Product added to cart successfully.')
    return redirect('product_list')

@login_required
def update_cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = int(request.POST.get('quantity', 0))
        cart_item = CartItem.objects.get(id=cart_item_id)
        if quantity == 0:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully.')
    return redirect('cart_view')

def login_register(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('product_list')
                else:
                    messages.error(request, 'Invalid username or password.')
        elif 'register' in request.POST:
            registration_form = UserCreationForm(request.POST)
            if registration_form.is_valid():
                registration_form.save()
                # Auto-login after register or redirect to a login page
                return redirect('login_user')  # Adjust the redirect as necessary
    else:
        login_form = AuthenticationForm()
        registration_form = UserCreationForm()

    return render(request, 'shopee/login_register.html', {'login_form': login_form, 'registration_form': registration_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')  # Redirect to a desired page
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'shopee/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect('login_user')  # Redirect to the login page
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
    return render(request, 'shopee/register.html', {'form': form})

@login_required
def update_user_info(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        address, created = Address.objects.get_or_create(user=user)
        address.street_address = request.POST.get('street_address', '').strip()
        address.city = request.POST.get('city', '').strip()
        address.state = request.POST.get('state', '').strip()
        address.country = request.POST.get('country', '').strip()
        address.zip_code = request.POST.get('zip_code', '').strip()

        if not address.street_address or not address.city or not address.state or not address.country or not address.zip_code:
            messages.error(request, 'All address fields must be filled out.')
            return redirect('user_detail')
        
        address.save()
        messages.success(request, 'User information updated successfully.')
        return redirect('user_detail')

    return render(request, 'shopee/update_user_info.html')

@login_required
def add_address(request):
    user = request.user
    if request.method == 'POST':
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')

        # Check if user already has an address
        address, created = Address.objects.get_or_create(user=user)
        address.street_address = street_address
        address.city = city
        address.state = state
        address.country = country
        address.zip_code = zip_code
        address.save()
        
        messages.success(request, 'Address updated successfully.')
        return redirect('user_detail')
    
    return render(request, 'shopee/add_address.html')

def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Account deleted successfully.')
        return redirect('index')
    
    return render(request, 'shopee/delete_account.html')