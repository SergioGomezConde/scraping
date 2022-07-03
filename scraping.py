import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def formatear_nombre(nombre_a_formatear):
    """
    :param nombre_a_formatear: nombre obtenido del Campus Virtual
    :return: nombre con un formato mas legible
    """
    nombres = nombre_a_formatear.split(' ')
    nombre_formateado = nombres[2].capitalize() + " " + nombres[0].capitalize() + " " + nombres[1].split(',')[
        0].capitalize()

    return nombre_formateado


# Fichero JSON donde almacenar la informacion
ficheroJSON = '/home/serggom/scraping/datos.json'
contenidoJSON = {'asignaturas': [], 'usuario': [], 'eventos': [], 'numero_mensajes': []}

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
URLPerfil = driver.find_element(by=By.XPATH,
                                value='/html/body/div[4]/div[2]/header/div/div/div/div[1]/div[1]/div/div[1]/a') \
    .get_attribute('href')
driver.get(URLPerfil)

# Obtencion del nombre
nombre_perfil = driver.find_element(by=By.XPATH,
                                    value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div[1]/div/div[1]/h3') \
    .text

# Acceso a la seccion de asignaturas
time.sleep(2)
driver.find_element(by=By.XPATH,
                    value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div[2]/div/div/ul/li[1]/a') \
    .click()

# Obtencion de las asignaturas
time.sleep(2)
elementos = driver.find_element(by=By.XPATH,
                                value='/html/body/div[4]/div[2]/div/div/section/'
                                      'div/div/div/div[2]/div/div/div/div[1]') \
    .find_elements(by=By.TAG_NAME, value='a')

# Obtencion de los porcentajes
porcentajes = driver.find_elements(by=By.CLASS_NAME, value='progress-circle')
i = 0

# Almacenamiento de la informacion en el fichero JSON
for elemento in elementos:
    nombre_asignatura = elemento.text.split(' (')[0].capitalize()

    if nombre_asignatura != "":
        plan_asignatura = elemento.text.split('-')[2]
        codigo_asignatura = elemento.text.split('-')[3]
        enlace_asignatura = elemento.get_attribute('href')
        porcentaje_asignatura = porcentajes[i].get_attribute('data-progress')

        contenidoJSON['asignaturas'].append({
            'nombre': nombre_asignatura,
            'porcentaje': porcentaje_asignatura,
            'plan': plan_asignatura,
            'codigo': codigo_asignatura,
            'enlace': enlace_asignatura,
            'enlace_participantes': enlace_participantes
        })

        i = i + 1


# Acceso a la seccion de detalles
driver.find_element(by=By.XPATH,
                    value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div[2]/div/div/ul/li[2]/a').click()

# Obtencion del email
time.sleep(2)
email = driver.find_element(by=By.XPATH,
                            value='/html/body/div[4]/div[2]/div/div/section/'
                                  'div/div/div/div[2]/div/div/div/div[2]/div/div/div/section[1]/div/ul/li[2]/dl/dd/a') \
    .text

# Almacenamiento de la informacion en el fichero JSON
contenidoJSON['usuario'].append({
    'nombre': formatear_nombre(nombre_perfil),
    'email': email
})

# Acceso a la seccion de mensajes
driver.get('https://campusvirtual.uva.es/message/index.php')

# Obtencion del numero de mensajes totales sin leer
time.sleep(10)
numeroMensajes = str(
    driver.find_element(by=By.XPATH, value='/html/body/nav/ul[2]/div[3]/a/div').get_attribute('aria-label').split(' ')[
        1])

time.sleep(20)

# Obtencion de los distintos numeros de mensajes
xpath_base = '/html/body/div[4]/div[2]/div/div/section/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/'

total_destacados = str(driver.find_element(by=By.XPATH,
                                           value=xpath_base + 'div[1]/div[1]/button/small').get_attribute(
    'aria-label').split(' ')[0])

destacados_sin_leer = str(driver.find_element(by=By.XPATH,
                                              value=xpath_base + 'div[1]/div[1]/button/span[5]').get_attribute(
    'aria-label').split(' ')[1])

total_grupo = str(driver.find_element(by=By.XPATH,
                                      value=xpath_base + 'div[2]/div[1]/button/small').get_attribute(
    'aria-label').split(' ')[0])

grupo_sin_leer = str(driver.find_element(by=By.XPATH,
                                         value=xpath_base + 'div[2]/div[1]/button/span[5]').get_attribute(
    'aria-label').split(' ')[1])

total_privados = str(driver.find_element(by=By.XPATH,
                                         value=xpath_base + 'div[3]/div[1]/button/small').get_attribute(
    'aria-label').split(' ')[0])

privados_sin_leer = str(driver.find_element(by=By.XPATH,
                                            value=xpath_base + 'div[3]/div[1]/button/span[5]').get_attribute(
    'aria-label').split(' ')[1])

# Almacenamiento de la informacion en el fichero JSON
contenidoJSON['numero_mensajes'].append({
    'totales_sin_leer': str(numeroMensajes),
    'total_destacados': total_destacados,
    'destacados_sin_leer': destacados_sin_leer,
    'total_grupo': total_grupo,
    'grupo_sin_leer': grupo_sin_leer,
    'total_privados': total_privados,
    'privados_sin_leer': privados_sin_leer
})

driver.get('https://campusvirtual.uva.es/calendar/export.php?')

driver.find_element(by=By.XPATH,
                    value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/form/div[2]/div[2]/fieldset/div/'
                          'label[1]/input').click()
driver.find_element(by=By.XPATH,
                    value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/form/div[3]/div[2]/fieldset/div/'
                          'label[5]/input').click()

time.sleep(2)

driver.find_element(by=By.XPATH,
                    value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div/form/div[4]/div[2]/fieldset/div/'
                          'div[2]/span/input').click()

time.sleep(5)

c = open('icalexport.ics', 'rb')
calendario = Calendar.from_ical(c.read())
for vevent in calendario.walk('vevent'):
    tmp = vevent.decoded('dtstart')
    dateStart = str(tmp.astimezone().strftime('%Y-%m-%d %H:%M')).split(" ")
    nombre_a_guardar = vevent.get('summary')
    fecha = dateStart[0].split("-")
    numero_dia = fecha[2]
    numero_mes = fecha[1]
    numero_anio = fecha[0]
    fecha_a_guardar = numero_dia + "/" + numero_mes + "/" + numero_anio
    hora = dateStart[1].split(":")
    numero_hora = hora[0]
    numero_minuto = hora[1]
    hora_a_guardar = numero_hora + ":" + numero_minuto

    numero_dia_a_comparar = int(numero_dia)
    numero_mes_a_comparar = int(numero_mes)
    numero_anio_a_comparar = int(numero_anio)
    numero_hora_a_comparar = int(numero_hora)
    numero_minuto_a_comparar = int(numero_minuto)
    now = datetime.now()

    if (numero_anio_a_comparar > now.year) or \
            ((numero_anio_a_comparar == now.year) and (numero_mes_a_comparar > now.month)) or \
            ((numero_anio_a_comparar == now.year) and (numero_mes_a_comparar == now.month) and (
                    numero_dia_a_comparar > now.day)) or \
            ((numero_anio_a_comparar == now.year) and (numero_mes_a_comparar == now.month) and (
                    numero_dia_a_comparar == now.day) and (numero_hora_a_comparar > now.hour)) or \
            ((numero_anio_a_comparar == now.year) and (numero_mes_a_comparar == now.month) and (
                    numero_dia_a_comparar == now.day) and (numero_hora_a_comparar == now.hour) and (
                     numero_minuto_a_comparar > now.minute)):
        contenidoJSON['eventos'].append({
            'nombre': nombre_a_guardar,
            'fecha': fecha_a_guardar,
            'hora': hora_a_guardar
        })

with open(ficheroJSON, 'w') as ficheroDatosJSON:
    json.dump(contenidoJSON, ficheroDatosJSON, indent=4)

ficheroDatosJSON.close()

driver.close()
