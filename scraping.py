from fileinput import close
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from datetime import date

def numero_a_mes(x):  # Funcion que devuelve el numero de mes introducido de manera escrita
    return{
        '1': "enero",
        '2': "febrero",
        '3': "marzo",
        '4': "abril",
        '5': "mayo",
        '6': "junio",
        '7': "julio",
        '8': "agosto",
        '9': "septiembre",
        '10': "octubre",
        '11': "noviembre",
        '12': "diciembre",
    }[x]


# Funcion para dar formato a una fecha y devolverla en la respuesta
def formatear_fecha(fecha_a_formatear):
    fecha_separada = fecha_a_formatear.split(", ")
    dia_semana = fecha_separada[0]
    if (dia_semana == "Hoy"):
        hora = fecha_separada[1]
        dia = date.today().day
        mes = date.today().month
        anio = date.today().year
        fecha_formateada = str(dia) + " de " + numero_a_mes(str(mes)) + " del " + str(anio) + " a las " + str(hora)

    elif (dia_semana == "Mañana"):
        hora = fecha_separada[1]
        dia = date.today().day
        mes = date.today().month
        anio = date.today().year
        # fecha_formateada = str(dia) + " de " + numero_a_mes(str(mes)) + " del " + str(anio) + " a las " + str(hora)
        fecha_formateada = str(dia) + "/" + str(mes) + "/" + str(anio) + " a las " + str(hora)

    else:
        hora = fecha_separada[2]
        mes_dia = fecha_separada[1].split(" ")
        dia = mes_dia[0]
        mes = mes_dia[1]
        anio = date.today().year
        fecha_formateada = str(dia) + " de " + numero_a_mes(str(mes)) + " del " + str(anio) + " a las " + str(hora)

    return fecha_formateada

# Funcion para dar formato a una hora y devolverla en la respuesta
def formatear_hora(hora_a_formatear):
    hora_separada = hora_a_formatear.split(", ")
    if(hora_separada[0] == "Mañana" or hora_separada[0] == "Hoy"):
        hora_formateada = hora_separada[1]
    else:
        hora_formateada = hora_separada[2]

    return hora_formateada

# Funcion que formatea el nombre obtenido desde Campus para que sea mas legible
def formatear_nombre(nombre_a_formatear):
    nombres = nombre_a_formatear.split(' ')
    nombre_formateado = nombres[2].capitalize() + " " + nombres[0].capitalize() + " " + nombres[1].split(',')[
        0].capitalize()
    return nombre_formateado

# Fichero JSON donde almacenar la informacion
ficheroJSON = '/home/serggom/scraping/datos.json'
contenidoJSON = {'asignaturas': [], 'usuario': [], 'eventos': [], 'siguiente_evento': [], 'eventos_hoy': [], 'mensajes': []}

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

# Acceso al perfil
URLPerfil = driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/header/div/div/div/div[1]/div[1]/div/div[1]/a').get_attribute('href')
driver.get(URLPerfil)

# Obtencion del nombre
nombre_perfil = driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div[1]/div/div[1]/h3').text
           
# Acceso a la seccion de asignaturas
time.sleep(2)
driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div[2]/div/div/ul/li[1]/a').click()

# Obtencion de las asignaturas
time.sleep(2)
elementos = driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div[2]/div/div/div/div[1]').find_elements(by=By.TAG_NAME, value='a')

# Obtencion de los porcentajes
porcentajes = driver.find_elements(by=By.CLASS_NAME, value='progress-circle')
i = 0

# Almacenamiento de la informacion en el fichero JSON
for elemento in elementos:
    nombre_asignatura = elemento.text.split(' (')[0].capitalize()
    
#     if (nombre_asignatura != "") and ("Grado en" not in nombre_asignatura):
    if (nombre_asignatura != ""):
        plan_asignatura = elemento.text.split('-')[2]
        codigo_asignatura = elemento.text.split('-')[3]
        enlace_asignatura = elemento.get_attribute('href')
        
        contenidoJSON['asignaturas'].append({
            'nombre': nombre_asignatura,
            'porcentaje': porcentajes[i].get_attribute('data-progress'), #TODO: ver si cambiar
            'plan': plan_asignatura,
            'codigo': codigo_asignatura,
            'enlace': enlace_asignatura
        })
        
        i = i + 1

