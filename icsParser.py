import json

from icalendar import Calendar

# Fichero JSON donde almacenar la informacion
ficheroJSON = '/home/serggom/scraping/datos.json'
contenidoJSON = {'eventos': []}

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

    contenidoJSON['eventos'].append({
        'nombre': nombre_a_guardar,
        'fecha': fecha_a_guardar,
        'hora': hora_a_guardar
    })

with open(ficheroJSON, 'a') as ficheroDatosJSON:
    json.dump(contenidoJSON, ficheroDatosJSON, indent=4)

ficheroDatosJSON.close()
