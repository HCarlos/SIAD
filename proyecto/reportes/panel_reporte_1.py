import json
import os.path
from datetime import datetime
from types import SimpleNamespace

from django.shortcuts import render, get_object_or_404
from fpdf import FPDF
from django.http import FileResponse
from django.http import HttpResponse
import matplotlib
import matplotlib.pyplot as plt
from django.core.serializers.json import DjangoJSONEncoder

from proyecto.models import Oficio
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





def reportespecial(request):
    print("EL REQUEST ES %s " % request)
    if request.POST:
        pdf = PDF()
        pdf.criterio_de_consulta = request.POST.get('Mensaje')
        pdf.Titulo = 'REPORTE ESPECIAL DE OFICIOS'
        pdf.add_page()
        pdf.set_font('Arial', '', 8)

        items = json.loads(request.POST.get('Oficios'))
        print("Total de Registros: %s" % len(items))

        if len(items) > 0:
            pdf.set_font('Arial', 'B', 8)
            pdf.cell(50, 6, "OFICIO", 'LTB', 0)
            pdf.cell(10, 6, "No.", 'LTB', 0)
            pdf.cell(130, 6, "ASUNTO", 'LTBR', 1)

            for item in items:
                Id = int(item['pk'])
                pdf.set_font('Arial', '', 8)
                pdf.Oficio = get_object_or_404(Oficio, pk=Id)
                pdf.cell(50, 6, "%s" % pdf.Oficio.oficio, 'LB', 0)
                pdf.cell(10, 6, "%s" % pdf.Oficio.consecutivo, 'LB', 0)
                pdf.cell(130, 6, pdf.Oficio.asunto, 'LBR', 1)
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


