import streamlit as st
from datetime import date, timedelta, datetime

st.set_page_config(page_title="Chicken Calculator", layout="centered")

st.title("🐔 Chicken Calculator")

# Session State initialisieren
if "staelle" not in st.session_state:
    st.session_state["staelle"] = {}

if "aktueller_stall" not in st.session_state:
    st.session_state["aktueller_stall"] = None

# Seitenleiste für Stallverwaltung
st.sidebar.header("📦 Stall verwalten")

stall_name = st.sidebar.text_input("Name des Stalls", placeholder="z. B. Hühnerstall 1", key="stall_name_input")
einstall_datum = st.sidebar.date_input("Einstall-Datum")
einstall_wochen = st.sidebar.number_input("Alter bei Einstallung (Wochen)", min_value=0, step=1, value=0)
einstall_tage = st.sidebar.number_input("Alter bei Einstallung (Tage)", min_value=0, max_value=6, step=1, value=0)

# Stall speichern
if st.sidebar.button("💾 Stall speichern"):
    if stall_name and einstall_datum is not None:
        st.session_state["staelle"][stall_name] = {
            "datum": einstall_datum,
            "wochen": int(einstall_wochen),
            "tage": int(einstall_tage)
        }
        st.session_state["aktueller_stall"] = stall_name
        st.rerun()
    else:
        st.sidebar.warning("⚠️ Bitte alle Felder ausfüllen!")

# Auswahl bestehender Ställe
if st.session_state["staelle"]:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📂 Bestehende Ställe")
    stall_liste = list(st.session_state["staelle"].keys())
    aktueller_stall = st.sidebar.selectbox("Stall auswählen", stall_liste, key="stall_selectbox")
    st.session_state["aktueller_stall"] = aktueller_stall

    # Stall löschen
    if st.sidebar.button("❌ Stall löschen"):
        del st.session_state["staelle"][aktueller_stall]
        st.session_state["aktueller_stall"] = None
        st.rerun()

# Wenn ein Stall ausgewählt ist
if st.session_state["aktueller_stall"]:
    stall = st.session_state["staelle"][st.session_state["aktueller_stall"]]
    st.subheader(f"📋 Stall: {st.session_state['aktueller_stall']}")

    st.caption(f"Einstall-Datum: {stall['datum'].strftime('%d.%m.%Y')} | Alter bei Einstallung: {stall['wochen']} Wochen, {stall['tage']} Tage")

    st.markdown("---")
    st.subheader("📅 Alter der Hennen zu bestimmtem Datum")
    ziel_datum = st.date_input("Datum wählen", key="datum_fuer_alter")

    saved_date = stall["datum"]
    saved_weeks = stall["wochen"]
    saved_days = stall["tage"]

    if ziel_datum >= saved_date:
        diff = (ziel_datum - saved_date).days
        total_days = saved_weeks * 7 + saved_days + diff
        wochen = total_days // 7
        tage = total_days % 7

        st.success(f"🟢 Die Hennen sind am {ziel_datum.strftime('%d.%m.%Y')} **{wochen} Wochen und {tage} Tage alt.**")
    else:
        st.warning("⚠️ Das gewählte Datum liegt vor dem Einstall-Datum.")

    st.markdown("---")
    st.subheader("📆 Datum zu bestimmtem Alter berechnen")
    ziel_wochen = st.number_input("Zielalter (Wochen)", min_value=0, step=1, value=0, key="ziel_wochen")
    ziel_tage = st.number_input("Zielalter (Tage)", min_value=0, max_value=6, step=1, value=0, key="ziel_tage")

    if st.button("📆 Datum berechnen"):
        tage_fuer_wochen = ziel_wochen * 7 + ziel_tage
        bisherige_tage = saved_weeks * 7 + saved_days
        diff_tage = tage_fuer_wochen - bisherige_tage

        if diff_tage >= 0:
            neues_datum = saved_date + timedelta(days=diff_tage)
            st.success(f"🟢 Die Hennen sind am **{neues_datum.strftime('%d.%m.%Y')}** genau {ziel_wochen} Wochen und {ziel_tage} Tage alt.")
        else:
            st.warning("⚠️ Zielalter liegt vor dem Einstallalter.")

else:
    st.info("ℹ️ Bitte zuerst einen Stall anlegen oder auswählen.")
 
