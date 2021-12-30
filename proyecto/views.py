from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from home.models import Usuario
from proyecto.modelform.model_forms import OficioForm
from proyecto.models import Oficio
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, render

@login_required()
def oficios_list(request):
    Oficios = Oficio.objects.all()
    if request.user.is_authenticated:
        user = Usuario.objects.filter(id=request.user.id).get()
        roles = Group.objects.filter(user=request.user)
        return render(request,'layouts/proyectos/oficios/oficios_list.html', {'User': user, 'Roles': roles, 'Oficios': Oficios, 'New': '/oficio_new'})

def oficio_new(request):
    if request.method == "POST":
        frmSet = OficioForm(request.POST)
        if frmSet.is_valid():
            frmSet.save()
            return redirect('oficios_list')
    else:
        frmSet = OficioForm()
    user = Usuario.objects.filter(id=request.user.id).get()
    roles = Group.objects.filter(user=request.user)
    return render(request, 'layouts/proyectos/oficios/oficio_new.html', {'User': user, 'Roles': roles, 'frmSet': frmSet})

def oficios_edit(request, id):
    Id = id
    Doc = get_object_or_404(Oficio, pk=Id)
    if request.method == 'POST':
        frmSet = OficioForm(request.POST or None, request.FILES or None, instance=Doc)
        if frmSet.is_valid():
            frmSet.save()
            return redirect('oficios_list')
    else:
        frmSet = OficioForm(instance=Doc)

    user = Usuario.objects.filter(id=request.user.id).get()
    roles = Group.objects.filter(user=request.user)
    return render(request, 'layouts/proyectos/oficios/oficio_edit.html', {'User': user, 'Roles': roles, 'Oficio': Doc, 'frmSet': frmSet})


def oficios_remove(request, id):
    Id = id
    Doc = get_object_or_404(Oficio, pk=Id)
    if Doc:
        Doc.delete()
        return redirect('oficios_list')
