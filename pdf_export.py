import fpdf
import datetime
import os

FONTS_DIR = 'font'

# Margin
m = 10 
# Page width: Width of A4 is 210mm
pw = 290 - 2*m 
#Cell height
ch = 80

def createpdf(data, report):
    #get timestamps
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #get emissions
    co2_transport = (report["transportation"]["plane"]["emissions"]+
    report["transportation"]["tgv"]["emissions"]+
    report["transportation"]["ev"]["emissions"]+
    report["transportation"]["car"]["emissions"]+
    report["transportation"]["rer"]["emissions"]+
    report["transportation"]["metro"]["emissions"]+
    report["transportation"]["bus"]["emissions"]+
    report["transportation"]["ebike"]["emissions"]+
    report["transportation"]["bike"]["emissions"])

    co2_digital = (
    report["digital"]["laptops"]["emissions"]+
    report["digital"]["smartphones"]["emissions"]+
    report["digital"]["emails"]["emissions"]+
    report["digital"]["videoconference"]["emissions"]+
    report["digital"]["storage"]["emissions"]+
    report["digital"]["machine learning"]["emissions"]
    )
    
    co2_office = report["printing"]["emissions"]

    # Custom class to overwrite the header and footer methods
    class PDF(fpdf.FPDF):
        def __init__(self):
            super().__init__()
            fpdf.set_global("SYSTEM_TTFONTS", os.path.join(os.path.dirname(''),FONTS_DIR))
            self.add_font('MontserratBlack', style="", fname=os.path.abspath(r"fonts/" + "Montserrat-Black.ttf"), uni=True)
            self.add_font('MontserratLight', style="", fname=os.path.abspath(r"fonts/" + "Montserrat-Light.ttf"), uni=True)
        def header(self):
            self.set_font('MontserratBlack', '', 12)
            self.cell(0, 15, 'Bilan carbone', 1, 1, 'C')
        def footer(self):
            self.set_y(-15)
            self.set_font('MontserratLight', '', 10)
            self.cell(0, 8, timestamp, 1, 0, 'C')

    pdf = PDF()
    # Add a Unicode system font (using full path)
    # first page
    pdf.add_page(orientation='L')
    pdf.ln(5)
    pdf.set_font('MontserratLight', '', 9)
    height=5
    width=50
    pdf.cell(w=width, h=height, txt='Nombre de collaborateurs:', ln=0, align='L') 
    pdf.cell(w=width, h=height, txt=str(report['associates']), ln=1, align='L') 
    pdf.cell(w=width, h=height, txt='Durée de la mission:', ln=0, align='L')
    pdf.cell(w=width, h=height, txt=str(report['duration'])+" mois", ln=1, align='L') 
    pdf.cell(w=width, h=height, txt='Secteur:', ln=0, align='L')
    pdf.cell(w=width, h=height, txt=report['sector'], ln=1, align='L')

    pdf.ln(5)
    #pdf.cell(w=width, h=height, txt="Déplacements:", ln=1, align='L')

    pdf.ln(5)
    #pdf.cell(w=width, h=height, txt="Numerique:", ln=1, align='L')

    pdf.ln(5)
    #pdf.cell(w=width, h=height, txt="Déplacements:", ln=1, align='L')

    #second page
    pdf.add_page(orientation='L')

    #spacer
    pdf.ln(5)

    #table parameters    
    table_w = 25
    tabel_h = 4
    # Table Header
    pdf.set_font('MontserratBlack', '', 7)
    pdf.cell(w=5, h=tabel_h, border=0, ln=0, align='C')
    pdf.cell(w=table_w, h=tabel_h, txt='Catégorie', border=1, ln=0, align='C')                
    pdf.cell(w=table_w+35, h=tabel_h, txt='Source', border=1, ln=0, align='C')
    pdf.cell(w=table_w, h=tabel_h, txt='kgCO2eq', border=1, ln=0, align='C')

    #get totals
    pdf.cell(w=10, ln=0)
    pdf.cell(w=0, h=4, txt="Total: "+str(round((co2_transport+co2_digital+co2_office),2))+" kgCO2eq", border=0, ln=1, align='L')

    # Table contents
    pdf.set_font('MontserratLight', '', 8)
    for i in range(0, len(data)):
        pdf.cell(w=5, h=tabel_h, border=0, ln=0, align='C')
        pdf.cell(w=table_w, h=tabel_h, 
                txt=data['Catégorie'].iloc[i], 
                border=1, ln=0, align='L')
        pdf.cell(w=table_w+35, h=tabel_h, 
                txt=data['Source'].iloc[i], 
                border=1, ln=0, align='L')
        pdf.cell(w=table_w, h=tabel_h, 
                txt=data['kgCO₂eq'].iloc[i].astype(str), 
                border=1, ln=1, align='R')


    pdf.ln(10)
    pdf.cell(w=5, ln=0)
    pdf.set_font('MontserratBlack', '', 8)
    pdf.cell(w=100, h=5, txt="Déplacements: "+str(round(co2_transport,2))+" kgCO2eq", ln=0, align='L')                
    pdf.cell(w=90, h=5, txt="Numérique: "+str(round(co2_digital, 2))+" kgCO2eq", ln=0, align='L')
    pdf.cell(w=95, h=5, txt="Papeterie: "+str(round(co2_office, 2))+" kgCO2eq", ln=1, align='L')
    pdf.cell(co2_transport)
    
    if os.path.exists("tmp/total_graph.png") and (co2_transport+co2_digital+co2_office) !=0:
        pdf.image("tmp/total_graph.png", x = 130, y = 30, w = 100, type='PNG')
    if os.path.exists("tmp/trasport_graph.png")  and co2_transport !=0:
        pdf.image('tmp/trasport_graph.png', x = 4, y = 120, w = 110, type='PNG')
    if os.path.exists("tmp/digital_graph.png") and co2_digital !=0:
        pdf.image('tmp/digital_graph.png', x = 90, y = 125, w = 100, type='PNG')
    if os.path.exists("tmp/office_graph.png") and co2_office !=0:
        pdf.image('tmp/office_graph.png', x = 180, y = 125, w = 100, type='PNG')

    return pdf.output(f'./tmp/bilan.pdf', 'F')
