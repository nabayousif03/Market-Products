from django.db import models
from django.contrib.auth import get_user_model
import uuid

from orgin.ent.tool import Entity

User = get_user_model()

class TypesOfProduct(Entity):
    dairy_products = 'DAIRY PRODUCTS'
    meet_seafood = 'MEET SEAFOOD'
    fresh_products = 'FRESH PRODUCTS'
    frozen_foods = 'FROZEN FOODS'
    canned = 'CANNED'
    bakery = 'BAKERY'
    snacks = 'SNACKS'
    sauces = 'SAUCES'
    paper_products = 'PAPER PRODUCTS'
    cleaning_supplies = 'CLEANING SUPPLIES'
    kitchen_ess = 'KITCHEN ESS'
    personal_care = 'PERSONAL CARE'
    pet_supplies = 'PET SUPPLIES'
    miscellaneous = 'MISCELLANEOUS'
    other = 'OTHER'
    title = models.CharField('title', max_length=256, choices=[
        (dairy_products, dairy_products),
        (meet_seafood, meet_seafood),
        (fresh_products,fresh_products),
        (frozen_foods, frozen_foods),
        (canned,canned),
        (bakery,bakery),
        (snacks, snacks),
        (sauces, sauces)
        (paper_products,paper_products),
        (cleaning_supplies,cleaning_supplies),
        (kitchen_ess,kitchen_ess),
        (personal_care, personal_care),
        (pet_supplies,pet_supplies),
        (miscellaneous,miscellaneous),
        (other,other),

])
    
    is_default = models.BooleanField('is_default')

    def __str__(self):
        return self.title
    

class Products(Entity):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='products')
    
    type = models.CharField(max_length=50, null=True, blank=True)
    product_name = models.CharField(max_length=50, null=True, blank=True)
    expire_date = models.DateTimeField(max_length=50, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    is_available = models.BooleanField(default=True, null=True, blank=True)
    no_of_product = models.IntegerField(max_length=244 , null= True, blank= True)
    @property

    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name






class Market(Entity):
    name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    phone = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=50, null=True, blank=True)
    logo = models.ImageField(upload_to='market_logo', blank=True, null=True)
    images = models.ImageField(upload_to='market_images', blank=True, null=True)
    about = models.TextField(max_length=500, null=True, blank=True)
    products = models.ManyToManyField('products', related_name='market')

    def __str__(self):
        return self.name
    
class timeLine(Entity):
    products  = models.ForeignKey(Products, on_delete=models.CASCADE)    
    day = models.CharField(max_length=50)
    start_time  = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.products.user.first_name + ' ' + self.products.user.last_name + ' ' + self.day




# Create your models here.
