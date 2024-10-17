"""
URL configuration for orgin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from ninja import NinjaAPI
from django.conf.urls.static import static


from orgin import settings
##from BatMan.controller import auth_controller
from process.controllers.Market import market_controller
from process.controllers.products import product_controller

api = NinjaAPI()
##api.add_router('BatMan', auth_controller)
api.add_router('Market', market_controller)
api.add_router('Product', product_controller)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    
]

