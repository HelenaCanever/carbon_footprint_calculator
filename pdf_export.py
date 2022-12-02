from fpdf import FPDF
import datetime
from PIL import Image
import os

# Margin
m = 10 
# Page width: Width of A4 is 210mm
pw = 290 - 2*m 
#Cell height
ch = 80

def createpdf(data, co2_transport, co2_digital, co2_office):
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # Custom class to overwrite the header and footer methods
    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.add_font('MontserratBlack', '', 'fonts/Montserrat-Black.ttf', uni=True)
            
            self.add_font('MontserratLight', '', 'fonts/Montserrat-Light.ttf', uni=True)
        def header(self):
            self.set_font('MontserratBlack', '', 12)
            self.cell(0, 15, 'Bilan carbone', 1, 1, 'C')
        def footer(self):
            self.set_y(-15)
            self.set_font('MontserratLight', '', 10)
            self.cell(0, 8, timestamp, 1, 0, 'C')

    pdf = PDF()
    # Add a Unicode system font (using full path)

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
    pdf.set_font('MontserratBlack', '', 7)
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