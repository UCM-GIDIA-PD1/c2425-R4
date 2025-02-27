from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


# Configuración del navegador
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # Ejecutar en segundo plano
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')

# Inicializar el driver
driver = webdriver.Chrome(options = options)
url = "https://www.ufc.com/athletes/all"
#url = "https://www.ufc.com/athletes/all?filters%5B0%5D=fighting_style%3A7144&filters%5B1%5D=status%3A23"
driver.get(url)
time.sleep(1)  # Esperar carga inicial

def cargar_mas():
    # Cargar más elementos mientras el botón esté disponible
    while True:
        try:
            # Buscar el botón "Load more items"
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.button[rel="next"]'))
            )

            # Hacer scroll hacia el botón antes de hacer clic
            driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
            time.sleep(2)  # Esperar un poco para evitar bloqueos

            # Hacer clic en el botón
            load_more_button.click()
            time.sleep(2)  # Esperar a que se carguen más elementos

        except Exception:
            print("No hay más elementos para cargar.")
            break  # Sale del bucle cuando ya no hay más botón


def extract_fighters(start_page, end_page=None):
    base_url = "https://www.ufc.com/athletes/all?page="
    all_links = []

    # Si no se especifica end_page, se extraen todas las páginas hasta que no haya más peleadores
    if end_page is None:
        end_page = float('inf')

    current_page = start_page
    while current_page <= end_page:
        url = base_url + str(current_page)
        driver.get(url)
        time.sleep(1)  # Esperar carga inicial

        # Obtener los enlaces de los peleadores
        fighter_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/athlete/']")
        links = [link.get_attribute("href") for link in fighter_links]

        if not links:
            print(f"No se encontraron más peleadores en la página {current_page}.")
            break

        all_links.extend(links)
        current_page += 1

    return all_links


