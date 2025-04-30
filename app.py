import streamlit as st
from datetime import date, datetime
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
neuer_stall = st.sidebar.text_input("Name des Stalls")
einstalldatum = st.sidebar.date_input("Einstalldatum")
startalter_wochen = st.sidebar.number_input("Alter bei Einstallen (in Wochen)", min_value=0, value=0)
startalter_tage = st.sidebar.number_input("Alter bei Einstallen (in Tagen)", min_value=0, value=0)

if st.sidebar.button("Stall speichern"):
    if neuer_stall and str(einstalldatum):
        staelle[neuer_stall] = {
            "einstalldatum": str(einstalldatum),
            "startalter_wochen": startalter_wochen,
            "startalter_tage": startalter_tage
        }
        with open(DATA_FILE, "w") as f:
            json.dump(staelle, f)
        st.sidebar.success(f"Stall '{neuer_stall}' gespeichert.")
    else:
        st.sidebar.error("Bitte alle Felder ausfüllen.")

# 📋 Stall auswählen
if staelle:
    st.subheader("📍 Stall auswählen")
    ausgewaehlter_stall = st.selectbox("Stall", list(staelle.keys()))

    if ausgewaehlter_stall:
        stall_daten = staelle[ausgewaehlter_stall]
        saved_date = datetime.strptime(stall_daten["einstalldatum"], "%Y-%m-%d").date()
        startalter_wochen = stall_daten["startalter_wochen"]
        startalter_tage = stall_daten["startalter_tage"]

        # 📅 Ziel-Datum für Berechnung auswählen
        st.markdown("Wähle ein Datum, für das du das Alter berechnen möchtest.")
        zieldatum = st.date_input("Datum", value=date.today())

        # Option 1: Alter an einem bestimmten Datum berechnen
        if st.button("Alter berechnen (Wochen)"):
            tage_seit_einstallung = (zieldatum - saved_date).days
            gesamtalter_wochen = startalter_wochen + (tage_seit_einstallung // 7)
            gesamtalter_tage = startalter_tage + (tage_seit_einstallung % 7)
            result_button = f"Alter der Hennen: **{gesamtalter_wochen} Wochen und {gesamtalter_tage} Tage**"
            st.markdown(f"<button>{result_button}</button>", unsafe_allow_html=True)

        # Option 2: Alter in Wochen und Tagen für ein Datum berechnen
        if st.button("Exaktes Alter berechnen (Wochen und Tage)"):
            tage_seit_einstallung = (zieldatum - saved_date).days
            gesamtalter_wochen = startalter_wochen + (tage_seit_einstallung // 7)
            gesamtalter_tage = startalter_tage + (tage_seit_einstallung % 7)
            st.success(f"Am {zieldatum.strftime('%d.%m.%Y')} sind die Hennen **{gesamtalter_wochen} Wochen und {gesamtalter_tage} Tage alt**.")

else:
    st.info("Noch keine Ställe gespeichert. Lege im Seitenmenü einen neuen Stall an.")
