import pandas as pd
import random
import json
import openpyxl

def seleccionar_tema_aleatorio(df):
    """Selecciona un tema aleatorio de una hoja dada, asegurándose de que no haya sido utilizado previamente."""
    if 'Utilizado' not in df.columns:
        df['Utilizado'] = 'No'
    temas_disponibles = df[df['Utilizado'] != 'Sí']
    if temas_disponibles.empty:
        return None
    return temas_disponibles.sample()

def marcar_como_utilizado(df, tema_seleccionado):
    """Marca el tema seleccionado como utilizado."""
    df.loc[tema_seleccionado.index, 'Utilizado'] = 'Sí'
    return df

def procesar_archivo_excel(file_path):
    """Procesa el archivo Excel seleccionando un tema aleatorio de una hoja aleatoria y marcándolo como utilizado."""
    todas_las_hojas = pd.read_excel(file_path, sheet_name=None)

    # Seleccionar una hoja y un tema de manera aleatoria
    nombre_hoja_seleccionada, hoja_seleccionada = random.choice(list(todas_las_hojas.items()))
    tema_seleccionado = seleccionar_tema_aleatorio(hoja_seleccionada)

    while tema_seleccionado is None:
        nombre_hoja_seleccionada, hoja_seleccionada = random.choice(list(todas_las_hojas.items()))
        tema_seleccionado = seleccionar_tema_aleatorio(hoja_seleccionada)

    hoja_actualizada = marcar_como_utilizado(hoja_seleccionada, tema_seleccionado)

    # Guardar los cambios en el archivo Excel
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        for hoja in todas_las_hojas:
            if hoja == nombre_hoja_seleccionada:
                hoja_actualizada.to_excel(writer, sheet_name=hoja, index=False)
            else:
                todas_las_hojas[hoja].to_excel(writer, sheet_name=hoja, index=False)

    # Convertir el tema seleccionado a JSON
    tema_json = tema_seleccionado.to_json(orient='records', force_ascii=False)
    return tema_json

# Ruta al archivo Excel
#ruta_archivo_excel = "C:\\Users\\Reyes\\Documents\\Main\\AletheAI\\VideoSubidaTikTok\\Video 2\\inputs videos\\visiones de una mente artificial\\visiones de una mente artificia.xlsx"
ruta_archivo_excel = "C:\\Users\\Reyes\\Documents\\Main\\AletheAI\\VideoSubidaTikTok\\Video 2\\inputs videos\\animalandIA\\animalandia.xlsx"

