import torch
from TTS.api import TTS
import nltk
from nltk.tokenize import sent_tokenize
from pydub import AudioSegment
import os
import spacy
from pydub.effects import speedup


# Cargar el modelo en español
nlp = spacy.load('es_core_news_sm')


def dividir_en_segmentos(texto, max_longitud=20):
    nlp = spacy.load("es_core_news_sm")
    doc = nlp(texto)
    segmentos = []

    for oracion in doc.sents:
        segmento_actual = []
        longitud_actual = 0

        for token in oracion:
            segmento_actual.append(token.text)
            longitud_actual += 1

            # Punto de corte basado en la longitud y ciertos signos de puntuación
            if token.text in [".", ",", ";", ":", "—","/n"] and longitud_actual >= max_longitud:
                segmento = ' '.join(segmento_actual).strip()
                if segmento:
                    segmentos.append(segmento)
                segmento_actual = []
                longitud_actual = 0

        # Añadir el último segmento si hay alguno y no es solo un salto de línea
        segmento = ' '.join(segmento_actual).strip()
        if segmento and not segmento.isspace():
            segmentos.append(segmento)

    # Eliminar comas al final de cada segmento
    segmentos = [seg.rstrip(",") for seg in segmentos]
    return segmentos


def adjust_speed(audio_segment, speed):
    # Adjust the speed of an audio segment
    # Speed less than 1.0 slows down, greater than 1.0 speeds up
    return speedup(audio_segment, playback_speed=speed)

def generar_audio_tts(oraciones, output_dir):
    # Asegurarse de que el directorio de salida existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    archivos_audio = []
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    for i, oracion in enumerate(oraciones):
        output_file = os.path.join(output_dir, f"output_{i}.wav")
        # Generar el archivo de audio para la oración
        speaker_wav_path = "E:\\code\\Video 2\\video1.3.mp3"
        tts.tts_to_file(text=oracion, speaker_wav=speaker_wav_path, language="es", file_path=output_file)
        archivos_audio.append(output_file)

    return archivos_audio

def combinar_archivos_audio(archivos_audio, archivo_final="output_final.wav"):
    combined = AudioSegment.empty()
    for archivo in archivos_audio:
        audio = AudioSegment.from_wav(archivo)
        audio = adjust_speed(audio, speed=1.25)
        combined += audio

    combined.export(archivo_final, format="wav")
    for archivo in archivos_audio:
        os.remove(archivo)


def voz(string):
    oraciones = dividir_en_segmentos(string)
    path_audio = "E:\\code\\Video 2\\audio_outputs"
    archivos_audio = generar_audio_tts(oraciones, path_audio)

    # Nombre del archivo de audio combinado
    archivo_final = "output_final.wav"
    path_archivo_final = os.path.join(path_audio, archivo_final)

    # Combinar en un archivo final
    combinar_archivos_audio(archivos_audio, path_archivo_final)
    
    # Retorna la ruta completa del archivo de audio combinado
    return path_archivo_final

#ejemplo= "Cuando hablamos de filosofía, nos referimos al estudio de la existencia, la vida y los fenómenos que la rodean. Es una disciplina que se remonta a la antigüedad, con filósofos como Sócrates, Platón y Aristóteles que llevaron a cabo investigaciones profundas sobre el mundo que nos rodea. Sin embargo, en el ámbito de la filosofía, se puede encontrar también un rincón oscuro, que alberga al nihilismo./nEl nihilismo es una corriente filosófica que cuestiona la existencia de cualquier tipo de valores, principios o sentido. Sus seguidores, los nihilistas, sostenían que la percepción del mundo es subjetiva y que, por lo tanto, no existe un orden inherente o verdades universales. Para ellos, la realidad es irreal, y la realidad del ser humano es una construcción falsa. En consecuencia, el nihilismo es a menudo visto como una posición de negación de la existencia misma./nComo forma de pensamiento, el nihilismo ha encontrado expresión en numerosos campos, desde la filosofía política, hasta la ética y la estética. Desde una perspectiva política, los nihilistas rechazan cualquier tipo de estructura social o política, ya que consideran que no existen principios éticos o morales sólidos. En cuanto a la ética, el nihilismo se opone a cualquier tipo de valoración moral, ya que creen que no existen valores universales absolutos. En lo que respecta a la estética, los nihilistas negarían la existencia de una belleza intrínseca y objetiva, ya que no existe un orden inherente en el mundo./nLa idea del nihilismo tiene sus orígenes en la Antigüedad, aunque fue durante el siglo XIX que adquirió popularidad. Filósofos como Fiódor Dostoievski y Friedrich Nietzsche, fueron algunos de los principales defensores de este pensamiento. En particular, Nietzsche se hizo famoso por su afirmación de que Dios estaba muerto, lo que llevó a una crisis de valores. Para él, la desaparición de la religión y las creencias tradicionales dejó una sensación de vacío en la vida de la gente./nAunque el nihilismo se ha convertido en un tema de discusión en numerosas obras literarias y artísticas, a lo largo de la historia, no ha sido aceptado como una filosofía plenamente desarrollada. Aun así, su legado ha sido significativo, ya que ha influido en varias corrientes del pensamiento, desde el existencialismo hasta el postmodernismo./nEn síntesis, el nihilismo es una filosofía que cuestiona la existencia de cualquier tipo de valores, principios, sentido y verdades universales. Tras su emergencia en el siglo XIX, ha influido en numerosas áreas del pensamiento, y aunque no es una filosofía en sí misma, sus ideas siguen siendo relevantes y activas en el debate filosófico contemporáneo   ."
