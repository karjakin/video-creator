import os
import json
import time
import random
from datetime import datetime
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, TextClip, concatenate_audioclips
from moviepy.video.tools.subtitles import SubtitlesClip
#from subtitulo import generate_subtitles
from moviepy.editor import TextClip
from textwrap import wrap
from moviepy.editor import TextClip
from textwrap import wrap
from moviepy.editor import CompositeAudioClip
from PIL import ImageFile
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips, CompositeAudioClip, vfx

import os

ImageFile.LOAD_TRUNCATED_IMAGES = True


def time_str_to_seconds(time_str):
    hours, minutes, seconds = time_str.split(':')
    seconds, milliseconds = seconds.split(',')
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds) + float(milliseconds) / 1000

def audio_duration(audio_file_path):
    audio = AudioFileClip(audio_file_path)
    return audio.duration

def create_video(json_data, audio_file_path, ruta_carpeta_output, nombre_archivo, target_size=(1080, 1920)):
    # Cargar audio principal
    audio_clip = AudioFileClip(audio_file_path)
    duracion_audio = audio_clip.duration
    carpeta_musica = "E:\\code\\Video 2\\Música App Tiktok\\Diálogos Filosóficos"
    
    # Seleccionar un archivo de audio de fondo aleatoriamente
    archivos_musica = [f for f in os.listdir(carpeta_musica) if f.endswith(('.mp3', '.wav'))]
    archivo_musica_fondo = random.choice(archivos_musica)
    musica_fondo = AudioFileClip(os.path.join(carpeta_musica, archivo_musica_fondo))

     # Asegurarse de que la música de fondo sea lo suficientemente larga
    if musica_fondo.duration < duracion_audio:
        # Calcular cuántas veces repetir la música de fondo
        veces_repetir = int(duracion_audio / musica_fondo.duration) + 1
        musica_fondo = concatenate_audioclips([musica_fondo] * veces_repetir)
    
    
    # Ajustar la duración y el volumen del audio de fondo
    musica_fondo = musica_fondo.set_duration(duracion_audio).volumex(0.3)
    # Combinar el audio principal con el de fondo
    audio_combinado = CompositeAudioClip([audio_clip, musica_fondo])

    # Utilizar directamente el diccionario json_data, ya que no es necesario convertirlo de JSON
    archivos_imagenes = [path for path in json_data.values()]
    num_imagenes = len(archivos_imagenes)
    duracion_imagen = duracion_audio / num_imagenes

    # Crear clips con la nueva duración
    clips = []
    for i, ruta_img in enumerate(archivos_imagenes):
        clip = ImageClip(ruta_img).set_duration(duracion_imagen)
        if i > 0:
            clip = clip.crossfadein(duracion_imagen)
        clips.append(clip)

    # Concatenar clips
    video_final = concatenate_videoclips(clips, method="compose")
    video_final = video_final.set_audio(audio_combinado)
    path= ruta_carpeta_output + "\\"+ nombre_archivo
    

    video_final.write_videofile(os.path.join(ruta_carpeta_output, nombre_archivo), fps=24)

    return path



def create_video3(json_data, json_audios, ruta_carpeta_output, nombre_archivo, carpeta_musica, target_size=(1080, 1920)):
    clips = []
    duracion_total_audio = 0  # Inicializar la duración total del audio

    # Preparar clips de video con sus audios
    for id_img, ruta_audio_dict in zip(json_data.keys(), json_audios):
        ruta_img = json_data[id_img]
        ruta_audio = ruta_audio_dict["archivo_audio"]
        
        try:
            if not os.path.exists(ruta_img) or not os.path.exists(ruta_audio):
                print(f"Skipping: Image or audio file does not exist. Image: {ruta_img}, Audio: {ruta_audio}")
                continue

            audio_clip = AudioFileClip(ruta_audio)
            duracion_audio = audio_clip.duration
            duracion_total_audio += duracion_audio  # Sumar duración al total

            clip = ImageClip(ruta_img).set_duration(duracion_audio).resize(newsize=target_size)
            clip = clip.set_audio(audio_clip)
            clips.append(clip)
        except Exception as e:
            print(f"Error processing file: Image: {ruta_img}, Audio: {ruta_audio}. Error: {e}")
            continue

    if not clips:
        print("No valid images or audio found. Unable to create the video.")
        return None

    # Concatenar clips para formar el video final
    video_final = concatenate_videoclips(clips, method="compose")

    # Seleccionar y preparar la música de fondo para toda la duración del video
    archivos_musica = [f for f in os.listdir(carpeta_musica) if f.endswith(('.mp3', '.wav'))]
    archivo_musica_fondo = random.choice(archivos_musica)
    musica_fondo = AudioFileClip(os.path.join(carpeta_musica, archivo_musica_fondo))

    if musica_fondo.duration < duracion_total_audio:
        veces_repetir = int(duracion_total_audio / musica_fondo.duration) + 1
        musica_fondo = concatenate_audioclips([musica_fondo] * veces_repetir)

    musica_fondo = musica_fondo.set_duration(duracion_total_audio).volumex(0.3)

    # Combinar el audio de todos los clips con la música de fondo
    audio_combinado = CompositeAudioClip([video_final.audio, musica_fondo])
    video_final = video_final.set_audio(audio_combinado)

    video_final_path = os.path.join(ruta_carpeta_output, nombre_archivo)
    
    # Escribir el archivo de video en el disco
    video_final.write_videofile(video_final_path, fps=24)

    return video_final_path

