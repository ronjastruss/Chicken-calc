import streamlit as st
from datetime import date, datetime, timedelta  # Import für timedelta hinzufügen
import json
import os

st.set_page_config(page_title="Chicken Calculator 🐔", page_icon="🐔")

st.title("🐔 Chicken Calculator")
st.markdown("Berechne das aktuelle Alter deiner Legehennen – für beliebig viele Ställe.")

# Lokale JSON-Datei zum Speichern der Stall-Daten
DATA_FILE = "staelle.json"

# 📂 Ställe laden oder initialisieren
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        staelle = json.load(f)
else:
    staelle = {}

# 🚧 Neuen Stall hinzufügen
st.sidebar.subheader("➕ Neuen Stall anlegen")
stall_name = st.sidebar.text_input("Name des Stalls", "Hühnerstall Hof 1")  # Standardwert für Stallname
einstalldatum = st.sidebar.date_input("Einstalldatum")
startalter_wochen = st.sidebar.number_input("Alter bei Einstallen (in Wochen)", min_value=0, value=0)
startalter_tage = st.sidebar.number_input("Alter bei Einstallen (in Tagen)", min_value=0, value=0)

if st.sidebar.button("Stall speichern"):
    if stall_name and str(einstalldatum):
        staelle[stall_name] = {
            "einstalldatum": str(einstalldatum),
            "startalter_wochen": startalter_wochen,
            "startalter_tage": startalter_tage
        }
        with open(DATA_FILE, "w") as f:
            json.dump(staelle, f)
        st.sidebar.success(f"Stall '{stall_name}' gespeichert.")
        
        # Felder nach dem Speichern leeren, damit der Benutzer einen neuen Stall anlegen kann
        stall_name = "Hühnerstall Hof 1"
        einstalldatum = None
        startalter_wochen = 0
        startalter_tage = 0
    else:
        st.sidebar.error("Bitte alle
