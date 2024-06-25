from tts2 import generar_audio_tts_y_guardar
from tts2 import dividir_en_segmentos
from tts2 import guardar_oraciones_json, combinar_archivos_audio
from comfyui import generate_random_15_digit_number
from promp import obtener_prompt_sentence,obtener_prompt_context,obtener_prompt_negative
import json
import os
import time
import re
separator = "-" * 50
from comfyui import json_imagen
from video import create_video3_with_transitions, create_video3_with_transitions_music
from video import create_video3
from borrar import borrar_contenido
from pydub import AudioSegment
from Narracion import obtener_narracion
from py1 import procesar_archivo_excel
from Narracion import obtener_titul, obtener_hashtags
from promp import obtener_short_narrative     
from promp import parse_prompts, parse_detailed_prompts  
from promp import obtener_prompt_context, obtener_hashtags
from comfyui import json_imagen
from comfyui import generate_random_15_digit_number
from video import create_video, create_video3_without_music
from tts import voz
import os
import time
import json
import re
from fullsub import fullsub
from promp import obtener_prompt_negative
from promp import obtener_prompt_video 
from video import audio_duration
def prompt_detail_json(datos, narracion, oraciones,titulo):
    
    prompts_mejorados = {}
    
    for indice, elemento in enumerate(oraciones, start=1):
        clave = str(indice)  # Convierte el índice a cadena para usar como clave
        oracion = elemento['oracion']
        oracion2=f"{oracion}+{titulo}"
        descripcion_datos = datos.get(clave, "Descripción no disponible")
        descripcion_mejorada = obtener_prompt_context(narracion,descripcion_datos,oracion2)
        # Combina los elementos para formar una descripción mejorada, incluyendo la narración directamente.
        #descripcion = f"{descripcion_datos} Narración: {narracion} Oración: {oracion}"
        #print (descripcion)
        prompts_mejorados[clave] = descripcion_mejorada
        print(separator)
        print(descripcion_mejorada)
        print(separator)
    
    return prompts_mejorados
def remove_categories(text):
    import re
    modified_text = re.sub(r'\n.*?:\s', '\n', text)
    return modified_text

def extraer_titulo(texto):
    match = re.search(r'Título.*?:\s*(.*)', texto)
    return match.group(1) if match else None

def limpiar_titulo(titulo):
    if isinstance(titulo, str):
        # Reemplaza o elimina caracteres no permitidos en nombres de archivos y carpetas, pero mantiene los signos de interrogación
        titulo_limpio = re.sub(r'[<>:"/\\|*]', '', titulo)  # Elimina caracteres no permitidos excepto los signos de interrogación
        return titulo_limpio
    else:
        # Manejar el caso en que el título no es una cadena
        raise ValueError("El título proporcionado no es una cadena de texto")

def guardar_variable_en_txt(nombre_archivo, variable):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(str(variable))
def crear_carpeta_con_titulo(titulo_li):
    # Ruta base donde se crearán las carpetas
    base_path = "E:\\code\\Video 2\\videossalida"

    # Construir la ruta completa de la nueva carpeta
    folder_path = os.path.join(base_path, titulo_li)

    # Crear la carpeta si no existe
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        print("La carpeta ya existe.")

    # Devolver la ruta de la carpeta
    return folder_path
def crear_archivo_texto(titulo, descripcion, gash_tags, carpeta):
    # Asegurarse de que la ruta de la carpeta termine con un separador de ruta
    if not carpeta.endswith(os.path.sep):
        carpeta += os.path.sep

    # Nombre del archivo .txt, guardado en la carpeta especificada
    file_name = carpeta + titulo + ".txt"

    # Crear o abrir el archivo en modo escritura
    with open(file_name, 'w', encoding='utf-8') as file:
        # Escribir el título
        file.write(titulo + "\n\n")

        # Escribir la descripción
        file.write(descripcion + "\n\n")

        # Escribir los hashtags
        if gash_tags:
            hashtags_formatted = " ".join(["#" + tag for tag in gash_tags.split()])
            file.write(hashtags_formatted)

    return file_name
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def verify_and_correct_path(file_path):
    # Correct the path by converting it to a raw string
    corrected_path = r"{}".format(file_path)

    # Verify if the path exists
    file_exists = os.path.exists(corrected_path)

    return corrected_path, file_exists

