import json
import os.path
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from fpdf import FPDF
from django.http import FileResponse

from proyecto.models import Oficio, Subdireccione
from siad.settings import BASE_DIR, REPORTS_ROOT



class PDF(FPDF):
    Oficio = Oficio()
    criterio_de_consulta = ""
    Titulo = ""

    def header(self):
        self.set_y(5)
        imageFile = os.path.join(BASE_DIR, 'static/images/logo-1.png')
        self.image(imageFile, 5, 5, 50, 15)
        # self.set_text_color(220, 50, 50)
        self.set_font('Arial', 'B', 12)
        self.cell(160, 6, "",'',1)
        self.set_x(55)
        self.cell(130, 6, self.Titulo,'',0)
        self.set_font('Arial', '', 12)
        self.cell(20, 6, ("FECHA Y HORA DE IMPRESIÓN %s" % datetime.now().strftime("%d-%m-%Y %H:%M:%S")), '', 1)
        self.ln(10)
        self.set_x(10)
        self.set_font('Arial', 'B', 10)
        self.cell(50, 9, "CRITERIOS DE BÚSQUEDA: ", '', 0)
        self.set_font('Times', '', 12)
        self.cell(150, 9, self.criterio_de_consulta, '', 1)
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
        pdf.set_auto_page_break(0)
        pdf.set_xy(5, 5)

        # pdf.def_orientation='l'
        pdf.criterio_de_consulta = request.POST.get('Mensaje')
        pdf.Titulo = 'REPORTE ESPECIAL DE OFICIOS'
        pdf.add_page("L")
        pdf.set_font('Arial', '', 12)

        items = json.loads(request.POST.get('Oficios'))
        print("Total de Registros: %s" % len(items))

        if len(items) > 0:
            pdf.set_font('Arial', 'B', 11)
            pdf.set_fill_color(128,128,128)
            pdf.set_draw_color(0, 80, 180)
            pdf.cell(20, 6, "NÚM.", 'LTB', 0, 'L', True)
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

                pdf.set_font('Arial', 'B', 14)
                pdf.set_text_color(255,255,255)
                Sub = get_object_or_404(Subdireccione, pk=Id)
                pdf.cell(280, 6, Sub.abreviatura, 'LTBR', 1, 'L', True)
                pdf.set_font('Arial', '', 11)
                pdf.set_text_color(32,32,32)
                for item in items:
                    Id = int(item['pk'])
                    pdf.Oficio = get_object_or_404(Oficio, pk=Id)
                    subdis = pdf.Oficio.subdireccion.all()
                    for dubdi in subdis:
                        if dubdi==Sub:
                            SizeCol = 40
                            pdf.set_font('Arial', '', 11)
                            pdf.cell(20, SizeCol, "%s" % pdf.Oficio.consecutivo, 'LTB', 0, 'C')

                            x = pdf.get_x()
                            y = pdf.get_y()
                            pdf.rect(x, y, 40, SizeCol, 1)
                            pdf.multi_cell(40, 5,  "%s" % pdf.Oficio.oficio, 0, 'L')
                            pdf.set_xy(x+40, y)

                            pdf.cell(30, SizeCol, "%s" % pdf.Oficio.fecha_documento.strftime("%d-%b-%y"), 'LTB', 0,  'C')

                            x = pdf.get_x()
                            y = pdf.get_y()
                            pdf.rect(x, y, 50, SizeCol, 1)
                            pdf.multi_cell(50, 5,  "%s" % pdf.Oficio.remitente, 0, 'L')
                            pdf.set_xy(x+50, y)

                            x = pdf.get_x()
                            y = pdf.get_y()
                            pdf.rect(x, y, 100, SizeCol, 1)
                            pdf.multi_cell(100, 5,  "%s" % pdf.Oficio.asunto, 0, 'J')
                            pdf.set_xy(x+100, y)

                            pdf.cell(40, SizeCol, "", 'LTRB', 1,  'C', False)

                            if pdf.get_y() > 150:
                                pdf.add_page(orientation='L')

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


