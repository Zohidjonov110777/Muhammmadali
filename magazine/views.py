from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Profile
from .cart import Cart
from .models import Order, Product
import requests
from httpx import post, get
from .forms import ProfileForm
from .models import Profile

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    
    action = request.POST.get('action') # 'decrease' yoki None (qo'shish)
    
    if action == 'decrease':
        # Mavjud miqdorga -1 qo'shamiz
        cart.add(product=product, quantity=-1, override_quantity=False)
    else:
        # Mavjud miqdorga +1 qo'shamiz
        cart.add(product=product, quantity=1, override_quantity=False)
        
    return redirect('cart_detail')


# Telegram Bot sozlamalari
TELEGRAM_BOT_TOKEN = '8546684735:AAFPhO_cxCLi80mlir1fzpf5hrP3isSdfQI'
TELEGRAM_ADMIN_ID = '7158438716' 

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_ADMIN_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegramga yuborishda xatolik: {e}")

def checkout(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        if first_name and phone:
            # 1. Buyurtmani bazada saqlash
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=first_name,
                phone=phone,
                address=address,
                total_price=cart.get_total_price()
            )

            # 2. Telegram uchun xabar tayyorlash
            message = f"<b>🛍 Yangi buyurtma!</b>\n\n"
            message += f"👤 <b>Mijoz:</b> {first_name}\n"
            message += f"📞 <b>Telefon:</b> {phone}\n"
            message += f"📍 <b>Manzil:</b> {address}\n\n"
            message += f"🛒 <b>Mahsulotlar:</b>\n"
            
            for item in cart:
                message += f" - {item['product'].name}: {item['quantity']} dona x {item['price']} so'm\n"
            
            message += f"\n💰 <b>Umumiy summa:</b> {cart.get_total_price()} so'm"

            # 3. Telegramga yuborish
            send_telegram_message(message)

            # 4. Savatni tozalash va natijani ko'rsatish
            cart.clear()
            return render(request, 'checkout.html', {'success': True, 'order': order})
            
    return render(request, 'checkout.html', {'cart': cart})


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'magazine/edit_profile.html', {'form': form})

@login_required
def profile_detail(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'magazine/profile_detail.html', {'profile': profile})



TELEGRAM_BOT_TOKEN = '8546684735:AAFPhO_cxCLi80mlir1fzpf5hrP3isSdfQI'

def send_message(chat_id, message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message
    }
    response = get(url, params=params)
    print(response.text, response.status_code)



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