from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Profile, Product, Cart
from django.core.files.storage import FileSystemStorage
from bs4 import BeautifulSoup
import requests
import urllib.request
from django.db.models import Q
def home(request):
	search_term = ''
	products = Product.objects.filter(~Q(seller=request.user))  
	#displalying all products which are not of the current user
	if 'search' in request.GET:
		search_term = request.GET['search']
		products = Product.objects.filter(title__icontains = search_term)

		catproducts=Product.objects.filter(category__icontains=search_term)
		print(products)
		if products.first() is None:
			products=catproducts
		print(products)
		#products = products.update(catproducts)
	context = {'products':products}
	return render(request, 'ecom/home.html', context)
# class ProductListView(ListView):
#     model = Product
#     template_name = 'ecom/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'products'
#     ordering = ['-date_posted']
#     paginate_by = 5


# class UserProductsListView(ListView):
#     model = Product
#     template_name = 'ecom/profile.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'products'
#     paginate_by = 5

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return Product.objects.filter(author=user).order_by('-date_posted')


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'description', 'price', 'image']

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title', 'description', 'price', 'image']

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Product
	success_url = '/'
	def test_func(self):
		product = self.get_object()
		if self.request.user == product.seller:
			carts = Cart.objects.all();
			for cart in carts:
				if product.id in cart.products:
					# print(cart.products)
					(cart.products).remove(product.id)
					cart.save()
			return True
		return False

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
			return redirect('login')
	else:
		form = UserRegistrationForm()
	return render(request, 'ecom/register.html', {'form': form})

@login_required
def profile(request):
	if request.method == 'POST':
		u_form=UserUpdateForm(request.POST, instance=request.user)
		p_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		
		
		if p_form.is_valid():
			url = p_form.cleaned_data['already_have_a_website']
			print(url)
			data=urllib.request.urlopen(url).read()
			soup=BeautifulSoup(str(data),"lxml")

		
		# print(p_form.instance.already_have_a_website)

			#web scraping code
		u_form.save()
		p_form.save()
		messages.success(request, f'Account updated!')

		return redirect('profile')
	else:
		u_form=UserUpdateForm(instance=request.user)
		p_form=ProfileUpdateForm(instance=request.user.profile)
	context={
    	'u_form':u_form,
    	'p_form':p_form
	}
	return render(request, 'ecom/profile.html',context)

@login_required
def addtocart(request, pk=None):
	# print(pk)
	if pk is not None:
		cart=Cart.objects.filter(user=request.user).first()
		if pk not in cart.products:
			cart.products.append(pk)
			cart.save()
		# (Cart.objects.filter(user=request.user).first()).products = cart.products
		print((Cart.objects.filter(user=request.user).first()).products)
		# (Cart.objects.filter(user=request.user).first()).products.append(pk)
		# print((Cart.objects.filter(user=request.user).first()).products)
	#return render(request, 'ecom/profile.html')	
	return redirect('home')
@login_required
def cart(request):
	objects = []
	cart=Cart.objects.filter(user=request.user).first()
	print(cart.products)
	for product in cart.products:
		# print(product)
		objects.append((Product.objects.filter(id = product)).first())
	context = {'products': objects}
	print(objects)
	return render(request, 'ecom/cart.html', context)
@login_required
def delete_from_cart(request, pk=None):
	if pk is not None:
		cart=Cart.objects.filter(user=request.user).first()
		if pk in cart.products:
			cart.products.remove(pk)
			cart.save()
	return redirect('cart')

class ProductListView(ListView):
    model = Product
    template_name = 'ecom/cart.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product

@login_required
def checkout(request):
	cart=Cart.objects.filter(user=request.user).first()
	print(cart.products)
	for product in cart.products:	
		pdt = (Product.objects.filter(id = product)).first()
		if (pdt).buyer==-1:
			pdt.buyer = request.user.profile.id
			pdt.save()
	return redirect('cart')

@login_required
def notif(request):
	objects = []
	products = Product.objects.filter(seller=request.user).filter(~Q(buyer=-1))
	for product in products:
		objects.append(Profile.objects.get(id=product.buyer))

	notifications=zip(products,objects)
	context = {
	'notifications' : notifications
	}
	return render(request,'ecom/notif.html',context)

# class ProductDeleteView(DeleteView):
#     model = Product
#     user.cart.products.pop()

# def prof_page(request, pk=None):
# 	q = About.objects.get(pk=pk)
# 	username = q.user.username
# 	qs = get_object_or_404(Profile, user__username=username)
# 	cou = Course.objects.filter(teacher__username=username)
# 	abo = About.objects.filter(user__username=username)

# 	context ={'q':q, 'qs':qs , 'cou':cou , 'abo':abo}

# 	return render(request,'ecom/response.html' ,context)
