from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Profile
from .cart import Cart
from .models import Order, Product



def checkout(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('cart_detail') # Savat bo'sh bo'lsa qaytarib yuboramiz

    if request.method == 'POST':
        # Formadan ma'lumotlarni olish
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        total_price = request.POST.get('total_price')

        # Buyurtmani saqlash
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone=phone,
            address=address,
            total_price=total_price
        )

        # Savatchani tozalash
        request.session['cart'] = {}
        
        return render(request, 'order_success.html', {'order': order})

    return render(request, 'checkout.html', {'cart': cart})



def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        # Formadan ma'lumotlarni olish
        first_name = request.POST.get('first_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        if first_name and phone:
            # 1. Buyurtmani bazada yaratish
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                first_name=first_name,
                phone=phone,
                address=address,
                total_price=cart.get_total_price()
            )
            
            # 2. Savatni tozalash
            cart.clear()
            
            # 3. Muvaffaqiyat sahifasini ko'rsatish
            return render(request, 'checkout.html', {'success': True, 'order': order})
            
    return render(request, 'checkout.html', {'cart': cart})


def index(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product_detail.html', {'product': product})

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def checkout(request):
    return render(request, 'checkout.html')

@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile_edit.html', {'profile': profile})