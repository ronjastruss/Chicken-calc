import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Hennen-Alter Rechner", layout="centered")

st.title("🐔 Chicken Calculator")

# Session-State initialisieren
if "staelle" not in st.session_state:
    st.session_state.staelle = {}
if "aktueller_stall" not in st.session_state:
    st.session_state.aktueller_stall = ""

# STALL ANLEGEN
st.sidebar.header("🔧 Neuen Stall anlegen")
stall_name = st.sidebar.text_input("Stallname", placeholder="z.B. Hühnerstall 1")
einstalldatum = st.sidebar.date_input("Einstalldatum")
einstall_alter_wochen = st.sidebar.number_input("Alter bei Einstallen (Wochen)", min_value=0, step=1)
einstall_alter_tage = st.sidebar.number_input("Alter bei Einstallen (Tage)", min_value=0, max_value=6, step=1)

if st.sidebar.button("Stall speichern"):
    if stall_name and einstalldatum:
        st.session_state.staelle[stall_name] = {
            "einstalldatum": einstalldatum,
            "alter_wochen": einstall_alter_wochen,
            "alter_tage": einstall_alter_tage
        }
        st.sidebar.success(f"Stall '{stall_name}' gespeichert.")
        st.session_state.aktueller_stall = stall_name
        # Eingaben zurücksetzen
        st.experimental_set_query_params()  # nur zur Sicherheit
    else:
        st.sidebar.error("Bitte alle Felder ausfüllen.")

# STALL AUSWÄHLEN UND VERWALTEN
st.header("📋 Stall auswählen")
if st.session_state.staelle:
    auswahl = st.selectbox("Wähle einen Stall", list(st.session_state.staelle.keys()))
    if auswahl:
        st.session_state.aktueller_stall = auswahl

        stall = st.session_state.staelle[auswahl]

        # Stall-Infos anzeigen (klein, hellgrau)
        with st.expander("📄 Stall-Details", expanded=True):
            st.markdown(
                f"<small style='color: gray;'>Einstalldatum: {stall['einstalldatum']}<br>"
                f"Alter bei Einstallen: {stall['alter_wochen']} Wochen, {stall['alter_tage']} Tage</small>",
                unsafe_allow_html=True
            )

        # Stall löschen
        col1, col2 = st.columns([0.8, 0.2])
        with col2:
            if st.button("🗑️ Löschen", key="loeschen", help="Stall löschen"):
                del st.session_state.staelle[auswahl]
                st.session_state.aktueller_stall = ""
                st.experimental_set_query_params()
                st.experimental_rerun()

        st.markdown("---")

        # FUNKTION 1 – Alter zu Datum X
        st.subheader("📆 1. Alter der Hennen zu einem bestimmten Datum")
        datum_x = st.date_input("Wähle das Datum")
        if st.button("Alter berechnen"):
            saved_date = stall['einstalldatum']
            saved_wochen = stall['alter_wochen']
            saved_tage = stall['alter_tage']

            gesamt_tage = (datum_x - saved_date).days + (saved_wochen * 7 + saved_tage)
            wochen = gesamt_tage // 7
            tage = gesamt_tage % 7
            st.success(f"Die Hennen sind am {datum_x.strftime('%d.%m.%Y')} genau {wochen} Wochen und {tage} Tage alt.")

        st.markdown("---")

        # FUNKTION 2 – Datum bei gewünschtem Alter
        st.subheader("⏳ 2. Datum berechnen für gewünschtes Alter")
        ziel_wochen = st.number_input("Zielalter (Wochen)", min_value=0, step=1)
        ziel_tage = st.number_input("Zielalter (Tage)", min_value=0, max_value=6, step=1)
        if st.button("Datum berechnen"):
            saved_date = stall['einstalldatum']
            saved_wochen = stall['alter_wochen']
            saved_tage = stall['alter_tage']

            tage_fuer_wochen = (ziel_wochen * 7 + ziel_tage) - (saved_wochen * 7 + saved_tage)
            neues_datum = saved_date + timedelta(days=tage_fuer_wochen)

            st.success(f"Die Hennen sind am {neues_datum.strftime('%d.%m.%Y')} genau {ziel_wochen} Wochen und {ziel_tage} Tage alt.")
else:
    st.info("Noch kein Stall gespeichert.")
