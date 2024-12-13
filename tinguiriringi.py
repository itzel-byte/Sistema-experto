import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Archivos para persistencia
archivo_bc = "base_conocimiento.json"
archivo_diagnosticos = "diagnosticos.json"
archivo_reglas = "reglas.json"

# Inicializar archivo de reglas
def inicializar_reglas():
    if not os.path.exists(archivo_reglas):
        with open(archivo_reglas, "w", encoding="utf-8") as archivo:
            json.dump({}, archivo, indent=4, ensure_ascii=False)

# Cargar reglas desde archivo
def cargar_reglas():
    try:
        with open(archivo_reglas, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Guardar reglas en archivo
def guardar_reglas(reglas):
    with open(archivo_reglas, "w", encoding="utf-8") as archivo:
        json.dump(reglas, archivo, indent=4, ensure_ascii=False)

# Cargar la base de conocimiento desde el archivo JSON
def cargar_base_conocimiento():
    try:
        with open("base_conocimiento.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

base_conocimiento = cargar_base_conocimiento()

# Función para inicializar la base de conocimiento
def inicializar_bc():
    base_inicial = {
        "depresion": {
            "sintomas": {
                "tristeza persistente": 5,
                "falta de energía": 4,
                "dificultad para concentrarse": 3,
                "cambios en el apetito": 2
            },
            "tratamiento": "Terapia psicológica, actividad física, y en algunos casos medicación.",
            "medicamentos": ["Antidepresivos (bajo prescripción médica)"],
            "descripcion": "La depresión es un trastorno mental caracterizado por tristeza persistente y pérdida de interés."
        },
        "ansiedad_generalizada": {
            "sintomas": {
                "preocupación excesiva": 5,
                "tensión muscular": 3,
                "dificultad para dormir": 4,
                "irritabilidad": 3
            },
            "tratamiento": "Terapia cognitivo-conductual, técnicas de relajación, y medicación si es necesario.",
            "medicamentos": ["Ansiolíticos (bajo prescripción médica)"],
            "descripcion": "El trastorno de ansiedad generalizada se caracteriza por preocupación y miedo excesivos." 
        },
        "trastorno_bipolar": {
            "sintomas": {
                "episodios de euforia": 5,
                "cambios drásticos en el estado de ánimo": 4,
                "hiperactividad": 3,
                "dificultad para dormir": 4
            },
            "tratamiento": "Terapia psicológica, estabilizadores del estado de ánimo, y apoyo familiar.",
            "medicamentos": ["Estabilizadores del ánimo", "Antipsicóticos"],
            "descripcion": "El trastorno bipolar implica cambios extremos en el estado de ánimo y niveles de energía."
        }
    }

    if not os.path.exists(archivo_bc):
        guardar_bc(base_inicial)
    else:
        base_cargada = cargar_bc()
        for enfermedad, datos in base_cargada.items():
            if isinstance(datos["sintomas"], list):
                datos["sintomas"] = {sintoma: 1 for sintoma in datos["sintomas"]}
        guardar_bc(base_cargada)

    return cargar_bc()

# Función para cargar la base de conocimiento desde el archivo
def cargar_bc():
    with open(archivo_bc, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

# Función para guardar la base de conocimiento en el archivo
def guardar_bc(base):
    with open(archivo_bc, "w", encoding="utf-8") as archivo:
        json.dump(base, archivo, indent=4, ensure_ascii=False)

# Función para inicializar la base de diagnósticos
def inicializar_diagnosticos():
    if not os.path.exists(archivo_diagnosticos):
        with open(archivo_diagnosticos, "w", encoding="utf-8") as archivo:
            json.dump([], archivo)

# Función para cargar los diagnósticos desde el archivo
def cargar_diagnosticos():
    try:
        with open(archivo_diagnosticos, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# Función para guardar un diagnóstico en el archivo
def guardar_diagnostico(diagnostico):
    diagnosticos = cargar_diagnosticos()
    diagnosticos.append(diagnostico)
    try:
        with open(archivo_diagnosticos, "w", encoding="utf-8") as archivo:
            json.dump(diagnosticos, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el diagnóstico: {e}")

def formulario_paciente():
    ventana_formulario = tk.Toplevel(root)
    ventana_formulario.title("Formulario del Paciente")
    ventana_formulario.geometry("400x300")

    tk.Label(ventana_formulario, text="Datos del Paciente", font=("Arial", 14)).pack(pady=10)

    tk.Label(ventana_formulario, text="Nombre:").pack(anchor="w", padx=10)
    entrada_nombre = tk.Entry(ventana_formulario)
    entrada_nombre.pack(fill="x", padx=10)

    tk.Label(ventana_formulario, text="Edad:").pack(anchor="w", padx=10)
    entrada_edad = tk.Entry(ventana_formulario)
    entrada_edad.pack(fill="x", padx=10)

    tk.Label(ventana_formulario, text="Género:").pack(anchor="w", padx=10)
    entrada_genero = tk.Entry(ventana_formulario)
    entrada_genero.pack(fill="x", padx=10)

    def iniciar_diagnostico():
        nombre = entrada_nombre.get().strip()
        edad = entrada_edad.get().strip()
        genero = entrada_genero.get().strip()

        if not nombre or not edad or not genero:
            messagebox.showwarning("Advertencia", "pon la edad wey.")
            return

        sintomas_confirmados = []
        for enfermedad, datos in base_conocimiento.items():
            for sintoma in datos["sintomas"].keys():
                respuesta = messagebox.askyesno("Síntoma", f"¿Presenta el síntoma: {sintoma}?")
                if respuesta:
                    sintomas_confirmados.append(sintoma)

        diagnostico_final = []
        for enfermedad, datos in base_conocimiento.items():
            sintomas_enfermedad = datos["sintomas"]
            peso_coincidencia = sum(sintomas_enfermedad[s] for s in sintomas_confirmados if s in sintomas_enfermedad)
            peso_total = sum(sintomas_enfermedad.values())
            porcentaje = (peso_coincidencia / peso_total) * 100 if peso_total else 0

            if porcentaje > 0:
                diagnostico_final.append({
                    "nombre": enfermedad,
                    "descripcion": datos["descripcion"],
                    "tratamiento": datos["tratamiento"],
                    "medicamentos": datos["medicamentos"],
                    "porcentaje": porcentaje
                })

        diagnostico_final.sort(key=lambda x: x["porcentaje"], reverse=True)

        mensaje = "Diagnóstico Completo:\n\n"
        for diag in diagnostico_final:
            mensaje += f"POSIBLE ENFERMEDAD: {diag['nombre'].capitalize()}\n\n"
            mensaje += f"DE QUE TRATA?: {diag['descripcion']}\n\n"
            mensaje += f"PORCENTAJE DE SIMILARIDAD: {diag['porcentaje']:.2f}%\n\n"
            mensaje += f"TRATAMIENTO: {diag['tratamiento']}\n\n"
            mensaje += f"MEDICAMENTO A USAR: {', '.join(diag['medicamentos'])}\n\n"

        messagebox.showinfo("Diagnóstico Final", mensaje)
        ventana_formulario.destroy()

    tk.Button(ventana_formulario, text="Iniciar Diagnóstico", command=iniciar_diagnostico).pack(pady=20)

def consultar_diagnosticos():
    ventana_consulta = tk.Toplevel(root)
    ventana_consulta.title("Diagnósticos Anteriores")
    ventana_consulta.geometry("400x400")

    tk.Label(ventana_consulta, text="Diagnósticos Registrados", font=("Arial", 14)).pack(pady=10)

    diagnosticos = cargar_diagnosticos()
    if not diagnosticos:
        tk.Label(ventana_consulta, text="No hay diagnósticos registrados.").pack(pady=10)
        return

    listbox = tk.Listbox(ventana_consulta, width=50, height=20)
    listbox.pack(pady=10)

    for i, diag in enumerate(diagnosticos):
        listbox.insert(tk.END, f"{i + 1}. {diag['nombre']} ({diag['edad']} años) - {diag['fecha']}")

    def ver_detalle():
        seleccion = listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un diagnóstico para ver los detalles.")
            return

        indice = seleccion[0]
        diag = diagnosticos[indice]

        detalle = f"Nombre: {diag['nombre']}\n"
        detalle += f"Edad: {diag['edad']}\n"
        detalle += f"Género: {diag['genero']}\n"
        detalle += f"Fecha: {diag['fecha']}\n"
        detalle += "\nDiagnóstico:\n"

        for enfermedad in diag["diagnostico"]:
            detalle += f"- {enfermedad['nombre'].capitalize()} ({enfermedad['porcentaje']:.2f}% de coincidencia)\n"

        messagebox.showinfo("Detalle del Diagnóstico", detalle)

    tk.Button(ventana_consulta, text="Ver Detalle", command=ver_detalle).pack(pady=5)

def ver_estadisticas():
    ventana_estadisticas = tk.Toplevel(root)
    ventana_estadisticas.title("Estadísticas de Diagnósticos")
    ventana_estadisticas.geometry("400x400")

    tk.Label(ventana_estadisticas, text="Estadísticas Generales", font=("Arial", 14)).pack(pady=10)

    diagnosticos = cargar_diagnosticos()
    if not diagnosticos:
        tk.Label(ventana_estadisticas, text="No hay diagnósticos registrados para mostrar estadísticas.").pack(pady=10)
        return

    conteo_enfermedades = {}
    for diag in diagnosticos:
        for enfermedad in diag["diagnostico"]:
            nombre = enfermedad["nombre"]
            conteo_enfermedades[nombre] = conteo_enfermedades.get(nombre, 0) + 1

    texto = "Enfermedades más diagnosticadas:\n\n"
    for enfermedad, conteo in sorted(conteo_enfermedades.items(), key=lambda x: x[1], reverse=True):
        texto += f"- {enfermedad.capitalize()}: {conteo} veces\n"

    tk.Label(ventana_estadisticas, text=texto, justify="left", wraplength=350).pack(pady=10)

def agregar_regla():
    ventana_regla = tk.Toplevel(root)
    ventana_regla.title("Agregar Nueva Regla")
    ventana_regla.geometry("400x300")

    tk.Label(ventana_regla, text="Agregar Enfermedad", font=("Arial", 14)).pack(pady=10)

    tk.Label(ventana_regla, text="Nombre").pack(anchor="w", padx=10)
    entrada_nombre = tk.Entry(ventana_regla)
    entrada_nombre.pack(fill="x", padx=10)

    tk.Label(ventana_regla, text="Descripción").pack(anchor="w", padx=10)
    entrada_descripcion = tk.Entry(ventana_regla)
    entrada_descripcion.pack(fill="x", padx=10)

    tk.Label(ventana_regla, text="Síntomas").pack(anchor="w", padx=10)
    entrada_sintomas = tk.Entry(ventana_regla)
    entrada_sintomas.pack(fill="x", padx=10)

    tk.Label(ventana_regla, text="Tratamiento").pack(anchor="w", padx=10)
    entrada_tratamiento = tk.Entry(ventana_regla)
    entrada_tratamiento.pack(fill="x", padx=10)

    tk.Label(ventana_regla, text="Medicamentos").pack(anchor="w", padx=10)
    entrada_medicamentos = tk.Entry(ventana_regla)
    entrada_medicamentos.pack(fill="x", padx=10)
    
    def nombres():
        ventana_nombres = tk.Toplevel(root)
        ventana_nombres.title("Diagnósticos Anteriores")
        ventana_nombres.geometry("400x400")

        tk.Label(ventana_nombres, text="21310158 Y 21310133", font=("Arial", 14)).pack(pady=10)

    def guardar_nueva_regla():
        nombre = entrada_nombre.get().strip().lower()
        descripcion = entrada_descripcion.get().strip()
        sintomas_raw = entrada_sintomas.get().strip()
        tratamiento = entrada_tratamiento.get().strip()
        medicamentos_raw = entrada_medicamentos.get().strip()

        if not (nombre and descripcion and sintomas_raw and tratamiento and medicamentos_raw):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        sintomas = {}
        try:
            for sintoma in sintomas_raw.split(","):
                clave, peso = sintoma.split(":")
                sintomas[clave.strip()] = int(peso.strip())
        except ValueError:
            messagebox.showerror("Error", "Formato de síntomas incorrecto.")
            return

        medicamentos = [med.strip() for med in medicamentos_raw.split(",")]

        nueva_regla = {
            "sintomas": sintomas,
            "descripcion": descripcion,
            "tratamiento": tratamiento,
            "medicamentos": medicamentos
        }

        base_conocimiento[nombre] = nueva_regla
        guardar_bc(base_conocimiento)
        messagebox.showinfo("Éxito", "Nueva enfermedad agregada correctamente.")
        ventana_regla.destroy()

    tk.Button(ventana_regla, text="Guardar", command=guardar_nueva_regla).pack(pady=20)

# Interfaz gráfica principal
root = tk.Tk()
root.title("NO PUES ESTA ES LA PESTAñA")
root.geometry("1080x720")

# Widgets de la interfaz
label_title = tk.Label(root, text="BIENVENIDO AL SISTEMA EXPERTO DE ENFERMEDADES MENTALES", font=("Comic Sans", 24))
label_title.pack(pady=20)

label_title = tk.Label(root, text="PROYECTO HECHO POR ", font=("Comic Sans", 12))
label_title.pack(pady=20)

label_title = tk.Label(root, text="GUSTAVO OROZCO 21310158 E ITZEL SOSA RAMOS 21310133", font=("Comic Sans", 12))
label_title.pack(pady=20)


btn_formulario = tk.Button(root, text="INICIAR UNA CONSULTA", command=formulario_paciente, width=30)
btn_formulario.pack(pady=10)

btn_consultar = tk.Button(root, text="HISTORIAL DE CONSULTAS", command=consultar_diagnosticos, width=30)
btn_consultar.pack(pady=10)



btn_estadisticas = tk.Button(root, text="VER STATS DE CONSULTA", command=ver_estadisticas, width=30)
btn_estadisticas.pack(pady=5)

btn_agregar_regla = tk.Button(root, text="INGRESAR UNA NUEVA ENFERMEDAD", command=agregar_regla, width=30)
btn_agregar_regla.pack(pady=5)

btn_salir = tk.Button(root, text="APAGAR SISTEMA", command=root.destroy, width=30, bg="purple", fg="black")
btn_salir.pack(pady=20)

# btn_consultar_reglas = tk.Button(root, text="Consultar Reglas", command=consultar_reglas, width=30)
# btn_consultar_reglas.pack(pady=5)

# Ejecutar la interfaz
root.mainloop()
