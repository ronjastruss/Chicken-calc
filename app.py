import streamlit as st
from datetime import date, datetime, timedelta
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
stall_name = st.sidebar.text_input("Name des Stalls", "Hühnerstall 1")  # Standardwert für Stallname
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
        stall_name = "Hühnerstall 1"
        einstalldatum = None
        startalter_wochen = 0
        startalter_tage = 0
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

        # 📝 Stall-Daten anzeigen
        st.markdown(f"### **Daten für Stall '{ausgewaehlter_stall}':**")
        st.write(f"<p style='color: lightgrey; font-size: 12px;'>Einstalldatum: {saved_date.strftime('%d.%m.%Y')}</p>", unsafe_allow_html=True)
        st.write(f"<p style='color: lightgrey; font-size: 12px;'>Alter bei Einstallen: {startalter_wochen} Wochen und {startalter_tage} Tage</p>", unsafe_allow_html=True)

        # 🗑️ Möglichkeit, Stall zu löschen
        delete_button = st.button(f"Stall '{ausgewaehlter_stall}' löschen", key="delete_button", use_container_width=True)
        if delete_button:
            del staelle[ausgewaehlter_stall]
            with open(DATA_FILE, "w") as f:
                json.dump(staelle, f)

            # Aktualisieren der Auswahlbox nach dem Löschen
            st.experimental_rerun()  # Seite neu laden

        # 📅 Ziel-Datum für Berechnung auswählen
        st.markdown("Wähle ein Datum, für das du das Alter berechnen möchtest.")
        zieldatum = st.date_input("Datum", value=date.today())

        # --- Erste Berechnung: Alter zum Datum X ---
        st.subheader("Berechnung 1: Alter zum Datum X")
        if st.button("Alter zum Datum X berechnen"):
            tage_seit_einstallung = (zieldatum - saved_date).days
            gesamtalter_wochen = startalter_wochen + (tage_seit_einstallung // 7)
            gesamtalter_tage = startalter_tage + (tage_seit_einstallung % 7)
            result_button = f"Alter der Hennen: **{gesamtalter_wochen} Wochen und {gesamtalter_tage} Tage**"
            st.markdown(f"<button style='background-color: green; color: white; padding: 10px 20px; font-size: 14px; border-radius: 5px;'>{result_button}</button>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)  # Trennlinie zwischen den beiden Berechnungen

        # --- Zweite Berechnung: Woche zu einem bestimmten Alter ---
        st.subheader("Berechnung 2: In welcher Woche sind die Hennen X Wochen alt?")
        wochen_eingabe = st.number_input("Woche, die du berechnen möchtest (z.B. 29)", min_value=1, value=29)
        if st.button("In welcher Woche sind die Hennen X Wochen alt?"):
            # Berechnung des Datums, an dem die Hennen X Wochen alt sind
            tage_fuer_wochen = wochen_eingabe * 7
            neues_datum = saved_date + timedelta(days=tage_fuer_wochen)
            st.markdown(f"<button style='background-color: green; color: white; padding: 10px 20px; font-size: 14px; border-radius: 5px;'>Am **{neues_datum.strftime('%d.%m.%Y')}** sind die Hennen **{wochen_eingabe} Wochen** alt.</button>", unsafe_allow_html=True)
else:
    st.info("Noch keine Ställe gespeichert. Lege im Seitenmenü einen neuen Stall an.")
