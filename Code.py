
#Este codigo unicamente sirve para descargar informacion de las actas de los votos presidenciales, pero realizando
#algunas modificaciones al código es posible descargar información congresal y parlamento andino. Asimismo, es posible
#descargar información para otros periodos.

import os
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver_path = r"C:\Program Files\Chromedriver\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = driver_path
driver = webdriver.Chrome(driver_path)

driver.get('https://www.web.onpe.gob.pe/modElecciones/elecciones/elecciones2016/PRPCP2016/Actas-por-Ubigeo.html#posicion')
time.sleep(2)

#Notar que para dpto, prov, dist y local siempre empieza en 1 porque esta la categoria "SELECCION".

#Departamento
seleccionar_dpto = Select(driver.find_element('id','cdgoDep'))
departamento = driver.find_element('id','cdgoDep')
dpto_conteo = departamento.find_elements(By.TAG_NAME,'option')
for dpto in range(1,len(dpto_conteo)):
	seleccionar_dpto.select_by_index(dpto)
	time.sleep(1)

	#Provincia
	seleccionar_prov = Select(driver.find_element('id','cdgoProv'))
	provincia = driver.find_element('id','cdgoProv')
	prov_conteo = provincia.find_elements(By.TAG_NAME,'option')
	for prov in range(1,len(prov_conteo)):
		seleccionar_prov.select_by_index(prov)
		time.sleep(1)

		#Distrito
		seleccionar_dist = Select(driver.find_element('id','cdgoDist'))
		distrito = driver.find_element('id','cdgoDist')
		dist_conteo = distrito.find_elements(By.TAG_NAME,'option')
		for dist in range(1,len(dist_conteo)):
			base_dato = []
			seleccionar_dist.select_by_index(dist)
			time.sleep(2)

			#Local
			seleccionar_local = Select(driver.find_element('name','actas_ubigeo'))
			local = driver.find_element('name','actas_ubigeo')
			local_conteo = local.find_elements(By.TAG_NAME,'option')
			for loc in range(1,len(local_conteo)):
				print("Local ",loc," de ",len(local_conteo))
				seleccionar_local.select_by_index(loc)
				time.sleep(2)

				#Conteo de mesas de votacion
				mesas = driver.find_element(By.CLASS_NAME,'table17')
				mesas_conteo = mesas.find_elements(By.TAG_NAME,'tr')
				print("Hay ",len(mesas_conteo)," filas")

				#Las mesas tienen como maximo 10 columnas y las organizaciones políticas se presentan de dos formas:
				if len(mesas_conteo)==1:
					for colu in range(1,11):
						try:
							driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div[1]/div/table/tbody/tr/td[' + str(colu) + ']').click()
							time.sleep(1)

							#Extraccion de datos
							n_mesa = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[1]/div/table/tbody/tr/td[1]').text
							n_copia = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[1]/div/table/tbody/tr/td[2]').text
							n_dpto = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/table/tbody/tr[2]/td[1]').text
							n_prov = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/table/tbody/tr[2]/td[2]').text
							n_dist = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/table/tbody/tr[2]/td[3]').text
							n_local = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/table/tbody/tr[2]/td[4]').text
							n_dire = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/table/tbody/tr[2]/td[5]').text
							n_ele_hab = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[3]/div/table/tbody/tr[2]/td[1]').text
							n_tot_vot = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[3]/div/table/tbody/tr[2]/td[2]').text
							n_est_act = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[3]/div/table/tbody/tr[2]/td[3]').text
							time.sleep(1)

							actas = driver.find_element(By.CLASS_NAME,'table06')
							actas_conteo = actas.find_elements(By.TAG_NAME,'tr')

							if len(actas_conteo)==20:
								#Votos
								n_voto_b1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[17]/td[1]").text
								n_voto_b2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[17]/td[2]').text

								n_voto_n1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[18]/td[1]").text
								n_voto_n2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[18]/td[2]').text

								n_voto_i1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[19]/td[1]").text
								n_voto_i2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[19]/td[2]').text

								n_voto_t1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[20]/td[1]").text
								n_voto_t2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[20]/td[2]').text
								time.sleep(1)

								#Agrupaciones politicas
								for grupo in ["2","3","4","5","6","7","9","10","11","12","13","14","15","16"]:
									n_org1a = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[' + str(grupo) + ']/td[1]').text
									n_org1b = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[' + str(grupo) + ']/td[3]').text

									base_dato.append([n_mesa,n_copia,n_dpto,n_prov,n_dist,n_local,n_dire,n_ele_hab,n_tot_vot,n_est_act,n_voto_b1,n_voto_b2,n_voto_n1,n_voto_n2,n_voto_i1,n_voto_i2,n_voto_t1,n_voto_t2,n_org1a,n_org1b])
									df = pd.DataFrame(base_dato,columns=['n_mesa','n_copia','n_dpto','n_prov','n_dist','n_local','n_dire','n_ele_hab','n_tot_vot','n_est_act','n_voto_b1','n_voto_b2','n_voto_n1','n_voto_n2','n_voto_i1','n_voto_i2','n_voto_t1','n_voto_t2','n_org1a','n_org1b'])
									df.to_csv('A_' + str(dpto) + '_' + str(prov) + '_' + str(dist) + '.csv',encoding='utf-8-sig',index=False)

								#Regresar a las mesas
								time.sleep(1)
								driver.execute_script("window.scrollTo(0,300)")
								time.sleep(1)
								driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/button').click()

							else:
								#Votos
								n_voto_b1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[18]/td[1]").text
								n_voto_b2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[18]/td[2]').text

								n_voto_n1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[19]/td[1]").text
								n_voto_n2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[19]/td[2]').text

								n_voto_i1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[20]/td[1]").text
								n_voto_i2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[20]/td[2]').text

								n_voto_t1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[21]/td[1]").text
								n_voto_t2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[21]/td[2]').text
								time.sleep(1)

								#Agrupaciones politicas
								for grupo in ["2","3","4","5","6","7","9","10","12","13","14","15","16","17"]:
									n_org1a = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[' + str(grupo) + ']/td[1]').text
									n_org1b = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[' + str(grupo) + ']/td[3]').text

									base_dato.append([n_mesa,n_copia,n_dpto,n_prov,n_dist,n_local,n_dire,n_ele_hab,n_tot_vot,n_est_act,n_voto_b1,n_voto_b2,n_voto_n1,n_voto_n2,n_voto_i1,n_voto_i2,n_voto_t1,n_voto_t2,n_org1a,n_org1b])
									df = pd.DataFrame(base_dato,columns=['n_mesa','n_copia','n_dpto','n_prov','n_dist','n_local','n_dire','n_ele_hab','n_tot_vot','n_est_act','n_voto_b1','n_voto_b2','n_voto_n1','n_voto_n2','n_voto_i1','n_voto_i2','n_voto_t1','n_voto_t2','n_org1a','n_org1b'])
									df.to_csv('A_' + str(dpto) + '_' + str(prov) + '_' + str(dist) + '.csv',encoding='utf-8-sig',index=False)

								#Regresar a las mesas
								time.sleep(1)
								driver.execute_script("window.scrollTo(0,300)")
								time.sleep(1)
								driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/button').click()

						except:
							pass

				else:
					for fila in range(1,len(mesas_conteo)+1):
						for colu in range(1,11):
							try:
								driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div[1]/div/table/tbody/tr[' + str(fila) + ']/td[' + str(colu) + ']').click()
								time.sleep(1)

								#Extraccion de datos
								n_mesa = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[1]/div/table/tbody/tr/td[1]').text
								n_copia = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[1]/div/table/tbody/tr/td[2]').text
								n_dpto = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/table/tbody/tr[2]/td[1]').text
								n_prov = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/table/tbody/tr[2]/td[2]').text
								n_dist = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/table/tbody/tr[2]/td[3]').text
								n_local = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/table/tbody/tr[2]/td[4]').text
								n_dire = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/table/tbody/tr[2]/td[5]').text
								n_ele_hab = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[3]/div/table/tbody/tr[2]/td[1]').text
								n_tot_vot = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[3]/div/table/tbody/tr[2]/td[2]').text
								n_est_act = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[3]/div/table/tbody/tr[2]/td[3]').text
								time.sleep(1)

								actas = driver.find_element(By.CLASS_NAME,'table06')
								actas_conteo = actas.find_elements(By.TAG_NAME,'tr')

								if len(actas_conteo)==20:
									#Votos
									n_voto_b1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[17]/td[1]").text
									n_voto_b2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[17]/td[2]').text

									n_voto_n1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[18]/td[1]").text
									n_voto_n2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[18]/td[2]').text

									n_voto_i1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[19]/td[1]").text
									n_voto_i2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[19]/td[2]').text

									n_voto_t1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[20]/td[1]").text
									n_voto_t2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[20]/td[2]').text
									time.sleep(1)

									#Agrupaciones politicas
									for grupo in ["2","3","4","5","6","7","9","10","11","12","13","14","15","16"]:
										n_org1a = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[' + str(grupo) + ']/td[1]').text
										n_org1b = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[' + str(grupo) + ']/td[3]').text

										base_dato.append([n_mesa,n_copia,n_dpto,n_prov,n_dist,n_local,n_dire,n_ele_hab,n_tot_vot,n_est_act,n_voto_b1,n_voto_b2,n_voto_n1,n_voto_n2,n_voto_i1,n_voto_i2,n_voto_t1,n_voto_t2,n_org1a,n_org1b])
										df = pd.DataFrame(base_dato,columns=['n_mesa','n_copia','n_dpto','n_prov','n_dist','n_local','n_dire','n_ele_hab','n_tot_vot','n_est_act','n_voto_b1','n_voto_b2','n_voto_n1','n_voto_n2','n_voto_i1','n_voto_i2','n_voto_t1','n_voto_t2','n_org1a','n_org1b'])
										df.to_csv('A_' + str(dpto) + '_' + str(prov) + '_' + str(dist) + '.csv',encoding='utf-8-sig',index=False)

								else:
									#Votos
									n_voto_b1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[18]/td[1]").text
									n_voto_b2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[18]/td[2]').text

									n_voto_n1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[19]/td[1]").text
									n_voto_n2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[19]/td[2]').text

									n_voto_i1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[20]/td[1]").text
									n_voto_i2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[20]/td[2]').text

									n_voto_t1 = driver.find_element('xpath',"/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[21]/td[1]").text
									n_voto_t2 = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[21]/td[2]').text
									time.sleep(1)

									#Agrupaciones politicas
									for grupo in ["2","3","4","5","6","7","9","10","12","13","14","15","16","17"]:
										n_org1a = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[' + str(grupo) + ']/td[1]').text
										n_org1b = driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/div/div/table/tbody/tr[' + str(grupo) + ']/td[3]').text

										base_dato.append([n_mesa,n_copia,n_dpto,n_prov,n_dist,n_local,n_dire,n_ele_hab,n_tot_vot,n_est_act,n_voto_b1,n_voto_b2,n_voto_n1,n_voto_n2,n_voto_i1,n_voto_i2,n_voto_t1,n_voto_t2,n_org1a,n_org1b])
										df = pd.DataFrame(base_dato,columns=['n_mesa','n_copia','n_dpto','n_prov','n_dist','n_local','n_dire','n_ele_hab','n_tot_vot','n_est_act','n_voto_b1','n_voto_b2','n_voto_n1','n_voto_n2','n_voto_i1','n_voto_i2','n_voto_t1','n_voto_t2','n_org1a','n_org1b'])
										df.to_csv('A_' + str(dpto) + '_' + str(prov) + '_' + str(dist) + '.csv',encoding='utf-8-sig',index=False)

								#Regresar a las mesas
								time.sleep(1)
								driver.execute_script("window.scrollTo(0,300)")
								time.sleep(1)
								driver.find_element('xpath','/html/body/div/section[2]/div/div[2]/div/div[3]/form/div[2]/div[3]/div/button').click()

							except:
								pass

				#Regresar a local
				pass
				seleccionar_local = Select(driver.find_element('name','actas_ubigeo'))

			#Regresar a distrito
			pass
			seleccionar_dist = Select(driver.find_element('id','cdgoDist'))

		#Regresar a provincia
		pass
		seleccionar_prov = Select(driver.find_element('id','cdgoProv'))

	#Regresar a departamento
	pass
	seleccionar_dpto = Select(driver.find_element('id','cdgoDep'))

driver.close()
