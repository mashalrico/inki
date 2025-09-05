from django.urls import path
from . import views
from . import views as home_views
urlpatterns = [
    path('', home_views.home_view, name='home'),
    path('category/<str:category>/', views.category_view, name='category_view'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),  # صفحة المنتج حسب ID
    path('payment/', views.payment, name='payment'),



]   
