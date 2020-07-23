from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from .views import (
	ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    # UserProductsListView
)
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
	path('register/', views.register, name='register'),
	path('login/', auth_views.LoginView.as_view(template_name='ecom/login.html'), name = 'login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='ecom/logout.html'), name = 'logout'),
	path('profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
	# Courses -->

    # path('user/<str:username>', UserProductListView.as_view(), name='user-products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/new/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('cart/<int:pk>/delete/', views.delete_from_cart, name='delete_from_cart'),
    path('product/<int:pk>/addtocart/', views.addtocart, name='addtocart'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('profile/notif/', views.notif, name='notif'),
   	# path('search/<int:pk>/', views.prof_page, name='prof_page'),
]


if settings.DEBUG:
	urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)