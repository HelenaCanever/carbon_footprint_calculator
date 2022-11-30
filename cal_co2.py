def transport(em, n, km, f_transport, associates, months):
	if f_transport:
		co2 = (em*n*km*associates*months)/1000
		return co2 
	else: 
		co2 = (em*n*km*associates)/1000
		return co2 

def laptops(data, list, m):
	em_laptops = 0
	for laptop in list:
		if data.loc[data["Model"]==laptop, "kg CO2e w/o use"].isna().values[0]==True:
			em_portables += float(data.loc[data["Model"]==laptop, "kg CO2e"])
		else:
			base =float(data.loc[data["Model"]==laptop, "kg CO2e w/o use"])
			years_use = float(data.loc[data["Model"]==laptop, "years_use"])
			co2_per_month = (float(data.loc[data["Model"]==laptop, "kg CO2e"])-base)/years_use/12
			em_laptops += (base+(co2_per_month*m))
	return 	em_laptops


def smartphones(data, list):
	em_smartphones = 0
	for phone in list:
		em_smartphones += float(data.loc[data["Model"]==phone, "kg CO2e"])
	return em_smartphones

def emails(n_mails_att,n_mails, months):
	em_mails = ((n_mails_att*4*months*3.4)+(n_mails*4*months*2.1))/1000
	return em_mails

def visio(camera_on, h_visio, data, outil_visio, months):
	if camera_on:
		em_visio = (h_visio*4*months*float(data.loc[data["Outil"]==outil_visio, "kgCO2eq/h Video+Audio"]))/1000
	else:
		em_visio = (h_visio*4*months*float(data.loc[data["Outil"]==outil_visio, "kgCO2eq/h Video+Audio"]))/1000*0.29
	return em_visio

def storage(tb_year, n_backups, months, retention_years, w, pue, f, offset, offset_ratio):
	if offset:
		percentage = offset_ratio/100
		em_storage = ((tb_year*(1+n_backups) *((months/12)*retention_years))*(w/1000)*8760*pue*(f*1000))* (1-percentage)
	else:
		em_storage = (tb_year*(1+n_backups) *((months/12)*retention_years))*(w/1000)*8760*pue*(f*1000)
	return em_storage

def ml(gpu_data, cloud_data, h_gpu, gpu, provider_gpu, zone_gpu, offset):
	kWh = (h_gpu * float((gpu_data.loc[gpu_data["name"]==gpu, "tdp_watts"])))/1000
	CO2_per_kWh = float(cloud_data.loc[(cloud_data["providerName"]==provider_gpu)&(cloud_data["region"]==zone_gpu), "impact"])
	if offset:
		percentage = float(cloud_data.loc[(cloud_data["providerName"]==provider_gpu)&(cloud_data["region"]==zone_gpu), "offsetRatio"])/100
		em_ml = ((kWh * CO2_per_kWh)/1000) * (1-percentage)
	else:
		em_ml = (kWh * CO2_per_kWh)/1000
	return em_ml

def printing(recto_verso, n_prints):
	if recto_verso:
		em_printing = (n_prints*4.68/2)/1000
	else:
		em_printing = (n_prints*4.68)/1000
	return em_printing
