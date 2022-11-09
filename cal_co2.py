def transport(em, n, km, f_transport, collaborateurs, mois):
	if f_transport:
		co2 = (em*n*km*collaborateurs*mois)/1000
		return co2 
	else: 
		co2 = (em*n*km*collaborateurs)/1000
		return co2 

def portables(data, list):
    em_portables = 0
    for ordi in list:
        em_portables += float(data.loc[data["Model"]==ordi, "kg CO2e"])
    return em_portables

def smartphones(data, list):
	em_smartphones = 0
	for phone in list:
		em_smartphones += float(data.loc[data["Model"]==phone, "kg CO2e"])
	return em_smartphones

def emails(n_mails_pj,n_mails, mois):
	em_mails = ((n_mails_pj*4*mois*35)+(n_mails*4*mois*4))/1000
	return em_mails

def visio(camera_on, h_visio, data, outil_visio, mois):
	if camera_on:
		em_visio = (h_visio*4*mois*float(data.loc[data["Outil"]==outil_visio, "kgCO2eq/h Video+Audio"]))/1000
	else:
		em_visio = (h_visio*4*mois*float(data.loc[data["Outil"]==outil_visio, "kgCO2eq/h Video+Audio"]))/1000*0.29
	return em_visio

def stockage(tb_year, n_backups, mois, retention_years, w, pue, f):
	em_stockage = (tb_year*(1+n_backups) *((mois/12)*retention_years))*(w/1000)*8760*pue*(f*1000)
	return em_stockage

def impressions(recto_verso, n_impression):
	if recto_verso:
		em_impression = (n_impression*4.68/2)/1000
	else:
		em_impression = (n_impression*4.68)/1000
	return em_impression