def monitor_directory(path, threshold, json_output_path):
    while True:
        try:
            # Lista todos los archivos en el directorio
            file_list = os.listdir(path)
            # Cuenta la cantidad de archivos
            file_count = len(file_list)

            print(f"Comprobando... {file_count} archivos encontrados.")  # Imprime la cantidad de archivos actual

            # Si se alcanza o supera el umbral, crea un archivo JSON
            if file_count >= threshold:
                image_data = {f"{i}": os.path.join(path, file) for i, file in enumerate(file_list, start=1)}
                with open(json_output_path, 'w') as json_file:
                    json.dump(image_data, json_file, indent=4)
                
                print(f"Archivo JSON creado con {file_count} elementos.")
                break  # Termina el bucle después de crear el archivo JSON
            else:
                print(f"Esperando a alcanzar el umbral de {threshold} archivos...")

            # Espera 10 segundos antes de la próxima comprobación
            time.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
            break
        
# Ruta al directorio a monitorear
directory_path = "C:\\Users\\jairc\\Pictures\\ComfyUI\\output\\video"
def cargar_json(nombre_archivo):
    try:
        # Check if the file is empty before loading
        if os.path.getsize(nombre_archivo) == 0:
            print("El archivo está vacío.")
            return []
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        print("El archivo no se encontró.")
        return []
    except json.JSONDecodeError:
        print("Error al decodificar JSON. El archivo no está correctamente formateado.")
        return []

def procesar_oraciones(oraciones):
    for i, oracion in enumerate(oraciones):
        prompt=obtener_prompt_sentence(oracion)
        print(f"Oración {i+1}: {oracion}")
        print(prompt)
 

def procesar_oraciones_desde_json(datos):
    if datos:
        for i, dato in enumerate(datos):
            
            oracion = dato['oracion']
            prompt=obtener_prompt_sentence(oracion)
            print(separator)
            print(f"Oración {i+1}: {oracion}")
            print(separator)
            print(prompt)
            
            dato['prompt'] = prompt
        # Guardar los datos modificados de vuelta al archivo JSON.
        with open("oraciones_modificadas.json", "w", encoding="utf-8") as archivo_modificado:
            json.dump(datos, archivo_modificado, ensure_ascii=False, indent=4)
        print("Datos procesados y guardados exitosamente.")
    else:
        print("No hay datos para procesar.")

def agrupar_audios(json_input, num_oraciones):
    # Inicializar la lista para almacenar los grupos de audios
    audios_agrupados = []
    # Inicializar una lista temporal para agrupar oraciones y audios
    grupo_temporal = []
    
    for i, item in enumerate(json_input):
        # Añadir el elemento actual al grupo temporal
        grupo_temporal.append(item)
        # Verificar si se alcanzó el número deseado de oraciones para agrupar o es el último elemento
        if (i + 1) % num_oraciones == 0 or i == len(json_input) - 1:
            # Procesar el grupo temporal
            archivos_agrupados = [elem['archivo_audio'] for elem in grupo_temporal]
            # Añadir a la lista de audios agrupados
            audios_agrupados.append({
                "archivo_audio": archivos_agrupados
            })
            # Reiniciar el grupo temporal para el siguiente lote
            grupo_temporal = []
    
    # Retornar el nuevo JSON de audios agrupados
    return audios_agrupados


def combinar_audios_y_guardar(grupos_de_audios):
    audios_combinados = []
    for index, grupo in enumerate(grupos_de_audios):
        # Inicializa un segmento de audio vacío
        combinado = AudioSegment.empty()
        for archivo in grupo['archivo_audio']:
            # Carga el archivo .wav actual y lo añade al segmento combinado
            audio = AudioSegment.from_wav(archivo)
            combinado += audio
        # Define el directorio y verifica si existe, crea si no existe
        output_dir = "E:\\code\\Video 2\\audio_outputs2"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Define el nombre del nuevo archivo combinado
        nuevo_nombre_archivo = os.path.join(output_dir, f"output_{index}_new.wav")
        # Exporta el audio combinado al nuevo archivo
        combinado.export(nuevo_nombre_archivo, format="wav")
        # Añade el path del nuevo archivo combinado a la lista
        audios_combinados.append({"archivo_audio": nuevo_nombre_archivo})
    return audios_combinados

