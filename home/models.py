# app/models.py
import os
from django.db import models
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from django.conf import settings

class Product(models.Model):
    name = models.CharField("اسم المنتج", max_length=200, blank=True, null=True)
    description = models.TextField("وصف المنتج", blank=True, null=True)
    followers_count = models.IntegerField("عدد المتابعين", blank=True, null=True)
    price = models.DecimalField("سعر المنتج", max_digits=12, decimal_places=2, blank=True, null=True)
    color = models.CharField("لون المنتج", max_length=100, blank=True, null=True)
    category = models.CharField("تصنيف المنتج", max_length=150, blank=True, null=True)
    product_number = models.CharField("رقم المنتج", max_length=100, blank=True, null=True)

    image1 = models.ImageField("صورة 1", upload_to="products/", blank=True, null=True)
    image2 = models.ImageField("صورة 2", upload_to="products/", blank=True, null=True)
    image3 = models.ImageField("صورة 3", upload_to="products/", blank=True, null=True)
    image4 = models.ImageField("صورة 4", upload_to="products/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name or f"منتج بدون اسم (ID={self.id})"

    # حذف الصور تلقائيًا عند حذف المنتج
    def delete(self, *args, **kwargs):
        for field in ['image1', 'image2', 'image3', 'image4']:
            img = getattr(self, field)
            if img and os.path.isfile(img.path):
                os.remove(img.path)
        super().delete(*args, **kwargs)

    # تعديل الصور عند الحفظ
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # حفظ الصورة أولاً

        logo_path = os.path.join(settings.STATIC_ROOT, "logo.png")
        website_text = "www.inki.com"

        for field in ['image1', 'image2', 'image3', 'image4']:
            img_field = getattr(self, field)
            if img_field:
                self.add_logo_and_text(img_field.path, logo_path, website_text)

    # --- دالة إضافة اللوجو والنص ---
    def add_logo_and_text(self, image_path, logo_path, website_text):
        """إضافة لوجو شفاف في المنتصف + نص مرة واحدة أسفله مباشرة"""
        base_image = Image.open(image_path).convert("RGBA")

        # معالجة اللوجو
        logo = Image.open(logo_path).convert("RGBA")
        logo_width = int(base_image.width * 0.3)
        logo_height = int((logo_width / logo.width) * logo.height)
        logo = logo.resize((logo_width, logo_height))

        # شفافية 70% للوجو
        alpha = logo.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(0.3)
        logo.putalpha(alpha)

        # وضع اللوجو في منتصف الصورة
        pos_x = (base_image.width - logo.width) // 2
        pos_y = (base_image.height - logo.height) // 2
        base_image.paste(logo, (pos_x, pos_y), logo)

        # إضافة النص أسفل اللوجو مباشرة
        txt_layer = Image.new("RGBA", base_image.size, (255,255,255,0))
        draw = ImageDraw.Draw(txt_layer)
        font_size = int(base_image.width * 0.05)
        try:
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()

        # حساب حجم النص
        bbox = font.getbbox(website_text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (base_image.width - text_width) // 2
        text_y = pos_y + logo.height + 10

        # النص بشفافية منخفضة 30%
        draw.text((text_x, text_y), website_text, fill=(255, 255, 255, 76), font=font)

        # دمج النص مع الصورة الأصلية
        combined = Image.alpha_composite(base_image, txt_layer)
        combined.convert("RGB").save(image_path, "JPEG", quality=95)
class PageVisit(models.Model):
    path = models.CharField(max_length=255)  # مسار الصفحة
    ip_address = models.GenericIPAddressField()  # عنوان IP للزائر
    session_key = models.CharField(max_length=40, null=True, blank=True)  # مفتاح الجلسة
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.path} - {self.ip_address}"