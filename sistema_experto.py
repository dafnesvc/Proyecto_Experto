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
        "gripe": {
            "sintomas": {
                "fiebre": 5,
                "tos": 4,
                "dolor de garganta": 3,
                "congestión nasal": 2
            },
            "tratamiento": "Reposo, hidratación, y analgésicos.",
            "medicamentos": ["Paracetamol", "Ibuprofeno"],
            "descripcion": "La gripe es una enfermedad viral que afecta el sistema respiratorio."
        },
        "migraña": {
            "sintomas": {
                "dolor de cabeza": 5,
                "náuseas": 3,
                "sensibilidad a la luz": 4
            },
            "tratamiento": "Analgesia y evitar estímulos luminosos.",
            "medicamentos": ["Aspirina", "Sumatriptán"],
            "descripcion": "La migraña es un tipo de dolor de cabeza severo, a menudo acompañado de náuseas y sensibilidad a la luz."
        },
        "covid-19": {
            "sintomas": {
                "fiebre": 5,
                "tos seca": 4,
                "dificultad para respirar": 6,
                "fatiga": 3
            },
            "tratamiento": "Aislamiento, monitoreo de oxigenación, y consultar a un médico.",
            "medicamentos": ["Antipiréticos", "Oxígeno suplementario (si es necesario)"],
            "descripcion": "COVID-19 es una enfermedad causada por el virus SARS-CoV-2, que afecta principalmente el sistema respiratorio."
        }
    }

    if not os.path.exists(archivo_bc):
        guardar_bc(base_inicial)
    else:
        # Validar si los síntomas tienen pesos; si no, convertir a diccionario con peso = 1
        base_cargada = cargar_bc()
        for enfermedad, datos in base_cargada.items():
            if isinstance(datos["sintomas"], list):
                # Convertir lista de síntomas a diccionario con peso predeterminado
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
            json.dump([], archivo)  # Inicializar como lista vacía

# Función para cargar los diagnósticos desde el archivo
def cargar_diagnosticos():
    try:
        with open(archivo_diagnosticos, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, FileNotFoundError):
        # Si el archivo está corrupto o no existe, inicializamos como lista vacía
        return []

