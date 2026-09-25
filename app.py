import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y DISEÑO
# ==========================================
st.set_page_config(page_title="Fit Wannabe", page_icon="🌿", layout="wide")

st.markdown('''
    <style>
    :root { --mint-primary: #3EB489; --mint-light: #E8F5EE; --text-dark: #2C3E50; }
    .stApp { background-color: #F8F9F9; }
    div.stButton > button:first-child { background-color: #3EB489; color: white; border: none; border-radius: 8px; font-weight: bold; }
    div.stButton > button:first-child:hover { background-color: #2e8b69; }
    .empty-state { background-color: #E8F5EE; padding: 20px; border-radius: 10px; text-align: center; color: #2C3E50; border-left: 5px solid #3EB489; margin-bottom: 20px; }
    .metric-card { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; }
    .metric-title { font-size: 14px; color: #7F8C8D; text-transform: uppercase; }
    .metric-value { font-size: 24px; font-weight: bold; color: #2C3E50; }
    </style>
''', unsafe_allow_html=True)

# ==========================================
# 2. CAPA DE BASE DE DATOS (SQLITE)
# ==========================================
DB_NAME = "fitwannabe.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS profile (id INTEGER PRIMARY KEY, edad INTEGER, sexo TEXT, estatura REAL, peso_actual REAL, peso_objetivo REAL, nivel_actividad TEXT, objetivo TEXT, unidades TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY, pasos INTEGER, actividad_minutos INTEGER, agua_litros REAL, sueno_horas REAL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS daily_logs (fecha TEXT PRIMARY KEY, peso REAL, pasos INTEGER, actividad TEXT, duracion_minutos INTEGER, agua_litros REAL, sueno_horas REAL, calorias INTEGER, notas TEXT)''')
        conn.commit()

init_db()

def get_profile():
    with get_db() as conn: return conn.execute("SELECT * FROM profile WHERE id=1").fetchone()
