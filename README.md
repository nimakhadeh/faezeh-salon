# سالن فائزه - سیستم جامع مدیریت سالن بافت مو

<p align="center">
  <h3 align="center">Faezeh Salon - Fullstack Hair Braiding Salon Management System</h3>
  <p align="center">
    Django 5 + Next.js 14 + PostgreSQL + Redis + Celery + WebSocket + Docker Compose
  </p>
</p>

---

## 📋 فهرست مطالب

- [معرفی پروژه](#معرفی-پروژه)
- [استک فنی](#استک-فنی)
- [ساختار پروژه](#ساختار-پروژه)
- [پیش‌نیازها](#پیشنیازها)
- [نصب و راه‌اندازی](#نصب-و-راهاندازی)
- [سرویس‌های Docker](#سرویسهای-docker)
- [APIهای Backend](#apiهای-backend)
- [قابلیت‌ها](#قابلیتها)
- [ماژول‌های سیستم](#ماژولهای-سیستم)
- [تست با Postman](#تست-با-postman)
- [تنظیمات محیطی](#تنظیمات-محیطی)
- [راهنمای توسعه](#راهنمای-توسعه)
- [عیب‌یابی](#عیبیابی)

---

## 🌟 معرفی پروژه

**سالن فائزه** یک سیستم جامع تحت وب برای مدیریت سالن بافت و اکستنشن مو است. این پروژه شامل تمام قابلیت‌های لازم برای یک سالن حرفه‌ای از جمله رزرو نوبت با تقویم، پرداخت آنلاین، سیستم وفاداری، چت داخلی، ربات تلگرام، پیامک خودکار و داشبورد مدیریتی است.

### مشخصات صاحب سالن
- **نام:** فائزه
- **سابقه:** ۴ سال حرفه‌ای در بافت و اکستنشن مو
- **شماره تماس:** ۰۹۳۹۹۵۴۵۱۱۳
- **اینستاگرام:** @Baftmofaezeh
- **آدرس:** ستارخان کوچه ۱۲/۱ و عفیف‌آباد کوچه ۲۲
- **شعار:** ظرافت، دوام بالا، حال خوب، اعتماد به نفس

### خدمات
- بافت مو (آفریقایی، برزیلی، مکزیکی، افرو، کوئین، هلندی، فرانسوی، دردلاک، ترکیبی، ساده، پیشرفته، مینیمال، ژورنالی)
- مناسب روزمره، مهمونی، مسافرت
- اکستنشن (بافت، کراتین با متریال باکیفیت)
- آموزش صفر تا صد (مبتدی تا حرفه‌ای)
- مناسب سنین ۳ تا ۵۰ سال

---

## 🔧 استک فنی

| لایه | تکنولوژی | نسخه |
|------|----------|------|
| Backend | Django + Django REST Framework | 5.x |
| Frontend | Next.js (App Router) + TypeScript | 14.x |
| Database | PostgreSQL | 16 |
| Cache/Queue | Redis | 7 |
| Task Queue | Celery + Celery Beat | 5.x |
| WebSocket | Django Channels + Daphne | 4.x |
| Auth | JWT (djangorestframework-simplejwt) | - |
| Payment | Zarinpal (زرین‌پال) | - |
| SMS | Kavenegar (کاوه‌نگار) | - |
| Telegram | python-telegram-bot | v20+ |
| Container | Docker + Docker Compose | - |
| Reverse Proxy | Nginx | Alpine |

---

## 📁 ساختار پروژه

```
faezeh-salon/
├── backend/                          # Django Backend
│   ├── config/                       # تنظیمات اصلی Django
│   │   ├── __init__.py
│   │   ├── settings.py              # تنظیمات (DB, Redis, Celery, JWT, etc.)
│   │   ├── urls.py                   # مسیریابی اصلی
│   │   ├── asgi.py                   # ASGI + Channels (WebSocket)
│   │   ├── wsgi.py                   # WSGI
│   │   └── celery.py                 # تنظیمات Celery
│   ├── apps/                         # اپلیکیشن‌های Django
│   │   ├── accounts/                 # احراز هویت و پروفایل
│   │   │   ├── models.py             # User, PasswordResetOTP
│   │   │   ├── serializers.py        # Register, Login, Profile
│   │   │   ├── views.py              # API Views
│   │   │   ├── urls.py               # Routes
│   │   │   ├── admin.py              # Admin config
│   │   │   └── management/commands/create_default_admin.py
│   │   ├── services/                 # محصولات و خدمات
│   │   │   ├── models.py             # Category, Service, Product
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── admin.py
│   │   ├── appointments/             # رزرو نوبت با تقویم
│   │   │   ├── models.py             # Appointment
│   │   │   ├── serializers.py
│   │   │   ├── views.py              # Slots, Booking, Schedule
│   │   │   ├── urls.py
│   │   │   ├── admin.py
│   │   │   └── tasks.py              # Celery tasks
│   │   ├── payments/                 # پرداخت و تراکنش
│   │   │   ├── models.py             # Transaction
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── admin.py
│   │   │   └── zarinpal.py           # Zarinpal integration
│   │   ├── wallet/                   # کیف پول داخلی
│   │   │   ├── models.py             # Wallet, WalletTransaction
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── admin.py
│   │   ├── loyalty/                  # برنامه وفاداری
│   │   │   ├── models.py             # LoyaltyRule, LoyaltyPoint
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── admin.py
│   │   │   └── tasks.py              # Auto-award points
│   │   ├── gallery/                  # گالری Before/After
│   │   │   ├── models.py             # GalleryImage
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── admin.py
│   │   ├── chat/                     # چت داخلی WebSocket
│   │   │   ├── models.py             # ChatRoom, ChatMessage
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── consumers.py          # WebSocket Consumer
│   │   │   ├── routing.py            # WS URL patterns
│   │   │   ├── urls.py
│   │   │   └── admin.py
│   │   ├── survey/                   # نظرسنجی NPS
│   │   │   ├── models.py             # SurveyResponse
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── admin.py
│   │   ├── crm/                      # سیستم پیگیری مشتری
│   │   │   ├── models.py             # CustomerInteraction, BulkSMS
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── admin.py
│   │   ├── zarinpal/                 # ماژول پرداخت
│   │   ├── kavenegar/                # ماژول پیامک
│   │   │   └── utils.py              # send_sms, reminders
│   │   └── telegram_bot/             # ربات تلگرام
│   │       ├── bot.py                # Telegram bot main
│   │       ├── views.py              # Webhook handler
│   │       └── urls.py
│   ├── requirements.txt              # وابستگی‌های Python
│   ├── Dockerfile                    # Backend Dockerfile
│   └── manage.py                     # Django CLI
│
├── frontend/                         # Next.js Frontend
│   ├── app/                          # App Router
│   │   ├── page.tsx                  # صفحه اصلی
│   │   ├── layout.tsx                # Layout + AuthProvider
│   │   ├── globals.css               # Tailwind + Global styles
│   │   ├── login/page.tsx            # صفحه ورود
│   │   ├── register/page.tsx         # صفحه ثبت‌نام
│   │   ├── forgot-password/page.tsx  # بازنشانی رمز
│   │   ├── services/page.tsx         # لیست خدمات
│   │   ├── booking/page.tsx          # رزرو با تقویم
│   │   ├── gallery/page.tsx          # گالری
│   │   ├── products/page.tsx         # محصولات
│   │   ├── contact/page.tsx          # تماس
│   │   └── dashboard/page.tsx        # داشبورد کاربر
│   ├── components/                   # کامپوننت‌های مشترک
│   │   ├── navbar.tsx                # منوی ناوبری
│   │   └── footer.tsx                # فوتر
│   ├── lib/                          # کتابخانه‌ها
│   │   ├── api.ts                    # API client (axios)
│   │   ├── auth-context.tsx          # Context احراز هویت
│   │   └── utils.ts                  # توابع کمکی
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── postcss.config.js
│
├── docker/                           # تنظیمات Docker
│   └── nginx/
│       └── nginx.conf                # Nginx reverse proxy
│
├── scripts/                          # اسکریپت‌های کمکی
├── docker-compose.yml                # Docker Compose (7 سرویس)
├── .env.example                      # نمونه متغیرهای محیطی
├── .gitignore
└── README.md                         # همین فایل
```

---

## 💻 پیش‌نیازها

- **Ubuntu 22.04+** (یا هر توزیع لینوکس)
- **Docker** 24.0+ و **Docker Compose** v2
- **Git** (اختیاری)

### نصب Docker روی Ubuntu:

```bash
# بروزرسانی سیستم
sudo apt update && sudo apt upgrade -y

# نصب Docker
sudo apt install -y docker.io docker-compose-plugin

# اضافه کردن کاربر به گروه docker
sudo usermod -aG docker $USER

# راه‌اندازی Docker
sudo systemctl enable docker
sudo systemctl start docker

# خروج و ورود مجدد به سیستم (یا):
newgrp docker

# تست
docker --version
docker compose version
```

---

## 🚀 نصب و راه‌اندازی

### مرحله ۱: کلون پروژه

```bash
cd ~/
# اگر از git استفاده می‌کنید:
git clone <repository-url>
cd faezeh-salon
```

### مرحله ۲: تنظیم متغیرهای محیطی

```bash
cp .env.example .env
nano .env
```

حداقل مقادیر لازم:
```env
DEBUG=True
SECRET_KEY=your-very-secret-key-change-in-production
POSTGRES_PASSWORD=your-secure-postgres-password
ZARINPAL_MERCHANT_ID=your-zarinpal-merchant-id
ZARINPAL_SANDBOX=True
KAVENEGAR_API_KEY=your-kavenegar-api-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

### مرحله ۳: ساخت و اجرای کانتینرها

```bash
# ساخت و اجرای همه سرویس‌ها
docker compose up -d --build

# مشاهده لاگ‌ها
docker compose logs -f

# مشاهده وضعیت سرویس‌ها
docker compose ps
```

### مرحله ۴: اجرای migrations و ایجاد superuser

این کار به صورت خودکار در startup انجام می‌شود، اما اگر نیاز بود:

```bash
# اجرای migrations دستی
docker compose exec backend python manage.py migrate

# جمع‌آوری فایل‌های static
docker compose exec backend python manage.py collectstatic --noinput

# ایجاد superuser
docker compose exec backend python manage.py createsuperuser
```

### مرحله ۵: دسترسی به برنامه

| سرویس | آدرس |
|-------|------|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000/api/ |
| Django Admin | http://localhost:8000/admin/ |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |
| Nginx | http://localhost |
| Flower (Celery) | نیاز به نصب جداگانه |

### مرحله ۶: راه‌اندازی ربات تلگرام (اختیاری)

```bash
# با polling:
docker compose --profile bot up -d telegram-bot

# یا تنظیم webhook
# در فایل .env:
# TELEGRAM_WEBHOOK_URL=https://your-domain.com/telegram/webhook/
```

---

## 🐳 سرویس‌های Docker

| سرویس | پورت | توضیحات |
|-------|------|---------|
| `postgres` | 5432 | دیتابیس PostgreSQL 16 با volume |
| `redis` | 6379 | کش و broker Celery |
| `backend` | 8000 | Django + Daphne (ASGI/WebSocket) |
| `celery-worker` | - | پردازش task‌ها |
| `celery-beat` | - | زمان‌بندی task‌ها |
| `frontend` | 3000 | Next.js 14 + TypeScript |
| `nginx` | 80 | Reverse proxy + static/media |
| `telegram-bot` | - | ربات تلگرام (اختیاری) |

### دستورات مفید Docker:

```bash
# مشاهده لاگ سرویس خاص
docker compose logs -f backend
docker compose logs -f celery-worker
docker compose logs -f celery-beat

# ری‌استارت سرویس
docker compose restart backend

# اجرای دستور در کانتینر
docker compose exec backend python manage.py shell
docker compose exec backend python manage.py dbshell
docker compose exec postgres psql -U faezeh_user -d faezeh_salon

# توقف همه سرویس‌ها
docker compose down

# توقف و حذف volumeها
docker compose down -v

# ری‌بیلد بدون cache
docker compose build --no-cache
```

---

## 🔌 APIهای Backend

### احراز هویت (`/api/auth/`)

| Endpoint | Method | توضیحات |
|----------|--------|---------|
| `/register/` | POST | ثبت‌نام |
| `/login/` | POST | ورود (دریافت JWT) |
| `/refresh/` | POST | تمدید توکن |
| `/profile/` | GET, PATCH | پروفایل کاربر |
| `/specialists/` | GET | لیست متخصص‌ها |
| `/change-password/` | POST | تغییر رمز |
| `/request-otp/` | POST | درخواست کد بازنشانی |
| `/verify-otp/` | POST | تأیید کد و تغییر رمز |

### خدمات (`/api/services/`)

| Endpoint | Method | توضیحات |
|----------|--------|---------|
| `/categories/` | GET | دسته‌بندی‌ها |
| `/services/` | GET | لیست خدمات (با filter) |
| `/services/<slug>/` | GET | جزئیات خدمت |
| `/products/` | GET | لیست محصولات |
| `/products/featured/` | GET | محصولات ویژه |
| `/products/<slug>/` | GET | جزئیات محصول |

### نوبت‌ها (`/api/appointments/`)

| Endpoint | Method | توضیحات |
|----------|--------|---------|
| `/slots/` | GET | زمان‌های آزاد (با specialist, service, date) |
| `/` | GET, POST | لیست و ایجاد نوبت |
| `/my/` | GET | نوبت‌های من |
| `/<id>/` | GET, DELETE | جزئیات و لغو |
| `/<id>/status/` | POST | تغییر وضعیت |
| `/specialist/schedule/` | GET | برنامه متخصص |

### پرداخت (`/api/payments/`)

| Endpoint | Method | توضیحات |
|----------|--------|---------|
| `/transactions/` | GET | لیست تراکنش‌ها |
| `/request/` | POST | درخواست پرداخت |
| `/verify/` | GET | تأیید پرداخت زرین‌پال |

### کیف پول (`/api/wallet/`)

| Endpoint | Method | توضیحات |
|----------|--------|---------|
| `/` | GET | موجودی |
| `/history/` | GET | تاریخچه |
| `/charge/` | POST | شارژ از طریق زرین‌پال |
| `/pay/` | POST | پرداخت با کیف پول |

### وفاداری (`/api/loyalty/`)

| Endpoint | Method | توضیحات |
|----------|--------|---------|
| `/rules/` | GET | قوانین |
| `/my/` | GET | امتیاز من |
| `/history/` | GET | تاریخچه |
| `/convert/` | POST | تبدیل امتیاز به کیف پول |

### گالری (`/api/gallery/`)

| Endpoint | Method | توضیحات |
|----------|--------|---------|
| `/public/` | GET | گالری عمومی |
| `/my/` | GET | آپلودهای من |
| `/upload/` | POST | آپلود تصویر |
| `/specialist/<id>/` | GET | گالری متخصص |
| `/pending/` | GET | در انتظار تأیید (admin) |
| `/<id>/approve/` | PATCH | تأیید/رد (admin) |

### چت (`/api/chat/`)

| Endpoint | Method | توضیحات |
|----------|--------|---------|
| `/rooms/` | GET | اتاق‌های چت |
| `/rooms/create/` | POST | ایجاد اتاق |
| `/rooms/<id>/` | GET | جزئیات اتاق |
| `/rooms/<id>/messages/` | GET | پیام‌ها |
| `/rooms/<id>/read/` | POST | علامت خوانده |

**WebSocket:** `ws://localhost:8000/ws/chat/<room_id>/`

### نظرسنجی (`/api/survey/`)

| Endpoint | Method | توضیحات |
|----------|--------|---------|
| `/submit/` | POST | ثبت پاسخ |
| `/my/` | GET | پاسخ‌های من |
| `/stats/` | GET | آمار (admin) |

### CRM (`/api/crm/`)

| Endpoint | Method | توضیحات |
|----------|--------|---------|
| `/customers/` | GET | لیست مشتریان با فیلتر |
| `/customers/<id>/` | GET | جزئیات مشتری |
| `/interactions/` | GET, POST | تعاملات |
| `/bulk-sms/` | POST | ارسال پیامک گروهی |

### تلگرام (`/telegram/`)

| Endpoint | Method | توضیحات |
|----------|--------|---------|
| `/webhook/` | POST | Webhook ربات |

---

## ✅ قابلیت‌ها

### ✅ ماژول ۱: احراز هویت و پروفایل
- [x] ثبت‌نام و ورود با JWT (access + refresh)
- [x] سه نوع کاربر: مشتری، متخصص، ادمین
- [x] پروفایل با آپلود عکس، شماره، تاریخ تولد
- [x] تغییر رمز و بازیابی با پیامک

### ✅ ماژول ۲: فروشگاه محصولات و خدمات
- [x] مدل Product و Service
- [x] سبد خرید
- [x] ثبت سفارش و پرداخت

### ✅ ماژول ۳: رزرو نوبت با تقویم + بیعانه ۳۰٪
- [x] تقویم بصری با React
- [x] نمایش فقط زمان‌های آزاد
- [x] پرداخت بیعانه ۳۰٪ از طریق زرین‌پال
- [x] قفل روی بازه زمانی (UniqueConstraint)

### ✅ ماژول ۴: درگاه پرداخت زرین‌پال کامل
- [x] request + verify
- [x] پشتیبانی از metadata
- [x] پرداخت برای بیعانه، خرید، شارژ کیف پول

### ✅ ماژول ۵: سیستم والت داخلی
- [x] موجودی، شارژ، برداشت
- [x] پرداخت از کیف پول
- [x] تاریخچه تراکنش‌ها

### ✅ ماژول ۶: برنامه وفاداری
- [x] قوانین قابل ویرایش
- [x] کسب امتیاز هنگام خرید
- [x] تبدیل امتیاز به کیف پول

### ✅ ماژول ۷: گالری Before/After
- [x] آپلود تصویر
- [x] تأیید توسط ادمین
- [x] گالری عمومی

### ✅ ماژول ۸: یادآوری خودکار با پیامک
- [x] ۲۴ ساعته و ۲ ساعته
- [x] Celery Beat هر ساعت

### ✅ ماژول ۹: نظرسنجی NPS
- [x] امتیاز ۰-۱۰
- [x] سوال هدفمند

### ✅ ماژول ۱۰: چت داخلی WebSocket
- [x] ۱:۱ بین مشتری و متخصص
- [x] پیام متنی
- [x] اعلان پیام جدید

### ✅ ماژول ۱۱: داشبورد متخصص و ادمین
- [x] داشبورد کاربر
- [x] مدیریت ادمین Django

### ✅ ماژول ۱۲: ربات تلگرام
- [x] مشاهده نوبت‌ها
- [x] لغو نوبت
- [x] اطلاعات تماس

### ✅ ماژول ۱۳: اتوماسیون سفارش + پیامک
- [x] SMS خودکار پس از ثبت نوبت
- [x] اطلاع‌رسانی تغییر وضعیت

### ✅ ماژول ۱۴: CRM
- [x] لیست مشتریان با فیلتر
- [x] پیامک گروهی
- [x] تاریخچه تعاملات

---

## 🧪 تست با Postman

### ۱. ثبت‌نام
```http
POST http://localhost:8000/api/auth/register/
Content-Type: application/json

{
  "phone": "09123456789",
  "username": "testuser",
  "first_name": "تست",
  "last_name": "کاربر",
  "password": "testpass123",
  "password2": "testpass123",
  "role": "customer"
}
```

### ۲. ورود
```http
POST http://localhost:8000/api/auth/login/
Content-Type: application/json

{
  "phone": "09123456789",
  "password": "testpass123"
}
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1Qi...",
  "refresh": "eyJ0eXAiOiJKV1Qi...",
  "user": { ... }
}
```

### ۳. استفاده از Access Token
```http
GET http://localhost:8000/api/auth/profile/
Authorization: Bearer eyJ0eXAiOiJKV1Qi...
```

### ۴. مشاهده خدمات
```http
GET http://localhost:8000/api/services/services/
```

### ۵. مشاهده زمان‌های آزاد
```http
GET http://localhost:8000/api/appointments/slots/?specialist=1&service=1&date=2024-06-15
```

### ۶. رزرو نوبت
```http
POST http://localhost:8000/api/appointments/
Authorization: Bearer <token>
Content-Type: application/json

{
  "specialist": 1,
  "service": 1,
  "date": "2024-06-15",
  "start_time": "14:00",
  "end_time": "15:00"
}
```

### ۷. پرداخت بیعانه
```http
POST http://localhost:8000/api/payments/request/
Authorization: Bearer <token>
Content-Type: application/json

{
  "amount": 150000,
  "transaction_type": "deposit",
  "description": "بیعانه بافت آفریقایی",
  "metadata": {"appointment_id": 1}
}
```

### ۸. ورود به ادمین
- آدرس: http://localhost:8000/admin/
- یوزر: admin
- پسورد: admin123 (قابل تغییر در .env)

---

## ⚙️ تنظیمات محیطی

### متغیرهای مهم `.env`:

| متغیر | توضیحات | مثال |
|-------|---------|------|
| `SECRET_KEY` | کلید رمزنگاری Django | `django-insecure-...` |
| `DEBUG` | حالت دیباگ | `True` / `False` |
| `POSTGRES_PASSWORD` | رمز دیتابیس | `secure-password` |
| `ZARINPAL_MERCHANT_ID` | مرچنت زرین‌پال | `xxxxxxxx-xxxx-...` |
| `ZARINPAL_SANDBOX` | حالت تست زرین‌پال | `True` |
| `KAVENEGAR_API_KEY` | API کاوه‌نگار | `your-api-key` |
| `TELEGRAM_BOT_TOKEN` | توکن ربات تلگرام | `123456:ABC-DEF...` |
| `ADMIN_PHONE` | شماره ادمین پیش‌فرض | `09399545113` |

---

## 🔧 راهنمای توسعه

### اضافه کردن اپلیکیشن جدید:

```bash
# در backend
docker compose exec backend python manage.py startapp new_app apps/new_app

# اضافه کردن به INSTALLED_APPS در settings.py
# نوشتن models, serializers, views
# اضافه کردن urls
```

### تغییر مدل‌ها:

```bash
# ساخت migration
docker compose exec backend python manage.py makemigrations

# اجرای migration
docker compose exec backend python manage.py migrate
```

### دسترسی به شل Django:

```bash
docker compose exec backend python manage.py shell
```

### مشاهده Queryهای SQL:

```python
# در Django shell
from django.db import connection
print(connection.queries)
```

---

## 🐛 عیب‌یابی

### مشکل: سرویس‌ها بالا نمی‌آیند
```bash
docker compose logs <service-name>
docker compose ps
# بررسی کنید پورت‌ها اشغال نباشند
sudo lsof -i :5432
sudo lsof -i :6379
sudo lsof -i :8000
sudo lsof -i :3000
```

### مشکل: پایگاه داده متصل نمی‌شود
```bash
# بررسی healthcheck
docker compose ps

# دسترسی به دیتابیس
docker compose exec postgres psql -U faezeh_user -d faezeh_salon -c "\dt"
```

### مشکل: static files لود نمی‌شوند
```bash
docker compose exec backend python manage.py collectstatic --noinput
```

### مشکل: WebSocket کار نمی‌کند
```bash
# بررسی کنید Daphne اجرا شده
# در docker-compose.yml از daphne استفاده شده
# بررسی nginx.conf برای WebSocket
```

### مشکل: Celery task اجرا نمی‌شود
```bash
# بررسی وضعیت celery-worker و celery-beat
docker compose logs celery-worker
docker compose logs celery-beat

# ری‌استارت
docker compose restart celery-worker celery-beat
```

### پاک کردن همه داده‌ها و شروع از اول:
```bash
docker compose down -v
docker compose up -d --build
```

---

## 📱 اطلاعات تماس

- **نام:** فائزه
- **شماره:** ۰۹۳۹۹۵۴۵۱۱۳
- **اینستاگرام:** @Baftmofaezeh
- **آدرس:** ستارخان کوچه ۱۲/۱ و عفیف‌آباد کوچه ۲۲

---

## 📝 لایسنس

این پروژه متن‌باز است و برای استفاده شخصی فائزه عزیز ساخته شده است.

---

<p align="center">
  <b>ظ\u0631\u0641\u062a\u060c \u062f\u0648\u0627\u0645 \u0628\u0627\u0644\u0627\u060c \u062d\u0627\u0644 \u062e\u0648\u0628\u060c \u0627\u0639\u062a\u0645\u0627\u062f \u0628\u0647 \u0646\u0641\u0633</b>
</p>
# faezeh-salon