def create_video3_with_transitions(json_data, json_audios, ruta_carpeta_output, nombre_archivo, carpeta_musica, target_size=(1080, 1920)):
    clips = []
    audio_clips = []
    duracion_total_video = 0
    tiempo_inicio_actual = 0  # Inicio del clip de audio actual

    # Cargar y preparar clips de imagen con audio
    for id_img, ruta_audio_dict in zip(json_data.keys(), json_audios):
        ruta_img = json_data[id_img]
        ruta_audio = ruta_audio_dict["archivo_audio"]
        
        if not os.path.exists(ruta_img) or not os.path.exists(ruta_audio):
            print(f"Skipping: Image or audio file does not exist. Image: {ruta_img}, Audio: {ruta_audio}")
            continue

        audio_clip = AudioFileClip(ruta_audio)
        duracion_audio = audio_clip.duration

        img_clip = ImageClip(ruta_img).set_duration(duracion_audio).resize(newsize=target_size)
        clips.append(img_clip)

        # Ajustar el audio para que comience en el tiempo correcto, sin sobrescribirse
        adjusted_audio_clip = audio_clip.set_start(tiempo_inicio_actual)
        audio_clips.append(adjusted_audio_clip)

        # Actualizar el tiempo de inicio para el próximo audio
        tiempo_inicio_actual += duracion_audio

    if not clips:
        print("No valid images or audio found. Unable to create the video.")
        return None

    # Aplicar transiciones entre clips y ajustar duración total del video
    final_clips = [clips[0]]
    for i in range(1, len(clips)):
        transition = 1  # Duración de la transición
        final_clips[-1] = final_clips[-1].crossfadeout(transition)
        clips[i] = clips[i].crossfadein(transition)
        final_clips.append(clips[i])
        # Restar la duración de la transición para el cálculo del tiempo de inicio del audio
        tiempo_inicio_actual -= transition

    # Concatenar clips con transiciones
    final_video = concatenate_videoclips(final_clips, method="compose")

    # Crear el clip de audio final ajustando los clips de audio
    final_audio = CompositeAudioClip(audio_clips)

    # Añadir música de fondo
    archivos_musica = [f for f in os.listdir(carpeta_musica) if f.endswith(('.mp3', '.wav'))]
    archivo_musica_fondo = random.choice(archivos_musica)
    musica_fondo = AudioFileClip(os.path.join(carpeta_musica, archivo_musica_fondo)).set_duration(tiempo_inicio_actual).volumex(0.3)

    # Combinar audio de clips con música de fondo
    final_audio_combined = CompositeAudioClip([final_audio, musica_fondo])
    final_video = final_video.set_audio(final_audio_combined)

    # Guardar el video final
    video_final_path = os.path.join(ruta_carpeta_output, nombre_archivo)
    final_video.write_videofile(video_final_path, fps=24)

    return video_final_path

