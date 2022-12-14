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
            self.ln(5)
        def footer(self):
            self.set_y(-15)
            self.set_font('MontserratLight', '', 10)
            self.cell(0, 8, timestamp, 1, 0, 'C')

    pdf = PDF()

    # first page
    pdf.add_page(orientation='L')

    height=5
    width=50
    pdf.set_font('MontserratBlack', '', 9)
    pdf.cell(w=width, h=height, txt="G??n??ral", ln=1, align='L') 

    pdf.set_font('MontserratLight', '', 9)
    pdf.cell(w=width, h=height, txt='   Nombre de collaborateurs: '+str(report['associates']), ln=1, align='L') 
    pdf.cell(w=width, h=height, txt='   Dur??e de la mission: '+str(report['duration'])+" mois", ln=1, align='L')
    pdf.cell(w=width, h=height, txt='   Secteur: '+report['sector'], ln=1, align='L')

    pdf.ln(5)
    if co2_transport !=0:
        pdf.set_font('MontserratBlack', '', 9)
        pdf.cell(w=width, h=height, txt="D??placements:", ln=1, align='L')

        for i in report["transportation"]:
            pdf.set_font('MontserratLight', '', 9)
            if report["transportation"][i]["emissions"]!=0:
                pdf.cell(w=width, h=height, txt="   "+report["transportation"][i]["fr_name"]+":", ln=1, align='L')
                if report["transportation"][i]["monthly"]:
                    pdf.cell(w=width, h=height, txt="       Nombre de d??placements:", ln=0, align='L')
                    pdf.cell(w=width, h=height, txt="           "+str(report["transportation"][i]["trips"])+" par mois", ln=1, align='L')
                    pdf.cell(w=width, h=height, txt="       Distance:", ln=1, align='L')
                    pdf.cell(w=width, h=height, txt="           "+str(report["transportation"][i]["kms"]*report["transportation"][i]["trips"])+" kilom??tres par mois", ln=1, align='L')
                    pdf.cell(w=width, h=height, txt="           "+str(report["transportation"][i]["kms"]*report["transportation"][i]["trips"]*report["duration"])+ " kilom??tres au total", ln=1, align='L')
                else:
                    pdf.cell(w=width, h=height, txt="       Nombre de d??placements:", ln=0, align='L')
                    pdf.cell(w=width, h=height, txt="           "+str(report["transportation"][i]["trips"])+" au total", ln=1, align='L')
                    pdf.cell(w=width, h=height, txt="       Distance:", ln=1, align='L')
                    pdf.cell(w=width, h=height, txt="           "+str(report["transportation"][i]["kms"]*report["transportation"][i]["trips"])+" kilom??tres au total", ln=1, align='L')
    
    pdf.ln(5)
    if co2_digital !=0:
        pdf.set_font('MontserratBlack', '', 9)
        pdf.cell(w=width, h=height, txt="Num??rique:", ln=1, align='L')

        for i in report["digital"]:
            pdf.set_font('MontserratLight', '', 9)
            if report["digital"][i]["emissions"]!=0:
                if i == "laptops":
                    pdf.cell(w=width, h=height, txt="   Ordinateurs portables: "+", ".join(report["digital"][i]["models"]), ln=1, align='L')
 
                if i == "smartphones":
                    pdf.cell(w=width, h=height, txt="   Smartphones: "+", ".join(report["digital"][i]["models"]), ln=1, align='L')

                if i == "emails":
                    pdf.cell(w=width, h=height, txt="   Emails envoy??s par semaine:", ln=1, align='L')
                    pdf.cell(w=width, h=height, txt="       Sans pi??ce jointe: "+str(report["digital"][i]["without attachment"]), ln=1, align='L')
                    pdf.cell(w=width, h=height, txt="       Avec pi??ce jointe: "+str(report["digital"][i]["with attachment"]), ln=1, align='L')

                if i == "videoconference":
                    pdf.cell(w=width, h=height, txt="   Visioconf??rences", ln=1, align='L')
                    pdf.cell(w=width, h=height, txt="       Heures de visioconf??rences par semaine: "+str(report["digital"][i]["hours per week"]), ln=1, align='L')
                    pdf.cell(w=width, h=height, txt="       Logiciel: "+str(report["digital"][i]["software"]), ln=1, align='L')
                    if report["digital"][i]["camera on"]:
                        pdf.cell(w=width, h=height, txt="     Camera allum??e: Oui", ln=1, align='L')
                    else:
                        pdf.cell(w=width, h=height, txt="     Camera allum??e: Non", ln=1, align='L')

                if i == "storage":
                    pdf.cell(w=width, h=height, txt="   Stockage", ln=1, align='L')
                    if report["digital"][i]["compensated"]:
                        pdf.cell(w=width, h=height, txt="       Prise en compte des compensations carbone : Oui", ln=1, align='L')
                    else:
                        pdf.cell(w=width, h=height, txt="       Prise en compte des compensations carbone : Non", ln=1, align='L')
                    
                    pdf.cell(w=width, h=height, txt="       Syst??me de cloud: " + report["digital"][i]["service"], ln=1, align='L')
                    pdf.cell(w=width, h=height, txt="       R??gion: " +report["digital"][i]["region"], ln=1, align='L')
                    pdf.cell(w=width, h=height, txt="       Donn??es g??n??r??es par mois :"+str(report["digital"][i]["bytes"])+" "+report["digital"][i]["tera or giga"], ln=1, align='L')
                    pdf.cell(w=width, h=height, txt="       Ann??es de conservation des donn??es: "+str(report["digital"][i]["retention years"]), ln=1, align='L')  
                    pdf.cell(w=width, h=height, txt="       Nombre de backups: "+str(report["digital"][i]["backups"]), ln=1, align='L')  

                if i == "machine learning":
                    pdf.cell(w=width, h=height, txt="   Machine Learning", ln=1, align='L')
                    if report["digital"][i]["compensated"]:
                        pdf.cell(w=width, h=height, txt="       Prise en compte des compensations carbone : Oui", ln=1, align='L')
                    else:
                        pdf.cell(w=width, h=height, txt="       Prise en compte des compensations carbone : Non", ln=1, align='L')

                    pdf.cell(w=width, h=height, txt="       Syst??me de cloud: " + report["digital"][i]["service"], ln=1, align='L')  
                    pdf.cell(w=width, h=height, txt="       R??gion: " +report["digital"][i]["region"], ln=1, align='L')
                    pdf.cell(w=width, h=height, txt="       Heures utilis??es: "+str(report["digital"][i]["hours"]), ln=1, align='L')
                    pdf.cell(w=width, h=height, txt="       GPU utilis??: "+report["digital"][i]["GPU"], ln=1, align='L')

    pdf.ln(5)
    if co2_office !=0:
        pdf.set_font('MontserratBlack', '', 9)
        pdf.cell(w=width, h=height, txt="Papeterie:", ln=1, align='L')
        pdf.set_font('MontserratLight', '', 9)
        pdf.cell(w=width, h=height, txt="   Impressions: ", ln=1, align='L')
        if report["printing"]["rectoverso"]:
            pdf.cell(w=width, h=height, txt="       "+str(report["printing"]["pages"])+" pages rectoverso", ln=1, align='L')
        else:
            pdf.cell(w=width, h=height, txt="       "+str(report["printing"]["pages"])+" pages en face unique", ln=1, align='L')
            print()

    #second page
    pdf.add_page(orientation='L')

    #table parameters    
    table_w = 25
    tabel_h = 4
    # Table Header
    pdf.set_font('MontserratBlack', '', 7)
    pdf.cell(w=5, h=tabel_h, border=0, ln=0, align='C')
    pdf.cell(w=table_w, h=tabel_h, txt='Cat??gorie', border=1, ln=0, align='C')                
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
                txt=data['Cat??gorie'].iloc[i], 
                border=1, ln=0, align='L')
        pdf.cell(w=table_w+35, h=tabel_h, 
                txt=data['Source'].iloc[i], 
                border=1, ln=0, align='L')
        pdf.cell(w=table_w, h=tabel_h, 
                txt=data['kgCO???eq'].iloc[i].astype(str), 
                border=1, ln=1, align='R')


    pdf.ln(10)
    pdf.cell(w=5, ln=0)
    pdf.set_font('MontserratBlack', '', 8)
    pdf.cell(w=100, h=5, txt="D??placements: "+str(round(co2_transport,2))+" kgCO2eq", ln=0, align='L')                
    pdf.cell(w=90, h=5, txt="Num??rique: "+str(round(co2_digital, 2))+" kgCO2eq", ln=0, align='L')
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
