"""siad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from datetime import datetime

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path
from django.contrib.auth import views as auth_views, login
from django.template.defaulttags import url
from django.urls import path, include

from home.views import welcome, home, myloginView, Usuario, nuevo_user, perfil_user, perfil_imagen, perfil_save_imagen
from proyecto.ajax.dependencias import getDependencias
from proyecto.views import oficios_list, oficio_new, oficios_edit, oficios_remove
from siad import settings

fecha = datetime.now()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome, name='welcome'),
    path('home/', home, name='home'),
    path('login/', myloginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(
        template_name='welcome.html',
        next_page=None), name='logout'),

    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('usuario/', Usuario, name='user-list'),
    path('nuevo_usuario/', nuevo_user, name='new-user'),
    path('usuario/<pk>', Usuario, name='user-view'),

    path('perfil/', perfil_user, name='perfil'),
    path('foto/', perfil_imagen, name='foto'),
    path('perfil_save_imagen/', perfil_save_imagen, name='perfil_save_imagen'),

    path('oficios_list/', oficios_list, name='oficios_list'),
    path('oficio_new/', oficio_new, name='oficio_new'),
    path('oficio_edit/<int:id>', oficios_edit, name='oficios_edit'),
    path('oficio_remove/<int:id>', oficios_remove, name='oficios_remove'),

    path('getDependencias/', getDependencias, name='/getDependencias'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )
