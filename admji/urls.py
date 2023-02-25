"""admji URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from programacao import views

from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/programacao/igreja/<int:index_alfabetico>/', views.igreja_ordem_alfabetica),
    path('api/programacao/mensagem/igrejas/', views.igrejas_mensagem),
    path('api/programacao/<str:semana>/<str:igreja>/', views.programacao_atual),
    path('api/programacao/mensagem/', views.programacao_mensagem),
]
