"""core URL Configuration

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

# core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# View simples para teste
def home(request):
    return HttpResponse("""
    <h1>🚀 Django no Railway - Deploy Bem Sucedido!</h1>
    <p>Sua aplicação está online e funcionando!</p>
    <ul>
        <li><a href="/admin/">Admin Django</a></li>
        <li><a href="/dashboard/">Dashboard</a></li>
    </ul>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('data-process/', include('data_process.urls')),
    path('', include('data_visual.urls')),
]