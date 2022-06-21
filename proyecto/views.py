import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from home.models import Usuario
from proyecto.modelform.model_forms import OficioForm, RespuestaForm
from proyecto.models import Oficio, Subdireccione, Respuestas
from siad.settings import ITEMS_FOR_PAGE

@login_required()
def oficios_list(request, tipo_documento):
    TD = Oficio.TIPO_DOCUMENTO[0][1] if tipo_documento == 0 else Oficio.TIPO_DOCUMENTO[1][1]
    TipoDocto = tipo_documento
    Grupo = Group.objects.filter(user=request.user, name__in=['ContraMun', 'Subdirector'])
    if Grupo.count() > 0:
        subd = Subdireccione.objects.filter(titular=request.user)
        Oficios = Oficio.objects.filter(subdireccion__in=subd, tipo_documento=TipoDocto).order_by('-id').distinct()
    else:
        Grupo = Group.objects.filter(user=request.user, name__in=['Administrador', 'SysOp', 'Capturista'])
        if Grupo.count() > 0:
            # subd = Subdireccione.objects.filter(titular=request.user)
            # print(subd)
            Oficios = Oficio.objects.filter(tipo_documento=TipoDocto).order_by('-id').distinct()
            # print("DOS")
        else:
            Oficios = []

    if request.user.is_authenticated:
        user = Usuario.objects.filter(id=request.user.id).get()
        roles = Group.objects.filter(user=request.user)

        paginator = Paginator(Oficios, ITEMS_FOR_PAGE)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request,'layouts/proyectos/oficios/oficios_list.html',
                      {
                          'User': user,
                          'Roles': roles,
                          'Oficios': Oficios,
                          'New': '/oficio_new/%s' % tipo_documento,
                          'TD': TD,
                          'tipo_documento': tipo_documento,
                          'page_obj': page_obj
                      })

@login_required()
def oficio_new(request, tipo_documento):
    TD = tipo_documento

    # Verificamos que ya exista Oficios en esa Categoría
    cant = Oficio.objects.filter(tipo_documento=TD).count()
    if cant > 0:
        Ofix = Oficio.objects.filter(tipo_documento=TD).latest('consecutivo')
        cant = Ofix.consecutivo + 1
    else:
        cant = 1

    # print(cant)

    if request.method == "POST":
        frmSet = OficioForm(request.POST)
        # if cant > 0:
        #     # Obj = Oficio.objects.filter(tipo_documento=TD).latest('consecutivo').consecutivo + 1
        #     Obj = cant + 1
        # else:
        #     Obj = 1
        frmSet.set_consecutivo(cant)
        frmSet.set_tipo_documento(TD)
        if frmSet.is_valid():
            Obj = frmSet.get_consecutivo(TD)
            frmSet.set_consecutivo(Obj)
            frmSet.save()
            return redirect('/oficios_list/%s' % TD)
    else:
        frmSet = OficioForm()
        # if cant > 0:
        #     Obj = Oficio.objects.filter(tipo_documento=TD).latest('consecutivo').consecutivo + 1
        # else:
        #     Obj = 1
        frmSet.set_consecutivo(cant)
        frmSet.set_tipo_documento(TD)

    user = Usuario.objects.filter(id=request.user.id).get()
    roles = Group.objects.filter(user=request.user)
    leyenda_form = Oficio.TIPO_DOCUMENTO[0][1] if tipo_documento == 0 else Oficio.TIPO_DOCUMENTO[1][1]

    return render(request, 'layouts/proyectos/oficios/oficio_new.html', {'User': user, 'Roles': roles, 'frmSet': frmSet, 'tipo_documento': tipo_documento, 'leyenda_form': leyenda_form})



@login_required()
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


@login_required()
@csrf_exempt
def oficios_remove(request, id, tipo_documento):
    Id = id
    Doc = get_object_or_404(Oficio, pk=Id)
    if Doc:
        Doc.delete()
        # return redirect('/oficios_list/%s' % tipo_documento)
        return JsonResponse({'status': 'OK', 'message': 'Item eliminado con éxito'}, status=200)

    return JsonResponse({'status': 'Error', 'message': 'El proceso ha fallado'}, status=200)


@login_required()
def oficios_search_data_list(request):
    Search = ""
    Objs = Oficio.objects.all()
    if request.method == 'GET':

        if request.GET.get("search"):
            Search = request.GET.get("search").strip()

            # print(search)

            Objs = Objs.filter(
                Q(asunto__contains=Search) |
                Q(oficio__contains=Search) |
                Q(dir_remitente__dependencia__contains=Search) |
                Q(dir_remitente__abreviatura__contains=Search) |
                Q(dir_remitente__titular__ap_paterno__contains=Search) |
                Q(dir_remitente__titular__ap_materno__contains=Search) |
                Q(dir_remitente__titular__nombre__contains=Search)
            )

    if request.user.is_authenticated:
        user = Usuario.objects.filter(id=request.user.id).get()
        roles = Group.objects.filter(user=request.user)

        Objs = Objs.order_by('-pk')

        paginator = Paginator(Objs, ITEMS_FOR_PAGE)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        TD = Oficio.TIPO_DOCUMENTO[0][1]

        return render(request, 'layouts/proyectos/oficios/oficios_list.html',
                      {
                          'User': user,
                          'Roles': roles,
                          'Oficios': Objs,
                          'New': '/oficio_new/%s' % 0,
                          'TD': TD,
                          'tipo_documento': 0,
                          'page_obj': page_obj
                      })


