import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Generador TC Purista", page_icon="🩻", layout="centered")

# --- TITULO E INTERFAZ ---
st.title("🩻 Generador de Reportes TC - Estilo Purista")
st.markdown("Ingresa los diagnósticos y presiona generar. El sistema aplicará el Motor Lógico y los 4 Módulos Anatómicos.")

# --- CONFIGURACIÓN DE LA API KEY ---
# Streamlit leerá la llave secreta desde su configuración
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# --- FUNCIÓN PARA CARGAR LOS MÓDULOS ---
@st.cache_data # Esto hace que los archivos se lean una sola vez para que sea súper rápido
def load_modules():
    modulos = ""
    archivos = [
        "MODULO_1_MOTOR_LOGICO.txt",
        "MODULO_2_NEURO_Y_CUELLO.txt",
        "MODULO_3_TORAX.txt",
        "MODULO_4_ABDOMEN_Y_PELVIS.txt",
        "MODULO_5_MSK_Y_TRAUMA.txt"
    ]
    for archivo in archivos:
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                modulos += f"\n\n{f.read()}"
        except FileNotFoundError:
            st.warning(f"No se encontró el archivo: {archivo}")
    return modulos

# --- INICIALIZAR EL MODELO ---
texto_base_datos = load_modules()

# Usamos el modelo flash que es rapidísimo y excelente para texto
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=texto_base_datos # Le inyectamos todo tu conocimiento como instrucción de sistema
)

# --- CAJA DE TEXTO PARA EL USUARIO ---
input_usuario = st.text_area("Diagnósticos de entrada:", height=150, placeholder="Ej: TCE, hematoma subdural derecho, normal...")

if st.button("Generar Reporte", type="primary"):
    if input_usuario.strip() == "":
        st.error("Por favor, ingresa al menos un diagnóstico.")
    else:
        with st.spinner("Procesando reporte con criterios puristas..."):
            try:
                # Enviamos el input al modelo
                respuesta = model.generate_content(input_usuario)
                
                st.success("¡Reporte generado con éxito!")
                
                # Mostramos el resultado en una caja de texto para que sea fácil de copiar
                st.text_area("Cuerpo del Informe:", value=respuesta.text, height=300)
                
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")