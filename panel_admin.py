import streamlit as st
import pandas as pd
from supabase import create_client

# 1. Configuración visual
st.set_page_config(page_title="Panel KINESLAB", page_icon="📅", layout="wide")

# 2. Escudo de seguridad (Contraseña simple)
st.sidebar.title("🔐 Acceso Privado")
password = st.sidebar.text_input("Introduce la contraseña de acceso:", type="password")

# Reemplazá 'sol2026' por la contraseña que quieras darle a ella
if password == "sol2026": 
    st.title("📅 Panel de Control de Turnos")
    st.write("Hola Sol, aquí tenés la lista actualizada de pacientes que reservaron web.")

    # 3. Conexión a Supabase (Poné tus claves reales aquí)
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
            
            # Buscador en tiempo real
            buscar = st.text_input("🔍 Buscar paciente por nombre:")
            if buscar:
                df_limpio = df_limpio[df_limpio['👤 Paciente'].str.contains(buscar, case=False)]

            # Mostrar la tabla estéticamente
            st.dataframe(df_limpio, use_container_width=True, hide_index=True)
            st.success(f"Se encontraron {len(df_limpio)} turnos registrados.")
        else:
            st.info("No hay turnos registrados todavía.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
else:
    if password != "":
        st.sidebar.error("❌ Contraseña incorrecta")
    st.title("🔒 Panel Protegido")
    st.info("Por favor, introduce la contraseña en la barra lateral para ver la agenda.")