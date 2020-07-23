from django.contrib import admin
from .models import Profile
from .models import Product
from .models import Cart

admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(Profile)
# Register your models here.