# Función para guardar un diagnóstico en el archivo
def guardar_diagnostico(diagnostico):
    diagnosticos = cargar_diagnosticos()  # Cargar diagnósticos existentes
    diagnosticos.append(diagnostico)
    try:
        with open(archivo_diagnosticos, "w", encoding="utf-8") as archivo:
            json.dump(diagnosticos, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el diagnóstico: {e}")

def agregar_regla():
    # Crear la ventana para agregar una nueva regla
    ventana_regla = tk.Toplevel(root)
    ventana_regla.title("Agregar Nueva Regla")
    ventana_regla.geometry("600x500")

    tk.Label(ventana_regla, text="Agregar Nueva Enfermedad", font=("Arial", 16)).pack(pady=10)

    # Campos para la enfermedad
    tk.Label(ventana_regla, text="Nombre de la Enfermedad:").pack(anchor="w", padx=10)
    entrada_nombre = tk.Entry(ventana_regla, width=50)
    entrada_nombre.pack(pady=5)

    tk.Label(ventana_regla, text="Descripción:").pack(anchor="w", padx=10)
    entrada_descripcion = tk.Text(ventana_regla, height=4, width=50)
    entrada_descripcion.pack(pady=5)

    # Campo para los síntomas
    tk.Label(ventana_regla, text="Síntomas (nombre:peso, separados por comas):").pack(anchor="w", padx=10)
    entrada_sintomas = tk.Entry(ventana_regla, width=50)
    entrada_sintomas.pack(pady=5)

    # Campo para el tratamiento
    tk.Label(ventana_regla, text="Tratamiento:").pack(anchor="w", padx=10)
    entrada_tratamiento = tk.Entry(ventana_regla, width=50)
    entrada_tratamiento.pack(pady=5)

    # Campo para los medicamentos
    tk.Label(ventana_regla, text="Medicamentos (separados por comas):").pack(anchor="w", padx=10)
    entrada_medicamentos = tk.Entry(ventana_regla, width=50)
    entrada_medicamentos.pack(pady=5)

    def guardar_regla():
        # Obtener los datos ingresados
        nombre = entrada_nombre.get().strip().lower()
        descripcion = entrada_descripcion.get("1.0", tk.END).strip()
        sintomas_raw = entrada_sintomas.get().strip()
        tratamiento = entrada_tratamiento.get().strip()
        medicamentos_raw = entrada_medicamentos.get().strip()

        if not nombre or not descripcion or not sintomas_raw or not tratamiento or not medicamentos_raw:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Procesar los síntomas
        sintomas = {}
        try:
            for sintoma in sintomas_raw.split(","):
                nombre_sintoma, peso = sintoma.split(":")
                sintomas[nombre_sintoma.strip().lower()] = int(peso.strip())
        except ValueError:
            messagebox.showerror("Error", "Formato de síntomas incorrecto. Use 'nombre:peso'.")
            return

        # Procesar los medicamentos
        medicamentos = [medicamento.strip() for medicamento in medicamentos_raw.split(",")]

        # Crear la nueva regla
        nueva_regla = {
            "descripcion": descripcion,
            "sintomas": sintomas,
            "tratamiento": tratamiento,
            "medicamentos": medicamentos,
        }

        # Guardar la nueva regla en la base de conocimiento
        base_conocimiento[nombre] = nueva_regla
        guardar_base_conocimiento()

        # Guardar las reglas en el archivo de reglas
        reglas = cargar_reglas()
        reglas[nombre] = {
            "si": [sintoma for sintoma in sintomas.keys()],
            "no": []  # Agrega lógica para condiciones "no" si es necesario
        }
        guardar_reglas(reglas)

        messagebox.showinfo("Éxito", f"La enfermedad '{nombre.capitalize()}' se agregó exitosamente.")
        ventana_regla.destroy()

    # Botón para guardar la regla
    tk.Button(ventana_regla, text="Guardar Regla", command=guardar_regla, width=20, bg="green", fg="white").pack(pady=10)

    # Botón para cancelar
    tk.Button(ventana_regla, text="Cancelar", command=ventana_regla.destroy, width=20).pack(pady=5)


# Guardar la base de conocimiento en un archivo JSON
def guardar_base_conocimiento():
    with open("base_conocimiento.json", "w", encoding="utf-8") as archivo:
        json.dump(base_conocimiento, archivo, indent=4, ensure_ascii=False)


# Base de conocimiento global
base_conocimiento = inicializar_bc()
inicializar_diagnosticos()

# Función para realizar backward chaining
def backward_chaining(nombre, edad, genero, sintomas_iniciales):
    posibles_enfermedades = []

    # Generar hipótesis basadas en los síntomas iniciales
    for enfermedad, datos in base_conocimiento.items():
        sintomas_enfermedad = datos["sintomas"]
        if isinstance(sintomas_enfermedad, list):
            sintomas_enfermedad = {sintoma: 1 for sintoma in sintomas_enfermedad}  # Convertir a dict con peso = 1

        sintomas_presentes = [s for s in sintomas_iniciales if s in sintomas_enfermedad]
        peso_total = sum(sintomas_enfermedad.values())
        peso_coincidencia = sum(sintomas_enfermedad[s] for s in sintomas_presentes)

        if peso_coincidencia > 0:
            porcentaje = (peso_coincidencia / peso_total) * 100
            posibles_enfermedades.append({
                "nombre": enfermedad,
                "descripcion": datos["descripcion"],
                "sintomas": list(sintomas_enfermedad.keys()),
                "tratamiento": datos["tratamiento"],
                "medicamentos": datos["medicamentos"],
                "coincidencias": sintomas_presentes,
                "faltantes": [s for s in sintomas_enfermedad if s not in sintomas_iniciales],
                "porcentaje": porcentaje,
                "peso_coincidencia": peso_coincidencia,
                "sintomas_con_peso": sintomas_enfermedad  # Guardar pesos para explicación
            })

    if not posibles_enfermedades:
        messagebox.showinfo("Diagnóstico", "No se encontró ninguna enfermedad coincidente.")
        return

    # Realizar preguntas para confirmar síntomas faltantes
    for enfermedad in posibles_enfermedades:
        sintomas_faltantes = enfermedad["faltantes"].copy()  # Crear copia para modificar
        for sintoma in sintomas_faltantes:
            respuesta = messagebox.askyesno("Confirmar Síntoma", f"¿Presenta el síntoma: {sintoma}?")
            if respuesta:
                enfermedad["coincidencias"].append(sintoma)
                enfermedad["faltantes"].remove(sintoma)
                enfermedad["peso_coincidencia"] += base_conocimiento[enfermedad["nombre"]]["sintomas"][sintoma]
                enfermedad["porcentaje"] = (enfermedad["peso_coincidencia"] / sum(base_conocimiento[enfermedad["nombre"]]["sintomas"].values())) * 100

    # Filtrar enfermedades con cero coincidencia tras preguntar
    posibles_enfermedades = [e for e in posibles_enfermedades if e["peso_coincidencia"] > 0]

    if not posibles_enfermedades:
        messagebox.showinfo("Diagnóstico", "No se encontró ninguna enfermedad coincidente después de confirmar los síntomas.")
        return

    # Ordenar por porcentaje de coincidencia actualizado
    posibles_enfermedades.sort(key=lambda x: x["porcentaje"], reverse=True)

    # Guardar diagnóstico
    diagnostico_final = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nombre": nombre,
        "edad": edad,
        "genero": genero,
        "sintomas": sintomas_iniciales,
        "diagnostico": posibles_enfermedades
    }
    guardar_diagnostico(diagnostico_final)

    # Mostrar resultados finales
    mensaje = f"Diagnóstico para {nombre}, {edad} años, {genero}:\n\n"
    principal = posibles_enfermedades[0]
    mensaje += (
        f"Enfermedad Principal: {principal['nombre'].capitalize()}\n"
        f"Descripción: {principal['descripcion']}\n"
        f"Coincidencia de síntomas (peso): {principal['peso_coincidencia']}/{sum(base_conocimiento[principal['nombre']]['sintomas'].values())} ({principal['porcentaje']:.2f}%)\n"
        f"Tratamiento: {principal['tratamiento']}\n"
        f"Medicamentos: {', '.join(principal['medicamentos'])}\n"
    )

    # Botón para mostrar explicación
    def mostrar_explicacion():
        ventana_explicacion = tk.Toplevel(root)
        ventana_explicacion.title("Explicación del Diagnóstico")
        ventana_explicacion.geometry("600x500")

        explicacion = f"Enfermedad Principal: {principal['nombre'].capitalize()}\n"
        explicacion += f"Descripción: {principal['descripcion']}\n\n"
        explicacion += "--- Síntomas Confirmados ---\n"
        for sintoma in principal["coincidencias"]:
            peso = principal["sintomas_con_peso"][sintoma]
            explicacion += f"- {sintoma.capitalize()} (Peso: {peso})\n"
        explicacion += "\n--- Síntomas Faltantes ---\n"
        for sintoma in principal["faltantes"]:
            peso = principal["sintomas_con_peso"][sintoma]
            explicacion += f"- {sintoma.capitalize()} (Peso: {peso})\n"
        explicacion += f"\nCoincidencia Total: {principal['peso_coincidencia']}/{sum(principal['sintomas_con_peso'].values())} ({principal['porcentaje']:.2f}%)"

        text_explicacion = tk.Text(ventana_explicacion, wrap="word", height=30, width=80)
        text_explicacion.insert("1.0", explicacion)
        text_explicacion.configure(state="disabled")  # Solo lectura
        text_explicacion.pack(padx=10, pady=10)

    tk.Button(root, text="Explicación del Diagnóstico", command=mostrar_explicacion).pack(pady=10)
    messagebox.showinfo("Diagnóstico Final", mensaje)


