import streamlit as st
from datetime import datetime, timedelta

st.title("Calculadora de Citas Intravítreas")

farmacos = ["AVASTIN", "XIMLUCI", "VABYSMO", "EYLEA 2MG", "EYLEA 8MG"]

# Entrada de fecha
fecha_input = st.date_input("Fecha del último tratamiento", datetime.today())

# Selector de ojo
ojo = st.selectbox("Ojo a tratar", ["Elige", "Derecho", "Izquierdo", "Ambos"])

# Función para calcular fechas

def formatear_semana(fecha):
    lunes = fecha - timedelta(days=fecha.weekday())
    viernes = lunes + timedelta(days=4)
    return f"{lunes.strftime('%d-%m-%Y')} al {viernes.strftime('%d-%m-%Y')}"

def lunes_a_viernes(fecha):
    while fecha.weekday() > 4:
        fecha += timedelta(days=1)
    return fecha

def calcular_fechas(base, intervalos):
    fechas = []
    acumulado = base
    for semanas in intervalos:
        acumulado += timedelta(weeks=semanas)
        fechas.append(lunes_a_viernes(acumulado))
    return fechas

resultado = ""

if ojo in ["Derecho", "Ambos"]:
    st.subheader("Ojo Derecho")
    farmaco_d = st.selectbox("Fármaco OD", farmacos, key='farm_d')
    dosis_d = st.number_input("Número de dosis OD", min_value=1, step=1, key='dosis_d')
    intervalos_d = []
    for i in range(dosis_d):
        sem = st.number_input(f"Intervalo {i+1} (semanas) OD", min_value=0, step=1, key=f"int_d_{i}")
        intervalos_d.append(sem)

    if intervalos_d:
        fechas = calcular_fechas(fecha_input, intervalos_d)
        resultado += f"\nOD ({farmaco_d}):\n"
        for i, f in enumerate(fechas):
            resultado += f"Dosis {i+1}: semana del {formatear_semana(f)}\n"

if ojo in ["Izquierdo", "Ambos"]:
    st.subheader("Ojo Izquierdo")
    farmaco_i = st.selectbox("Fármaco OI", farmacos, key='farm_i')
    dosis_i = st.number_input("Número de dosis OI", min_value=1, step=1, key='dosis_i')
    intervalos_i = []
    for i in range(dosis_i):
        sem = st.number_input(f"Intervalo {i+1} (semanas) OI", min_value=0, step=1, key=f"int_i_{i}")
        intervalos_i.append(sem)

    if intervalos_i:
        fechas = calcular_fechas(fecha_input, intervalos_i)
        resultado += f"\nOI ({farmaco_i}):\n"
        for i, f in enumerate(fechas):
            resultado += f"Dosis {i+1}: semana del {formatear_semana(f)}\n"

if st.button("Calcular"):
    st.text_area("Resultado", resultado, height=300)
