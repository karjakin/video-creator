from Narracion import obtener_narracion
from py1 import procesar_archivo_excel
from Narracion import obtener_titul, obtener_hashtags
from promp import obtener_prompt        
from promp import parse_prompts, parse_detailed_prompts  
from promp import obtener_prompt_context   
from comfyui import json_imagen
from comfyui import generate_random_15_digit_number
from video import create_video
from tts import voz
import os
import time
import json
import re
from fullsub import fullsub
from promp import obtener_prompt_negative
from promp import obtener_prompt_video 
from video import audio_duration


def monitor_directory(path, threshold, json_output_path):
    while True:
        try:
            # Lista todos los archivos en el directorio
            file_list = os.listdir(path)
            # Cuenta la cantidad de archivos
            file_count = len(file_list)

            # Si se alcanza o supera el umbral, crea un archivo JSON
            if file_count >= threshold:
                image_data = {f"{i}": os.path.join(path, file) for i, file in enumerate(file_list, start=1)}
                with open(json_output_path, 'w') as json_file:
                    json.dump(image_data, json_file, indent=4)
                
                print(f"Archivo JSON creado con {len(image_data)} elementos.")
                break  # Termina el bucle después de crear el archivo JSON

            # Espera 10 segundos antes de la próxima comprobación
            time.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
            break
# Ruta al directorio a monitorear
directory_path = "C:\\Users\\jairc\\Pictures\\ComfyUI\\output\\video"

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
def generar_videos():
    try:
        # Llamada a la función para obtener la narración
        code=generate_random_15_digit_number()
        
        tema = procesar_archivo_excel("E:\\code\\Video 2\\inputs videos\\animalandIA\\animalandia.xlsx")
        #tema = procesar_archivo_excel("C:\\Users\\Reyes\\Documents\\Main\\AletheAI\\VideoSubidaTikTok\\Video 2\\inputs videos\\visiones de una mente artificial\\visiones de una mente artificia.xlsx")
        #tema = procesar_archivo_excel("C:\\Users\\Reyes\\Documents\\Main\\AletheAI\\VideoSubidaTikTok\\Video 2\\inputs videos\\filosofai\\Filosofai.xlsx")
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
        print(narracion)
        guardar_variable_en_txt("narracion.txt", narracionfix)

        vozz = voz(narracionfix)
        print("La voz es: ")
        print(vozz)
        length = 0
        while length < 7:
            prompts = obtener_prompt(narracion_str)
            prompts_str = str(prompts)
            print("El primer prompt es:")
            print(prompts_str)
            prompts_str = obtener_prompt_context(narracion_str,prompts_str)
            prompts_str = str(prompts_str)
            print("El prompt con contexto es:")
            print(prompts_str)
            negative = obtener_prompt_negative(prompts_str)
            negative = str(negative)
            print("Los negativos son: ")
            print(negative)
            json_output = parse_prompts(prompts_str)
            print(json_output)
            length = len(json_output.items())

        json_imagen(json_output,code,negative)
        print("El json de la imagen es:")
        print(json_imagen)
        finalpath= f"{directory_path}\\{code}"
        json_output_path = "output.json"
        monitor_directory(finalpath,length,json_output_path)
        with open("output.json", 'r') as json_file:
            json_data = json.load(json_file)
        titulo_video= titulo_li + ".mp4"
        #provicionales---
        descripcion = "Esta es una descripción detallada del contenido del archivo."
        
        gash_tags = "etiqueta1 etiqueta2 etiqueta3"


        metadata= crear_archivo_texto(titulo_li,descripcion,gash_tags,carpeta)
        audio_length=audio_duration(r"./audio_outputs/output_final.wav")
        video_segmentation = obtener_prompt_video(narracion_str,length,prompts_str,audio_length)
        print("El video segmentado es: ")
        
        print(video_segmentation,audio_length)
        vide= create_video(json_data, r"./audio_outputs/output_final.wav", carpeta, titulo_video)
        corrected_path, exists = verify_and_correct_path(vide)
        print(exists)
        print(vide)
        final= fullsub(corrected_path)
        #pause until enter is pressed
        input("Press Enter to continue...")
        
        """
        # Session ID (presumably for the upload session)
        session_id = "0c7712ba3c842f59075de2b71ddb81a9"

        # Construct the full file path for the video
        file_path = final

        titulo = obtener_titul(tema)
        print(titulo)
        print("_--------------")
        titulo_str = str(titulo)
        print (titulo_str)
        print("_--------------")
        # Title and tags for the video
        title = titulo_str
        title2= limpiar_titulo(title)
        tags = obtener_hashtags(tema)



        # Publish the video
        
        uploadVideo(session_id, file_path, title2, tags)

        print("Video generado con éxito.")
        """
    except Exception as e:
        print(f"Se encontró un error: {e}")
        # Aquí manejas el error, pero no detienes el bucle

while True:
    generar_videos()  # Opcional: Agrega una pausa si es necesario
    # time.sleep(segundos_de_espera)
