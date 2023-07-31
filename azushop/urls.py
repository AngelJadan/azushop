"""
URL configuration for azushop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from ventas import views
from django.urls import path, include
from django.conf import settings  # new
from django.urls import path, include  # new
from django.conf.urls.static import static 
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView



urlpatterns = [
    path('openapi/', get_schema_view(
        title="School Service",
        description="API developers hpoing to use our service"
    ), name='openapi-schema'),
    path('documentation/', TemplateView.as_view(
        template_name='documentation_api.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='documentation'),
    path('admin/', admin.site.urls),
    path('register-user/', views.RegisterUsers.as_view(), name="register-user"),
    path('login/',views.Login.as_view(),name="login"),
    path('logout/',views.Logout.as_view(),name="logout"),
    path("ventas/", include('ventas.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