# with open(ficheroJSON, 'w') as ficheroDatosJSON:
#     json.dump(contenidoJSON, ficheroDatosJSON, indent=4)           
           
# ficheroDatosJSON.close()
            
# Acceso a la seccion de detalles
driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div[2]/div/div/ul/li[2]/a').click()

# Obtencion del email
time.sleep(2)
email = driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div[2]/div/div/div/div[2]/div/div/div/section[1]/div/ul/li[2]/dl/dd/a').text

# Almacenamiento de la informacion en el fichero JSON
contenidoJSON['usuario'].append({
           'nombre': formatear_nombre(nombre_perfil),
           'email': email
})

# with open(ficheroJSON, 'w') as ficheroDatosJSON:
#     json.dump(contenidoJSON, ficheroDatosJSON, indent=4)

# ficheroDatosJSON.close()
    
###
##
# Acceso a la seccion de mensajes
driver.get('https://campusvirtual.uva.es/message/index.php')

# Obtencion del numero de mensajes totales sin leer
time.sleep(10)
numeroMensajes = str(driver.find_element(by=By.XPATH, value='/html/body/nav/ul[2]/div[3]/a/div').get_attribute('aria-label').split(' ')[1])

time.sleep(20)

# Obtencion de los distintos numeros de mensajes
total_destacados = str(driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/button/small').get_attribute('aria-label').split(' ')[0])
destacados_sin_leer = str(driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/button/span[5]').get_attribute('aria-label').split(' ')[1])
total_grupo = str(driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/button/small').get_attribute('aria-label').split(' ')[0])
grupo_sin_leer = str(driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/button/span[5]').get_attribute('aria-label').split(' ')[1])
total_privados = str(driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/button/small').get_attribute('aria-label').split(' ')[0])
privados_sin_leer = str(driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/button/span[5]').get_attribute('aria-label').split(' ')[1])
        
# Almacenamiento de la informacion en el fichero JSON
contenidoJSON['mensajes'].append({
    'totales_sin_leer': str(numeroMensajes),
    'total_destacados': total_destacados,
    'destacados_sin_leer': destacados_sin_leer,
    'total_grupo': total_grupo,
    'grupo_sin_leer': grupo_sin_leer,
    'total_privados': total_privados,
    'privados_sin_leer': privados_sin_leer
})
        
# with open(ficheroJSON, 'w') as ficheroDatosJSON:
#     json.dump(contenidoJSON, ficheroDatosJSON, indent=4)
        
# ficheroDatosJSON.close()

###
##
# Acceso a la seccion de calendario

# Acceso al calendario en vista de eventos proximos
driver.get('https://campusvirtual.uva.es/calendar/view.php?view=upcoming')

# Obtencion de la lista de eventos proximos
eventos_siguientes = driver.find_elements(by=By.CLASS_NAME, value='event')

# Comprobacion de que exista algun evento proximo
if len(eventos_siguientes) > 0:
    # Almacenamiento de la informacion en el fichero JSON
    fecha = str(formatear_fecha(eventos_siguientes[0].find_element(by=By.CLASS_NAME, value='col-11').text.split(" » ")[0])).split(" a las ")
    contenidoJSON['siguiente_evento'].append({
        'nombre': eventos_siguientes[0].find_element(by=By.TAG_NAME, value='h3').text,
        'fecha': fecha[0],
        'hora': fecha[1]
    })

# Acceso al dia actual en el calendario
driver.get('https://campusvirtual.uva.es/calendar/view.php?view=day')

numero_dia = date.today().day
numero_mes = date.today().month
numero_anio = date.today().year
fecha_a_buscar = str(numero_dia) + "/" + str(numero_mes) + "/" + str(numero_anio)


# Obtencion de la lista de eventos del dia
eventos_dia = driver.find_elements(by=By.CLASS_NAME, value='event')

for evento in eventos_dia:
    contenidoJSON['eventos_hoy'].append({
        'nombre': evento.find_element(by=By.TAG_NAME, value='h3').text,
        'fecha': fecha_a_buscar,
        'hora': formatear_hora(evento.find_element(by=By.CLASS_NAME, value='col-11').text.split(
        " » ")[0])
    })
    
with open(ficheroJSON, 'w') as ficheroDatosJSON:
    json.dump(contenidoJSON, ficheroDatosJSON, indent=4)
    
ficheroDatosJSON.close()

driver.close()

