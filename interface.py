import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
import cal_co2

import streamlit as st
import plotly.express as px 


### Config
st.set_page_config(
    page_title="Mon empreinte Talan",
    page_icon="🍃",
    layout="centered",
        menu_items={
        'Report a bug': "mailto:helena.canever@talan.com",
        'Get help': "mailto:helena.canever@talan.com",
        'About': "Développé par le Centre de Recherche et d'Innovation de Talan. Source code: https://github.com/HelenaCanever/carbon_footprint_calculator"
    }
)

### Data upload
@st.cache
def load_laptop_data():
    laptop_data = pd.read_csv("data/laptop_data.csv")
    return laptop_data

laptop_data = load_laptop_data()

def load_smartphone_data():
    smartphone_data = pd.read_csv("data/smartphone_data.csv")
    return smartphone_data

smartphone_data = load_smartphone_data()

def load_visio_data():
    visio_data = pd.read_csv("data/visio_data.csv")
    return visio_data

visio_data = load_visio_data()

def load_storage_data():
    storage_data = pd.read_csv("data/storage_emission_data.csv")
    return storage_data

storage_data = load_storage_data()

def load_cloud_data():
    cloud_data = pd.read_csv("data/providers.csv")
    return cloud_data

cloud_data = load_cloud_data()

def load_gpu_data():
    gpu_data = pd.read_csv("data/gpu.csv")
    return gpu_data

gpu_data = load_gpu_data()

### Setting personalised palette
#palette = ['#19764C', '#25B172', '#8FE8C0', '#B5EFD5', '#DAF7EA']
palette = ['#0c3d27','#19764C', '#209560','#25b172','#5ecf9c','#8fe8c0','#97eac4','#a3eccb','#DAF7EA']
pio.templates["palette"] = go.layout.Template(
    layout = {
        'title':
            {'font': {'color': '#45D896'}
            },
        'font': {'color': '#45D896'},
        'colorway': palette,
    }
)
pio.templates.default = "palette"

#logo Talan
st.image("logos/Logo-Talan_HD_baseline-blanc.png")

tab1, tab2 = st.tabs(["Calculateur", "Méthodes et sources de données"])

