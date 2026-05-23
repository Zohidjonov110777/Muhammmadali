from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Product, Order, Category, Profile
from .cart import Cart
from .utils import send_order_notification, send_message
from .models import Product
import difflib


# ======================
# HOME PAGE
# ======================
def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    return render(request, 'index.html', {
        'products': products,
        'categories': categories
    })


# ======================
# PRODUCT DETAIL
# ======================
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    reviews = product.reviews.all().order_by('-created_at')

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews
    })


# ======================
# CART DETAIL
# ======================
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})


# ======================
# ADD TO CART
# ======================
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    action = request.POST.get('action')

    if action == 'decrease':
        cart.add(product=product, quantity=-1, override_quantity=False)
    else:
        cart.add(product=product, quantity=1, override_quantity=False)

    return redirect('cart_detail')


# ======================
# REMOVE FROM CART
# ======================
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)
    return redirect('cart_detail')


# ======================
# CHECKOUT + TELEGRAM
# ======================
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        total_price = cart.get_total_price()

        # BUYURTMA YARATISH
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone=phone,
            address=address,
            total_price=total_price
        )

        print("===================================")
        print("✅ Buyurtma yaratildi:", order.id)
        print("===================================")

        # Mahsulotlar ro'yxatini matn ko'rinishiga keltiramiz
        products_text = ""
        for item in cart:
            # Bu yerda sizning Cart modelingizga qarab item.product.title yoki item['product'].name bo'lishi mumkin
            products_text += f"- {item['product'].name} ({item['quantity']} dona)\n"

        # TELEGRAM YUBORISH
        try:
            # Vergul o'rniga \n (yangi qator) bilan matnlarni birlashtiramiz (Oddiy String bo'lishi shart!)
            text = (
                f"🛍 YANGI BUYURTMA #{order.id}\n\n"
                f"👤 Mijoz: {order.full_name}\n"
                f"📞 Telefon: {order.phone}\n"
                f"📍 Manzil: {order.address}\n"
                f"💰 Jami: {order.total_price} so'm\n\n"
                f"📦 Mahsulotlar:\n{products_text}"
            )
            
            print("📤 Telegramga yuborilmoqda...")
            send_message(7158438716, text)

        except Exception as e:
            print("❌ Telegram xatosi:", e)

        # CART CLEAR
        cart.clear()

        return redirect("https://www.paynet.uz/")

    return render(request, 'checkout.html', {'cart': cart})


# ======================
# PROFILE
# ======================
@login_required
def profile_detail(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    profile, _ = Profile.objects.get_or_create(user=request.user)

    return render(request, 'profile_detail.html', {
        'orders': orders,
        'profile': profile
    })


# ======================
# EDIT PROFILE
# ======================
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


def search(request):
    query = request.GET.get('q', '').lower()

    results = []

    if query:

        # barcha productlarni olamiz
        products = Product.objects.all()

        matched_products = []

        for product in products:

            product_name = product.name.lower()

            # oddiy qidiruv
            if query in product_name:
                matched_products.append(product)

            else:
                # noto'g'ri yozilgan harflarni ham topadi
                similarity = difflib.SequenceMatcher(
                    None,
                    query,
                    product_name
                ).ratio()

                if similarity > 0.5:
                    matched_products.append(product)

        results = matched_products

    return render(request, 'search.html', {
        'query': query,
        'results': results
    })