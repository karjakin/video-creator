import os
import json

# Función para borrar el contenido de archivos JSON específicos
def borrar_contenido_json(archivos_json):
    for archivo in archivos_json:
        try:
            with open(archivo, 'w') as f:
                json.dump({}, f)  # Escribe un diccionario vacío para borrar el contenido
            print(f"El contenido de {archivo} ha sido borrado.")
        except Exception as e:
            print(f"Error al borrar el contenido de {archivo}: {e}")

# Función para borrar todos los archivos dentro de las carpetas específicas
def borrar_contenido_carpetas(carpetas):
    for carpeta in carpetas:
        try:
            for archivo in os.listdir(carpeta):
                ruta_archivo = os.path.join(carpeta, archivo)
                if os.path.isfile(ruta_archivo):
                    os.remove(ruta_archivo)
            print(f"Todos los archivos en {carpeta} han sido borrados.")
        except Exception as e:
            print(f"Error al borrar los archivos en {carpeta}: {e}")

def borrar_contenido():
    # Lista de archivos JSON a borrar
    archivos_json = ['oraciones.json', 'oraciones_modificadas.json']
    # Lista de carpetas cuyo contenido se debe borrar
    carpetas = ['audio_outputs', 'audio_outputs2']
    # Llamando a las funciones
    borrar_contenido_json(archivos_json)
    borrar_contenido_carpetas(carpetas)

#borrar_contenido()