def apply_random_effect(clip, target_size):
    effects = ['zoom_in', 'zoom_out', 'parallax']
    effect = random.choice(effects)

    if effect == 'zoom_in':
        # Asegurarse de que el efecto de zoom in no genere bordes negros ajustando adecuadamente
        zoom_factor = 1.0  # Iniciar sin zoom
        end_zoom_factor = 1.5  # Terminar con un poco de zoom
        return clip.resize(lambda t: min(zoom_factor + 0.005*t, end_zoom_factor)).set_duration(clip.duration)
    elif effect == 'zoom_out':
        # El efecto de zoom out comienza con la imagen completa y luego se aleja
        # Si este efecto es satisfactorio, lo dejamos como está
        start_zoom = 1.2  # Empezar un poco más grande
        end_zoom = 1.0  # Terminar al tamaño original
        return clip.resize(lambda t: max(start_zoom - 0.01*t, end_zoom)).set_duration(clip.duration)
    elif effect == 'parallax':
        # Ajuste de parallax para evitar bordes negros y hacer el movimiento más notable
        clip = clip.resize(width=clip.size[0]*1.1)  # Hacer la imagen un poco más ancha
        return clip.set_position(lambda t: ('center', max(0, 50 - 5*t)), relative=True)
    else:
        # Sin efecto, solo redimensionar al tamaño objetivo
        return clip.resize(target_size)
    
def create_video3_with_transitions_music(json_data, json_audios, ruta_carpeta_output, nombre_archivo, carpeta_musica, target_size=(1080, 1920)):
    clips = []
    audio_clips = []
    duracion_total_video = 0
    tiempo_inicio_actual = 0  # Inicio del clip de audio actual

    # Cargar y preparar clips de imagen con audio
    for id_img, ruta_audio_dict in zip(json_data.keys(), json_audios):
        ruta_img = json_data[id_img]
        ruta_audio = ruta_audio_dict["archivo_audio"]
        
        if not os.path.exists(ruta_img) or not os.path.exists(ruta_audio):
            print(f"Skipping: Image or audio file does not exist. Image: {ruta_img}, Audio: {ruta_audio}")
            continue

        audio_clip = AudioFileClip(ruta_audio)
        duracion_audio = audio_clip.duration

        img_clip = ImageClip(ruta_img).set_duration(duracion_audio).resize(newsize=target_size)
        clips.append(img_clip)

        # Ajustar el audio para que comience en el tiempo correcto, sin sobrescribirse
        adjusted_audio_clip = audio_clip.set_start(tiempo_inicio_actual)
        audio_clips.append(adjusted_audio_clip)

        # Actualizar el tiempo de inicio para el próximo audio
        tiempo_inicio_actual += duracion_audio

    if not clips:
        print("No valid images or audio found. Unable to create the video.")
        return None

    # Aplicar transiciones entre clips y ajustar duración total del video
    final_clips = [clips[0]]
    for i in range(1, len(clips)):
        transition = 1  # Duración de la transición
        final_clips[-1] = final_clips[-1].crossfadeout(transition)
        clips[i] = clips[i].crossfadein(transition)
        final_clips.append(clips[i])
        # Restar la duración de la transición para el cálculo del tiempo de inicio del audio
        tiempo_inicio_actual -= transition

    # Concatenar clips con transiciones
    final_video = concatenate_videoclips(final_clips, method="compose")

    # Crear el clip de audio final ajustando los clips de audio
    final_audio = CompositeAudioClip(audio_clips)

    # Añadir música de fondo
    archivos_musica = [f for f in os.listdir(carpeta_musica) if f.endswith(('.mp3', '.wav'))]
    archivo_musica_fondo = random.choice(archivos_musica)
    musica_fondo = AudioFileClip(os.path.join(carpeta_musica, archivo_musica_fondo)).set_duration(tiempo_inicio_actual).volumex(0.3)

    # Combinar audio de clips con música de fondo
    final_audio_combined = CompositeAudioClip([final_audio, musica_fondo])
    final_video = final_video.set_audio(final_audio_combined)

    # Guardar el video final
    video_final_path = os.path.join(ruta_carpeta_output, nombre_archivo)
    final_video.write_videofile(video_final_path, fps=24)

    return video_final_path
