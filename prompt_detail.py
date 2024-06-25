separator = "-" * 50
import json
from promp import obtener_prompt_context, obtener_short_narrative 
from sentence import cargar_json, procesar_oraciones


def guardar_json(datos, nombre_archivo):
    
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

def imprimir_json(datos):
    """Imprime cada elemento de un diccionario JSON."""
    for clave, valor in datos.items():
        print(f"Elemento {clave}: {valor}\n")



def prompt_detail_json(datos, narracion, oraciones):
    
    prompts_mejorados = {}
    
    for indice, elemento in enumerate(oraciones, start=1):
        clave = str(indice)  # Convierte el índice a cadena para usar como clave
        oracion = elemento['oracion']
        descripcion_datos = datos.get(clave, "Descripción no disponible")
        descripcion_mejorada = obtener_prompt_context(narracion,descripcion_datos,oracion)
        # Combina los elementos para formar una descripción mejorada, incluyendo la narración directamente.
        #descripcion = f"{descripcion_datos} Narración: {narracion} Oración: {oracion}"
        #print (descripcion)
        prompts_mejorados[clave] = descripcion_mejorada
        print(descripcion_mejorada)
    
    return prompts_mejorados




"""
datos = cargar_json("oraciones.json")  
print(datos)
#archivo_modificado_path, json_data = procesar_oraciones(datos,1)
print(separator)
#print(json_data)
print(separator)
json_data= cargar_json("prompts.json")
#guardar_json(json_data,"prompts.json")
#imprimir_json(json_data)
"""
ejemplo= """
¿Cómo se aseguran las plantas de regiones con mucho viento y áreas tranquilas de propagar su semilla y mantener su especie? Este es el enigma que nos invita a explorar estrategias de polinización únicas.

En regiones ventosas, las flores han desarrollado adaptaciones para aprovechar el viento. Un ejemplo son las flores erectas y con forma de bandera que utilizan el viento para dispersar polen, como las del género Plantago. Estas estrategias son cruciales para sobrevivir en ambientes desafiantes.

Por otro lado, en áreas tranquilas, la polinización se debe a visitas de animales. Las plantas crean nectar y emiten aromas para atraer abejas, mariposas y otros polinizadores, y protegen su polen con estructuras como el pelusco en las flores del género Echium.

La diversidad de estrategias de polinización entre estas regiones nos muestra la increíble adaptación de las plantas para sobrevivir y prosperar en entornos diferentes.

Ahora, ¿cómo comparar y contrastar estos sorprendentes mecanismos? Aprende más sobre estas Estrategias de Polinización de las Plantas de Regiones Ventosas y Plantas de Regiones Tranquilas, y descubre cómo la naturaleza nos enseña a ajustarnos y prosperar en circunstancias desafiantes. ¡Compara y Contrasta!
"""
"""
ejemplo2=obtener_short_narrative(ejemplo)
print(ejemplo2)
a=prompt_detail_json(json_data,ejemplo2,datos)
print(a)
"""

