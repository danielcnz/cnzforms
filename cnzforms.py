import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configuración de la Base de Datos
def crear_db():
    conn = sqlite3.connect('encuesta.db')
    c = conn.cursor()
    # Creamos la tabla con 10 columnas de preguntas + fecha
    c.execute('''CREATE TABLE IF NOT EXISTS respuestas
                 (fecha TEXT, p1 TEXT, p2 TEXT, p3 TEXT, p4 TEXT, p5 TEXT, 
                  p6 TEXT, p7 TEXT, p8 TEXT, p9 TEXT, p10 TEXT)''')
    conn.commit()
    conn.close()

crear_db()

st.title("📋 Sistema de Encuestas Privado")

# 2. Formulario de Entrada
with st.form("encuesta_form", clear_on_submit=True):
    st.subheader("Por favor, completa tus datos")
    
    respuestas = []
    for i in range(1, 11):
        respuestas.append(st.text_input(f"Pregunta {i}:", key=f"q{i}"))
    
    boton_enviar = st.form_submit_button("Enviar Respuestas")

if boton_enviar:
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('encuesta.db')
    c = conn.cursor()
    c.execute("INSERT INTO respuestas VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
              (fecha_actual, *respuestas))
    conn.commit()
    conn.close()
    st.success("¡Tus respuestas han sido guardadas localmente!")

# 3. Sección de Administración (Descarga)
st.markdown("---")
with st.expander("🛠️ Panel de Administración"):
    password = st.text_input("Introduce la clave para descargar datos:", type="password")
    if password == "1234": # Puedes cambiar esta clave
        conn = sqlite3.connect('encuesta.db')
        df = pd.read_sql_query("SELECT * FROM respuestas", conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(df) # Vista previa de los datos
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Base de Datos (CSV)",
                data=csv,
                file_name=f"reporte_encuesta_{datetime.now().strftime('%d_%m')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("Aún no hay respuestas registradas.")
