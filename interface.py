import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go

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
    laptop_data = pd.read_csv("laptop_data.csv")
    return laptop_data

laptop_data = load_laptop_data()

def load_smartphone_data():
    smartphone_data = pd.read_csv("smartphone_data.csv")
    return smartphone_data

smartphone_data = load_smartphone_data()

def load_visio_data():
    visio_data = pd.read_csv("visio_data.csv")
    return visio_data

visio_data = load_visio_data()



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

#insert title
st.markdown("<h1 style='text-align: center'>Calculateur d'empreinte carbone</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center'>version 0.0</h2>", unsafe_allow_html=True)

#insert explanation
st.markdown(""" 
Saisissez les informations relatives à votre mission pour connaître notre estimation de son empreinte carbone.
""")

###Section 1####################################################################################################
st.markdown("<h2 style='text-align: center'>Informations générales</h2>", unsafe_allow_html=True)


#number of collaborators
collaborateurs = st.number_input('Combien de collaborateurs travaillent sur la mission?', min_value=1, max_value=None, value=1, step=1, format=None, key=None,)

#number of months
mois = st.number_input('Combien de mois dure la mission ?', min_value=1, max_value=None, value=1, step=1, format=None, key=None,)

#sector
secteur = st.selectbox(
    'Lequel des secteurs de Talan est concerné ?',
    ('Assurance', 'Finance', 'Énergie et Environnement', 'Secteur Public', 'Télécom', 'Transport et Logistique'),
    help='Ces informations aideront notre IA à prédire les émissions futures.')


###Section 2####################################################################################################
st.markdown("<h2 style='text-align: center'>Déplacements</h2>", unsafe_allow_html=True)

st.subheader("Avion ✈️")

f_avion = st.radio(
    "Déplacements:",
    ('par mois', 'totals'), 
    key="avion")

if f_avion == 'par mois':
    mois_avion = True
else:
    mois_avion = False

