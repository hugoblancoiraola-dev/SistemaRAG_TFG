#Código scrapping de datos

import requests
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup  # type: ignore # Para procesar el HTML obtenido
import shutil
import json 

# Configuración adicional para robust_request
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    # Agregar más User-Agents si es necesario
]
REFERRERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.yahoo.com/",
    # Agregar más referers si es necesario
]

# Función para realizar solicitudes robustas
def robust_request(url, max_retries=10):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "es-ES,es;q=0.9", 
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Referer": random.choice(REFERRERS),
    }

    for attempt in range(1, max_retries + 1):
        delay = random.uniform(2, 5)
        try:
            response = requests.get(url, headers=headers, timeout=(4.05, 10))
            if response.status_code == 200:
                return response.text  # Devuelve el contenido HTML
            elif 500 <= response.status_code < 600:
                print(f"Error del servidor {response.status_code}. Reintento {attempt}/{max_retries}.")
            else:
                print(f"Error HTTP {response.status_code}. Reintento {attempt}/{max_retries}.")
        except requests.exceptions.Timeout:
            print(f"Timeout en {url}. Reintento {attempt}/{max_retries}.")
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {url} ({e}). Reintento {attempt}/{max_retries}.")
        time.sleep(delay * (attempt + random.uniform(0.5, 1.5)))

    print(f"Falló el acceso a {url} después de {max_retries} intentos.")
    return None

# Configuración de Chrome
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-maximized")  # Depuración
chrome_options.add_argument("--headless=new")  # Comenta esta línea para depurar
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--disable-extensions")



chrodriver_path = shutil.which("chromedriver")
print(f"Chromedriver path: {chrodriver_path}")

# Inicializar WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    base_url = "https://oa.upm.es/cgi/search/archive/advanced?screen=Search&dataset=archive&title_merge=ALL&title=&creators_name_merge=ALL&creators_name=&contributors_name_merge=ALL&contributors_name=&abstract_merge=ALL&abstract=&keywords_merge=ALL&keywords=&subjects_merge=ANY&type=other&master_title_merge=ALL&master_title=&institution=ETSI_Sistemas_Infor&editors_name_merge=ALL&editors_name=&refereed=EITHER&event_title_merge=ALL&event_title=&note_merge=ALL&note=&date=&imarina_id=&satisfyall=ALL&order=-date%2Fcreators_name%2Ftitle&_action_search=Buscar"
    count_tfgs=0
    tfgs=[]

    while True: #Recorrer todas las páginas disponibles

        if count_tfgs>=6:
            print("Limite de TFGs alcanzado")
            break 

        html_content = robust_request(base_url)  # Obtener el contenido de la página inicial
        

        if html_content:
            soup = BeautifulSoup(html_content, "html.parser")

            # Extraer enlaces a los TFGs
            links = [a["href"] for a in soup.select(".ep_search_result a")]

            for link in links :
                if link == "https://oa.upm.es/view/institution/ETSI=5FSistemas=5FInfor/" or '.pdf' in link or '.zip' in link : continue
                #if count_tfgs>=6:
                #    break
                tfg_html = robust_request(link)  # Obtener la página del TFG
                if tfg_html:
                    tfg_soup = BeautifulSoup(tfg_html, "html.parser")

                    tfg = {
                        # Extraer datos
                        "título" : tfg_soup.find("h1").get_text(strip= True) if tfg_soup.find("h1") else "No especificado",
                        "autor" : tfg_soup.find("span", class_="person_name").get_text(strip= True) if tfg_soup.find("span", class_="person_name") else "No especificado",
                        "director" : tfg_soup.find("tr", class_="contributors").get_text(strip= True) if tfg_soup.find("tr", class_="contributors") else "No especificado",
                        "tipo_documento" : tfg_soup.find("tr", class_="type").get_text(strip= True) if tfg_soup.find("tr", class_="type") else "No especificado",
                        "grado" : tfg_soup.find("tr", class_="grado").get_text(strip= True) if tfg_soup.find("tr", class_="grado") else "No especificado",
                        "fecha" : tfg_soup.find("tr", class_="date").get_text(strip= True) if tfg_soup.find("tr", class_="date") else "No especificado",
                        "asignaturas" : tfg_soup.find("tr", class_="subjects").get_text(strip= True) if tfg_soup.find("tr", class_="subjects") else "No especificado",
                        "ods" : tfg_soup.find("tr", class_="ods").get_text(strip= True) if tfg_soup.find("tr", class_="ods") else "No especificado",
                        "palabras_clave" : tfg_soup.find("tr", class_="keywords").get_text(strip= True) if tfg_soup.find("tr", class_="keywords") else "No especificado",
                        "institución" : tfg_soup.find("tr", class_="institution").get_text(strip= True) if tfg_soup.find("tr", class_="institution") else "No especificado",
                        "departamento" : tfg_soup.find("tr", class_="department").get_text(strip= True) if tfg_soup.find("tr", class_="department") else "No especificado",
                        "derechos" : tfg_soup.find("tr", class_="rights").get_text(strip= True) if tfg_soup.find("tr", class_="rights") else "No especificado",
                        "PDF_link" : tfg_soup.find("a", class_="ep_document_link")["href"] if tfg_soup.find("a", class_="ep_document_link") else "No especificado",
                        "resumen" : tfg_soup.find("div", class_="ep_block abstract").get_text(strip= True) if tfg_soup.find("div", class_="ep_block abstract") else "No especificado"
                    }

                    count_tfgs +=1
                    tfgs.append(tfg)
            #Intenta pasar de página
            try:                
                next_button = driver.find_element(By.LINK_TEXT, "Siguiente")
                next_button.click()
                time.sleep(3)
            except Exception:
                print("No hay más páginas") 
    driver.quit()

except Exception as e:
    print(f"Error general: {e}")
    driver.quit()

#finally:
#    driver.quit()

with open("tfgs.json", "w+", encoding="utf-8") as f:
    json.dump(tfgs, f, ensure_ascii=False, indent=4)
print("Datos guardados en tfgs.json") 