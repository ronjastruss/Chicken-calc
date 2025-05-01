import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Chicken Calculator", layout="centered")

# Session State initialisieren
if "staelle" not in st.session_state:
    st.session_state["staelle"] = {}
if "aktueller_stall" not in st.session_state:
    st.session_state["aktueller_stall"] = None

# 🐣 Sidebar: Stall erstellen
st.sidebar.header("🔧 Neuen Stall anlegen")
if "stall_name" not in st.session_state:
    st.session_state["stall_name"] = ""
stall_name = st.sidebar.text_input("Stallname", value=st.session_state["stall_name"], placeholder="z. B. Hühnerstall 1")
einstall_datum = st.sidebar.date_input("Einstall-Datum")
einstall_wochen = st.sidebar.number_input("Alter bei Einstallung (Wochen)", min_value=0, step=1)
einstall_tage = st.sidebar.number_input("Zusätzliche Tage", min_value=0, max_value=6, step=1)

if st.sidebar.button("💾 Stall speichern"):
    if stall_name and einstall_datum:
        st.session_state["staelle"][stall_name] = {
            "datum": einstall_datum,
            "wochen": int(einstall_wochen),
            "tage": int(einstall_tage)
        }
        st.session_state["aktueller_stall"] = stall_name
        # Felder zurücksetzen (ohne rerun)
        st.session_state["stall_name"] = ""
    else:
        st.sidebar.error("Bitte alle Felder ausfüllen!")

# 🏠 Stall auswählen
st.sidebar.header("📂 Stall auswählen")
if st.session_state["staelle"]:
    auswahl = st.sidebar.selectbox("Wähle einen Stall", list(st.session_state["staelle"].keys()))
    st.session_state["aktueller_stall"] = auswahl

    # Stall löschen
    if st.sidebar.button("❌ Stall löschen"):
        del st.session_state["staelle"][auswahl]
        st.session_state["aktueller_stall"] = None
        st.experimental_set_query_params()  # Optional zum Aufräumen
        st.stop()

# 📋 Hauptinhalt
if st.session_state["aktueller_stall"]:
    stall = st.session_state["staelle"][st.session_state["aktueller_stall"]]
    st.subheader(f"📄 Stall: {st.session_state['aktueller_stall']}")
    st.caption(f"📅 Einstall-Datum: {stall['datum']} | Alter: {stall['wochen']} Wochen + {stall['tage']} Tage")

    # 1. Alter zum Datum X berechnen
    st.markdown("---")
    st.subheader("🔎 Alter zum Datum X")
    ziel_datum = st.date_input("Datum auswählen")
    gesamtdauer = (ziel_datum - stall["datum"]).days + (stall["wochen"] * 7 + stall["tage"])
    if gesamtdauer < 0:
        st.warning("⚠️ Das gewählte Datum liegt vor dem Einstall-Datum.")
    else:
        wochen = gesamtdauer // 7
        tage = gesamtdauer % 7
        st.success(f"Die Hennen sind am {ziel_datum} genau **{wochen} Wochen und {tage} Tage alt.**")

    # 2. Datum zur gewünschten Woche berechnen
    st.markdown("---")
    st.subheader("📆 Datum für gewünschtes Alter")
    ziel_wochen = st.number_input("Woche eingeben (z. B. Impfzeitpunkt)", min_value=0, step=1)
    ziel_tage = st.number_input("Zusätzliche Tage", min_value=0, max_value=6, step=1)
    if ziel_wochen + ziel_tage > 0:
        gesamttage = ziel_wochen * 7 + ziel_tage - (stall["wochen"] * 7 + stall["tage"])
        neues_datum = stall["datum"] + timedelta(days=gesamttage)
        if gesamttage < 0:
            st.warning("⚠️ Dieses Alter wurde bereits erreicht.")
        else:
            st.success(f"Die Hennen sind am **{neues_datum}** genau **{ziel_wochen} Wochen und {ziel_tage} Tage alt.**")
else:
    st.info("Lege links in der Seitenleiste zuerst einen Stall an oder wähle einen bestehenden.")
