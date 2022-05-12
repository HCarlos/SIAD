import json
import os.path
from datetime import datetime
from types import SimpleNamespace

from django.contrib.auth.decorators import login_required
from django.db.models.functions import Substr
from django.shortcuts import render, get_object_or_404
from fpdf import FPDF
from django.http import FileResponse
from django.http import HttpResponse
import matplotlib
import matplotlib.pyplot as plt
from django.core.serializers.json import DjangoJSONEncoder

from proyecto.models import Oficio, Subdireccione
from siad.settings import STATICFILES_DIRS, BASE_DIR, REPORTS_URL, REPORTS_ROOT

class PDF(FPDF):
    Oficio = Oficio()
    criterio_de_consulta = ""
    Titulo = ""
    # def header(self):
    #     print(STATICFILES_DIRS)
    #
    #     imageFile = os.path.join(BASE_DIR, 'static/images/logo-0.png')
    #     self.image(imageFile, 5, 5, 50, 20)
    #
    #     # Arial bold 15
    #     self.set_font('Arial', 'B', 10)
    #     # Calculate width of title and position
    #     # w = self.get_string_width(title) + 6
    #     # self.set_x((210 - w) / 2)
    #     # Colors of frame, background and text
    #     self.set_draw_color(0, 80, 180)
    #     self.set_fill_color(230, 230, 0)
    #     self.set_text_color(220, 50, 50)
    #     # Thickness of frame (1 mm)
    #     self.set_line_width(1)
    #     # Title
    #     self.cell(150, 9, title, 1, 1, 'C', 1)
    #     # self.cell(w, 9, "self.items.count()", 1, 1, 'C', 1)
    #     # Line break
    #     self.ln(10)

    def header(self):
        imageFile = os.path.join(BASE_DIR, 'static/images/logo-1.png')
        self.image(imageFile, 5, 5, 50, 15)
        # self.set_text_color(220, 50, 50)
        self.set_font('Arial', 'B', 10)
        self.set_x(55)
        self.cell(125, 9, self.Titulo,'B',0)
        self.set_font('Arial', '', 8)
        self.cell(20, 9, datetime.now().strftime("%d-%m-%Y %H:%M:%S"), '', 1)
        self.ln(5)
        self.set_x(10)
        self.set_font('Arial', 'B', 8)
        self.cell(40, 9, "CRITERIOS DE BÚSQUEDA: ", '', 0)
        self.set_font('Times', '', 7)
        self.cell(160, 9, self.criterio_de_consulta, '', 1)
        self.ln(5)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Página ' + str(self.page_no()), 0, 0, 'C')





@login_required()
def reportespecial(request):
    print("EL REQUEST ES %s " % request)
    if request.POST:
        pdf = PDF()
        pdf.def_orientation='l'
        pdf.criterio_de_consulta = request.POST.get('Mensaje')
        pdf.Titulo = 'REPORTE ESPECIAL DE OFICIOS'
        pdf.add_page()
        pdf.set_font('Arial', '', 8)

        items = json.loads(request.POST.get('Oficios'))
        print("Total de Registros: %s" % len(items))

        if len(items) > 0:
            pdf.set_font('Arial', 'B', 8)
            pdf.set_fill_color(128,128,128)
            pdf.set_draw_color(0, 80, 180)
            pdf.cell(20, 6, "CONSEC", 'LTB', 0, 'L', True)
            pdf.cell(40, 6, "OFICIO", 'LTB', 0,  'L', True)
            pdf.cell(30, 6, "FECHA OFICIO", 'LTB', 0,  'C', True)
            pdf.cell(50, 6, "REMITENTE", 'LTB', 0,  'L', True)
            pdf.cell(100, 6, "ASUNTO", 'LTB', 0,  'L', True)
            pdf.cell(40, 6, "FIRMA", 'LTBR', 1,  'C', True)
            pdf.ln(1)
            # Subs = Subdirecciones
            SubDirs = request.POST.get('SubDirs').split(',')
            print(SubDirs)
            for index, value in enumerate(SubDirs):
                Id = SubDirs[index]

                Sub = get_object_or_404(Subdireccione, pk=Id)
                pdf.cell(280, 6, Sub.abreviatura, 'LTBR', 1, 'L', True)
                for item in items:
                    Id = int(item['pk'])
                    pdf.Oficio = get_object_or_404(Oficio, pk=Id)
                    subdis = pdf.Oficio.subdireccion.all()
                    for dubdi in subdis:
                        if dubdi==Sub:
                            MaxLen = 55
                            Asunto = pdf.Oficio.asunto[0:MaxLen]
                            Asunto = Asunto if len(pdf.Oficio.asunto) <= MaxLen else "%s..." % Asunto
                            pdf.set_font('Arial', '', 8)
                            pdf.cell(20, 6, "%s" % pdf.Oficio.consecutivo, 'LTB', 0, 'L')
                            pdf.cell(40, 6, "%s" % pdf.Oficio.oficio, 'LTB', 0,  'L')
                            pdf.cell(30, 6, "%s" % pdf.Oficio.fecha_documento, 'LTB', 0,  'C')
                            pdf.cell(50, 6, "%s" % pdf.Oficio.remitente, 'LTB', 0,  'L')
                            pdf.cell(100, 6, "%s" % Asunto, 'LTB', 0,  'L')

                            # pdf.multi_cell(100, 5,  "%s" % Asunto, 1, 0)

                            pdf.cell(40, 6, "", 'LR', 1,  'C')

            pdf.cell(280, 6, "", 'T', 1,  'C')

        else:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(190, 6, "NO SE ENCONTRARON REGISTRO", '', 1)
    else:
        pdf = PDF()
        pdf.criterio_de_consulta = ""
        pdf.Titulo = 'REPORTE ESPECIAL DE OFICIOS'
        pdf.add_page()
        pdf.set_font('Arial', '', 8)
        pdf.cell(190, 6, "NO SE ENCONTRARON Datos", '', 1)

    nombre_report = os.path.join(REPORTS_ROOT, 'special_report_1.pdf')
    pdf.output( nombre_report )

    return FileResponse(open(nombre_report, 'rb'), as_attachment=True, content_type='application/pdf')