def procesar_oraciones(datos, n, titulo):
    prompts_ordenados = []
    oraciones_procesadas = []

    i = 0
    while i < len(datos):
        oraciones_compuestas = " ".join(datos[j]['oracion'] for j in range(i, min(i+n, len(datos))))
        oraciones_procesadas.append(oraciones_compuestas)
        oraciones_compuestas2= f"{oraciones_compuestas}+{titulo}"
        prompt = obtener_prompt_sentence(oraciones_compuestas2)
        prompts_ordenados.append(prompt)
        
        print("Procesando oración(es):", oraciones_compuestas)
        print("Prompt resultado:", prompt)

        i += n

    # Crear un nuevo objeto JSON para almacenar los prompts ordenados
    json_data = {str(i): prompt for i, prompt in enumerate(prompts_ordenados, start=1)}
    
    # Guardar los prompts ordenados en un archivo JSON
    archivo_modificado_path = "oraciones_modificadas.json"
    with open(archivo_modificado_path, "w", encoding="utf-8") as archivo_modificado:
        json.dump(json_data, archivo_modificado, ensure_ascii=False, indent=4)
    
    print("Prompts procesados y guardados exitosamente en:", archivo_modificado_path)
    
    return archivo_modificado_path, json_data

def limpiar_narracion_de_hashtags(narracion):
    """
    Esta función elimina cualquier texto que comience con '#' y cualquier espacio antes del hashtag,
    y guarda los hashtags encontrados en una lista separada.
    Se asume que los hashtags pueden estar separados por espacios y no necesariamente al final de la oración.
    """
    # Regex para encontrar hashtags
    hashtags = re.findall(r'\s?#([\wÁÉÍÓÚáéíóúÑñ]+)', narracion)
    
    # Regex para eliminar hashtags y espacios opcionales antes de estos
    narracion_limpia = re.sub(r'\s?#[\wÁÉÍÓÚáéíóúÑñ]+', '', narracion)
    
    return narracion_limpia, hashtags

