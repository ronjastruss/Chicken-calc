import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Chicken Calculator", layout="centered")

# Session State initialisieren
if "staelle" not in st.session_state:
    st.session_state["staelle"] = {}
if "aktueller_stall" not in st.session_state:
    st.session_state["aktueller_stall"] = None
if "stall_name_input" not in st.session_state:
    st.session_state["stall_name_input"] = ""

# Sidebar: Neuen Stall anlegen
st.sidebar.header("🔧 Neuen Stall anlegen")
stall_name = st.sidebar.text_input("Stallname", value=st.session_state["stall_name_input"], placeholder="z. B. Hühnerstall 1")
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
        st.session_state["stall_name_input"] = ""
    else:
        st.sidebar.warning("⚠️ Bitte alle Felder ausfüllen!")

# Sidebar: Stall auswählen und löschen
st.sidebar.header("📂 Stall auswählen")
if st.session_state["staelle"]:
    ausgewaehlt = st.sidebar.selectbox("Wähle einen Stall", list(st.session_state["staelle"].keys()))
    st.session_state["aktueller_stall"] = ausgewaehlt

    if st.sidebar.button("❌ Stall löschen"):
        if ausgewaehlt in st.session_state["staelle"]:
            del st.session_state["staelle"][ausgewaehlt]
            st.session_state["aktueller_stall"] = None
            st.success(f"✅ Stall '{ausgewaehlt}' wurde gelöscht.")

# Hauptbereich
if st.session_state["aktueller_stall"]:
    stall = st.session_state["staelle"][st.session_state["aktueller_stall"]]
    st.subheader(f"📄 Stall: {st.session_state['aktueller_stall']}")
    st.caption(f"📅 Einstall-Datum: {stall['datum']} | Alter: {stall['wochen']} Wochen + {stall['tage']} Tage")

    # Abschnitt 1: Alter zum Datum X
    st.markdown("### 🔍 Alter zum Datum X")
    datum_x = st.date_input("Datum eingeben für Altersabfrage")
    tage_gesamt = (datum_x - stall["datum"]).days + (stall["wochen"] * 7 + stall["tage"])
    if tage_gesamt < 0:
        st.warning("⚠️ Dieses Datum liegt vor dem Einstall-Datum.")
    else:
        wochen = tage_gesamt // 7
        tage = tage_gesamt % 7
        st.success(f"🐓 Die Hennen sind am {datum_x} **{wochen} Wochen und {tage} Tage alt.**")

    # Abschnitt 2: Datum für gewünschte Woche berechnen
    st.markdown("### 📆 Datum für gewünschtes Alter")
    ziel_wochen = st.number_input("Ziel-Wochenalter", min_value=0, step=1)
    ziel_tage = st.number_input("Zusätzliche Tage", min_value=0, max_value=6, step=1)
    if ziel_wochen + ziel_tage > 0:
        delta_tage = (ziel_wochen * 7 + ziel_tage) - (stall["wochen"] * 7 + stall["tage"])
        datum_ziel = stall["datum"] + timedelta(days=delta_tage)
        if delta_tage < 0:
            st.warning("⚠️ Die Hennen hatten dieses Alter bereits.")
        else:
            st.success(f"📅 Am **{datum_ziel}** sind die Hennen **{ziel_wochen} Wochen und {ziel_tage} Tage alt.**")
else:
    st.info("Bitte lege in der Seitenleiste einen Stall an oder wähle einen bestehenden.")