# Función para mostrar el formulario del paciente
def formulario_paciente():
    ventana_formulario = tk.Toplevel(root)
    ventana_formulario.title("Formulario del Paciente")
    ventana_formulario.geometry("600x400")

    # Variables para los datos del paciente
    nombre_var = tk.StringVar()
    edad_var = tk.StringVar()
    genero_var = tk.StringVar()

    # Datos del paciente
    tk.Label(ventana_formulario, text="Datos del Paciente", font=("Arial", 14)).pack(pady=10)
    tk.Label(ventana_formulario, text="Nombre:").pack(anchor="w", padx=10)
    tk.Entry(ventana_formulario, textvariable=nombre_var).pack(fill="x", padx=10)

    tk.Label(ventana_formulario, text="Edad:").pack(anchor="w", padx=10)
    tk.Entry(ventana_formulario, textvariable=edad_var).pack(fill="x", padx=10)

    tk.Label(ventana_formulario, text="Género:").pack(anchor="w", padx=10)
    tk.Entry(ventana_formulario, textvariable=genero_var).pack(fill="x", padx=10)

    def comenzar_preguntas():
        nombre = nombre_var.get().strip()
        edad = edad_var.get().strip()
        genero = genero_var.get().strip()

        if not nombre or not edad or not genero:
            messagebox.showwarning("Advertencia", "Todos los campos del formulario deben ser completados.")
            return

        ventana_formulario.destroy()

        # Lógica de preguntas
        realizar_preguntas(nombre, edad, genero)

    tk.Button(ventana_formulario, text="Comenzar Diagnóstico", command=comenzar_preguntas).pack(pady=20)

