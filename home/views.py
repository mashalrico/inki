from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Product, PageVisit

# ---------------------------
# دوال مساعدة لتسجيل الزوار
# ---------------------------
def get_client_ip(request):
    """استخراج عنوان IP للزائر"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_visit(request):
    """تسجيل زيارة الزائر إذا كانت فريدة لهذه الصفحة"""
    ip = get_client_ip(request)
    session_key = request.session.session_key
    path = request.path

    # إنشاء جلسة إذا لم تكن موجودة
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    # تسجيل الزيارة إذا لم تسجل من قبل بنفس الجلسة
    if not PageVisit.objects.filter(path=path, session_key=session_key).exists():
        PageVisit.objects.create(path=path, ip_address=ip, session_key=session_key)

def get_unique_visits(path=None):
    """عدد الزوار الفريدين لكل صفحة أو لكل الموقع"""
    if path:
        return PageVisit.objects.filter(path=path).values('session_key').distinct().count()
    else:
        return PageVisit.objects.values('session_key').distinct().count()

# ---------------------------
# الـ Views الرئيسية
# ---------------------------
def home_view(request):
    log_visit(request)  # تسجيل زيارة الصفحة
    categories_dict = {}
    products = Product.objects.all()
    
    for product in products:
        if product.category and product.category not in categories_dict:
            categories_dict[product.category] = product
    
    categories = list(categories_dict.values())
    
    messages_list = [
        "مرحبا بك في INKI!",
        "احصل على أفضل العروض الآن!",
        "تسوق منتجاتك المفضلة بسهولة.",
        "تابعنا لتصلك أحدث التحديثات."
    ]
    
    # مثال: إظهار عدد الزوار في الصفحة
    unique_home_visits = get_unique_visits('/')  # عدد الزوار الفريدين للصفحة الرئيسية
    total_unique_visits = get_unique_visits()    # عدد الزوار الفريدين للموقع كامل

    return render(request, 'home.html', {
        'categories': categories,
        'messages_list': messages_list,
        'unique_home_visits': unique_home_visits,
        'total_unique_visits': total_unique_visits
    })

def category_view(request, category):
    log_visit(request)
    products = Product.objects.filter(category=category)
    unique_visits = get_unique_visits(path=request.path)
    total_unique_visits = get_unique_visits()

    return render(request, 'category.html', {
        'products': products,
        'category': category,
        'unique_visits': unique_visits,
        'total_unique_visits': total_unique_visits
    })

def product_detail(request, pk):
    log_visit(request)
    product = get_object_or_404(Product, pk=pk)
    unique_visits = get_unique_visits(path=request.path)
    total_unique_visits = get_unique_visits()

    return render(request, 'product_detail.html', {
        'product': product,
        'unique_visits': unique_visits,
        'total_unique_visits': total_unique_visits
    })

def payment(request):
    log_visit(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        amounts = request.POST.getlist('amount[]')  # قائمة كل الحقول
        email = request.POST.get('email')
        payment_method = request.POST.get('payment_method')

        amounts_str = ', '.join(amounts)  # تحويل قائمة الرصيد لسلسلة نصية

        subject = f"طلب دفع جديد - منتج {product_id}"
        message = f"""
رقم المنتج: {product_id}
الرصيد: {amounts_str}
البريد الإلكتروني: {email}
طريقة الدفع: {payment_method}
"""
        recipient_list = ['loluiuinnl66@gmail.com']  # استبدل ببريدك
        send_mail(subject, message, 'loluiuinnl66@gmail.com', recipient_list)

        messages.success(request, 'تم إرسال البيانات بنجاح!')
        return redirect('payment')

    unique_visits = get_unique_visits(path=request.path)
    total_unique_visits = get_unique_visits()
    return render(request, 'payment.html', {
        'unique_visits': unique_visits,
        'total_unique_visits': total_unique_visits
    })
