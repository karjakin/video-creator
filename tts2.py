import os
import json
import torch
from TTS.api import TTS  # Asegúrate de que esta importación refleje cómo accedes a TTS en tu entorno
from pydub import AudioSegment
import spacy
from pydub.effects import speedup

# Cargar el modelo en español de Spacy
nlp = spacy.load('es_core_news_sm')

def dividir_en_segmentos(texto, max_longitud=27):
    doc = nlp(texto)
    segmentos = []

    for oracion in doc.sents:
        segmento_actual = []
        longitud_actual = 0

        for token in oracion:
            segmento_actual.append(token.text)
            longitud_actual += 1

            if token.text in [".", ",", ";", ":", "—"] and longitud_actual >= max_longitud:
                segmento = ' '.join(segmento_actual).strip()
                if segmento:
                    segmentos.append(segmento)
                segmento_actual = []
                longitud_actual = 0

        segmento = ' '.join(segmento_actual).strip()
        if segmento and not segmento.isspace():
            segmentos.append(segmento)

    segmentos = [seg.rstrip(",") for seg in segmentos]
    return segmentos


def generar_audio_tts_y_guardar(oraciones, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    archivos_audio = []
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)  # Asegúrate de que la ruta del modelo es correcta

    for i, oracion in enumerate(oraciones):
        output_file = os.path.join(output_dir, f"output_{i}.wav")
        # Asume que tienes un archivo de audio del locutor; ajusta según sea necesario
        speaker_wav_path = r"C:\Users\jairc\Downloads\max.mpeg"
        tts.tts_to_file(text=oracion, speaker_wav=speaker_wav_path, language="es", file_path=output_file)
        archivos_audio.append(output_file)

    return archivos_audio

def combinar_archivos_audio(archivos_audio, archivo_final="output_final.wav"):
    combined = AudioSegment.empty()
    for archivo in archivos_audio:
        audio = AudioSegment.from_wav(archivo)
        combined += audio
    combined.export(archivo_final, format="wav")

def adjust_speed(audio_segment, speed):
    # Adjust the speed of an audio segment
    # Speed less than 1.0 slows down, greater than 1.0 speeds up
    return speedup(audio_segment, playback_speed=speed)

def guardar_oraciones_json(oraciones, archivos_audio, nombre_archivo="oraciones.json"):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            # Intenta cargar el archivo existente
            try:
                datos = json.load(archivo)
                # Asegúrate de que datos sea una lista, si no, inicialízala como una lista vacía
                if not isinstance(datos, list):
                    datos = []
            except json.JSONDecodeError:
                # Si el archivo está vacío o mal formateado, inicializa como lista vacía
                datos = []
    except FileNotFoundError:
        # Si el archivo no existe, inicializa como lista vacía
        datos = []

    # Añade las nuevas oraciones y archivos de audio a la lista de datos
    for oracion, archivo_audio in zip(oraciones, archivos_audio):
        datos.append({"oracion": oracion, "archivo_audio": archivo_audio})

    # Guarda el contenido actualizado en el archivo JSON
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


#combinar_archivos_audio(archivos_audio, "output_final.wav")
if __name__=="__main__":       
    narracion="""
    Que pinche calor hace en Cuautla
    En ese Vips me cobraron el aire acondicionado, mejor una pancita de Don Chendo
    Vamos a ver el desfile del 2 de mayo
    Siéntate un rato conmigo en la Alameda
    """
    segmentos = dividir_en_segmentos(narracion)
    print(segmentos)
    path_audio = "E:\\code\\Video 2\\audio_outputs"
    archivos_audio = generar_audio_tts_y_guardar(segmentos, path_audio)