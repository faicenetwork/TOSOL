```python
import datetime
import pandas as pd
from supabase import create_client

# Usa las mismas credenciales que sacaste en el Paso 3
URL_SUPABASE = "https://alfbhquzojffyqitftbn.supabase.co"
CLAVE_SUPABASE = "
sb_publishable_Brou4uCaIEgQvF5NuPIdyg_94cFl22W"

supabase = create_client(URL_SUPABASE, CLAVE_SUPABASE)

def ver_agenda_de_hoy():
    # Obtener la fecha de hoy en formato AAAA-MM-DD
    hoy = datetime.date.today().isoformat()
    
    # Hacer la consulta filtrando por el día de hoy
    resultado = supabase.table("turnos").select("*").eq("fecha", hoy).execute()
    
    if resultado.data:
        # Convertir los datos a una tabla limpia con Pandas
        df = pd.DataFrame(resultado.data)
        df = df[['hora', 'nombre_paciente', 'telefono', 'notas']]
        
        print(f"\n--- 📅 TURNOS REGISTRADOS PARA HOY ({hoy}) ---")
        print(df.to_string(index=False))
        
        # Opcional: Te genera un archivo Excel en tu carpeta automáticamente
        df.to_excel(f"turnos_{hoy}.xlsx", index=False)
        print(f"\n¡Se ha guardado una copia en: turnos_{hoy}.xlsx!")
    else:
        print(f"\nNo hay turnos agendados en el sistema para hoy ({hoy}).")

if __name__ == "__main__":
    ver_agenda_de_hoy()