def realizar_preguntas(nombre, edad, genero):
    # Inicializar preguntas dinámicas
    sintomas_restantes = {sintoma for datos in base_conocimiento.values() for sintoma in datos["sintomas"]}
    sintomas_confirmados = []
    enfermedades_posibles = list(base_conocimiento.keys())

    def siguiente_pregunta():
        nonlocal sintomas_restantes, sintomas_confirmados

        if not sintomas_restantes:
            # Finalizar diagnóstico si no hay más síntomas
            generar_diagnostico(nombre, edad, genero, sintomas_confirmados, enfermedades_posibles)
            ventana_preguntas.destroy()
            return

        # Seleccionar un síntoma para preguntar
        sintoma_actual = sintomas_restantes.pop()

        # Limpiar la ventana para la siguiente pregunta
        for widget in ventana_preguntas.winfo_children():
            widget.destroy()

        tk.Label(
            ventana_preguntas,
            text=f"¿Presenta el síntoma: {sintoma_actual.capitalize()}?",
            font=("Arial", 12)
        ).pack(pady=20)

        def respuesta_si():
            sintomas_confirmados.append(sintoma_actual)
            siguiente_pregunta()

        def respuesta_no():
            siguiente_pregunta()

        # Botones para responder "Sí" o "No"
        tk.Button(ventana_preguntas, text="Sí", command=respuesta_si).pack(side="left", padx=20, pady=10)
        tk.Button(ventana_preguntas, text="No", command=respuesta_no).pack(side="right", padx=20, pady=10)

    def generar_diagnostico(nombre, edad, genero, sintomas_confirmados, enfermedades_posibles):
        # Filtrar enfermedades posibles basándose en los síntomas confirmados
        diagnostico_final = []
        for enfermedad in enfermedades_posibles:
            sintomas_enfermedad = base_conocimiento[enfermedad]["sintomas"]
            peso_total = sum(sintomas_enfermedad.values())
            peso_coincidencia = sum(
                sintomas_enfermedad[s] for s in sintomas_confirmados if s in sintomas_enfermedad
            )
            if peso_coincidencia > 0:
                porcentaje = (peso_coincidencia / peso_total) * 100
                diagnostico_final.append({
                    "nombre": enfermedad,
                    "descripcion": base_conocimiento[enfermedad]["descripcion"],
                    "tratamiento": base_conocimiento[enfermedad]["tratamiento"],
                    "medicamentos": base_conocimiento[enfermedad]["medicamentos"],
                    "coincidencias": sintomas_confirmados,
                    "faltantes": [s for s in sintomas_enfermedad if s not in sintomas_confirmados],
                    "peso_coincidencia": peso_coincidencia,
                    "porcentaje": porcentaje
                })

        # Ordenar por porcentaje de coincidencia
        diagnostico_final.sort(key=lambda x: x["porcentaje"], reverse=True)

        # Guardar diagnóstico en el archivo JSON
        diagnostico_para_guardar = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nombre": nombre,
            "edad": edad,
            "genero": genero,
            "sintomas_confirmados": sintomas_confirmados,
            "diagnostico": diagnostico_final
        }
        guardar_diagnostico(diagnostico_para_guardar)

        # Mostrar diagnóstico final
        if diagnostico_final:
            mensaje = f"Diagnóstico para {nombre}, {edad} años, {genero}:\n\n"
            for enfermedad in diagnostico_final:
                mensaje += (
                    f"Enfermedad: {enfermedad['nombre'].capitalize()}\n"
                    f"Descripción: {enfermedad['descripcion']}\n"
                    f"Coincidencia de síntomas: {enfermedad['peso_coincidencia']} / {sum(base_conocimiento[enfermedad['nombre']]['sintomas'].values())} "
                    f"({enfermedad['porcentaje']:.2f}%)\n"
                    f"Tratamiento: {enfermedad['tratamiento']}\n"
                    f"Medicamentos: {', '.join(enfermedad['medicamentos'])}\n\n"
                )
            messagebox.showinfo("Diagnóstico Final", mensaje)
        else:
            messagebox.showinfo("Diagnóstico", "No se encontró ninguna enfermedad coincidente.")

    # Crear la ventana de preguntas
    ventana_preguntas = tk.Toplevel(root)
    ventana_preguntas.title("Preguntas de Diagnóstico")
    ventana_preguntas.geometry("400x200")

    siguiente_pregunta()



