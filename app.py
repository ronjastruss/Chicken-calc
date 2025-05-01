import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Chicken Calculator", layout="centered")

# Titel
st.title("🐔 Chicken Calculator")

# Initialisierung
if "staelle" not in st.session_state:
    st.session_state["staelle"] = {}
if "aktueller_stall" not in st.session_state:
    st.session_state["aktueller_stall"] = None
if "stall_name_input" not in st.session_state:
    st.session_state["stall_name_input"] = ""

# Seitenleiste: Stall anlegen
st.sidebar.header("➕ Stall anlegen")
stall_name = st.sidebar.text_input("Name des Stalls", placeholder="z. B. Hühnerstall 1", key="stall_name_input")
einstall_datum = st.sidebar.date_input("Einstall-Datum")
einstall_wochen = st.sidebar.number_input("Alter bei Einstallung (Wochen)", min_value=0, max_value=100, value=0)
einstall_tage = st.sidebar.number_input("Zusätzliche Tage", min_value=0, max_value=6, value=0)

if st.sidebar.button("💾 Stall speichern"):
    if stall_name and einstall_datum is not None:
        st.session_state["staelle"][stall_name] = {
            "datum": einstall_datum,
            "wochen": int(einstall_wochen),
            "tage": int(einstall_tage)
        }
        st.session_state["aktueller_stall"] = stall_name
        st.session_state["stall_name_input"] = ""
        st.rerun()
    else:
        st.sidebar.warning("⚠️ Bitte alle Felder ausfüllen!")

# Bestehende Ställe anzeigen
if st.session_state["staelle"]:
    st.subheader("🐔 Stall auswählen")
    stall_optionen = list(st.session_state["staelle"].keys())
    ausgewaehlter_stall = st.selectbox("Wähle einen Stall", stall_optionen, index=stall_optionen.index(st.session_state["aktueller_stall"]) if st.session_state["aktueller_stall"] else 0)

    # Stall löschen
    col1, col2 = st.columns([5,1])
    with col1:
        st.markdown(f"🗂️ <small style='color:gray'>Daten zu {ausgewaehlter_stall}:</small>", unsafe_allow_html=True)
        stall_info = st.session_state["staelle"][ausgewaehlter_stall]
        st.markdown(f"<small style='color:gray'>Einstall-Datum: {stall_info['datum'].strftime('%d.%m.%Y')} – Alter: {stall_info['wochen']} Wochen und {stall_info['tage']} Tage</small>", unsafe_allow_html=True)
    with col2:
        if st.button("🗑️", help="Stall löschen", key="loeschen_button"):
            del st.session_state["staelle"][ausgewaehlter_stall]
            st.session_state["aktueller_stall"] = None
            st.rerun()

    # Weiter mit Berechnungen
    st.markdown("---")
    st.subheader("📆 Alter zu bestimmtem Datum")
    ziel_datum = st.date_input("Wähle ein Datum", key="datum_input")
    if st.button("📏 Alter berechnen"):
        stall_daten = st.session_state["staelle"][ausgewaehlter_stall]
        startdatum = stall_daten["datum"] - timedelta(weeks=stall_daten["wochen"], days=stall_daten["tage"])
        differenz = (ziel_datum - startdatum).days
        wochen = differenz // 7
        tage = differenz % 7
        st.success(f"Am {ziel_datum.strftime('%d.%m.%Y')} sind die Hennen **{wochen} Wochen und {tage} Tage** alt.")

    st.markdown("")

    st.subheader("📅 Datum zu gewünschtem Alter")
    ziel_alter_wochen = st.number_input("Alter in Wochen", min_value=0, max_value=100, value=20, key="ziel_wochen")
    ziel_datum2 = None
    if st.button("📆 Datum berechnen"):
        stall_daten = st.session_state["staelle"][ausgewaehlter_stall]
        startdatum = stall_daten["datum"] - timedelta(weeks=stall_daten["wochen"], days=stall_daten["tage"])
        ziel_datum2 = startdatum + timedelta(weeks=ziel_alter_wochen)
        st.success(f"Die Hennen sind am **{ziel_datum2.strftime('%d.%m.%Y')}** genau **{ziel_alter_wochen} Wochen** alt.")

else:
    st.info("➕ Lege zuerst einen Stall über die Seitenleiste an.")