def create_video3_without_music(json_data, json_audios, ruta_carpeta_output, nombre_archivo, target_size=(1080, 1920)):
    clips = []
    audio_clips = []
    duracion_total_video = 0
    tiempo_inicio_actual = 0  # Inicio del clip de audio actual

    # Cargar y preparar clips de imagen con audio
    for id_img, ruta_audio_dict in zip(json_data.keys(), json_audios):
        ruta_img = json_data[id_img]
        ruta_audio = ruta_audio_dict["archivo_audio"]
        
        if not os.path.exists(ruta_img) or not os.path.exists(ruta_audio):
            print(f"Skipping: Image or audio file does not exist. Image: {ruta_img}, Audio: {ruta_audio}")
            continue

        audio_clip = AudioFileClip(ruta_audio)
        duracion_audio = audio_clip.duration

        img_clip = ImageClip(ruta_img).set_duration(duracion_audio).resize(newsize=target_size)
        clips.append(img_clip)

        # Ajustar el audio para que comience en el tiempo correcto, sin sobrescribirse
        adjusted_audio_clip = audio_clip.set_start(tiempo_inicio_actual)
        audio_clips.append(adjusted_audio_clip)

        # Actualizar el tiempo de inicio para el próximo audio
        tiempo_inicio_actual += duracion_audio

    if not clips:
        print("No valid images or audio found. Unable to create the video.")
        return None

    # Aplicar transiciones entre clips y ajustar duración total del video
    final_clips = [clips[0]]
    for i in range(1, len(clips)):
        transition = 1  # Duración de la transición
        final_clips[-1] = final_clips[-1].crossfadeout(transition)
        clips[i] = clips[i].crossfadein(transition)
        final_clips.append(clips[i])
        # Restar la duración de la transición para el cálculo del tiempo de inicio del audio
        tiempo_inicio_actual -= transition

    # Concatenar clips con transiciones
    final_video = concatenate_videoclips(final_clips, method="compose")

    # Crear el clip de audio final ajustando los clips de audio
    final_audio = CompositeAudioClip(audio_clips)

    # Establecer el audio final al video
    final_video = final_video.set_audio(final_audio)

    # Guardar el video final
    video_final_path = os.path.join(ruta_carpeta_output, nombre_archivo)
    final_video.write_videofile(video_final_path, fps=24)

    return video_final_path

# Recuerda actualizar la función create_video3_with_transitions_and_effects con esta versión actualizada de apply_random_effect.
def create_video3_with_transitions_and_effects(json_data, json_audios, ruta_carpeta_output, nombre_archivo, carpeta_musica, target_size=(1080, 1920)):
    clips = []
    audio_clips = []
    tiempo_inicio_actual = 0

    for id_img, ruta_audio_dict in zip(json_data.keys(), json_audios):
        ruta_img = json_data[id_img]
        ruta_audio = ruta_audio_dict["archivo_audio"]
        
        if not os.path.exists(ruta_img) or not os.path.exists(ruta_audio):
            print(f"Skipping: Image or audio file does not exist. Image: {ruta_img}, Audio: {ruta_audio}")
            continue

        audio_clip = AudioFileClip(ruta_audio)
        duracion_audio = audio_clip.duration

        img_clip = ImageClip(ruta_img).set_duration(duracion_audio)
        img_clip = apply_random_effect(img_clip, target_size)  # Aplicar efecto aleatorio
        clips.append(img_clip)

        adjusted_audio_clip = audio_clip.set_start(tiempo_inicio_actual)
        audio_clips.append(adjusted_audio_clip)
        tiempo_inicio_actual += duracion_audio

    if not clips:
        print("No valid images or audio found. Unable to create the video.")
        return None

    final_clips = [clips[0]]
    for i in range(1, len(clips)):
        transition = 1
        final_clips[-1] = final_clips[-1].crossfadeout(transition)
        clips[i] = clips[i].crossfadein(transition)
        final_clips.append(clips[i])
        tiempo_inicio_actual -= transition

    final_video = concatenate_videoclips(final_clips, method="compose")
    final_audio = CompositeAudioClip(audio_clips)

    archivos_musica = [f for f in os.listdir(carpeta_musica) if f.endswith(('.mp3', '.wav'))]
    archivo_musica_fondo = random.choice(archivos_musica)
    musica_fondo = AudioFileClip(os.path.join(carpeta_musica, archivo_musica_fondo)).set_duration(tiempo_inicio_actual).volumex(0.3)

    final_audio_combined = CompositeAudioClip([final_audio, musica_fondo])
    final_video = final_video.set_audio(final_audio_combined)

    video_final_path = os.path.join(ruta_carpeta_output, nombre_archivo)
    final_video.write_videofile(video_final_path, fps=24)

    return video_final_path