def generar_diagnostico(nombre, edad, genero, sintomas_confirmados, enfermedades_posibles):
    # Filtrar enfermedades posibles basándose en los síntomas confirmados
    diagnostico_final = []
    for enfermedad in enfermedades_posibles:
        sintomas_enfermedad = base_conocimiento[enfermedad]["sintomas"]
        peso_total = sum(sintomas_enfermedad.values())
        peso_coincidencia = sum(
            sintomas_enfermedad[s] for s in sintomas_confirmados if s in sintomas_enfermedad
        )
        if peso_coincidencia > 0:
            porcentaje = (peso_coincidencia / peso_total) * 100
            diagnostico_final.append({
                "nombre": enfermedad,
                "descripcion": base_conocimiento[enfermedad]["descripcion"],
                "tratamiento": base_conocimiento[enfermedad]["tratamiento"],
                "medicamentos": base_conocimiento[enfermedad]["medicamentos"],
                "coincidencias": sintomas_confirmados,
                "faltantes": [s for s in sintomas_enfermedad if s not in sintomas_confirmados],
                "peso_coincidencia": peso_coincidencia,
                "porcentaje": porcentaje,
                "sintomas_con_peso": sintomas_enfermedad  # Agregar clave explícitamente
            })

    # Ordenar por porcentaje de coincidencia
    diagnostico_final.sort(key=lambda x: x["porcentaje"], reverse=True)

    # Guardar diagnóstico en el archivo JSON
    diagnostico_para_guardar = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nombre": nombre,
        "edad": edad,
        "genero": genero,
        "sintomas_confirmados": sintomas_confirmados,
        "diagnostico": diagnostico_final
    }
    guardar_diagnostico(diagnostico_para_guardar)

    # Mostrar diagnóstico final
    if diagnostico_final:
        mensaje = f"Diagnóstico para {nombre}, {edad} años, {genero}:\n\n"
        for enfermedad in diagnostico_final:
            mensaje += (
                f"Enfermedad: {enfermedad['nombre'].capitalize()}\n"
                f"Descripción: {enfermedad['descripcion']}\n"
                f"Coincidencia de síntomas: {enfermedad['peso_coincidencia']} / {sum(base_conocimiento[enfermedad['nombre']]['sintomas'].values())} "
                f"({enfermedad['porcentaje']:.2f}%)\n"
                f"Tratamiento: {enfermedad['tratamiento']}\n"
                f"Medicamentos: {', '.join(enfermedad['medicamentos'])}\n\n"
            )
        messagebox.showinfo("Diagnóstico Final", mensaje)
    else:
        messagebox.showinfo("Diagnóstico", "No se encontró ninguna enfermedad coincidente.")



