from datetime import datetime

from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, render
from django.template import RequestContext

from home.models import Usuario
from siad.functions import UserFormBasic, UserFormFoto


def welcome(request):
    return render(request,'welcome.html')

def home(request):
    if request.user.is_authenticated:
        user = Usuario.objects.filter(id=request.user.id).get()
        roles = Group.objects.filter(user=request.user)
        fecha = datetime.now()
        return render(request, 'home.html', {'User': user, 'Roles': roles, 'Fecha': fecha})

class myloginView(views.LoginView):
    fecha = datetime.now()
    template_name='registration/login.html'
    extra_context = {'Fecha': fecha}

# ************************************************************************
# Profile CONTROLLER
# ************************************************************************

def perfil_user(request):
    if request.user.is_authenticated:
        user = Usuario.objects.filter(id=request.user.id).get()
        roles = Group.objects.filter(user=request.user)
        return render(request,'layouts/partials/otros/menu/perfil.html', {'User': user, 'Roles': roles})

@login_required
def perfil_imagen(request):
    Id =request.user.id
    if request.user.is_authenticated & Id > 0:
        usuario = get_object_or_404(Usuario, pk=request.user.id)
        frmNewUser = UserFormFoto(instance=usuario)
        if usuario.id > 0:
            roles = Group.objects.filter(user=Id)
            return render(request, 'layouts/partials/otros/menu/foto.html', {'User': usuario, 'Roles': roles, 'formUser': frmNewUser})

@login_required
def perfil_save_imagen(request):
    Id =request.user.id
    if request.user.is_authenticated & Id > 0:
        usuario = get_object_or_404(Usuario, pk=Id)
        print(usuario)
        if request.method == "POST":
            frmNewUser = UserFormFoto(request.POST or None, request.FILES or None, instance=usuario)
            if frmNewUser.is_valid():
                try:
                    result = frmNewUser.save()
                    return redirect('foto')
                except Exception as e:
                    raise e
            else:
                return redirect('foto')
        else:
            return redirect('foto')

# ************************************************************************
# UserS CONTROLLER
# ************************************************************************

# Listado de Users
def user(request):
    Users = Usuario.objects.all()
    return render(request, "User/Users_list.html", context={
        "files": Users,
    })


# Agregando nuevo usurio

def nuevo_user(request):
    if request.method == "POST":
        frmNewUser = UserFormBasic(request.POST)
        if frmNewUser.is_valid():
            frmNewUser.save()
            Users = Usuario.objects.all()
            print(Users)
            return redirect('user-list')
    else:
        frmNewUser = UserFormBasic()

    print(frmNewUser)
    return render(request, "User/User_new.html", context={
        'formUser': frmNewUser
    })

