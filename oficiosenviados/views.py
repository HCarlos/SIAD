from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from home.models import Usuario
from oficiosenviados.modelforms.oficio_enviado_form import OficioEnviadoForm
from oficiosenviados.models import OficioEnviado
from proyecto.modelform.model_forms import RespuestaForm
from proyecto.models import Subdireccione, Respuestas, Dependencia
from siad.settings import ITEMS_FOR_PAGE, URL_OFICIO_ENVIADO


@login_required()
def OficioEnviados_list(request):
    Grupo = Group.objects.filter(user=request.user, name__in=['ContraMun', 'Subdirector'])
    if Grupo.count() > 0:
        subd = Dependencia.objects.filter(titular=request.user)
        OficioEnviados = OficioEnviado.objects.filter(destinatarios__in=subd).order_by('-id').distinct()
    else:
        Grupo = Group.objects.filter(user=request.user, name__in=['Administrador', 'SysOp', 'Capturista'])
        if Grupo.count() > 0:
            OficioEnviados = OficioEnviado.objects.filter().order_by('-id').distinct()
        else:
            OficioEnviados = []

    if request.user.is_authenticated:
        user = Usuario.objects.filter(id=request.user.id).get()
        roles = Group.objects.filter(user=request.user)

        paginator = Paginator(OficioEnviados, ITEMS_FOR_PAGE)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        Is_Subdirector = Group.objects.filter(user=request.user, name__in=['Subdirector'])

        return render(request,'layouts/oficioenviado/oficios/oficiosenviados_list.html',
                      {
                          'User': user,
                          'Roles': roles,
                          'oficiosenviados': OficioEnviados,
                          'New': '/oficioenviado_new',
                          'page_obj': page_obj,
                          'is_subdirector': Is_Subdirector.count(),
                          'mod_search': URL_OFICIO_ENVIADO
                      })

@login_required()
def OficioEnviado_new(request):

    # Verificamos que ya exista OficioEnviados en esa Categoría
    cant = OficioEnviado.objects.filter().count()
    if cant > 0:
        Ofix = OficioEnviado.objects.filter().latest('consecutivo')
        cant = Ofix.consecutivo + 1
    else:
        cant = 1

    # print(cant)

    if request.method == "POST":
        frmSet = OficioEnviadoForm(request.POST, user_id=request.user.id, oficioenviado_id=0)
        frmSet.set_consecutivo(cant)
        if frmSet.is_valid():
            Obj = frmSet.get_consecutivo()
            frmSet.set_consecutivo(Obj)
            frmSet.save()
            return redirect('/oficiosenviados_list')
    else:
        frmSet = OficioEnviadoForm(user_id=request.user.id, oficioenviado_id=0)
        frmSet.set_consecutivo(cant)

    user = Usuario.objects.filter(id=request.user.id).get()
    roles = Group.objects.filter(user=request.user)

    return render(request, 'layouts/oficioenviado/oficios/oficioenviado_new.html',
                  {
                      'User': user,
                      'Roles': roles,
                      'frmSet': frmSet,
                      'mod_search': URL_OFICIO_ENVIADO
                  })



@login_required()
def OficioEnviados_edit(request, id):
    Id = id
    Doc = get_object_or_404(OficioEnviado, pk=Id)
    if request.method == 'POST':
        frmSet = OficioEnviadoForm(request.POST or None, request.FILES or None, instance=Doc, user_id=request.user.id, oficioenviado_id=Doc.id)
        if frmSet.is_valid():
            frmSet.save()
            return redirect('/oficiosenviados_list')
    else:
        frmSet = OficioEnviadoForm(instance=Doc, user_id=request.user.id, oficioenviado_id=Doc.id)
        frmSet.set_consecutivo(Doc.consecutivo)

    user = Usuario.objects.filter(id=request.user.id).get()
    roles = Group.objects.filter(user=request.user)
    return render(request, 'layouts/oficioenviado/oficios/oficioenviado_edit.html',
                  {
                      'User': user,
                      'Roles': roles,
                      'OficioEnviado': Doc,
                      'frmSet': frmSet,
                      'mod_search': URL_OFICIO_ENVIADO
                  })

# nomeselacontraseña


@login_required()
@csrf_exempt
def OficioEnviados_remove(request, id, tipo_documento):
    Id = id
    Doc = get_object_or_404(OficioEnviado, pk=Id)
    if Doc:
        Doc.delete()
        # return redirect('/OficioEnviados_list/%s' % tipo_documento)
        return JsonResponse({'status': 'OK', 'message': 'Item eliminado con éxito'}, status=200)

    return JsonResponse({'status': 'Error', 'message': 'El proceso ha fallado'}, status=200)