# Función para consultar diagnósticos
def consultar_diagnosticos():
    # Crear la ventana de consulta
    ventana_consulta = tk.Toplevel(root)
    ventana_consulta.title("Consultar Diagnósticos")
    ventana_consulta.geometry("600x400")

    tk.Label(ventana_consulta, text="Diagnósticos Guardados", font=("Arial", 14)).pack(pady=10)

    # Cargar diagnósticos desde el archivo JSON
    diagnosticos = cargar_diagnosticos()

    if not diagnosticos:
        tk.Label(ventana_consulta, text="No hay diagnósticos registrados.").pack(pady=10)
        return

    # Crear una lista para mostrar los diagnósticos
    listbox = tk.Listbox(ventana_consulta, width=80, height=20)
    listbox.pack(pady=10)

    for i, diag in enumerate(diagnosticos):
        listbox.insert(tk.END, f"{i + 1}. {diag['fecha']} - {diag['nombre']} ({diag['edad']} años, {diag['genero']})")

    def abrir_diagnostico():
        seleccion = listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un diagnóstico de la lista.")
            return

        index = seleccion[0]
        diag = diagnosticos[index]

        ventana_detalles = tk.Toplevel(ventana_consulta)
        ventana_detalles.title("Detalles del Diagnóstico")
        ventana_detalles.geometry("600x600")

        # Diagnóstico general
        detalles = (
            f"FECHA: {diag['fecha']}\n"
            f"NOMBRE DEL PACIENTE: {diag['nombre']}\n"
            f"EDAD: {diag['edad']} años\n"
            f"GÉNERO: {diag['genero']}\n"
            f"\n{'=' * 50}\n"
            f"                  DIAGNÓSTICO GENERAL\n"
            f"{'=' * 50}\n\n"
        )

        for enfermedad in diag["diagnostico"]:
            # Validar si 'sintomas_con_peso' existe; si no, reconstruirlo
            if "sintomas_con_peso" not in enfermedad:
                enfermedad["sintomas_con_peso"] = base_conocimiento.get(enfermedad["nombre"], {}).get("sintomas", {})
                if not enfermedad["sintomas_con_peso"]:
                    messagebox.showerror(
                        "Error",
                        f"No se encontraron datos de síntomas para la enfermedad '{enfermedad['nombre']}'."
                    )
                    return

            # Validar si 'peso_coincidencia' existe; si no, calcularlo
            if "peso_coincidencia" not in enfermedad:
                enfermedad["peso_coincidencia"] = sum(
                    enfermedad["sintomas_con_peso"].get(sintoma, 1) for sintoma in enfermedad.get("coincidencias", [])
                )

            detalles += (
                f"ENFERMEDAD: {enfermedad['nombre'].capitalize()}\n"
                f"  Descripción: {enfermedad['descripcion']}\n"
                f"  Coincidencia de síntomas (peso): {enfermedad['peso_coincidencia']} / "
                f"{sum(enfermedad['sintomas_con_peso'].values())} ({enfermedad.get('porcentaje', 0):.2f}%)\n"
                f"  Tratamiento: {enfermedad['tratamiento']}\n"
                f"  Medicamentos: {', '.join(enfermedad['medicamentos'])}\n"
                f"\n{'-' * 50}\n"
                f"               EXPLICACIÓN DETALLADA\n"
                f"{'-' * 50}\n"
            )

            # Síntomas Confirmados
            detalles += "  SÍNTOMAS CONFIRMADOS:\n"
            for sintoma in enfermedad.get("coincidencias", []):
                peso = enfermedad["sintomas_con_peso"].get(sintoma, 1)  # Asumir peso predeterminado de 1 si no está definido
                detalles += f"    - {sintoma.capitalize():<20} (Peso: {peso})\n"

            # Síntomas Faltantes
            detalles += "\n  SÍNTOMAS FALTANTES:\n"
            for sintoma in enfermedad.get("faltantes", []):
                peso = enfermedad["sintomas_con_peso"].get(sintoma, 1)  # Asumir peso predeterminado de 1 si no está definido
                detalles += f"    - {sintoma.capitalize():<20} (Peso: {peso})\n"
            detalles += f"\n{'=' * 50}\n\n"

        # Crear una caja de texto para mostrar los detalles
        text_area = tk.Text(ventana_detalles, wrap="word", height=30, width=80)
        text_area.insert("1.0", detalles)
        text_area.configure(state="disabled")  # Hacer el texto solo lectura
        text_area.pack(padx=10, pady=10)

    tk.Button(ventana_consulta, text="Abrir Diagnóstico", command=abrir_diagnostico).pack(pady=10)


