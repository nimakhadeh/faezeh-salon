"""
Services App - Products (محصولات) and Services (خدمات)
"""

from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    icon = models.CharField(max_length=50, blank=True, verbose_name="آیکون")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Service(models.Model):
    BRAID_TYPES = [
        ("african", "آفریقایی"),
        ("brazilian", "برزیلی"),
        ("mexican", "مکزیکی"),
        ("afro", "افرو"),
        ("queen", "کوئین"),
        ("dutch", "هلندی"),
        ("french", "فرانسوی"),
        ("dreadlock", "دردلاک"),
        ("combined", "ترکیبی"),
        ("simple", "ساده"),
        ("advanced", "پیشرفته"),
        ("minimal", "مینیمال"),
        ("journal", "ژورنالی"),
        ("daily", "مناسب روزمره"),
        ("party", "مناسب مهمونی"),
        ("travel", "مناسب مسافرت"),
        ("extension_braid", "اکستنشن بافت"),
        ("extension_keratin", "اکستنشن کراتین"),
        ("training", "آموزش"),
    ]

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="services", verbose_name="دسته‌بندی")
    name = models.CharField(max_length=200, verbose_name="نام خدمت")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    description = models.TextField(verbose_name="توضیحات")
    braid_type = models.CharField(max_length=30, choices=BRAID_TYPES, verbose_name="نوع بافت")
    duration_minutes = models.PositiveIntegerField(default=60, verbose_name="مدت زمان (دقیقه)")
    base_price = models.PositiveIntegerField(validators=[MinValueValidator(1000)], verbose_name="قیمت پایه (تومان)")
    max_price = models.PositiveIntegerField(blank=True, null=True, verbose_name="قیمت حداکثر (تومان)")
    image = models.ImageField(upload_to="services/", blank=True, null=True, verbose_name="تصویر")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    suitable_ages = models.CharField(max_length=100, default="۳ تا ۵۰ سال", verbose_name="مناسب سنین")
    requires_deposit = models.BooleanField(default=True, verbose_name="نیاز به بیعانه")
    deposit_percent = models.PositiveIntegerField(default=30, verbose_name="درصد بیعانه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "خدمت"
        verbose_name_plural = "خدمات"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_braid_type_display()})"

    @property
    def price_range(self):
        if self.max_price and self.max_price > self.base_price:
            return f"{self.base_price:,} - {self.max_price:,}"
        return f"{self.base_price:,}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products", verbose_name="دسته‌بندی")
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    description = models.TextField(verbose_name="توضیحات")
    price = models.PositiveIntegerField(validators=[MinValueValidator(1000)], verbose_name="قیمت (تومان)")
    discount_price = models.PositiveIntegerField(blank=True, null=True, verbose_name="قیمت تخفیف‌خورده")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="تصویر")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def has_discount(self):
        return self.discount_price is not None and self.discount_price < self.price

    @property
    def final_price(self):
        return self.discount_price or self.price

    @property
    def discount_percent(self):
        if self.has_discount:
            return int((1 - self.discount_price / self.price) * 100)
        return 0
