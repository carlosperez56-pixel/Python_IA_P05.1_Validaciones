## 3MLIDTS-CarlosPerez-05.1Python
### Formulario de registro con validaciones
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
 
# El TXT se guarda junto a este archivo .py, sin importar desde dónde se ejecute
RUTA_ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos.txt")
COLOR_ERROR = "#ffcccc"
 
 
### Funciones de validación
def es_texto_valido(valor):
    # Solo letras (con acentos y ñ) y espacios, de 2 a 40 caracteres
    return 2 <= len(valor) <= 40 and valor.replace(" ", "").isalpha()
 
 
def es_edad_valida(valor):
    return valor.isdecimal() and 1 <= int(valor) <= 120
 
 
def es_estatura_valida(valor):
    try:
        return 0.5 <= float(valor) <= 2.5
    except ValueError:
        return False
 
 
def limitar_digitos(texto, maximo):
    # Se ejecuta en cada tecla: solo permite números y hasta "maximo" dígitos
    return texto == "" or (texto.isdecimal() and len(texto) <= int(maximo))
 
 
### Funciones de los botones
def guardar_datos():
    # Obtener los datos (strip quita espacios sobrantes)
    nombres = entry_nombres.get().strip()
    apellidos = entry_apellidos.get().strip()
    edad = entry_edad.get().strip()
    estatura = entry_estatura.get().strip().replace(",", ".")
    telefono = entry_telefono.get().strip()
    genero = var_genero.get()
 
    # Cada regla: (campo, ¿es válido?, mensaje de error)
    reglas = [
        (entry_nombres, es_texto_valido(nombres), "Nombres: solo letras (mínimo 2)."),
        (entry_apellidos, es_texto_valido(apellidos), "Apellidos: solo letras (mínimo 2)."),
        (entry_edad, es_edad_valida(edad), "Edad: debe estar entre 1 y 120."),
        (entry_estatura, es_estatura_valida(estatura), "Estatura: entre 0.5 y 2.5 m (ej. 1.70)."),
        (entry_telefono, telefono.isdecimal() and len(telefono) == 10, "Teléfono: deben ser 10 dígitos."),
    ]
 
    # Pinta de rojo los campos incorrectos y junta los mensajes
    errores = []
    for entry, valido, mensaje in reglas:
        entry.config(bg="white" if valido else COLOR_ERROR)
        if not valido:
            errores.append(mensaje)
    if genero == "":
        errores.append("Género: seleccione una opción.")
 
    if errores:
        messagebox.showwarning("Datos inválidos", "\n".join(errores))
        return
 
    # Armar el registro (mismo formato del TXT de la práctica en C#)
    datos = (f"Nombres: {nombres.title()}\n"
             f"Apellidos: {apellidos.title()}\n"
             f"Genero: {genero}\n"
             f"Edad: {int(edad)}\n"
             f"Telefono: {telefono}\n"
             f"Estatura: {float(estatura):.2f}\n"
             f"Fecha: {datetime.now():%d/%m/%Y %H:%M}")
 
    # Confirmar antes de guardar
    if not messagebox.askokcancel("¿Guardar este registro?", datos):
        return
 
    # Guardar en el TXT controlando posibles errores
    try:
        with open(RUTA_ARCHIVO, "a", encoding="utf-8") as archivo:
            archivo.write(datos + "\n\n")
    except OSError as error:
        messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{error}")
        return
 
    messagebox.showinfo("Éxito", "Registro guardado correctamente.")
    limpiar_campos()
 
 
def limpiar_campos():
    for entry in entradas:
        entry.delete(0, tk.END)
        entry.config(bg="white")  # Quita el color de error
    var_genero.set("")
    entry_nombres.focus()         # Cursor listo en el primer campo
 
 
### Creación de la ventana
ventana = tk.Tk()
ventana.title("Formulario de Registro")
ventana.geometry("360x520")
ventana.resizable(False, False)
ventana.eval("tk::PlaceWindow . center")  # Abre centrada en la pantalla
 
# Variable para los RadioButtons
var_genero = tk.StringVar()
 
# Permite que Edad y Teléfono solo acepten números al teclear
vcmd = ventana.register(limitar_digitos)
 
## Creación de etiquetas y campos de entrada
label_nombres = tk.Label(ventana, text="Nombres:")
label_nombres.pack(pady=(10, 0))
entry_nombres = tk.Entry(ventana, width=30)
entry_nombres.pack()
 
label_apellidos = tk.Label(ventana, text="Apellidos:")
label_apellidos.pack(pady=(10, 0))
entry_apellidos = tk.Entry(ventana, width=30)
entry_apellidos.pack()
 
label_edad = tk.Label(ventana, text="Edad:")
label_edad.pack(pady=(10, 0))
entry_edad = tk.Entry(ventana, width=30, validate="key", validatecommand=(vcmd, "%P", 3))
entry_edad.pack()
 
label_estatura = tk.Label(ventana, text="Estatura (m):")
label_estatura.pack(pady=(10, 0))
entry_estatura = tk.Entry(ventana, width=30)
entry_estatura.pack()
 
label_telefono = tk.Label(ventana, text="Teléfono:")
label_telefono.pack(pady=(10, 0))
entry_telefono = tk.Entry(ventana, width=30, validate="key", validatecommand=(vcmd, "%P", 10))
entry_telefono.pack()
 
# Lista con todos los campos (la usa limpiar_campos)
entradas = [entry_nombres, entry_apellidos, entry_edad, entry_estatura, entry_telefono]
 
## Creación de RadioButtons
label_genero = tk.Label(ventana, text="Género:")
label_genero.pack(pady=(10, 0))
 
rb_masculino = tk.Radiobutton(ventana, text="Masculino", variable=var_genero, value="Masculino")
rb_masculino.pack()
 
rb_femenino = tk.Radiobutton(ventana, text="Femenino", variable=var_genero, value="Femenino")
rb_femenino.pack()
 
rb_otro = tk.Radiobutton(ventana, text="Otro", variable=var_genero, value="Otro")
rb_otro.pack()
 
## Creación de Botones
btn_guardar = tk.Button(ventana, text="Guardar", width=15, bg="#4CAF50", fg="white",
                        command=guardar_datos)
btn_guardar.pack(pady=(20, 5))
 
btn_borrar = tk.Button(ventana, text="Borrar Campos", width=15, command=limpiar_campos)
btn_borrar.pack()
 
ventana.bind("<Return>", lambda evento: guardar_datos())  # Enter = Guardar
entry_nombres.focus()
 
### Ejecución de la ventana
ventana.mainloop()
