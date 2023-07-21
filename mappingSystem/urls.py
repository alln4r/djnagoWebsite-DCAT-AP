"""mappingSystem URL Configuration

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
from django.contrib.auth import views as auth_views
from .apresentacao.validador.loginForm import UserLoginForm
from .apresentacao.controladores import controller, controllerAddFields, controllerMappedAPI


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', controller.home, name="home"),
    path('addFields', controllerAddFields.add_field_view, name="addFields"),
    path('mappedAPI', controllerMappedAPI.mappedAPI_view, name="mappedAPI"),


    # Django Auth
    path('login', auth_views.LoginView.as_view(redirect_authenticated_user=True,
         template_name="login.html", authentication_form=UserLoginForm), name="login"),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),
]