# ****************************************************************************************************************
#  R  E  S  P  U  E  S  T  A  S
# ****************************************************************************************************************

@login_required()
def oficio_respuestas_list(request, oficio, tipo_documento):
    TD = Oficio.TIPO_DOCUMENTO[0][1] if tipo_documento == 0 else Oficio.TIPO_DOCUMENTO[1][1]
    Obj = get_object_or_404(Oficio, pk=oficio)

    if request.user.is_authenticated:
        user = Usuario.objects.filter(id=request.user.id).get()
        roles = Group.objects.filter(user=request.user)
        return render(request,'layouts/proyectos/oficios/respuestas/respuestas_list.html',
                      {
                          'User': user,
                          'Roles': roles,
                          'Oficio': Obj,
                          'List': '/oficio_respuestas_list/%s/%s'.format(oficio, tipo_documento),
                          'New': ('/respuesta_new/%s' % oficio),
                          'TD': TD,
                          'tipo_documento': tipo_documento
                      })







@login_required()
def respuesta_new(request, oficio):
    Obj = Oficio.objects.get(pk=oficio)
    tipo_documento = Obj.get_tipo_documento()
    TD = Oficio.TIPO_DOCUMENTO[0][1] if tipo_documento == 0 else Oficio.TIPO_DOCUMENTO[1][1]
    if request.method == "POST":
        frmSet = RespuestaForm(request.POST, request.FILES)
        if frmSet.is_valid():
            Resp = frmSet.save()
            Obj.respuestas.add(Resp)
            return redirect('/oficio_respuestas_list/{0}/{1}'.format(oficio, tipo_documento))
    else:
        frmSet = RespuestaForm()
    user = Usuario.objects.filter(id=request.user.id).get()
    roles = Group.objects.filter(user=request.user)
    return render(request, 'layouts/proyectos/oficios/respuestas/respuesta_new.html',
                  {
                      'User': user,
                      'Roles': roles,
                      'frmSet': frmSet,
                      'Oficio': Obj,
                      'TD': TD,
                      'tipo_documento': tipo_documento,
                  })



@login_required()
def respuesta_edit(request, id):
    Ofi = Oficio.objects.get(respuestas__id=id)
    TD = Ofi.TIPO_DOCUMENTO[0][1] if Ofi.tipo_documento == 0 else Ofi.TIPO_DOCUMENTO[1][1]
    Resp = get_object_or_404(Respuestas, pk=id)
    if request.method == "POST":
        frmSet = RespuestaForm(request.POST or None, request.FILES or None, instance=Resp)
        if frmSet.is_valid():
            frmSet.save()
            return redirect('/oficio_respuestas_list/{0}/{1}'.format(Ofi.id, Ofi.tipo_documento))
    else:
        frmSet = RespuestaForm(instance=Resp)
    user = Usuario.objects.filter(id=request.user.id).get()
    roles = Group.objects.filter(user=request.user)
    return render(request, 'layouts/proyectos/oficios/respuestas/respuesta_edit.html',
                  {
                      'User': user,
                      'Roles': roles,
                      'frmSet': frmSet,
                      'Oficio': Ofi,
                      'Respuesta': Resp,
                      'TD': TD,
                      'tipo_documento': Ofi.tipo_documento,
                  })




@login_required()
def respuesta_remove(request, id):
    Obj = Oficio.objects.get(respuestas__id=id)
    Respuesta = get_object_or_404(Respuestas, pk=id)
    if Respuesta:
        Respuesta.delete()
        return redirect('/oficio_respuestas_list/{0}/{1}'.format(Obj.id, Obj.tipo_documento))








# ****************************************************************************************************************
# M  O  D  U  L  O   D  E   B  Ú  S  Q  U  E  D  A
# ****************************************************************************************************************