@login_required()
def OficiosEnviados_search_data_list(request):
    Search = ""
    Objs = OficioEnviado.objects.all()
    if request.method == 'GET':

        if request.GET.get("search"):
            Search = request.GET.get("search").strip()

            if Search.isnumeric():
                Sec = int(Search)
                Objs = Objs.filter(consecutivo=Sec)
            else:
                Objs = Objs.filter(
                    Q(asunto__contains=Search) |
                    Q(oficio__contains=Search)
                )

    if request.user.is_authenticated:
        user = Usuario.objects.filter(id=request.user.id).get()
        roles = Group.objects.filter(user=request.user)

        Objs = Objs.order_by('-pk')

        paginator = Paginator(Objs, ITEMS_FOR_PAGE)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        Is_Subdirector = Group.objects.filter(user=request.user, name__in=['Subdirector'])

        return render(request, 'layouts/oficioenviado/oficios/oficiosenviados_list.html',
                      {
                          'User': user,
                          'Roles': roles,
                          'OficioEnviados': Objs,
                          'New': '/OficioEnviado_new/%s' % 0,
                          'tipo_documento': 0,
                          'page_obj': page_obj,
                          'is_subdirector': Is_Subdirector.count(),
                          'mod_search': URL_OFICIO_ENVIADO
                      })


# ****************************************************************************************************************
#  R  E  S  P  U  E  S  T  A  S
# ****************************************************************************************************************

@login_required()
def OficioEnviado_respuestas_list(request, OficioEnviado, tipo_documento):
    Obj = get_object_or_404(OficioEnviado, pk=OficioEnviado)

    if request.user.is_authenticated:
        user = Usuario.objects.filter(id=request.user.id).get()
        roles = Group.objects.filter(user=request.user)
        return render(request,'layouts/oficioenviado/oficios/respuestas/oficioenviado_respuestas_list.html',
                      {
                          'User': user,
                          'Roles': roles,
                          'OficioEnviado': Obj,
                          'List': '/oficioenviado_respuestas_list/%s/%s'.format(OficioEnviado, tipo_documento),
                          'New': ('/respuesta_new/%s' % OficioEnviado),
                          'tipo_documento': tipo_documento,
                          'mod_search': URL_OFICIO_ENVIADO
                      })







@login_required()
def oficioenviado_respuesta_new(request, OficioEnviado):
    Obj = OficioEnviado.objects.get(pk=OficioEnviado)
    tipo_documento = Obj.get_tipo_documento()
    if request.method == "POST":
        frmSet = RespuestaForm(request.POST, request.FILES)
        if frmSet.is_valid():
            Resp = frmSet.save()
            Obj.respuestas.add(Resp)
            return redirect('/oficioenviado_respuestas_list/{0}/{1}'.format(OficioEnviado, tipo_documento))
    else:
        frmSet = RespuestaForm()
    user = Usuario.objects.filter(id=request.user.id).get()
    roles = Group.objects.filter(user=request.user)
    return render(request, 'layouts/oficioenviado/oficios/respuestas/oficioenviado_respuesta_new.html',
                  {
                      'User': user,
                      'Roles': roles,
                      'frmSet': frmSet,
                      'OficioEnviado': Obj,
                      'tipo_documento': tipo_documento,
                      'mod_search': URL_OFICIO_ENVIADO
                  })



@login_required()
def oficioenviado_respuesta_edit(request, id):
    Ofi = OficioEnviado.objects.get(respuestas__id=id)
    Resp = get_object_or_404(Respuestas, pk=id)
    if request.method == "POST":
        frmSet = RespuestaForm(request.POST or None, request.FILES or None, instance=Resp)
        if frmSet.is_valid():
            frmSet.save()
            return redirect('/oficioenviado_respuestas_list/{0}/{1}'.format(Ofi.id, Ofi.tipo_documento))
    else:
        frmSet = RespuestaForm(instance=Resp)
    user = Usuario.objects.filter(id=request.user.id).get()
    roles = Group.objects.filter(user=request.user)
    return render(request, 'layouts/oficioenviado/oficios/respuestas/oficioenviado_respuesta_edit.html',
                  {
                      'User': user,
                      'Roles': roles,
                      'frmSet': frmSet,
                      'OficioEnviado': Ofi,
                      'Respuesta': Resp,
                      'tipo_documento': Ofi.tipo_documento,
                      'mod_search': URL_OFICIO_ENVIADO
                  })




@login_required()
def oficioenviado_respuesta_remove(request, id):
    Obj = OficioEnviado.objects.get(respuestas__id=id)
    Respuesta = get_object_or_404(Respuestas, pk=id)
    if Respuesta:
        Respuesta.delete()
        return redirect('/oficioenviado_respuestas_list/{0}/{1}'.format(Obj.id, Obj.tipo_documento))