# Función para ver estadísticas de diagnósticos
def ver_estadisticas():
    # Crear ventana para mostrar estadísticas
    ventana_estadisticas = tk.Toplevel(root)
    ventana_estadisticas.title("Estadísticas de Diagnósticos")
    ventana_estadisticas.geometry("600x500")

    tk.Label(ventana_estadisticas, text="Estadísticas Generales", font=("Arial", 16)).pack(pady=10)

    # Cargar diagnósticos desde el archivo JSON
    diagnosticos = cargar_diagnosticos()

    if not diagnosticos:
        tk.Label(ventana_estadisticas, text="No hay diagnósticos registrados para mostrar estadísticas.").pack(pady=10)
        return

    # Calcular estadísticas
    conteo_enfermedades = {}
    coincidencias_enfermedades = {}
    conteo_sintomas = {}

    for diag in diagnosticos:
        for enfermedad in diag["diagnostico"]:
            nombre_enfermedad = enfermedad["nombre"]
            porcentaje = enfermedad.get("porcentaje", 0)

            # Contar ocurrencias de la enfermedad
            if nombre_enfermedad not in conteo_enfermedades:
                conteo_enfermedades[nombre_enfermedad] = 0
                coincidencias_enfermedades[nombre_enfermedad] = []
            conteo_enfermedades[nombre_enfermedad] += 1
            coincidencias_enfermedades[nombre_enfermedad].append(porcentaje)

            # Contar ocurrencias de síntomas
            for sintoma in enfermedad.get("coincidencias", []):
                if sintoma not in conteo_sintomas:
                    conteo_sintomas[sintoma] = 0
                conteo_sintomas[sintoma] += 1

    # Generar texto de estadísticas
    texto_estadisticas = "Enfermedades Más Diagnosticadas:\n"
    for enfermedad, conteo in sorted(conteo_enfermedades.items(), key=lambda x: x[1], reverse=True):
        promedio_coincidencia = (
            sum(coincidencias_enfermedades[enfermedad]) / len(coincidencias_enfermedades[enfermedad])
        )
        texto_estadisticas += f"- {enfermedad.capitalize()}: {conteo} diagnósticos, Coincidencia promedio: {promedio_coincidencia:.2f}%\n"

    texto_estadisticas += "\nSíntomas Más Frecuentes:\n"
    for sintoma, conteo in sorted(conteo_sintomas.items(), key=lambda x: x[1], reverse=True):
        texto_estadisticas += f"- {sintoma.capitalize()}: {conteo} ocurrencias\n"

    # Mostrar estadísticas en un cuadro de texto
    text_area = tk.Text(ventana_estadisticas, wrap="word", height=25, width=70)
    text_area.insert("1.0", texto_estadisticas)
    text_area.configure(state="disabled")  # Solo lectura
    text_area.pack(padx=10, pady=10)

