import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Generador TC Purista", page_icon="🩻", layout="centered")

# --- TITULO ---
st.title("🩻 Generador TC - Estilo Purista")
st.markdown("Ingresa los diagnósticos y presiona generar.")

# --- API KEY ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Error: No se encontró la API Key en los Secrets de Streamlit.")

# --- CARGAR MÓDULOS ---
@st.cache_data
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
            st.warning(f"No se encontró: {archivo}")
    return modulos

# --- INICIALIZAR EL MOTOR ---
contexto_completo = load_modules()

# Usamos 'gemini-1.5-flash', que es el estándar actual más estable y rápido
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=contexto_completo
)

# --- INTERFAZ DE USUARIO ---
input_usuario = st.text_area("Diagnósticos (Input):", height=150, placeholder="Ej: TCE, hematoma subdural derecho...")

if st.button("Generar Reporte", type="primary"):
    if not input_usuario.strip():
        st.error("Escribe algo para procesar.")
    else:
        with st.spinner("Procesando con rigor radiológico..."):
            try:
                # Generar contenido
                response = model.generate_content(input_usuario)
                
                # Resultado
                st.success("¡Reporte listo!")
                st.text_area("Cuerpo del Informe (Output):", value=response.text, height=350)
                st.info("Copia el texto de arriba directamente a tu sistema de informes.")
                
            except Exception as e:
                # Si falla el 1.5 Flash por alguna razón de región, probamos el nombre alternativo
                st.error(f"Error técnico: {e}")
                st.info("Sugerencia: Verifica que tu API Key sea válida en Google AI Studio.")