col1, col2 = st.columns(2)
n_avion = col1.number_input('Nombre de déplacements en avion', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
km_avion = col2.number_input('Moyenne de kms par déplacement en avion', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)

##########
st.subheader("TGV 🚄")

f_TGV = st.radio(
    "Déplacements:",
    ('par mois', 'totals'), 
    key="TGV")

if f_TGV == 'par mois':
    mois_TGV = True
else:
    mois_TGV = False

col3, col4 = st.columns(2)
n_TGV = col3.number_input('Nombre de déplacements en TGV', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
km_TGV = col4.number_input('Moyenne de kms par déplacement en TGV', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)

##########

st.subheader("Train Intercity 🚉")

f_train = st.radio(
    "Déplacements:",
    ('par mois', 'totals'), 
    key="train")

if f_train == 'par mois':
    mois_train = True
else:
    mois_train = False

col5, col6 = st.columns(2)
n_train = col5.number_input('Nombre de déplacements en train', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
km_train = col6.number_input('Moyenne de kms par déplacement en train', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)

##########

st.subheader("Voiture (électrique) 🚗⚡")

f_ev = st.radio(
    "Déplacements:",
    ('par mois', 'totals'), 
    key="ev")

if f_ev == 'par mois':
    mois_ev = True
else:
    mois_ev = False

col7, col8 = st.columns(2)
n_ev = col7.number_input('Nombre de déplacements en voiture électrique', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
km_ev = col8.number_input('Moyenne de kms par déplacement en voiture électrique', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)

##########

st.subheader("Voiture (thermique) 🚗")

f_voiture = st.radio(
    "Déplacements:",
    ('par mois', 'totals'), 
    key="voiture")

if f_voiture == 'par mois':
    mois_voiture = True
else:
    mois_voiture = False

col9, col10 = st.columns(2)
n_voiture = col9.number_input('Nombre de déplacements en voiture', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
km_voiture = col10.number_input('Moyenne de kms par déplacement en voiture', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)

##########

st.subheader("RER ou Transilien 🚉")

f_rer = st.radio(
    "Déplacements:",
    ('par mois', 'totals'), 
    key="rer")

if f_rer == 'par mois':
    mois_rer = True
else:
    mois_rer = False

col11, col12 = st.columns(2)
n_rer = col11.number_input('Nombre de déplacements en RER ou Transilien', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
km_rer = col12.number_input('Moyenne de kms par déplacement en RER ou Transilien', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)

##########

st.subheader("Metro 🚇")

f_metro = st.radio(
    "Déplacements:",
    ('par mois', 'totals'), 
    key="metro")

if f_metro == 'par mois':
    mois_metro = True
else:
    mois_metro = False

col13, col14 = st.columns(2)
n_metro = col13.number_input('Nombre de déplacements en metro', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
km_metro = col14.number_input('Moyenne de kms par déplacement en metro', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)

##########

st.subheader("Bus (thermique) 🚌")

f_bus = st.radio(
    "Déplacements:",
    ('par mois', 'totals'), 
    key="bus")

if f_bus == 'par mois':
    mois_bus = True
else:
    mois_bus = False

col15, col16 = st.columns(2)
n_bus = col15.number_input('Nombre de déplacements en bus', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
km_bus = col16.number_input('Moyenne de kms par déplacement en bus', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)

##########

st.subheader("Vélo (ou trottinette) à assistance électrique 🚲⚡")

f_veloAE = st.radio(
    "Déplacements:",
    ('par mois', 'totals'), 
    key="veloAE")

if f_veloAE == 'par mois':
    mois_veloAE = True
else:
    mois_veloAE = False

col17, col18 = st.columns(2)
n_veloAE = col17.number_input('Nombre de déplacements en vélo (ou trottinette) à assistance électrique', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
km_veloAE = col18.number_input('Moyenne de kms par déplacement en vélo (ou trottinette) à assistance électrique', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)

##########

st.subheader("Vélo ou marche 🚲 🚶‍♀️")

f_velo = st.radio(
    "Déplacements:",
    ('par mois', 'totals'), 
    key="velo")

if f_velo == 'par mois':
    mois_velo = True
else:
    mois_velo = False

col19, col20 = st.columns(2)
n_velo = col19.number_input('Nombre de déplacements en vélo ou marche', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
km_velo = col20.number_input('Moyenne de kms par déplacement en vélo ou marche', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)

### total emissions deplacements
#emissions in gr/person/km

em_avion = 186.25 #average emissions
em_TGV = 1.73
em_train = 5.29
em_ev = 19.8
em_voiture = 193
em_rer = 4.1
em_metro = 2.5
em_bus = 103
em_veloAE = 2
em_velo = 0

def cal_co2_transport(em, n, km, f_transport):
	if f_transport:
		co2 = (em*n*km*collaborateurs*mois)/1000
		return co2 
	else: 
		co2 = (em*n*km*collaborateurs)/1000
		return co2 

co2_avion = cal_co2_transport(em_avion, n_avion, km_avion, f_avion)
co2_TGV = cal_co2_transport(em_TGV, n_TGV, km_TGV, f_TGV)
co2_train = cal_co2_transport(em_train, n_train, km_train, f_train)
co2_ev = cal_co2_transport(em_ev, n_ev, km_ev, f_ev)
co2_voiture = cal_co2_transport(em_voiture, n_voiture, km_voiture, f_voiture)
co2_rer = cal_co2_transport(em_rer, n_rer, km_rer, f_rer)
co2_metro = cal_co2_transport(em_metro, n_metro, km_metro, f_metro)
co2_bus = cal_co2_transport(em_bus, n_bus, km_bus, f_bus)
co2_veloAE = cal_co2_transport(em_veloAE, n_veloAE, km_veloAE, f_veloAE)
co2_velo = cal_co2_transport(em_velo, n_velo, km_velo, f_velo)

co2_deplacements = co2_avion+co2_TGV+co2_train+co2_ev+co2_voiture+co2_rer+co2_metro+co2_bus+co2_veloAE+co2_velo

###Section 3####################################################################################################
st.markdown("<h2 style='text-align: center'>Numérique</h2>", unsafe_allow_html=True)

#ordinateurs
st.subheader("Ordinateurs portables 💻")

if 'portables' not in st.session_state:
    st.session_state['portables'] = []

laptop = st.selectbox("Sélectionner un modèle",laptop_data["Model"])

if st.button("Ajouter", key="laptop_key"):
    if laptop:
        st.session_state.portables.append(laptop)
        
st.write("Modèles sélectionnés: ")
st.write(", ".join(st.session_state.portables))

def cal_co2_portables():
    em_portables = 0
    for ordi in st.session_state.portables:
        em_portables += float(laptop_data.loc[laptop_data["Model"]==ordi, "kg CO2e"])
    return em_portables

co2_portables = cal_co2_portables()




#smartphones
st.subheader("Smartphones 📱")

if 'smartphones' not in st.session_state:
    st.session_state['smartphones'] = []

smartphone = st.selectbox("Sélectionner un modèle",smartphone_data["Model"])

if st.button("Ajouter", key="smartphone_key"):
    if smartphone:
        st.session_state.smartphones.append(smartphone)
        
st.write("Modèles sélectionnés: ")
st.write(", ".join(st.session_state.smartphones))

def cal_co2_smartphones():
    em_smartphones = 0
    for phone in st.session_state.smartphones:
        em_smartphones += float(smartphone_data.loc[smartphone_data["Model"]==phone, "kg CO2e"])
    return em_smartphones

co2_smartphones = cal_co2_smartphones()


#emails
st.subheader("Emails 📧")

col21, col22 = st.columns(2)
n_mails_pj = col21.number_input('Nombre de mails par semaine (avec pièce jointe)', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
n_mails = col22.number_input('Nombre de mails par semaine (sans pièce jointe)', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)

def cal_co2_mails():
    em_mails = ((n_mails_pj*4*mois*35)+(n_mails*4*mois*4))/1000
    return em_mails

co2_emails = cal_co2_mails()

#visioconférences 
st.subheader("Visioconférences 📞")

col23, col24 = st.columns(2)

h_visio = col23.number_input('Heures de visioconférences par semaine', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)
outil_visio =  col24.selectbox(
    'Outil',
    visio_data["Outil"])

camera = st.radio(
    "Caméra plutôt...",
    ('allumée', 'éteinte'))

if camera == 'allumée':
    camera_on = True
else:
    camera_on = False

def cal_co2_visio():
    if camera_on:
        em_visio = (h_visio*4*mois*float(visio_data.loc[visio_data["Outil"]==outil_visio, "kgCO2eq/h Video+Audio"]))/1000
    else:
        em_visio = (h_visio*4*mois*float(visio_data.loc[visio_data["Outil"]==outil_visio, "kgCO2eq/h Video+Audio"]))/1000*0.29
    return em_visio

co2_visio = cal_co2_visio()

#stockage

co2_numerique = co2_portables + co2_smartphones + co2_emails + co2_visio



###Section 4####################################################################################################
st.markdown("<h2 style='text-align: center'>Papeterie et fournitures de bureau</h2>", unsafe_allow_html=True)

st.subheader("Impressions 🖨️")

col25, col26 = st.columns(2)

n_impression =  col25.number_input('Nombre de pages imprimées par semaine', min_value=0, max_value=None, value=0, step=1, format=None, key=None,)

impression = col26.radio(
    "Impression",
    ('recto verso', 'recto'))

if impression == 'recto verso':
    recto_verso = True
else:
    recto_verso = False
    
def cal_co2_visio():
    if recto_verso:
        em_impression = (n_impression*4.68/2)/1000
    else:
        em_impression = (n_impression*4.68)/1000
    return em_impression

co2_bureau = cal_co2_visio()

###Section 5####################################################################################################
st.markdown("<h2 style='text-align: center'>Résultats</h2>", unsafe_allow_html=True)

#total
co2_total = co2_deplacements + co2_numerique + co2_bureau

st.metric(label="Empreinte carbone totale", value=str(round(co2_total, 2))+" kgCO2eq")

fig = px.pie(values=[co2_deplacements, co2_numerique, co2_bureau], 
names=["Déplacements", "Numérique", "Bureau"])
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)

#deplacement
st.metric(label="Déplacements", value=str(round(co2_deplacements, 2))+" kgCO2eq")

fig = px.pie(values=[co2_avion, co2_TGV, co2_train, co2_ev, co2_voiture, co2_rer, co2_metro, co2_bus, co2_veloAE], 
names=["Avion", "TGV", "Train", "Voiture électrique", "Voiture thermique", "RER ou Transilien", "Metro", "Bus", "Vélo ou trotinette assistance électrique"])
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)


#numerique
st.metric(label="Numérique", value=str(round(co2_numerique, 2))+" kgCO2eq")
fig = px.pie(values=[co2_portables, co2_smartphones, co2_emails, co2_visio], 
names=["Ordinateurs", "Smartphones", "Mails", "Visioconférences"])
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)


#bureau
st.metric(label="Papeterie et fournitures de bureau", value=str(round(co2_bureau, 2))+" kgCO2eq")
fig = px.pie(values=[co2_bureau], 
names=["Impressions"])
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)

#download data as csv
emissions_deplacement = [co2_avion, co2_TGV, co2_train, co2_ev, co2_voiture, co2_rer, co2_metro, co2_bus, co2_veloAE, co2_velo]

dict_deplacements = {'catégorie':['Déplacements'] * len(emissions_deplacement),
        'Emission':["Avion", "TGV", "Train", "Voiture électrique", "Voiture thermique", "RER ou Transilien", "Metro", "Bus", "Vélo ou trotinette assistance électrique", "Vélo ou marche"],
        'kgCO2eq':emissions_deplacement
       }
  
results = pd.DataFrame(dict_deplacements)

emissions_numerique = [co2_portables, co2_smartphones, co2_emails, co2_visio]

dict_numerique = {'catégorie':['Numérique'] * len(emissions_numerique),
        'Emission':["Ordinateurs", "Smartphones", "Mails", "Visioconférences"],
        'kgCO2eq':emissions_numerique
       }
  
results_numerique = pd.DataFrame(dict_numerique)
results = pd.concat([results, results_numerique], ignore_index=True)
  
dict_bureau = {'catégorie':['Papeterie et fournitures de bureau'],
        'Emission':["Impressions"],
        'kgCO2eq':co2_bureau
       }

results_bureau = pd.DataFrame(dict_bureau)
results = pd.concat([results, results_bureau], ignore_index=True)

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
