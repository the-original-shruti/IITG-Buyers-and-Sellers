from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models import IntegerField, Model
from django_mysql.models import ListTextField
from django.urls import reverse
Categories = (
	('all','All'),
	('sports','Sports'),
	('electric','Electric Appliances'),
)
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	already_have_a_website = models.CharField(default='',max_length=500, blank=True)
	# productn = ListTextField(base_field=IntegerField(), size=100,null=True)
	address = models.TextField(default=None,blank=True,null=True)
	# buyern = ListTextField(base_field=IntegerField(), size=100,null=True)
	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)

		img = Image.open(self.image.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

class Cart(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	products = ListTextField(base_field=IntegerField(), size=100,)
	def save(self, *args, **kwargs):
		super(Cart, self).save(*args, **kwargs)

	# def __str__(self):
	# 	return self.user
class Product(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
	image = models.ImageField(default='tiger.jpg', upload_to='product_pics')
	category=models.CharField(max_length=50,choices=Categories,default='all')
	buyer = models.IntegerField(default = -1)
	# ordered = models.BooleanField(default = false)
	# delivered = models.BooleanField(default = false)
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('product-detail', kwargs={'pk': self.pk})

# Create your models here.
