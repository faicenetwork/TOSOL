import streamlit as st
import pandas as pd
from supabase import create_client

# 1. Configuración de la página
st.set_page_config(page_title="Panel KINESLAB", page_icon="📅", layout="wide")

# 2. Inicializar el estado de la contraseña si no existe
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# 3. Control de Pantallas
if not st.session_state.autenticado:
    # --- PANTALLA DE LOGIN ---
    st.title("🔒 Panel Protegido")
    st.info("Por favor, introduce la contraseña para ver la agenda del consultorio.")
    
    password = st.text_input("Contraseña de acceso:", type="password", key="password_input")
    boton_ingresar = st.button("Ingresar")
    
    if boton_ingresar:
        if password == "sol2026":
            st.session_state.autenticado = True
            st.rerun()  # Limpia el navegador de forma segura y redibuja la pantalla
        else:
            st.error("❌ Contraseña incorrecta")
else:
    # --- PANTALLA PRINCIPAL (SÓLO SI YA SE AUTENTICÓ) ---
    st.title("📅 Panel de Control de Turnos")
    st.write("Hola Sol, aquí tenés la lista actualizada de pacientes que reservaron desde la web.")
    
    # Botón para cerrar sesión en la barra lateral
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

    # 4. Conexión a Supabase
    URL_SUPABASE = "https://alfbhquzojffyqitftbn.supabase.co"
    CLAVE_SUPABASE = "sb_publishable_Brou4uCaIEgQvF5NuPIdyg_94cFl22W"
    
    try:
        supabase = create_client(URL_SUPABASE, CLAVE_SUPABASE)
        resultado = supabase.table("turnos").select("*").order("fecha", descending=False).execute()

        if resultado.data:
            df = pd.DataFrame(resultado.data)
            df_limpio = df[['fecha', 'hora', 'nombre_paciente', 'telefono', 'notas']].rename(
                columns={
                    'fecha': '📅 Fecha',
                    'hora': '⏰ Hora',
                    'nombre_paciente': '👤 Paciente',
                    'telefono': '📱 WhatsApp',
                    'notas': '📝 Notas'
                }
            )
            
            buscar = st.text_input("🔍 Buscar paciente por nombre:")
            if buscar:
                df_limpio = df_limpio[df_limpio['👤 Paciente'].str.contains(buscar, case=False)]

            st.dataframe(df_limpio, use_container_width=True, hide_index=True)
            st.success(f"Se encontraron {len(df_limpio)} turnos registrados.")
        else:
            st.info("No hay turnos registrados todavía.")
            
    except Exception as e:
        st.error(f"Error de conexión con la base de datos: {e}")