def consultar_reglas():
    ventana_reglas = tk.Toplevel(root)
    ventana_reglas.title("Consultar Reglas")
    ventana_reglas.geometry("600x400")

    tk.Label(ventana_reglas, text="Reglas Guardadas", font=("Arial", 16)).pack(pady=10)

    reglas = cargar_reglas()
    if not reglas:
        tk.Label(ventana_reglas, text="No hay reglas registradas.").pack(pady=10)
        return

    listbox = tk.Listbox(ventana_reglas, width=80, height=20)
    listbox.pack(pady=10)

    for nombre, regla in reglas.items():
        listbox.insert(tk.END, f"{nombre.capitalize()}: {regla}")

    def mostrar_arbol():
        seleccion = listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una regla de la lista.")
            return

        nombre = list(reglas.keys())[seleccion[0]]
        regla = reglas[nombre]

        def dibujar_arbol(arbol, x=0, y=0, dx=1.5, dy=1, ax=None):
            if not arbol:
                return

            if ax is None:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.axis('off')

            ax.text(x, y, arbol["nombre"], ha='center', va='center',
                    bbox=dict(boxstyle="round", fc="lightblue"))

            if "si" in arbol and arbol["si"]:
                for i, nodo in enumerate(arbol["si"]):
                    ax.plot([x, x - dx], [y, y - dy], 'k-')
                    dibujar_arbol(nodo, x - dx, y - dy, dx * 0.6, dy, ax)

            if "no" in arbol and arbol["no"]:
                for i, nodo in enumerate(arbol["no"]):
                    ax.plot([x, x + dx], [y, y - dy], 'k-')
                    dibujar_arbol(nodo, x + dx, y - dy, dx * 0.6, dy, ax)

            if not ax:
                plt.show()

        # Convertir regla a formato de árbol semántico
        arbol = {"nombre": nombre, "si": [{"nombre": r} for r in regla.get("si", [])],
                 "no": [{"nombre": r} for r in regla.get("no", [])]}

        dibujar_arbol(arbol)

    tk.Button(ventana_reglas, text="Mostrar Árbol", command=mostrar_arbol).pack(pady=10)    



# Interfaz gráfica principal
root = tk.Tk()
root.title("Sistema Experto Médico")
root.geometry("400x300")

# Widgets de la interfaz
label_title = tk.Label(root, text="Sistema Experto Médico", font=("Arial", 16))
label_title.pack(pady=20)

btn_formulario = tk.Button(root, text="Nuevo Diagnóstico", command=formulario_paciente, width=30)
btn_formulario.pack(pady=10)

btn_consultar = tk.Button(root, text="Consultar Diagnósticos", command=consultar_diagnosticos, width=30)
btn_consultar.pack(pady=10)

btn_salir = tk.Button(root, text="Salir", command=root.destroy, width=30, bg="red", fg="white")
btn_salir.pack(pady=20)

btn_estadisticas = tk.Button(root, text="Ver Estadísticas", command=ver_estadisticas, width=30)
btn_estadisticas.pack(pady=5)

btn_agregar_regla = tk.Button(root, text="Agregar Nueva Regla", command=agregar_regla, width=30)
btn_agregar_regla.pack(pady=5)

btn_consultar_reglas = tk.Button(root, text="Consultar Reglas", command=consultar_reglas, width=30)
btn_consultar_reglas.pack(pady=5)



# Ejecutar la interfaz
root.mainloop()
