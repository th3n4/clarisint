import re

###MOVER ESTO A BACKEND
def procesar_texto(txt_to_process):
    patrones_basura = [
        re.compile(r'^[^\w\s]*$'),                # Líneas que no contienen caracteres alfanuméricos
        re.compile(r'\bHSU\w*\b'),                # Palabras que empiezan con HSU
        re.compile(r'\bHSW\w*\b'),                # Palabras que empiezan con HSW
        re.compile(r'\bSVW\w*\b'),                # Palabras que empiezan con SVW
        re.compile(r'\bUAV\w*\b'),                # Palabras que empiezan con UAV
        re.compile(r'\bUAWA\w*\b'),               # Palabras que empiezan con UAWA
        re.compile(r'\bAWAV\w*\b'),               # Palabras que empiezan con AWAV
        re.compile(r'\bUVW\w*\b'),                # Palabras que empiezan con UVW
        re.compile(r'[^\w\s.@*\-\']|(?<![\w.])[.@]'),            # Cualquier cosa que no sea alfanumérica, espacio, punto, arroba, asterisco, guion o comilla
        re.compile(r'^[^a-zA-Z0-9]*$'),           # Líneas que no contienen letras o números
        re.compile(r'^.{1,3}$'),                  # Líneas muy cortas
        re.compile(r'^\d+$'),                     # Líneas que contienen solo números
        re.compile(r'^.*?\$(?![\w.]|\S\S\S).*?$'),                # Líneas que contienen el símbolo $
        re.compile(r'\b(?:储墨墨悪|균기길김|储墨您梨)\b'),  # Caracteres aleatorios no identificables
        re.compile(r'[^\x00-\x7F]+'),             # Caracteres no ASCII, suponiendo que no sean relevantes
        re.compile(r'^[\s\W_]+$'),                # Líneas que contienen solo espacios, caracteres no alfanuméricos y guiones bajos
        re.compile(r'\b(?:b\\p|B\\p|\\l#mW|RHS8DAdNTsLCOIEV\.X\.PU|0pc3d5b7-9lBsDEF)\b'),  # Patrones de texto aleatorio o sin sentido
        re.compile(r'\b(?:P\s+"|储墨墨悪|균기길김|储墨您梨)\b'),  # Patrones específicos de caracteres extraños o sin sentido
        re.compile(r'^\d{1,2}:\d{2}:\d{2}\s+\d{4}-\d{2}-\d{2}$'),  # Formatos de fecha y hora sin contexto
        re.compile(r'\b(?:[a-fA-F0-9]{16,})\b'),  # Secuencias largas de caracteres hexadecimales
        re.compile(r'^\d+.*$'),                   # Líneas que comienzan con números
        re.compile(r'\b(?:AVVWSH|VWUSH|gffffffff|gfffffff)\b'),  # Palabras repetidas y sin contexto
        re.compile(r'\b(?:[a-zA-Z]\d+[a-zA-Z])\b'),  # Patrones de letras y números sin sentido (e.g., t-H9s, BQRAPAQH)
        re.compile(r'\b(?:H9Q\s+u1H|3L9f0t|7L9v8t|tyH9_)\b'),  # Combinaciones específicas de letras y números sin sentido
        re.compile(r'\b(?:[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_]{10,})\b'),  # Secuencias largas de caracteres alfanuméricos y guiones bajos
        re.compile(r'\b(?:Bla World Bla Bla)\b'),  # Frases sin sentido
        re.compile(r'^\d{4,}\b'),  # Líneas con muchos números
        #nuevos
        re.compile(r'(.)\1{3,}') #Identifica lineas con 5 o mas caracteres seguidos
        ]

    lineas = txt_to_process.split('\n')
    lineas_limpias = []
    for linea in lineas:
        es_basura = False
        for patron in patrones_basura:
            if patron.search(linea):
                es_basura = True
                break
        if not es_basura:
            lineas_limpias.append(linea)

    with open("mnlr3.txt", "w") as f:
        f.writelines('\n'.join(lineas_limpias))
    return lineas_limpias


with open(r"C:\Users\th3n4\Desktop\All\Herramientas\Strings2\mnlr.txt", 'r', encoding='utf-8') as file:
    x = [line.replace('\n', '') for line in file.readlines() if line != '\n']
    y = procesar_texto('\n'.join(x))
    pass


######## CODIGO PRUEBA PARA MARCAR TEXTO EN BASE DE DATOS

import tkinter as tk
from tkinter import scrolledtext

# Asume que ya tienes una conexión a la base de datos
sql_connection = ...  # tu conexión a la base de datos

def on_procesar_click():
    if current_option == "Original" and contenido_guardado[current_option] != "":
        process_txt_btn.configure(state="disabled") # Deshabilitar botón de procesar, CAMBIAR
        buttons.configure(state="normal") # Habilitar botones secundarios
        txt_to_process = contenido_guardado["Original"]
        cleaned_text = backend.procesar_texto(txt_to_process)
        nombres_contenido = obtener_nombres_contenido(sql_connection)
        marcar_coincidencias(cleaned_text, nombres_contenido, text_box)

def obtener_nombres_contenido(sql_connection):
    cursor = sql_connection.cursor()
    query = "SELECT nombre FROM Contenido"
    try:
        result = cursor.execute(query)
        nombres = [row[0] for row in result.fetchall()]
        return nombres
    except Exception as e:
        print(f"Error ejecutando query: {e}")
        return []
    finally:
        cursor.close()

def marcar_coincidencias(texto_limpio, nombres_contenido, text_widget):
    lineas = texto_limpio.split('\n')
    for i, linea in enumerate(lineas):
        for nombre in nombres_contenido:
            if nombre in linea:
                start_index = f"{i+1}.0"
                end_index = f"{i+1}.end"
                text_widget.tag_add(f"coincidencia_{i}", start_index, end_index)
                text_widget.tag_config(f"coincidencia_{i}", background="red", foreground="white")
                break

root = tk.Tk()
root.title("Text Highlighter")

text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
text_box.pack(pady=20)

process_txt_btn = tk.Button(root, text="Procesar Texto", command=on_procesar_click)
process_txt_btn.pack()

buttons = tk.Frame(root)  # Assume que tienes un frame para botones secundarios
buttons.pack()

root.mainloop()