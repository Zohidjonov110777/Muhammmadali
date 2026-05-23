import os
from pathlib import Path

# 1. BAZAVIY YO'LLAR
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. XAVFSIZLIK (Ishlab chiqish rejimi)
SECRET_KEY = 'django-insecure-your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = []

# 3. ILOVALAR (INSTALLED APPS)
INSTALLED_APPS = [
    # Django standart applar
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
     'django.contrib.humanize', 
    # Allauth applar
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # SIZNING APPLARINGIZ
    'magazine', 
    'widget_tweaks',
]

# 4. MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Shundan keyin
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Va shundan keyin
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # MANA SHU QATORNI QO'SHING:
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'root.urls' # Loyihangiz nomi 'root' bo'lsa shunday qoladi

# 5. TEMPLATES (Savat soni chiqishi uchun context_processors qo'shilgan)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # SHU QATORGA E'TIBOR BERING
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'root.wsgi.application'

# 6. MA'LUMOTLAR BAZASI
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 7. PAROLLARNI TEKSHIRISH
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# 8. TILI VA VAQTI (O'zbekiston vaqtiga moslangan)
LANGUAGE_CODE = 'uz-uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# 9. STATIK VA MEDIA FAYLLAR (Rasmlar chiqishi uchun)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 10. DEFAULT AUTO FIELD
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 11. SAVATCHA VA LOGIN SOZLAMALARI
CART_SESSION_ID = 'cart'

LOGIN_REDIRECT_URL = 'index'  # Login qilgach bosh sahifaga o'tish
LOGOUT_REDIRECT_URL = 'index' # Logout qilgach bosh sahifaga o'tish
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_EMAIL_VERIFICATION = 'none'
# Agar foydalanuvchi login qilmagan bo'lsa login sahifasiga yuborish
LOGIN_URL = 'login'

SITE_ID = 1

# 12. TELEGRAM BOT SOZLAMALARI
TELEGRAM_BOT_TOKEN = '8546684735:AAEMiY-mFqsG7yhcLSXshp1Lb9nCDL0IVI4'
TELEGRAM_CHAT_ID = '5287906523'


USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = '.'