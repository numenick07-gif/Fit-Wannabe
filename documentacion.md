# Documentación Técnica: Fit Wannabe

## 1. Arquitectura del Proyecto
Fit Wannabe es una aplicación web interactiva desarrollada con el framework Streamlit. Utiliza un esquema de enrutamiento basado en el estado de la sesión (`st.session_state`) para ofrecer la experiencia de una Single Page Application (SPA).

## 2. Base de Datos (SQLite)
La aplicación garantiza la privacidad utilizando una base de datos local `fitwannabe.db`.
**Esquema de Tablas:**
- `profile`: Almacena información biométrica y preferencias del usuario (edad, sexo, estatura, objetivos).
- `goals`: Centraliza las metas diarias (pasos, agua en litros, horas de sueño).
- `daily_logs`: Tabla transaccional para el registro diario. Usa la fecha como Primary Key para evitar duplicados y facilitar el reemplazo (`REPLACE INTO`).

## 3. Reglas de Negocio Implementadas
- **Cero Datos Ficticios:** Todo renderizado en la capa visual depende de la validación matemática de la base de datos.
- **Tolerancia a Fallos Matemáticos:** Función dedicada `calc_progress` para manejar divisiones por cero.
- **Manejo de Sobrecumplimiento:** Los progresos visuales están limitados mediante `min(progreso, 1.0)` para no quebrar los widgets de Streamlit, pero el texto muestra porcentajes mayores a 100% libremente.
