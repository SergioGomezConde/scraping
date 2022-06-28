from fileinput import close
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Fichero JSON donde almacenar la informacion
ficheroJSON = "/home/serggom/scraping/data.json"
informacion = {'asignaturas': [], 'usuario': [], 'eventos': [], 'siguiente_evento': [], 'mensajes': []}

# Datos de acceso fijos
usuario = 'e71180769r'
contrasena = 'p5irZ9Jm4@9C#6WUaE!z9%@V'

# Modo headless
options = Options()
options.headless = True
options.add_argument("--windows-size=1920,1200")

# Acceso a pagina
driver = webdriver.Chrome(options=options)
driver.get('https://campusvirtual.uva.es/login/index.php')

# Inicio de sesion
driver.find_element(by=By.NAME, value='adAS_username').send_keys(usuario)
driver.find_element(by=By.NAME, value='adAS_password').send_keys(contrasena)
driver.find_element(by=By.NAME, value='adAS_submit').click()

# Aceptar cookies
driver.implicitly_wait(10)
driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/a[1]').click()



# Acceso a la seccion de mensajes
driver.get('https://campusvirtual.uva.es/message/index.php')

# Obtencion del numero de mensajes totales sin leer
time.sleep(10)
numeroMensajes = str(driver.find_element(by=By.XPATH, value='/html/body/nav/ul[2]/div[3]/a/div').get_attribute('aria-label').split(' ')[1])

time.sleep(10)
        
# Obtencion de los distintos numeros de mensajes
total_destacados = str(driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/button/small').get_attribute('aria-label').split(' ')[0])
destacados_sin_leer = str(driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/button/span[5]').get_attribute('aria-label').split(' ')[1])
total_grupo = str(driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/button/small').get_attribute('aria-label').split(' ')[0])
grupo_sin_leer = str(driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/button/span[5]').get_attribute('aria-label').split(' ')[1])
total_privados = str(driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/button/small').get_attribute('aria-label').split(' ')[0])
privados_sin_leer = str(driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/button/span[5]').get_attribute('aria-label').split(' ')[1])
        
# Almacenamiento de la informacion en el fichero JSON
informacion['mensajes'].append({
    'totales_sin_leer': str(numeroMensajes),
    'total_destacados': total_destacados,
    'destacados_sin_leer': destacados_sin_leer,
    'total_grupo': total_grupo,
    'grupo_sin_leer': grupo_sin_leer,
    'total_privados': total_privados,
    'privados_sin_leer': privados_sin_leer
})
        
with open(ficheroJSON, 'w') as ficheroDatos:
        json.dump(informacion, ficheroDatos, indent=4)
ficheroDatos.close()

driver.close()

