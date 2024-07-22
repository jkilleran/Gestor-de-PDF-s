import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinterdnd2 import DND_FILES, TkinterDnD

# Lista para almacenar temporalmente los archivos arrastrados
archivos_seleccionados = []

def mostrar_mensaje_archivos_seleccionados():
    if not archivos_seleccionados:
        console.insert(tk.END, "No hay archivos seleccionados.\n")

def split_selected_pdfs():
    mostrar_mensaje_archivos_seleccionados()
    if archivos_seleccionados:
        split_pdfs(archivos_seleccionados)

def split_pdfs_in_folder(folder_path):
    console.insert(tk.END, f"Procesando la carpeta: {folder_path}\n")
    for filename in os.listdir(folder_path):
        console.insert(tk.END, f"Procesando el archivo: {filename}\n")
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(reader.pages)

                console.insert(tk.END, f"El archivo tiene {num_pages} páginas.\n")
                if num_pages > 1:
                    for page_number in range(num_pages):
                        writer = PyPDF2.PdfWriter()
                        writer.add_page(reader.pages[page_number])
                        
                        new_file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}_page_{page_number + 1}.pdf")
                        with open(new_file_path, 'wb') as new_pdf_file:
                            writer.write(new_pdf_file)
                        console.insert(tk.END, f"Página {page_number + 1} guardada como: {new_file_path}\n")
                    
                    pdf_file.close()
                    os.remove(file_path)
                    console.insert(tk.END, f"Archivo original {file_path} eliminado.\n")
                else:
                    console.insert(tk.END, f"El archivo {filename} tiene solo una página. No se dividió.\n")
        else:
            console.insert(tk.END, f"El archivo {filename} no es un PDF. Se omite.\n")

