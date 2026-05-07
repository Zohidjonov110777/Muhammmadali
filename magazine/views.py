from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Order, Review, Category, Profile
from .cart import Cart

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    reviews = product.reviews.all().order_by('-created_at')
    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})

def index(request):
    # Bazadagi barcha mahsulotlar va kategoriyalarni olamiz
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Ularni context orqali html-ga uzatamiz
    return render(request, 'index.html', {
        'products': products,
        'categories': categories
    })

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get('action') 
    if action == 'decrease':
        cart.add(product=product, quantity=-1, override_quantity=False)
    else:
        cart.add(product=product, quantity=1, override_quantity=False)
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def checkout(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        total_price = cart.get_total_price()

        # Buyurtmani yaratish
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone=phone,
            address=address,
            total_price=total_price
        )

        cart.clear()  # Savatni tozalash

        # Paynet-ga yo'naltirish
        paynet_url = "https://www.paynet.uz/" 
        return redirect(paynet_url)

    # Mana shu qatorda xato bor edi (qavs yopilmagan edi)
    return render(request, 'checkout.html', {'cart': cart})

@login_required
def profile_detail(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile_detail.html', {'orders': orders, 'profile': profile})

@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.email = request.POST.get('email')
        profile.phone = request.POST.get('phone')
        request.user.save()
        profile.save()
        return redirect('profile_detail')
    return render(request, 'edit_profile.html', {'profile': profile})