with tab1:
    #insert title
    st.markdown("<h1 style='text-align: center'>Calculateur d'empreinte carbone</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center'>version 0.2</h2>", unsafe_allow_html=True)

    #insert explanation
    st.markdown(""" 
    Saisissez les informations relatives à votre mission pour connaître notre estimation de son empreinte carbone.
    """)

    ###Section 1####################################################################################################
    st.markdown("<h2 style='text-align: center'>Informations générales</h2>", unsafe_allow_html=True)


    #number of collaborators
    associates = st.number_input('Combien de collaborateurs travaillent sur la mission?', min_value=1, value=1, step=1)

    #number of months
    months = st.number_input('Combien de mois dure la mission ?', min_value=1, value=1, step=1)

    #sector
    sector = st.selectbox(
        'Lequel des secteurs de Talan est concerné ?',
        ('Assurance', 'Finance', 'Énergie et Environnement', 'Secteur Public', 'Télécom', 'Transport et Logistique'),
        help='Ces informations aideront notre IA à prédire les émissions futures.')


    ###Section 2####################################################################################################
    st.markdown("<h2 style='text-align: center'>Déplacements</h2>", unsafe_allow_html=True)

    st.write("Sélectionner les moyens de déplacement utilisés :")

    ### total emissions deplacements

    col0, col00 = st.columns(2)

    b_plane = col0.checkbox('Avion')
    b_TGV = col0.checkbox('TGV')
    b_train = col0.checkbox('Train Intercity')
    b_ev = col0.checkbox('Voiture (électrique)')
    b_car = col0.checkbox('Voiture (thermique)')
    b_rer = col00.checkbox('RER ou Transilien')
    b_metro = col00.checkbox('Metro')
    b_bus = col00.checkbox('Bus')
    b_ebike = col00.checkbox('Vélo (ou trottinette) à assistance électrique')
    b_bike = col00.checkbox('Vélo ou marche')

    #emissions in gr/person/km

    em_plane = 186.25 #average emissions, does not take into account the lenght of the flight
    em_TGV = 1.73
    em_train = 5.29
    em_ev = 19.8
    em_car = 193
    em_rer = 4.1
    em_metro = 2.5
    em_bus = 103
    em_ebike = 2
    em_bike = 0

    if b_plane:
        st.subheader("✈️ Avion ")

        f_plane = st.radio(
            "Déplacements par personne:",
            ('par mois', 'totaux'), 
            key="avion")

        if f_plane == 'par mois':
            plane_monthly = True
        else:
            plane_monthly = False

        col1, col2 = st.columns(2)
        n_plane = col1.number_input('Nombre de déplacements en avion', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        km_plane = col2.number_input('Moyenne de kms par déplacement en avion', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        co2_plane = cal_co2.transport(em_plane, n_plane, km_plane, plane_monthly, associates, months)
    else:
        co2_plane = 0
    ##########

    if b_TGV:
        st.subheader("🚄 TGV ")

        f_TGV = st.radio(
            "Déplacements par personne:",
            ('par mois', 'totaux'), 
            key="TGV")

        if f_TGV == 'par mois':
            TGV_monthly = True
        else:
            TGV_monthly = False

        col3, col4 = st.columns(2)
        n_TGV = col3.number_input('Nombre de déplacements en TGV', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        km_TGV = col4.number_input('Moyenne de kms par déplacement en TGV', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        co2_TGV = cal_co2.transport(em_TGV, n_TGV, km_TGV, TGV_monthly, associates, months)
    else:
        co2_TGV = 0

    ##########

    if b_train:
        st.subheader("🚉 Train Intercity ")

        f_train = st.radio(
            "Déplacements par personne:",
            ('par mois', 'totaux'), 
            key="train")

        if f_train == 'par mois':
            train_monthly = True
        else:
            train_monthly = False

        col5, col6 = st.columns(2)
        n_train = col5.number_input('Nombre de déplacements en train', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        km_train = col6.number_input('Moyenne de kms par déplacement en train', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        co2_train = cal_co2.transport(em_train, n_train, km_train, train_monthly, associates, months )
    else:
        co2_train=0
        ##########

    if b_ev:
        st.subheader("🚗⚡ Voiture (électrique)")

        f_ev = st.radio(
            "Déplacements par personne:",
            ('par mois', 'totaux'), 
            key="ev")

        if f_ev == 'par mois':
            ev_monthly = True
        else:
            ev_monthly = False

        col7, col8 = st.columns(2)
        n_ev = col7.number_input('Nombre de déplacements en voiture électrique', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        km_ev = col8.number_input('Moyenne de kms par déplacement en voiture électrique', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        co2_ev = cal_co2.transport(em_ev, n_ev, km_ev, ev_monthly, associates, months)
    else:
        co2_ev=0

    ##########

    if b_car:
        st.subheader("🚗 Voiture (thermique) ")

        f_car = st.radio(
            "Déplacements par personne:",
            ('par mois', 'totaux'), 
            key="voiture")

        if f_car == 'par mois':
            car_monthly = True
        else:
            car_monthly = False

        col9, col10 = st.columns(2)
        n_car = col9.number_input('Nombre de déplacements en voiture', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        km_car = col10.number_input('Moyenne de kms par déplacement en voiture', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        co2_car = cal_co2.transport(em_car, n_car, km_car, car_monthly, associates, months)
    else:
        co2_car=0
    ##########

    if b_rer:
        st.subheader("🚉 RER ou Transilien")

        f_rer = st.radio(
            "Déplacements par personne:",
            ('par mois', 'totaux'), 
            key="rer")

        if f_rer == 'par mois':
            rer_monthly = True
        else:
            rer_monthly = False

        col11, col12 = st.columns(2)
        n_rer = col11.number_input('Nombre de déplacements en RER ou Transilien', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        km_rer = col12.number_input('Moyenne de kms par déplacement en RER ou Transilien', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        co2_rer = cal_co2.transport(em_rer, n_rer, km_rer, rer_monthly, associates, months)
    else:
        co2_rer = 0

        ##########
    if b_metro:
        st.subheader("🚇 Metro ")

        f_metro = st.radio(
            "Déplacements par personne:",
            ('par mois', 'totaux'), 
            key="metro")

        if f_metro == 'par mois':
            metro_monthly = True
        else:
            metro_monthly = False

        col13, col14 = st.columns(2)
        n_metro = col13.number_input('Nombre de déplacements en metro', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        km_metro = col14.number_input('Moyenne de kms par déplacement en metro', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        co2_metro = cal_co2.transport(em_metro, n_metro, km_metro, metro_monthly, associates, months)
    else:
        co2_metro=0
    ##########
    if b_bus:
        st.subheader("🚌 Bus (thermique)")

        f_bus = st.radio(
            "Déplacements par personne:",
            ('par mois', 'totaux'), 
            key="bus")

        if f_bus == 'par mois':
            bus_monthly = True
        else:
            bus_monthly = False

        col15, col16 = st.columns(2)
        n_bus = col15.number_input('Nombre de déplacements en bus', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        km_bus = col16.number_input('Moyenne de kms par déplacement en bus', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        co2_bus = cal_co2.transport(em_bus, n_bus, km_bus, bus_monthly, associates, months)
    else:
        co2_bus = 0

    ##########
    if b_ebike:
        st.subheader("Vélo (ou trottinette) à assistance électrique 🚲⚡")

        f_ebike = st.radio(
            "Déplacements par personne:",
            ('par mois', 'totaux'), 
            key="veloAE")

        if f_ebike == 'par mois':
            ebike_monthly = True
        else:
            ebike_monthly = False

        col17, col18 = st.columns(2)
        n_ebike = col17.number_input('Nombre de déplacements en vélo (ou trottinette) à assistance électrique', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        km_ebike = col18.number_input('Moyenne de kms par déplacement en vélo (ou trottinette) à assistance électrique', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        co2_ebike = cal_co2.transport(em_ebike, n_ebike, km_ebike, ebike_monthly, associates, months )
    else:
        co2_ebike = 0
    ##########

    if b_bike:
        st.subheader("Vélo ou marche 🚲 🚶‍♀️")

        f_bike = st.radio(
            "Déplacements par personne:",
            ('par mois', 'totaux'), 
            key="velo")

        if f_bike == 'par mois':
            bike_monthly = True
        else:
            bike_monthly = False

        col19, col20 = st.columns(2)
        n_bike = col19.number_input('Nombre de déplacements en vélo ou marche', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        km_bike = col20.number_input('Moyenne de kms par déplacement en vélo ou marche', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
        co2_bike = cal_co2.transport(em_bike, n_bike, km_bike, bike_monthly, associates, months )
    else:
        co2_bike = 0

    #total
    co2_transport = co2_plane+co2_TGV+co2_train+co2_ev+co2_car+co2_rer+co2_metro+co2_bus+co2_ebike+co2_bike

    ###Section 3####################################################################################################
    st.markdown("<h2 style='text-align: center'>Numérique</h2>", unsafe_allow_html=True)

    #ordinateurs
    st.subheader("💻 Ordinateurs portables")

    if 'laptops' not in st.session_state:
        st.session_state['laptops'] = []

    laptop = st.selectbox("Sélectionner un modèle",laptop_data["Model"], 
    help="Sélectionnez chaque produit autant de fois que le nombre de personnes auxquelles il a été distribué. Par exemple : si les deux collaborateurs reçoivent un Dell Latitude 5430, sélectionnez le modèle deux fois.")

    if st.button("Ajouter", key="laptop_key"):
        if laptop:
            st.session_state.laptops.append(laptop)
            
    st.write("Modèles sélectionnés: ")
    st.write(", ".join(st.session_state.laptops))

    co2_laptops = cal_co2.laptops(laptop_data, st.session_state.laptops, months)

    #smartphones
    st.subheader("📱 Smartphones ")

    if 'smartphones' not in st.session_state:
        st.session_state['smartphones'] = []

    smartphone = st.selectbox("Sélectionner un modèle",smartphone_data["Model"], 
    help="Sélectionnez chaque produit autant de fois que le nombre de personnes auxquelles il a été distribué. Par exemple : si les deux collaborateurs reçoivent un iPhone 14 Pro Max, sélectionnez le modèle deux fois.")

    if st.button("Ajouter", key="smartphone_key"):
        if smartphone:
            st.session_state.smartphones.append(smartphone)
            
    st.write("Modèles sélectionnés: ")
    st.write(", ".join(st.session_state.smartphones))

    co2_smartphones = cal_co2.smartphones(smartphone_data, st.session_state.smartphones)

    #emails
    st.subheader("📧 Emails ")

    col21, col22 = st.columns(2)
    n_emails_att = col21.number_input('Nombre de mails par semaine (avec pièce jointe)', min_value=0, value=0, step=1)
    n_emails = col22.number_input('Nombre de mails par semaine (sans pièce jointe)', min_value=0, value=0, step=1)

    co2_emails = cal_co2.emails(n_emails_att,n_emails, months)

    #visioconférences 
    st.subheader("📞 Visioconférences ")

    col23, col24 = st.columns(2)

    h_visio = col23.number_input('Heures de visioconférences par semaine', min_value=0, value=0, step=1)
    visio_software =  col24.selectbox(
        'Outil',
        visio_data["Outil"])

    camera = st.radio(
        "Caméra plutôt...",
        ('allumée', 'éteinte'))

    if camera == 'allumée':
        camera_on = True
    else:
        camera_on = False

    co2_visio = cal_co2.visio(camera_on, h_visio, visio_data, visio_software, months)

#stockage
    st.subheader("🗃️ Stockage ")

    if st.checkbox('Je souhaite prendre en compte la compensation carbone proposée par le système de cloud.', key = "stockage"):
        offset_storage = True
    else:
        offset_storage = False

    col_provider_1, col_provider_2 = st.columns(2)
    provider = col_provider_1.selectbox("Sélectionner un système de cloud",storage_data["Provider"].unique())
    zone = col_provider_2.selectbox("Sélectionner une région",storage_data.loc[storage_data["Provider"]==provider, "Region"])

    col_bytes_1, col_bytes_2 = st.columns(2)
    bytes_month = col_bytes_1.number_input("Octets générés par mois", min_value=0, max_value=None, value=0, step=1, format=None, key=None)
    tera_or_giga = col_bytes_2.radio(
        "",
        ('Teraoctets (Tb)', 'Gigaoctets (Gb)'))

    if tera_or_giga == 'Teraoctets (Tb)':
        tb_year = bytes_month*12
    else:
        tb_year = (bytes_month/1000)*12

    col_backup_1, col_backup_2 = st.columns(2)
    retention_years = col_backup_1.number_input("Période de conservation des données (en années)",min_value=0, max_value=None, value=0, step=1)
    n_backups = col_backup_2.number_input("Nombre de backups",min_value=0, max_value=None, value=0, step=1)

    pue = float(storage_data.loc[(storage_data["Provider"]==provider)&(storage_data["Region"]==zone), "p"])
    w = float(storage_data.loc[(storage_data["Provider"]==provider)&(storage_data["Region"]==zone), "w"])
    f = float(storage_data.loc[(storage_data["Provider"]==provider)&(storage_data["Region"]==zone), "CO2e (metric ton/kWh)"])
    offset_ratio = float(storage_data.loc[(storage_data["Provider"]==provider)&(storage_data["Region"]==zone), "offsetRatio"])
    co2_storage = cal_co2.storage(tb_year, n_backups, months, retention_years, w, pue, f, offset_storage, offset_ratio)

#machine learning
    st.subheader("👩‍💻 Machine learning ")

    if st.checkbox('Je souhaite prendre en compte la compensation carbone proposée par le système de cloud.', key = "ml"):
        offset_ml = True
    else:
        offset_ml = False

    col_ML_1, col_ML_2 = st.columns(2)
    provider_gpu = col_ML_1.selectbox("Sélectionner un système de cloud", cloud_data["providerName"].unique())
    zone_gpu = col_ML_2.selectbox("Sélectionner une région", cloud_data.loc[cloud_data["providerName"]==provider_gpu, "region"])
    col_ML_3, col_ML_4 = st.columns(2)
    h_gpu = col_ML_3.number_input("Heures utilisées", min_value=0, value=0, step=1 )
    gpu = col_ML_4.selectbox("Sélectionner un GPU", gpu_data["name"])

    co2_ml = cal_co2.ml(gpu_data, cloud_data, h_gpu, gpu, provider_gpu, zone_gpu, offset_ml)

    #total
    co2_digital = co2_laptops + co2_smartphones + co2_emails + co2_visio + co2_storage + co2_ml

    ###Section 4####################################################################################################
    st.markdown("<h2 style='text-align: center'>Papeterie et fournitures de bureau</h2>", unsafe_allow_html=True)

    st.subheader("🖨️ Impressions ")

    col25, col26 = st.columns(2)

    n_prints =  col25.number_input('Nombre de pages imprimées par semaine', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)

    print_type = col26.radio(
        "Impression",
        ('recto verso', 'recto'))

    if print_type == 'recto verso':
        recto_verso = True
    else:
        recto_verso = False

    co2_office = cal_co2.printing(recto_verso, n_prints)

    ###Section 5####################################################################################################
    st.markdown("<h2 style='text-align: center'>Résultats</h2>", unsafe_allow_html=True)

    #total
    co2_total = co2_transport + co2_digital + co2_office

    st.metric(label="Empreinte carbone totale", value=str(round(co2_total, 2))+" kgCO2eq")

    fig = px.pie(values=[co2_transport, co2_digital, co2_office], 
    names=["Déplacements", "Numérique", "Bureau"])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig, use_container_width=True)

    #deplacement
    st.metric(label="Déplacements", value=str(round(co2_transport, 2))+" kgCO2eq")

    fig = px.pie(values=[co2_plane, co2_TGV, co2_train, co2_ev, co2_car, co2_rer, co2_metro, co2_bus, co2_ebike], 
    names=["Avion", "TGV", "Train", "Voiture électrique", "Voiture thermique", "RER ou Transilien", "Metro", "Bus", "Vélo ou trotinette assistance électrique"])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig, use_container_width=True)


    #numerique
    st.metric(label="Numérique", value=str(round(co2_digital, 2))+" kgCO2eq")
    fig = px.pie(values=[co2_laptops, co2_smartphones, co2_emails, co2_visio, co2_storage, co2_ml], 
    names=["Ordinateurs", "Smartphones", "Mails", "Visioconférences", "Stockage", "Machine Learning"])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig, use_container_width=True)


    #bureau
    st.metric(label="Papeterie et fournitures de bureau", value=str(round(co2_office, 2))+" kgCO2eq")
    fig = px.pie(values=[co2_office], 
    names=["Impressions"])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig, use_container_width=True)

    #download data as csv
    emissions_deplacement = [co2_plane, co2_TGV, co2_train, co2_ev, co2_car, co2_rer, co2_metro, co2_bus, co2_ebike, co2_bike]

    dict_transport = {'catégorie':['Déplacements'] * len(emissions_deplacement),
            'Source':["Avion", "TGV", "Train", "Voiture électrique", "Voiture thermique", "RER ou Transilien", "Metro", "Bus", "Vélo ou trotinette assistance électrique", "Vélo ou marche"],
            'kgCO2eq':emissions_deplacement
        }
    
    results = pd.DataFrame(dict_transport)

    digital_emissions = [co2_laptops, co2_smartphones, co2_emails, co2_visio, co2_storage, co2_ml]

    dict_digital = {'catégorie':['Numérique'] * len(digital_emissions),
            'Source':["Ordinateurs", "Smartphones", "Mails", "Visioconférences", "Stockage", "Machine Learning"],
            'kgCO2eq':digital_emissions
        }
    
    results_digital = pd.DataFrame(dict_digital)
    results = pd.concat([results, results_digital], ignore_index=True)
    
    dict_office = {'catégorie':['Papeterie et fournitures de bureau'],
            'Source':["Impressions"],
            'kgCO2eq':co2_office
        }

    results_office = pd.DataFrame(dict_office)
    results = pd.concat([results, results_office], ignore_index=True)

    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(results)

    st.download_button(
        label="Télécharger le bilan en format csv",
        data=csv,
        file_name='bilan.csv',
        mime='text/csv',
    )

    st.subheader(":mailbox: Des suggestions ou des commentaires? Contactez nous!")

    contact_form = """
    <form action="https://formsubmit.co/f5f3a06dfd337deb6a1c180bf4c507d2" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Votre nom" required>
        <input type="email" name="email" placeholder="Votre email" required>
        <textarea name="message" placeholder="Votre message ici"></textarea>
        <button type="submit">Envoyer</button>
    </form>
    """

    st.markdown(contact_form, unsafe_allow_html=True)

    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("style/style.css")

with tab2:
    st.header("Méthodes et sources de données")
    st.markdown("""Conformément à la politique sur l'open source du Centre de recherche et de développement de Talan, 
    le code source du calculateur et les données utilisées pour le calcul sont disponibles 
    sur [GitHub](https://github.com/HelenaCanever/carbon_footprint_calculator). """)
    st.subheader("Déplacements")
    st.markdown("""
    - Pour calculer l'empreinte carbone des déplacements, nous nous sommes appuyés sur le service DATAGIR de l’ Agence de la Transition Ecologique (ADEME) qui offre ces données sous forme de API [Mon Impact Transport](https://api.monimpacttransport.fr/) pour quantifier les émissions des transports sur la base des kilomètres parcouru. Les émissions en grammes par personne et par kilomètre proviennent du [code source de l'API](https://github.com/datagir/monimpacttransport).
    """)
    st.subheader("Numérique")
    formula = r'$$(g \times(n+1) \times (d_1 \times d_2)) \times \frac{w}{1000} \times8760 \times \rho \times (f \times 1000) = \text{Storage CO2 Emissions}$$'

    st.markdown("""
    - Dans le calcul de l'empreinte carbone des ordinateurs portables et des smartphones, nous prenons en compte une durée de vie de 3-4 ans selon la marque. Les versions futures affineront le calcul en fonction de la durée de vie réelle considérée comme étant celle de la durée de la mission.
    - Les données relatives à l'empreinte carbone des ordinateurs portables et des smartphones ont été obtenues auprès des producteurs et sont basées sur la base de données [laptop-co2e](https://github.com/rarecoil/laptop-co2e) sur Github.
    - Ressources producteurs:
        - [Apple](https://www.apple.com/environment/)
        - [Google](https://sustainability.google/reports/)
        - [Samsung](https://www.samsung.com/latin_en/sustainability/environment/environment-data/)
        - [Dell](https://www.dell.com/en-us/dt/corporate/social-impact/advancing-sustainability/sustainable-products-and-services/product-carbon-footprints.htm#tab0=0)
        - [Microsoft](https://www.microsoft.com/en-us/download/details.aspx?id=55974)
        - [Lenovo](https://www.lenovo.com/us/en/compliance/eco-declaration/)
        - [HP](https://h20195.www2.hp.com/v2/library.aspx?doctype=95&footer=95&filter_doctype=no&filter_country=no&cc=us&lc=en&filter_oid=no&filter_prodtype=rw&prodtype=ij&showproductcompatibility=yes&showregion=yes&showreglangcol=yes&showdescription=yes3doctype-95&sortorder-popular&teasers-off&isRetired-false&isRHParentNode-false&titleCheck-false#doctype-95&product_type-ij&sortorder-popular&teasers-off&isRetired-false&isRHParentNode-false)
    
    - Pour calculer l'empreinte carbone des email nous nous sommes basés sur les estimations de l'[ADEME](https://librairie.ademe.fr/cadic/6555/guide-en-route-vers-sobriete-numerique.pdf) de 1 mail avec pièce jointe = 35 gCO2eq/unité, 1 mail sans pièce jointe 4 gCO2eq/unité
    - Pour estimer l'empreinte carbone de la vidéoconférence, nous nous sommes basés sur cet [article](https://greenspector.com/fr/impact-applications-visioconferences-2022/).
    - Pour estimer l'empreinte carbone du stockage des données, nous nous sommes basés sur les données publié sur le [site web de CCF](https://www.cloudcarbonfootprint.org/docs/methodology/#appendix-i-energy-coefficients) et sur la formule suivante: 
    """)


    formula = r'''{\scriptstyle (g \times(n+1) \times (d_1 \times d_2)) \times \frac{w}{1000} \times8760 \times \rho \times (f \times 1000) = \text{Storage CO2 Emissions} }'''
    st.latex(formula)
    legend_1 = r'''{\scriptstyle g = \text{TB per year}}'''
    legend_2 = r'''{\scriptstyle d_1 = \text{Project Duration}}'''
    legend_3 = r'''{\scriptstyle d_2 = \text{Data retention in years}}'''
    legend_4 = r'''{\scriptstyle w = \text{Power Consumption in Watts}}'''
    legend_5 = r'''{\scriptstyle rho = \text{Power Usage Effectiveness}}'''
    legend_6 = r'''{\scriptstyle f = \text{CO2 Emission Factor}}'''

    st.latex(legend_1)
    st.latex(legend_2)
    st.latex(legend_3)
    st.latex(legend_4)
    st.latex(legend_5)
    st.latex(legend_6)


    st.markdown("""
    - Pour estimer l'empreinte carbone de l'apprentissage automatique, nous nous sommes basés sur la méthodologie de [ML CO2 Impact](https://mlco2.github.io/impact/#co2eq) et leurs données publiées [ici](https://github.com/mlco2/impact).
    """)

    st.subheader("Papeterie et fournitures de bureau")
    st.markdown("""
    - Pour calculer l'empreinte carbone des empressions nous nous sommes basés sur les estimations de l'[ADEME](https://bilans-ges.ademe.fr/documentation/UPLOAD_DOC_FR/index.htm?papier__carton_et_articles_en_.htm) sur l'empreinte carbone d'une ramette papier A4
    """)