"""
def procesar_oraciones_en_pares(datos):
    prompts_ordenados = []
    i = 0
    while i < len(datos) - 1:  # Ensure not to go out of range
        oracion_compuesta = datos[i]['oracion'] + " " + datos[i+1]['oracion']
        prompt = obtener_prompt_sentence(oracion_compuesta)
        
        # Store the generated prompt for each pair, avoiding repetition
        if prompt not in prompts_ordenados:
            prompts_ordenados.append(prompt)
        
        i += 2  # Move to the next pair
        
    # Create a new JSON object to store the ordered prompts without repetition
    json_data = {str(i): prompt for i, prompt in enumerate(prompts_ordenados, start=1)}
    
    # Save the ordered prompts to a JSON file
    archivo_modificado_path = "oraciones_modificadas.json"
    with open(archivo_modificado_path, "w", encoding="utf-8") as archivo_modificado:
        json.dump(json_data, archivo_modificado, ensure_ascii=False, indent=4)
    print("Ordered prompts processed and saved successfully.")
    
    return archivo_modificado_path, json_data
"""
def generar_videos():
    try:
        borrar_contenido()
        code=generate_random_15_digit_number()
            
        tema = procesar_archivo_excel("E:\\code\\Video 2\\inputs videos\\animalandIA\\animalandia.xlsx")
        #tema = procesar_archivo_excel("E:\\code\\Video 2\\inputs videos\\visiones de una mente artificial\\visiones de una mente artificia.xlsx")
        #tema = procesar_archivo_excel(r"E:\code\Video 2\inputs videos\filosofai\Filosofai.xlsx")
        print(tema)
        tema2 = json.loads(tema)
        title = tema2[0]["Título Semilla"]

        narracion = obtener_narracion(tema)
        narracion_str = str(narracion)
        titulo = title
        titulo_str = str(titulo)

        try:
            titulo_li = limpiar_titulo(titulo_str)
        except ValueError as e:
            print(e)
            # Manejar el error, como establecer un título por defecto o saltar el procesamiento
            titulo_li = "titulo_por_defecto"
        carpeta = crear_carpeta_con_titulo(titulo_li)
        narracionfix = remove_categories(narracion)
        print("La narración es: ")
        
        narracion_limpia, hash= limpiar_narracion_de_hashtags(str(narracionfix))
        print(narracion_limpia)
        guardar_variable_en_txt("narracion.txt", narracion_limpia)
        print(hash)
        hashtags = obtener_hashtags(str(narracion_limpia))
        metadata= crear_archivo_texto(titulo_li," ",hashtags,carpeta)
        print(metadata)

        ejemplo= """ 
        Imagina protegerte de un peligro con tu propio cuerpo. ¿Cómo serías capaz de hacerlo? Encontramos una respuesta en el armadillo, un animal curioso de América del Sur que posee tácticas de supervivencia impresionantes",

        mostramos a un armadillo atravesando una savana en movimientos cautelosos, de repente detecta un coyote a su alcance. Inmediatamente, se enrolla en un globo compacto con una agilidad que deja sin aliento.

        La clave de esta defensa está en su caparazón, una armadura única y rígida formada por placas óseas, un arma natural que lo protege de sus depredadores. Puedes contar hasta cinco en menos de un segundo: cada uno de los cinco huesos de cada placa del caparazón de un armadillo se mueve bruscamente en respuesta a cualquier sensación de peligro.

        Al ver cómo el pequeño mamífero se protege en un esfuerzo instantáneo, nos enseña la importancia de adaptar y sobrevivir en un mundo hostil. Esta táctica del enrolling es solo un ejemplo de cómo el armadillo ha desarrollado adaptaciones increíbles para enfrentar la vida.

        Ahora que conoces este detalle curioso, ¡comparte con tus amigos cómo otros animales se defienden y explora la diversidad de estrategias de supervivencia en nuestro planeta.
        """
        #hast,narracion_limpia=limpiar_narracion_de_hashtags(str(narracionfix))  
        
        oraciones = dividir_en_segmentos(str(narracionfix))
        path_audio = "E:\\code\\Video 2\\audio_outputs"
        archivos_audio = generar_audio_tts_y_guardar(oraciones, path_audio)
        archivo_final = "output_final.wav"
        path_archivo_final = os.path.join(path_audio, archivo_final)
        combinar_archivos_audio(archivos_audio, path_archivo_final)

        guardar_oraciones_json(oraciones, archivos_audio)
        #procesar_oraciones_desde_json()
        code=generate_random_15_digit_number()
        datos = cargar_json("oraciones.json")  
        archivo_modificado_path, json_data = procesar_oraciones(datos,1," ")
        print(separator)
        print(json_data)
        print(separator)
        negative="(lowres, low quality, worst quality:1.2), (text:1.2), watermark, glitch, deformed, mutated, cross-eyed,hands,toy,naked"
        print(separator)
        print(separator)
        short_narrative=obtener_short_narrative(narracionfix)

        new_prompt=prompt_detail_json(json_data,short_narrative,datos," ")
        print(new_prompt)

        json_imagen(new_prompt,code,negative)
        print("El json de la imagen es:")
        print(json_imagen)
        finalpath= f"{directory_path}\\{code}"
        json_output_path = "output.json"
        length = len(json_data.items())
        monitor_directory(finalpath,length,json_output_path)

        #titulo_li="ejemplo2"
        carpeta = crear_carpeta_con_titulo(titulo_li)
        titulo_video= titulo_li + ".mp4"
        with open('output.json', 'r', encoding='utf-8') as file:
            output = json.load(file)

        with open('oraciones.json', 'r', encoding='utf-8') as file:
            oraciones = json.load(file)
        num_oraciones = 1 # Definir cuántas oraciones agrupar
        json_audios0 = agrupar_audios(oraciones, num_oraciones)
        json_audios = combinar_audios_y_guardar(json_audios0)
        # Imprimir el nuevo JSON para verificación
        print(json.dumps(json_audios, indent=4))
        carpeta_musica = "E:\\code\\Video 2\\Música App Tiktok\\Diálogos Filosóficos"
        #vide= create_video3_with_transitions_music(output,json_audios, carpeta, titulo_video,carpeta_musica)
        vide= create_video3_without_music(output,json_audios, carpeta, titulo_video)
        corrected_path, exists = verify_and_correct_path(vide)
        print(exists)
        print(vide)
        #path = r"E:\code\Video 2\videossalida\La Sorprendente Estrategia de Supervivencia del Pato\La Sorprendente Estrategia de Supervivencia del Pato.mp4"
        #res = fullsub(corrected_path)
        
    except Exception as e:
            print(f"Se encontró un error: {e}")
            
while True:
    generar_videos()