def save_profile(data):
    with get_db() as conn:
        conn.execute("DELETE FROM profile WHERE id=1")
        conn.execute("INSERT INTO profile (id, edad, sexo, estatura, peso_actual, peso_objetivo, nivel_actividad, objetivo, unidades) VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        conn.commit()
def get_goals():
    with get_db() as conn: return conn.execute("SELECT * FROM goals WHERE id=1").fetchone()
def save_goals(data):
    with get_db() as conn:
        conn.execute("DELETE FROM goals WHERE id=1")
        conn.execute("INSERT INTO goals (id, pasos, actividad_minutos, agua_litros, sueno_horas) VALUES (1, ?, ?, ?, ?)", data)
        conn.commit()
def get_log(fecha):
    with get_db() as conn: return conn.execute("SELECT * FROM daily_logs WHERE fecha=?", (fecha,)).fetchone()
def save_log(data):
    with get_db() as conn:
        conn.execute("REPLACE INTO daily_logs (fecha, peso, pasos, actividad, duracion_minutos, agua_litros, sueno_horas, calorias, notas) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        conn.commit()
def get_all_logs():
    with get_db() as conn: return pd.read_sql_query("SELECT * FROM daily_logs ORDER BY fecha ASC", conn)

def calc_progress(current, goal):
    if not goal or goal == 0: return None
    if current is None: return 0.0
    return (current / goal)

# ==========================================
# 3. NAVEGACIÓN Y VISTAS
# ==========================================
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Landing Page"

def change_page(page):
    st.session_state.current_page = page

st.sidebar.title("🌿 Fit Wannabe")
menu = ["Landing Page", "Dashboard", "Mi Perfil", "Mis Metas", "Registro Diario", "Historial"]

# Sincronizar el radio button con el session_state
choice = st.sidebar.radio("Navegación", menu, index=menu.index(st.session_state.current_page))
if choice != st.session_state.current_page:
    st.session_state.current_page = choice
    st.rerun()

profile = get_profile()
goals = get_goals()

# --- VISTA: LANDING PAGE ---
if st.session_state.current_page == "Landing Page":
    st.title("🌿 Fit Wannabe")
    st.subheader("Tu Espacio de Salud Personal y Real")
    
    st.markdown("### 📌 El Problema")
    st.write("La mayoría de las aplicaciones de salud están llenas de anuncios, asumen datos genéricos o te obligan a interactuar con perfiles ficticios. **Fit Wannabe** nace de la necesidad de tener una herramienta completamente privada, donde el único progreso que ves es el tuyo, basado 100% en información real.")
    
    st.markdown("### 🎯 Objetivos SMART")
    st.markdown('''
    - **Específico (S):** Proveer un sistema personal para el registro diario de hábitos físicos y de salud.
    - **Medible (M):** Controlar métricas específicas como pasos diarios, hidratación (L), horas de sueño y actividad física.
    - **Alcanzable (A):** Arquitectura basada en Python y Streamlit con base de datos SQLite embebida.
    - **Relevante (R):** Eliminar la frustración de las metas irreales usando el constructo "Cero Datos Ficticios".
    - **Temporal (T):** Desplegable de forma inmediata en la nube o local.
    ''')
    
    st.markdown("### 🏢 Organización")
    st.info("**Diseño y Desarrollo:** Liskeidy Rosario Pérez\n**Ubicación:** Villa Altagracia, San Cristóbal, República Dominicana.")
    
    st.markdown("### 📸 Vistas de la Aplicación")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("[🖼️ Ver Interfaz del Dashboard (Imagen de muestra)](https://via.placeholder.com/800x400.png?text=Dashboard+Fit+Wannabe)")
    with col2:
        st.markdown("[🔗 Enlace al despliegue en Streamlit Cloud](https://fit-wannabe-liskeidy.streamlit.app/)")
        
    st.markdown("---")
    if st.button("🚀 Entrar a la Aplicación", use_container_width=True):
        change_page("Dashboard")
        st.rerun()

# --- VISTA: MI PERFIL ---
elif st.session_state.current_page == "Mi Perfil":
    st.header("👤 Mi Perfil")
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        unidades = col1.selectbox("Sistema", ["Métrico (kg/cm)", "Imperial"], index=0)
        edad = col1.number_input("Edad", min_value=10, value=profile['edad'] if profile else None, step=1)
        sexo = col2.selectbox("Sexo", ["Femenino", "Masculino", "Otro"], index=0)
        estatura = col1.number_input("Estatura", min_value=0.0, value=profile['estatura'] if profile else None)
        peso_actual = col2.number_input("Peso actual", min_value=0.0, value=profile['peso_actual'] if profile else None)
        peso_objetivo = col1.number_input("Peso objetivo", min_value=0.0, value=profile['peso_objetivo'] if profile else None)
        nivel_actividad = col2.selectbox("Actividad", ["Sedentario", "Activo"], index=0)
        objetivo = st.selectbox("Objetivo", ["Mantener", "Perder peso", "Salud"], index=2)
        if st.form_submit_button("Guardar Perfil"):
            save_profile((edad, sexo, estatura, peso_actual, peso_objetivo, nivel_actividad, objetivo, unidades))
            st.success("Perfil guardado.")
            st.rerun()

# --- VISTA: MIS METAS ---
elif st.session_state.current_page == "Mis Metas":
    st.header("🎯 Mis Metas")
    with st.form("goals_form"):
        pasos = st.number_input("Meta de pasos diarios", min_value=0, value=goals['pasos'] if goals else None)
        actividad = st.number_input("Meta actividad (min)", min_value=0, value=goals['actividad_minutos'] if goals else None)
        agua = st.number_input("Meta hidratación (L)", min_value=0.0, value=goals['agua_litros'] if goals else None)
        sueno = st.number_input("Meta sueño (Horas)", min_value=0.0, value=goals['sueno_horas'] if goals else None)
        if st.form_submit_button("Guardar Metas"):
            save_goals((pasos, actividad, agua, sueno))
            st.success("Metas actualizadas.")
            st.rerun()

# --- VISTA: REGISTRO DIARIO ---
elif st.session_state.current_page == "Registro Diario":
    st.header("📝 Registro Diario")
    fecha_sel = st.date_input("Fecha", date.today())
    log_actual = get_log(str(fecha_sel))
    with st.form("log_form"):
        col1, col2 = st.columns(2)
        peso_log = col1.number_input("Peso", value=log_actual['peso'] if log_actual else None)
        pasos_log = col2.number_input("Pasos", value=log_actual['pasos'] if log_actual else None)
        act_log = col1.text_input("Actividad", value=log_actual['actividad'] if log_actual else "")
        dur_log = col2.number_input("Duración (min)", value=log_actual['duracion_minutos'] if log_actual else None)
        agua_log = col1.number_input("Agua (L)", value=log_actual['agua_litros'] if log_actual else None)
        sueno_log = col2.number_input("Sueño (h)", value=log_actual['sueno_horas'] if log_actual else None)
        cal_log = col1.number_input("Calorías", value=log_actual['calorias'] if log_actual else None)
        notas_log = st.text_area("Notas", value=log_actual['notas'] if log_actual else "")
        if st.form_submit_button("Guardar"):
            save_log((str(fecha_sel), peso_log, pasos_log, act_log, dur_log, agua_log, sueno_log, cal_log, notas_log))
            st.success("Guardado.")
            st.rerun()

# --- VISTA: DASHBOARD ---
elif st.session_state.current_page == "Dashboard":
    st.header("🌿 Dashboard")
    hoy = str(date.today())
    log_hoy = get_log(hoy)
    if not log_hoy:
        st.markdown('<div class="empty-state"><h3>Sin registros de hoy</h3></div>', unsafe_allow_html=True)
    else:
        cols = st.columns(4)
        metrics = []
        if goals and goals['pasos']: metrics.append(("Pasos", log_hoy['pasos'], goals['pasos'], "pasos"))
        if goals and goals['actividad_minutos']: metrics.append(("Actividad", log_hoy['duracion_minutos'], goals['actividad_minutos'], "min"))
        if goals and goals['agua_litros']: metrics.append(("Agua", log_hoy['agua_litros'], goals['agua_litros'], "L"))
        if goals and goals['sueno_horas']: metrics.append(("Sueño", log_hoy['sueno_horas'], goals['sueno_horas'], "hrs"))
        
        for i, (titulo, actual, meta, un) in enumerate(metrics):
            with cols[i%4]:
                act = actual if actual else 0
                prog = calc_progress(act, meta)
                st.markdown(f'<div class="metric-card"><div class="metric-title">{titulo}</div><div class="metric-value">{act} / {meta} {un}</div><div>{int(prog*100)}% completado</div></div>', unsafe_allow_html=True)
                st.progress(min(prog, 1.0))

# --- VISTA: HISTORIAL ---
elif st.session_state.current_page == "Historial":
    st.header("📈 Historial")
    df = get_all_logs()
    if df.empty:
        st.info("Sin datos registrados.")
    else:
        df['fecha'] = pd.to_datetime(df['fecha'])
        df.set_index('fecha', inplace=True)
        st.line_chart(df[['pasos']].dropna())