def extraer_peleadores(pag_ini, pag_fin):    
    # Obtener los enlaces de los peleadores
    fighter_links = extract_fighters(pag_ini, pag_fin)

    # Lista para almacenar los datos
    data = []

    try:
        # Recorrer cada enlace y extraer la información
        for link in fighter_links:
            driver.get(link)
            time.sleep(1.5)  # Esperar a que la página del peleador cargue

            try:
                name = driver.find_element(By.CSS_SELECTOR, "h1.hero-profile__name").text
                print(f"Procesando a {name}...")

                # Diccionario para almacenar los datos del peleador
                fighter_data = {"Nombre": name}


                ######################### EFECTIVIDAD DE GOLPEO #####################
                try:
                    golpeo_section = driver.find_element(By.XPATH, '//h2[@class="e-t3" and contains(text(), "Striking accuracy")]')
                    efectividad_golpeo = driver.find_element(By.CSS_SELECTOR, "text.e-chart-circle__percent").text
                    fighter_data["Striking accuracy (%)"] = efectividad_golpeo
                except:
                    print(f"No se encontró 'Striking accuracy' para {name}")

                ######################### EFECTIVIDAD DE DERRIBO #####################
                try:
                    derribo_section = driver.find_element(By.XPATH, '//h2[@class="e-t3" and contains(text(), "Takedown Accuracy")]')
                    efectividad_derribo = driver.find_element(By.CSS_SELECTOR, "text.e-chart-circle__percent").text
                    fighter_data["Efectividad de derribo (%)"] = efectividad_derribo
                except:
                    print(f"No se encontró 'Takedown Accuracy' para {name}")

                ######################### GOLPES SIGNIFICATIVOS #####################
                try:
                    dt_element = driver.find_element(By.XPATH, '//dt[@class="c-overlap__stats-text" and contains(text(), "Sig. Strikes Landed")]')
                    dd_element = dt_element.find_element(By.XPATH, './following-sibling::dd[@class="c-overlap__stats-value"]')
                    fighter_data["Golpes Significativos Conectados"] = dd_element.text
                except:
                    print(f"No se encontró 'Sig. Strikes Landed' para {name}")

                try:
                    dt_element = driver.find_element(By.XPATH, '//dt[@class="c-overlap__stats-text" and contains(text(), "Sig. Strikes Attempted")]')
                    dd_element = dt_element.find_element(By.XPATH, './following-sibling::dd[@class="c-overlap__stats-value"]')
                    fighter_data["Golpes Significativos Intentados"] = dd_element.text
                except:
                    print(f"No se encontró 'Sig. Strikes Attempted' para {name}")
                    
                ######################### DERRIBOS ########################
                try:
                    dt_element = driver.find_element(By.XPATH, '//dt[@class="c-overlap__stats-text" and contains(text(), "Takedowns Landed")]')
                    dd_element = dt_element.find_element(By.XPATH, './following-sibling::dd[@class="c-overlap__stats-value"]')
                    fighter_data["Derribos conseguidos"] = dd_element.text
                except:
                    print(f"No se encontró 'Derribos conseguidos' para {name}")

                try:
                    dt_element = driver.find_element(By.XPATH, '//dt[@class="c-overlap__stats-text" and contains(text(), "Takedowns Attempted")]')
                    dd_element = dt_element.find_element(By.XPATH, './following-sibling::dd[@class="c-overlap__stats-value"]')
                    fighter_data["Derribos intentados"] = dd_element.text
                except:
                    print(f"No se encontró 'Derribos Intentados' para {name}")
                    
                ######################## CUADRO 1 ########################################
                try:
                    t_por_minuto = driver.find_element(By.XPATH, '//div[@class="c-stat-compare__label" and contains(text(), "Sig. Str. Landed")]')
                    v_por_minuto = t_por_minuto.find_element(By.XPATH, './preceding-sibling::div[@class="c-stat-compare__number"]')
                    golpes_por_minuto = v_por_minuto.text.strip()
                    fighter_data["Golpes Significativos Conectados Por Minuto"] = golpes_por_minuto
                    
                except:
                    print(f"No se encontró 'Golpes Significativos Conectados Por Minuto' para {name}")
                
                try:
                    t_por_minuto = driver.find_element(By.XPATH, '//div[@class="c-stat-compare__label" and contains(text(), "Sig. Str. Absorbed")]')
                    v_por_minuto = t_por_minuto.find_element(By.XPATH, './preceding-sibling::div[@class="c-stat-compare__number"]')
                    golpes_por_minuto = v_por_minuto.text.strip()
                    fighter_data["Golpes Significativos Recibidos Por Minuto"] = golpes_por_minuto
                    
                except:
                    print(f"No se encontró 'Golpes Significativos Recibidos Por Minuto' para {name}")
                
                try:
                    t_por_minuto = driver.find_element(By.XPATH, '//div[@class="c-stat-compare__label" and contains(text(), "Takedown avg")]')
                    v_por_minuto = t_por_minuto.find_element(By.XPATH, './preceding-sibling::div[@class="c-stat-compare__number"]')
                    golpes_por_minuto = v_por_minuto.text.strip()
                    fighter_data["Promedio de Knockdown Por 15m"] = golpes_por_minuto
                    
                except:
                    print(f"No se encontró 'Promedio de Knockdown Por 15m' para {name}")
                    
                try:
                    t_por_minuto = driver.find_element(By.XPATH, '//div[@class="c-stat-compare__label" and contains(text(), "Submission avg")]')
                    v_por_minuto = t_por_minuto.find_element(By.XPATH, './preceding-sibling::div[@class="c-stat-compare__number"]')
                    golpes_por_minuto = v_por_minuto.text.strip()
                    fighter_data["Promedio de Sumisión Por 15m"] = golpes_por_minuto
                    
                except:
                    print(f"No se encontró 'Promedio de Sumisión Por 15m' para {name}")
                
                    
                ######################## CUADRO 2 ########################################
                try:
                    # Defensa de Golpes Sig.
                    t_por_minuto = driver.find_element(By.XPATH, '//div[@class="c-stat-compare__label" and contains(text(), "Sig. Str. Defense")]')
                    v_por_minuto = t_por_minuto.find_element(By.XPATH, './preceding-sibling::div[@class="c-stat-compare__number"]')
                    defensa_golpes_sig = v_por_minuto.text.strip().replace("\n", "").replace(" ", "")  
                    fighter_data["Defensa de Golpes Sig."] = defensa_golpes_sig
                    
                except:
                    print(f"No se encontró 'Defensa de Golpes Sig.' para {name}")

                try:
                    # Defensa De Derribo
                    t_por_minuto = driver.find_element(By.XPATH, '//div[@class="c-stat-compare__label" and contains(text(), "Takedown Defense")]')
                    v_por_minuto = t_por_minuto.find_element(By.XPATH, './preceding-sibling::div[@class="c-stat-compare__number"]')
                    defensa_derribo = v_por_minuto.text.strip().replace("\n", "").replace(" ", "") 
                    fighter_data["Defensa De Derribo"] = defensa_derribo
                    
                except:
                    print(f"No se encontró 'Defensa De Derribo' para {name}")

                try:
                    # Promedio de Tiempo de Pelea
                    t_por_minuto = driver.find_element(By.XPATH, '//div[@class="c-stat-compare__label" and contains(text(), "Average fight time")]')
                    v_por_minuto = t_por_minuto.find_element(By.XPATH, './preceding-sibling::div[@class="c-stat-compare__number"]')
                    tiempo_pelea = v_por_minuto.text.strip()
                    fighter_data["Promedio de Tiempo de Pelea"] = tiempo_pelea
                    
                except:
                    print(f"No se encontró 'Promedio de Tiempo de Pelea' para {name}")
                
                ##################### GOLPES POR POSICIÓN ############################################
                try:
                    # Extraer datos para "De pie"
                    de_pie = driver.find_element(By.XPATH, '//div[@class="c-stat-3bar__label" and contains(text(), "Standing ")]/following-sibling::div[@class="c-stat-3bar__value"]')
                    de_pie_text = de_pie.text.strip()  
                    golpes_de_pie, porcentaje_de_pie = de_pie_text.split(" (")  
                    porcentaje_de_pie = porcentaje_de_pie.replace(")", "")  
                    fighter_data["Golpes De Pie"] = golpes_de_pie
                    fighter_data["Porcentaje De Pie"] = porcentaje_de_pie
                except Exception as e:
                    print(f"Error al extraer los datos: {e}")
                try:
                    # Extraer datos para "Clinch"
                    clinch = driver.find_element(By.XPATH, '//div[@class="c-stat-3bar__label" and contains(text(), "Clinch")]/following-sibling::div[@class="c-stat-3bar__value"]')
                    clinch_text = clinch.text.strip()  
                    golpes_clinch, porcentaje_clinch = clinch_text.split(" (")  
                    porcentaje_clinch = porcentaje_clinch.replace(")", "")  
                    fighter_data["Golpes Clinch"] = golpes_clinch
                    fighter_data["Porcentaje Clinch"] = porcentaje_clinch
                except Exception as e:
                    print(f"Error al extraer los datos: {e}")
                try:
                    # Extraer datos para "Suelo"
                    suelo = driver.find_element(By.XPATH, '//div[@class="c-stat-3bar__label" and contains(text(), "Ground ")]/following-sibling::div[@class="c-stat-3bar__value"]')
                    suelo_text = suelo.text.strip()  
                    golpes_suelo, porcentaje_suelo = suelo_text.split(" (")  
                    porcentaje_suelo = porcentaje_suelo.replace(")", "")  
                    fighter_data["Golpes Suelo"] = golpes_suelo
                    fighter_data["Porcentaje Suelo"] = porcentaje_suelo

                except Exception as e:
                    print(f"Error al extraer los datos: {e}")
                    
                ################ SIG. STR. TARGET #####################
                try:
                    # Extraer datos para "Cabeza"
                    golpes_cabeza = driver.find_element(By.ID, "e-stat-body_x5F__x5F_head_value").text.strip()
                    porcentaje_cabeza = driver.find_element(By.ID, "e-stat-body_x5F__x5F_head_percent").text.strip()
                    fighter_data["Golpes Cabeza"] = golpes_cabeza
                    fighter_data["Porcentaje Cabeza"] = porcentaje_cabeza
                except Exception as e:
                    print(f"Error al extraer los datos: {e}")

                    # Extraer datos para "Cuerpo"
                    golpes_cuerpo = driver.find_element(By.ID, "e-stat-body_x5F__x5F_body_value").text.strip()
                    porcentaje_cuerpo = driver.find_element(By.ID, "e-stat-body_x5F__x5F_body_percent").text.strip()
                    fighter_data["Golpes Cuerpo"] = golpes_cuerpo
                    fighter_data["Porcentaje Cuerpo"] = porcentaje_cuerpo
                try:
                    # Extraer datos para "Pierna"
                    golpes_pierna = driver.find_element(By.ID, "e-stat-body_x5F__x5F_leg_value").text.strip()
                    porcentaje_pierna = driver.find_element(By.ID, "e-stat-body_x5F__x5F_leg_percent").text.strip()
                    fighter_data["Golpes Pierna"] = golpes_pierna
                    fighter_data["Porcentaje Pierna"] = porcentaje_pierna

                except Exception as e:
                    print(f"Error al extraer los datos: {e}")
                    
                ######################## WIN METHOD######################
                
                try:
                    # Extraer datos para "KO/TKO"
                    ko_tko = driver.find_element(By.XPATH, '//div[@class="c-stat-3bar__label" and contains(text(), "KO/TKO")]/following-sibling::div[@class="c-stat-3bar__value"]')
                    ko_tko_text = ko_tko.text.strip()  
                    ko_tko_value, ko_tko_percent = ko_tko_text.split(" (")  # Separar número y porcentaje
                    ko_tko_percent = ko_tko_percent.replace(")", "")  # Eliminar el paréntesis final
                    fighter_data["KO/TKO"] = ko_tko_value
                    fighter_data["Porcentaje KO/TKO"] = ko_tko_percent
                except Exception as e:
                    print(f"Error al extraer los datos: {e}")
                try:
                    # Extraer datos para "DEC"
                    dec = driver.find_element(By.XPATH, '//div[@class="c-stat-3bar__label" and contains(text(), "DEC")]/following-sibling::div[@class="c-stat-3bar__value"]')
                    dec_text = dec.text.strip()  
                    dec_value, dec_percent = dec_text.split(" (")  # Separar número y porcentaje
                    dec_percent = dec_percent.replace(")", "")  # Eliminar el paréntesis final
                    fighter_data["DEC"] = dec_value
                    fighter_data["Porcentaje DEC"] = dec_percent
                except Exception as e:
                    print(f"Error al extraer los datos: {e}")
                try:
                    # Extraer datos para "SUB"
                    sub = driver.find_element(By.XPATH, '//div[@class="c-stat-3bar__label" and contains(text(), "SUB")]/following-sibling::div[@class="c-stat-3bar__value"]')
                    sub_text = sub.text.strip()  
                    sub_value, sub_percent = sub_text.split(" (")  # Separar número y porcentaje
                    sub_percent = sub_percent.replace(")", "")  # Eliminar el paréntesis final
                    fighter_data["SUB"] = sub_value
                    fighter_data["Porcentaje SUB"] = sub_percent
                    
                except Exception as e:
                    print(f"Error al extraer los datos: {e}")
                ####################################
                #AÑADIDO NUEVO
                ###########################
                
                ###########DATOS DEL PELEADOR###################
                try:
                    status = driver.find_element(By.XPATH, '//div[@class="c-bio__label" and contains(text(), "Status")]/following-sibling::div')
                    fighter_data["Status"] = status.text.strip()
                except:
                    pass

                try:
                    place_of_birth = driver.find_element(By.XPATH, '//div[@class="c-bio__label" and contains(text(), "Place of Birth")]/following-sibling::div')
                    fighter_data["Place of Birth"] = place_of_birth.text.strip()
                except:
                    pass

                try:
                    fighting_style = driver.find_element(By.XPATH, '//div[@class="c-bio__label" and contains(text(), "Fighting style")]/following-sibling::div')
                    fighter_data["Fighting Style"] = fighting_style.text.strip()
                except:
                    pass

                try:
                    age = driver.find_element(By.XPATH, '//div[@class="c-bio__label" and contains(text(), "Age")]/following-sibling::div')
                    fighter_data["Age"] = age.text.strip()
                except:
                    pass

                try:
                    height = driver.find_element(By.XPATH, '//div[@class="c-bio__label" and contains(text(), "Height")]/following-sibling::div')
                    fighter_data["Height"] = height.text.strip()
                except:
                    pass

                try:
                    weight = driver.find_element(By.XPATH, '//div[@class="c-bio__label" and contains(text(), "Weight")]/following-sibling::div')
                    fighter_data["Weight"] = weight.text.strip()
                except:
                    pass

                try:
                    debut = driver.find_element(By.XPATH, '//div[@class="c-bio__label" and contains(text(), "Octagon Debut")]/following-sibling::div')
                    fighter_data["Octagon Debut"] = debut.text.strip()
                except:
                    pass

                try:
                    reach = driver.find_element(By.XPATH, '//div[@class="c-bio__label" and contains(text(), "Reach")]/following-sibling::div')
                    fighter_data["Reach"] = reach.text.strip()
                except:
                    pass

                try:
                    leg_reach = driver.find_element(By.XPATH, '//div[@class="c-bio__label" and contains(text(), "Leg reach")]/following-sibling::div')
                    fighter_data["Leg Reach"] = leg_reach.text.strip()
                except:
                    pass
                try:
                    # Extraer la división
                    division_element = driver.find_element(By.XPATH, '//p[@class="hero-profile__division-title"]')
                    division = division_element.text.strip()
                    fighter_data["Division"] = division
                except:
                    print("No se encontró la división")

                try:
                    # Extraer el récord
                    record_element = driver.find_element(By.XPATH, '//p[@class="hero-profile__division-body"]')
                    record = record_element.text.strip()
                    fighter_data["Record"] = record
                except:
                    print("No se encontró el récord")
                    
                ######IMAGEN###########
                try:
                    img_element = driver.find_element(By.XPATH, '//div[@class="hero-profile__image-wrap"]/img')
                    fighter_data["Imagen"] = img_element.get_attribute("src")
                except:
                    print(f"No se encontró la imagen para {name}")
                            
                    
                # Agregar los datos del peleador a la lista
                data.append(fighter_data)

            except Exception as e:
                print(f"Error al procesar {link}: {e}")
                
            

    finally:
        # Guardar los datos antes de cerrar el navegador
        df = pd.DataFrame(data)
        df.to_csv(r"../data/raw/peleadores.csv", index=False, encoding="utf-8")
        print("Datos guardados en peleadores.csv")

        # Cerrar el navegador
        driver.quit()
        