@login_required()
def oficios_search_list(request):
    Objs = []
    msg = ""
    if request.method == 'POST':
        Objs = Oficio.objects.all()

        if request.POST.get("asunto"):
            Asunto = request.POST.get("asunto").strip()
            asunto = "ASUNTO => " + Asunto
            msg += asunto
            Objs = Objs.filter(asunto__contains=Asunto)
            # Objs = Objs.filter(Q(dir_remitente__titular__ap_paterno__contains=asunto))

        # if request.POST.get("ciudadano"):
        #     ciudadano = "Datos ciudadano => " + request.POST.get("ciudadano").strip()
        #     msg += ciudadano
        #     Objs = Objs.filter(
        #         Q(dir_remitente__titular__ap_paterno__contains=ciudadano) |
        #         Q(dir_remitente__titular__ap_materno__contains=ciudadano) |
        #         Q(dir_remitente__titular__nombre__contains=ciudadano)
        #     )

        if request.POST.get("oficio"):
            no_oficio = request.POST.get("oficio").strip()
            # msg += ", no_oficio => " if msg != "" else ("no_oficio => %s " % no_oficio)
            msg += (", " if msg != "" else "") + ("NÚMERO DE OFICIO => %s " % no_oficio)
            Objs = Objs.filter(oficio__contains=no_oficio)

        if request.POST.get("subdireccion"):
            nSubDir = request.POST.get("subdireccion").strip()
            if int(nSubDir) > 0:
                vSubDir = Subdireccione.objects.get(pk=nSubDir)
                # msg += ", subdireccion => " if msg != "" else " {0} ({1})".format(vSubDir.subdireccion, vSubDir.abreviatura)
                msg += (", " if msg != "" else "") + "SUBDIRECCIÓN => {0} ({1})".format(vSubDir.subdireccion, vSubDir.abreviatura)
                Objs = Objs.filter(subdireccion=nSubDir)

        # if request.POST.get("tipo_documento"):
        #     tipo_documento = request.POST.get("tipo_documento").strip()
        #     if int(tipo_documento) == 0 or int(tipo_documento) == 1:
        #         msg += (", tipo_documento => " if msg != "" else "") + (" %s " % tipo_documento)
        #         Objs = Objs.filter(tipo_documento=tipo_documento)

        if request.POST.get("is_rango_oficio"):
            deel = request.POST.get("del").strip()
            al = request.POST.get("al").strip()
            if int(deel) <= int(al):
                # msg += (", Rango de Fecha => " if msg != "" else "") + "{0} - {1}".format(fecha_inicial, fecha_final)
                msg += (", " if msg != "" else "") + "RANGO DE CONSECUTIVOS => {0} - {1}".format(deel, al)
                Objs = Objs.filter(consecutivo__range=(deel, al))

        if request.POST.get("is_fecha"):
            fecha_inicial = request.POST.get("fecha_inicial").strip()
            fecha_final = request.POST.get("fecha_final").strip()
            ff_inicial = fecha_inicial.split('-')
            ff_final = fecha_inicial.split('-')
            f_fecha_inicial = "{0}-{1}-{2}".format(ff_inicial[2], ff_inicial[1], ff_inicial[0])
            f_fecha_final = "{0}-{1}-{2}".format(ff_final[2], ff_final[1], ff_final[0])
            msg += (", " if msg != "" else "") + "RANGO DE FECHA => {0} - {1}".format(f_fecha_inicial, f_fecha_final)
            Objs = Objs.filter(fecha_captura__range=(fecha_inicial,fecha_final))

        Grupo = Group.objects.filter(user=request.user, name__in=['Subdirector'])
        if Grupo.count() > 0:
            subd = Subdireccione.objects.filter(titular=request.user)
            Objs = Objs.filter(subdireccion__in=subd)
            # Oficios = Oficio.objects.filter(subdireccion__in=subd).order_by('-id').distinct()


    else:
        msg = ''
    user = Usuario.objects.filter(id=request.user.id).get()
    roles = Group.objects.filter(user=request.user)
    fecha = datetime.date.today().isoformat()
    Subdirecciones = Subdireccione.objects.filter(is_visible=True);

    IdSubs = ""
    TotSubss = ""
    IdOficios = ""

    subdirecciones_list = []

    for item in Objs:
        IdOficios += ("," if (IdOficios != "") else "") + str(item.pk)
        Id = item.pk
        Ofix= get_object_or_404(Oficio, pk=Id)
        subdis = Ofix.subdireccion.all()
        for Sub in subdis:
            if len(subdirecciones_list) > 0:
                Paso = True
                for M in subdirecciones_list:
                    if M == Sub.pk:
                        Paso = False
                if Paso:
                    subdirecciones_list.append(Sub.pk)
                    IdSubs += ("," if (IdSubs != "") else "") + str(Sub.pk)
            else:
                subdirecciones_list.append(Sub.pk)
                IdSubs += ("," if (IdSubs != "") else "") + str(Sub.pk)

    print(IdOficios)
    print(IdSubs)
    # print(TotSubss)

    # print(subdirecciones_list)
    # print(IdSubs)
    # print(TotSubss)

    # print( encodings.utf_8.decode(msg) )

    return render(request, 'layouts/proyectos/oficios/oficios_search_list.html',
                  {
                      'Oficios': Objs,
                      'Items': serializers.serialize("json", Objs),
                      'User': user,
                      'Roles': roles,
                      'Subdirecciones': Subdirecciones,
                      'SubDirs': IdSubs,
                      'Mensaje':  msg,
                      'Fecha': fecha,

                  })








    # return HttpResponseRedirect(reverse('firstapp:create') + '?' + urlencode({'next': nextos }))
















