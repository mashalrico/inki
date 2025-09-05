# app/utils.py
from PIL import Image, ImageDraw, ImageFont
import os

def add_logo_and_text(image_path, logo_path, website_text, output_path):
    """
    تضيف اللوجو والنص (رابط الموقع) على الصورة
    """
    # افتح الصورة الأساسية
    base_image = Image.open(image_path).convert("RGBA")
    
    # افتح اللوجو
    logo = Image.open(logo_path).convert("RGBA")
    
    # غيّر حجم اللوجو إذا احتجت
    logo_width = int(base_image.width * 0.15)  # 15% من عرض الصورة
    logo_height = int((logo_width / logo.width) * logo.height)
    logo = logo.resize((logo_width, logo_height))
    
    # حط اللوجو في الركن العلوي الأيسر (يمكن تغييره)
    position = (10, 10)
    base_image.paste(logo, position, logo)
    
    # إضافة النص (رابط الموقع)
    draw = ImageDraw.Draw(base_image)
    font_path = "arial.ttf"  # ضع مسار الخط على السيرفر
    font_size = int(base_image.width * 0.04)  # حجم الخط 4% من عرض الصورة
    font = ImageFont.truetype(font_path, font_size)
    
    text_position = (10, base_image.height - font_size - 10)  # الركن السفلي الأيسر
    draw.text(text_position, website_text, fill=(255,255,255,255), font=font)
    
    # حفظ الصورة الجديدة
    base_image.save(output_path)
    return output_path