def split_pdfs(archivos):
    for archivo in archivos:
        try:
            console.insert(tk.END, f"Dividiendo archivo: {archivo}\n")
            with open(archivo, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(reader.pages)

                console.insert(tk.END, f"El archivo tiene {num_pages} páginas.\n")
                if num_pages > 1:
                    for page_number in range(num_pages):
                        writer = PyPDF2.PdfWriter()
                        writer.add_page(reader.pages[page_number])
                        
                        new_file_path = os.path.join(os.path.dirname(archivo), f"{os.path.splitext(os.path.basename(archivo))[0]}_page_{page_number + 1}.pdf")
                        with open(new_file_path, 'wb') as new_pdf_file:
                            writer.write(new_pdf_file)
                        console.insert(tk.END, f"Página {page_number + 1} guardada como: {new_file_path}\n")
                else:
                    console.insert(tk.END, f"El archivo {os.path.basename(archivo)} tiene solo una página. No se dividió.\n")
        except Exception as e:
            console.insert(tk.END, f"Error al dividir el archivo '{archivo}': {e}\n")

def leer_primera_linea_pdf(archivo_pdf):
    try:
        with open(archivo_pdf, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            primera_linea = pdf_reader.pages[0].extract_text().split('\n')[0]
            return primera_linea.strip()
    except Exception as e:
        console.insert(tk.END, f"Error al leer la primera línea del archivo PDF '{archivo_pdf}': {e}\n")
        return None

def renombrar_pdf(archivo_pdf, nuevo_nombre):
    try:
        nueva_ruta_pdf = os.path.join(os.path.dirname(archivo_pdf), nuevo_nombre)
        contador = 1
        while os.path.exists(nueva_ruta_pdf):
            nombre_base, extension = os.path.splitext(nuevo_nombre)
            nuevo_nombre = f"{nombre_base}_{contador}{extension}"
            nueva_ruta_pdf = os.path.join(os.path.dirname(archivo_pdf), nuevo_nombre)
            contador += 1

        nuevo_nombre = ' '.join(nuevo_nombre.split()[1:])
        os.rename(archivo_pdf, nueva_ruta_pdf)
        console.insert(tk.END, f"El archivo '{archivo_pdf}' se ha renombrado exitosamente a '{nuevo_nombre}'.\n")
    except Exception as e:
        console.insert(tk.END, f"Error al renombrar el archivo PDF '{archivo_pdf}': {e}\n")

def procesar_archivos_pdf(carpeta):
    archivos_en_carpeta = os.listdir(carpeta)
    archivos_pdf = [archivo for archivo in archivos_en_carpeta if archivo.endswith(".pdf")]

    if archivos_pdf:
        for archivo_pdf in archivos_pdf:
            ruta_pdf = os.path.join(carpeta, archivo_pdf)
            primera_linea = leer_primera_linea_pdf(ruta_pdf)
            if primera_linea:
                renombrar_pdf(ruta_pdf, primera_linea + ".pdf")
    else:
        console.insert(tk.END, "No se encontraron archivos PDF en la carpeta especificada.\n")

def seleccionar_carpeta_split():
    folder_path = filedialog.askdirectory()
    if folder_path:
        split_pdfs_in_folder(folder_path)

def seleccionar_carpeta_rename():
    folder_path = filedialog.askdirectory()
    if folder_path:
        procesar_archivos_pdf(folder_path)

def on_drop(event):
    global archivos_seleccionados
    archivos = event.data.split('} {')
    # Limpiar los nombres de archivo para quitar llaves '{' y '}'
    archivos = [archivo.strip('{}') for archivo in archivos]
    archivos_seleccionados.extend(archivos)
    console.insert(tk.END, f"Archivos seleccionados: {archivos_seleccionados}\n")

def combinar_archivos_seleccionados():
    mostrar_mensaje_archivos_seleccionados()
    global archivos_seleccionados
    if archivos_seleccionados:
        combinar_pdfs(archivos_seleccionados)
        archivos_seleccionados = []  # Limpiar la lista después de combinar

def combinar_pdfs(archivos):
    merger = PyPDF2.PdfMerger()
    for archivo in archivos:
        try:
            console.insert(tk.END, f"Combinando archivo: {archivo}\n")
            with open(archivo, 'rb') as pdf_file:
                merger.append(pdf_file)
        except Exception as e:
            console.insert(tk.END, f"Error al combinar el archivo '{archivo}': {e}\n")
    output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
    if output_file:
        try:
            with open(output_file, 'wb') as output:
                merger.write(output)
            console.insert(tk.END, f"Archivos combinados guardados como: {output_file}\n")
        except Exception as e:
            console.insert(tk.END, f"Error al guardar el archivo combinado '{output_file}': {e}\n")

def plex():
    mostrar_mensaje_archivos_seleccionados()
    global archivos_seleccionados
    if archivos_seleccionados:
        merger = PyPDF2.PdfMerger()
        output_filename = os.path.basename(archivos_seleccionados[-1]) + " Comprobante"
        
        try:
            for archivo in archivos_seleccionados:
                with open(archivo, 'rb') as pdf_file:
                    merger.append(pdf_file)
                    
            output_path = os.path.dirname(archivos_seleccionados[-1])
            output_file = os.path.join(output_path, output_filename + ".pdf")
            
            with open(output_file, 'wb') as output:
                merger.write(output)
            
            console.insert(tk.END, f"Archivos combinados guardados como: {output_file}\n")
            
            # Eliminar archivos seleccionados
            for archivo in archivos_seleccionados:
                os.remove(archivo)
                console.insert(tk.END, f"Archivo eliminado: {archivo}\n")
            
            archivos_seleccionados = []  # Limpiar la lista después de combinar y eliminar
        except Exception as e:
            console.insert(tk.END, f"Error al combinar y/o eliminar archivos: {e}\n")
    else:
        console.insert(tk.END, "No hay archivos seleccionados para combinar.\n")


def plex_2(carpeta):
    try:
        archivos_en_carpeta = os.listdir(carpeta)
        archivos_pdf = [archivo for archivo in archivos_en_carpeta if archivo.endswith(".pdf")]

        for archivo in archivos_pdf:
            ruta_completa = os.path.join(carpeta, archivo)
            nuevo_nombre = ' '.join(archivo.split()[1:])
            nuevo_path = os.path.join(carpeta, nuevo_nombre)
            os.rename(ruta_completa, nuevo_path)
            console.insert(tk.END, f"Archivo renombrado: {archivo} -> {nuevo_nombre}\n")

        console.insert(tk.END, "Proceso completado.\n")
    except Exception as e:
        console.insert(tk.END, f"Error al renombrar archivos: {e}\n")

# Crear la ventana principal con soporte para arrastrar y soltar
ventana = TkinterDnD.Tk()
ventana.title("Gestor de Archivos PDF")

# Botón para dividir PDFs seleccionados
boton_dividir_seleccionados = tk.Button(ventana, text="Dividir PDFs Seleccionados", command=split_selected_pdfs)
boton_dividir_seleccionados.pack(pady=10)

# Botón para dividir PDFs por carpeta
boton_dividir_carpeta = tk.Button(ventana, text="Dividir PDFs en Carpeta", command=seleccionar_carpeta_split)
boton_dividir_carpeta.pack(pady=10)

# Botón para renombrar PDFs por carpeta
boton_renombrar_carpeta = tk.Button(ventana, text="Renombrar PDFs en Carpeta", command=seleccionar_carpeta_rename)
boton_renombrar_carpeta.pack(pady=10)

# Botón para combinar PDFs seleccionados
boton_combinar_seleccionados = tk.Button(ventana, text="Combinar PDFs Seleccionados", command=combinar_archivos_seleccionados)
boton_combinar_seleccionados.pack(pady=10)

# Botón para la función plex
boton_plex = tk.Button(ventana, text="Plex", command=plex)
boton_plex.pack(pady=10)

# Botón para la función plex_2
boton_plex_2 = tk.Button(ventana, text="Plex_2", command=lambda: plex_2(filedialog.askdirectory()))
boton_plex_2.pack(pady=10)

# Consola para mostrar el progreso y los mensajes
console = scrolledtext.ScrolledText(ventana, width=80, height=20)
console.pack(pady=10)

# Función para manejar el arrastre y soltado de archivos
ventana.drop_target_register(DND_FILES)
ventana.dnd_bind('<<Drop>>', on_drop)

# Ejecutar la ventana
ventana.mainloop()
