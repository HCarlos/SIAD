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

from fpdf.php import sprintf
from fpdf.py3k import basestring

from proyecto.models import Oficio, Subdireccione
from siad.settings import STATICFILES_DIRS, BASE_DIR, REPORTS_URL, REPORTS_ROOT



class PDF(FPDF):
    Oficio = Oficio()
    criterio_de_consulta = ""
    Titulo = ""
    #
    # def __init__(self, orientation='l', unit='mm', format='LETTER'):
    #
    #     print("Entró......................")
    #     # Some checks
    #     # self._dochecks()
    #     # Initialization of properties
    #     self.offsets={}                 # array of object offsets
    #     self.page=0                     # current page number
    #     self.n=2                        # current object number
    #     self.buffer=''                  # buffer holding in-memory PDF
    #     self.pages={}                   # array containing pages
    #     self.orientation_changes={}     # array indicating orientation changes
    #     self.state=0                    # current document state
    #     self.fonts={}                   # array of used fonts
    #     self.font_files={}              # array of font files
    #     self.diffs={}                   # array of encoding differences
    #     self.images={}                  # array of used images
    #     self.page_links={}              # array of links in pages
    #     self.links={}                   # array of internal links
    #     self.in_footer=0                # flag set when processing footer
    #     self.lastw=0
    #     self.lasth=0                    # height of last cell printed
    #     self.font_family=''             # current font family
    #     self.font_style=''              # current font style
    #     self.font_size_pt=12            # current font size in points
    #     self.underline=0                # underlining flag
    #     self.draw_color='0 G'
    #     self.fill_color='0 g'
    #     self.text_color='0 g'
    #     self.color_flag=0               # indicates whether fill and text colors are different
    #     self.ws=0                       # word spacing
    #     self.angle=0
    #     # Standard fonts
    #     self.core_fonts={'courier':'Courier','courierB':'Courier-Bold','courierI':'Courier-Oblique','courierBI':'Courier-BoldOblique',
    #         'helvetica':'Helvetica','helveticaB':'Helvetica-Bold','helveticaI':'Helvetica-Oblique','helveticaBI':'Helvetica-BoldOblique',
    #         'times':'Times-Roman','timesB':'Times-Bold','timesI':'Times-Italic','timesBI':'Times-BoldItalic',
    #         'symbol':'Symbol','zapfdingbats':'ZapfDingbats'}
    #     # Scale factor
    #     if(unit=='pt'):
    #         self.k=1
    #     elif(unit=='mm'):
    #         self.k=72/25.4
    #     elif(unit=='cm'):
    #         self.k=72/2.54
    #     elif(unit=='in'):
    #         self.k=72.
    #     else:
    #         self.error('Incorrect unit: '+unit)
    #     # Page format
    #     if(isinstance(format, basestring)):
    #         format=format.lower()
    #         if(format=='a3'):
    #             format=(841.89,1190.55)
    #         elif(format=='a4'):
    #             format=(595.28,841.89)
    #         elif(format=='a5'):
    #             format=(420.94,595.28)
    #         elif(format=='letter'):
    #             format=(612,792)
    #         elif(format=='legal'):
    #             format=(612,1008)
    #         else:
    #             self.error('Unknown page format: '+format)
    #         self.fw_pt=format[0]
    #         self.fh_pt=format[1]
    #     else:
    #         self.fw_pt=format[0]*self.k
    #         self.fh_pt=format[1]*self.k
    #     self.fw=self.fw_pt/self.k
    #     self.fh=self.fh_pt/self.k
    #     # Page orientation
    #     orientation=orientation.lower()
    #     if(orientation=='p' or orientation=='portrait'):
    #         self.def_orientation='P'
    #         self.w_pt=self.fw_pt
    #         self.h_pt=self.fh_pt
    #     elif(orientation=='l' or orientation=='landscape'):
    #         self.def_orientation='L'
    #         self.w_pt=self.fh_pt
    #         self.h_pt=self.fw_pt
    #     else:
    #         self.error('Incorrect orientation: '+orientation)
    #
    #     self.def_orientation = 'L'
    #     self.cur_orientation=self.def_orientation
    #     self.w=self.w_pt/self.k
    #     self.h=self.h_pt/self.k
    #     # Page margins (1 cm)
    #     margin=28.35/self.k
    #     self.set_margins(margin,margin)
    #     # Interior cell margin (1 mm)
    #     self.c_margin=margin/10.0
    #     # line width (0.2 mm)
    #     self.line_width=.567/self.k
    #     # Automatic page break
    #     self.set_auto_page_break(1,2*margin)
    #     # Full width display mode
    #     self.set_display_mode('fullwidth')
    #     # Enable compression
    #     self.set_compression(1)
    #     # Set default PDF version number
    #     self.pdf_version='1.3'
    #
    # def check_page(fn):
    #     "Decorator to protect drawing methods"
    #     @wraps(fn)
    #     def wrapper(self, *args, **kwargs):
    #         if not self.page and not kwargs.get('split_only'):
    #             self.error("No page open, you need to call add_page() first")
    #         else:
    #             return fn(self, *args, **kwargs)
    #     return wrapper
    #
    # def add_page(self, orientation='L'):
    #     "Start a new page"
    #     if(self.state==0):
    #         self.open()
    #     family=self.font_family
    #     if self.underline:
    #         style = self.font_style + 'U'
    #     else:
    #         style = self.font_style
    #     size=self.font_size_pt
    #     lw=self.line_width
    #     dc=self.draw_color
    #     fc=self.fill_color
    #     tc=self.text_color
    #     cf=self.color_flag
    #     if(self.page>0):
    #         #Page footer
    #         self.in_footer=1
    #         self.footer()
    #         self.in_footer=0
    #         #close page
    #         self._endpage()
    #     #Start new page
    #     self._beginpage(orientation)
    #     #Set line cap style to square
    #     self._out('2 J')
    #     #Set line width
    #     self.line_width=lw
    #     self._out(sprintf('%.2f w',lw*self.k))
    #     #Set font
    #     if(family):
    #         self.set_font(family,style,size)
    #     #Set colors
    #     self.draw_color=dc
    #     if(dc!='0 G'):
    #         self._out(dc)
    #     self.fill_color=fc
    #     if(fc!='0 g'):
    #         self._out(fc)
    #     self.text_color=tc
    #     self.color_flag=cf
    #     #Page header
    #     self.header()
    #     #Restore line width
    #     if(self.line_width!=lw):
    #         self.line_width=lw
    #         self._out(sprintf('%.2f w',lw*self.k))
    #     #Restore font
    #     if(family):
    #         self.set_font(family,style,size)
    #     #Restore colors
    #     if(self.draw_color!=dc):
    #         self.draw_color=dc
    #         self._out(dc)
    #     if(self.fill_color!=fc):
    #         self.fill_color=fc
    #         self._out(fc)
    #     self.text_color=tc
    #     self.color_flag=cf


    def header(self):
        self.set_y(5)
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
        pdf.set_auto_page_break(0)
        pdf.set_xy(5, 5)

        # pdf.def_orientation='l'
        pdf.criterio_de_consulta = request.POST.get('Mensaje')
        pdf.Titulo = 'REPORTE ESPECIAL DE OFICIOS'
        pdf.add_page("L")
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
                            SizeCol = 30
                            pdf.set_font('Arial', '', 8)
                            pdf.cell(20, SizeCol, "%s" % pdf.Oficio.consecutivo, 'LTB', 0, 'C')

                            x = pdf.get_x()
                            y = pdf.get_y()
                            pdf.rect(x, y, 40, SizeCol, 1)
                            pdf.multi_cell(40, 5,  "%s" % pdf.Oficio.oficio, 0, 'L')
                            pdf.set_xy(x+40, y)

                            pdf.cell(30, SizeCol, "%s" % pdf.Oficio.fecha_documento.strftime("%d-%b-%y"), 'LTB', 0,  'C')
                            pdf.cell(50, SizeCol, "%s" % pdf.Oficio.remitente, 'LTB', 0,  'L')
                            x = pdf.get_x()
                            y = pdf.get_y()
                            pdf.rect(x, y, 100, SizeCol, 1)
                            pdf.multi_cell(100, 5,  "%s" % pdf.Oficio.asunto, 0, 'L')
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


