from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q

from home.models import Usuario
from proyecto.modelform.model_forms import OficioForm, RespuestaForm
from proyecto.models import Oficio, Subdireccione
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, render

@login_required()
def oficios_list(request, tipo_documento):
    TD = Oficio.TIPO_DOCUMENTO[0][1] if tipo_documento == 0 else Oficio.TIPO_DOCUMENTO[1][1]
    TipoDocto = tipo_documento
    Grupo = Group.objects.filter(user=request.user, name__in=['Administrador','CONTRAMUN'])
    print("Num de Reg: %s = Registro: %s", Grupo.count(), Grupo)
    if Grupo.count() <= 0:
        subd = Subdireccione.objects.filter(titular=request.user)
        Oficios = Oficio.objects.filter(subdireccion__in=subd, tipo_documento=TipoDocto).order_by('-id').distinct()
    else:
        Oficios = Oficio.objects.filter(tipo_documento=TipoDocto).order_by('-id').distinct()
        # user = Usuario.objects.filter(id=request.user.id).get()
        # roles = Group.objects.filter(user=request.user)
        # fecha = datetime.now()
        # return render(request, 'home.html', {'User': user, 'Roles': roles, 'Fecha': fecha})

        # Oficios = Oficio.objects.filter(subdireccion__in=subd).order_by('-id').distinct()
    if request.user.is_authenticated:
        user = Usuario.objects.filter(id=request.user.id).get()
        roles = Group.objects.filter(user=request.user)
        return render(request,'layouts/proyectos/oficios/oficios_list.html',
                      {
                          'User': user,
                          'Roles': roles,
                          'Oficios': Oficios,
                          'New': '/oficio_new/%s' % tipo_documento,
                          'TD': TD,
                          'tipo_documento': tipo_documento
                      })

def oficio_new(request, tipo_documento):
    TD = tipo_documento
    cant = Oficio.objects.filter(tipo_documento=TD).count()
    if request.method == "POST":
        frmSet = OficioForm(request.POST)
        if cant > 0:
            Obj = Oficio.objects.filter(tipo_documento=TD).latest('consecutivo').consecutivo + 1
        else:
            Obj = 1
        frmSet.set_consecutivo(Obj)
        frmSet.set_tipo_documento(TD)
        if frmSet.is_valid():
            frmSet.save()
            return redirect('/oficios_list/%s' % TD)
    else:
        frmSet = OficioForm()
        if cant > 0:
            Obj = Oficio.objects.filter(tipo_documento=TD).latest('consecutivo').consecutivo + 1
        else:
            Obj = 1
        frmSet.set_consecutivo(Obj)
        frmSet.set_tipo_documento(TD)
    user = Usuario.objects.filter(id=request.user.id).get()
    roles = Group.objects.filter(user=request.user)
    leyenda_form = Oficio.TIPO_DOCUMENTO[0][1] if tipo_documento == 0 else Oficio.TIPO_DOCUMENTO[1][1]
    return render(request, 'layouts/proyectos/oficios/oficio_new.html', {'User': user, 'Roles': roles, 'frmSet': frmSet, 'tipo_documento': tipo_documento, 'leyenda_form': leyenda_form})

def oficios_edit(request, id, tipo_documento):
    Id = id
    Doc = get_object_or_404(Oficio, pk=Id)
    if request.method == 'POST':
        frmSet = OficioForm(request.POST or None, request.FILES or None, instance=Doc)
        if frmSet.is_valid():
            frmSet.save()
            return redirect('/oficios_list/%s' % tipo_documento)
    else:
        frmSet = OficioForm(instance=Doc)
        frmSet.set_consecutivo(Doc.consecutivo)
        frmSet.set_tipo_documento(tipo_documento)

    user = Usuario.objects.filter(id=request.user.id).get()
    roles = Group.objects.filter(user=request.user)
    leyenda_form = Oficio.TIPO_DOCUMENTO[0][1] if tipo_documento == 0 else Oficio.TIPO_DOCUMENTO[1][1]
    return render(request, 'layouts/proyectos/oficios/oficio_edit.html', {'User': user, 'Roles': roles, 'Oficio': Doc, 'frmSet': frmSet, 'tipo_documento': tipo_documento, 'leyenda_form': leyenda_form})

# nomeselacontraseña

def oficios_remove(request, id, tipo_documento):
    Id = id
    Doc = get_object_or_404(Oficio, pk=Id)
    if Doc:
        Doc.delete()
        return redirect('/oficios_list/%s' % tipo_documento)




# ****************************************************************************************************************
#  R  E  S  P  U  E  S  T  A  S
# ****************************************************************************************************************

def respuesta_new(request, oficio):
    Obj = Oficio.objects.get(pk=oficio)
    if request.method == "POST":
        frmSet = RespuestaForm(request.POST)
        if frmSet.is_valid():
            Resp = frmSet.save()
            Obj.respuestas.add(Resp)
            return redirect('/oficios_list/0')
    else:
        frmSet = RespuestaForm()
    user = Usuario.objects.filter(id=request.user.id).get()
    roles = Group.objects.filter(user=request.user)
    return render(request, 'layouts/proyectos/oficios/respuestas/respuesta_new.html', {'User': user, 'Roles': roles, 'frmSet': frmSet, 'Oficio': Obj})
