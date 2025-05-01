import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Chicken Calculator", layout="centered")

st.title("🐔 Chicken Calculator")

# Initialisierung der Session States
if "staelle" not in st.session_state:
    st.session_state["staelle"] = {}

if "aktueller_stall" not in st.session_state:
    st.session_state["aktueller_stall"] = None

st.sidebar.header("📋 Stallverwaltung")
st.sidebar.divider()

# Stall anlegen
stall_name = st.sidebar.text_input("Neuen Stall anlegen", placeholder="z.B. Hühnerstall 1")
einstall_datum = st.sidebar.date_input("Einstall-Datum")
einstall_wochen = st.sidebar.number_input("Alter in Wochen bei Einstallung", min_value=0, step=1)
einstall_tage = st.sidebar.number_input("Zusätzliche Tage", min_value=0, max_value=6, step=1)

if st.sidebar.button("💾 Stall speichern"):
    if stall_name and einstall_datum is not None:
        st.session_state["staelle"][stall_name] = {
            "datum": einstall_datum,
            "wochen": int(einstall_wochen),
            "tage": int(einstall_tage)
        }
        st.session_state["aktueller_stall"] = stall_name
        st.rerun()
        return
    else:
        st.sidebar.warning("⚠️ Bitte alle Felder ausfüllen!")

st.sidebar.divider()

# Auswahl bestehender Ställe
if st.session_state["staelle"]:
    aktueller_stall = st.sidebar.selectbox("🐔 Stall auswählen", options=list(st.session_state["staelle"].keys()))
    if aktueller_stall:
        st.session_state["aktueller_stall"] = aktueller_stall
        stall_info = st.session_state["staelle"][aktueller_stall]
        with st.sidebar.expander("ℹ️ Stall-Details", expanded=False):
            st.markdown(f"**Einstall-Datum:** :gray[{stall_info['datum'].strftime('%d.%m.%Y')}]")
            st.markdown(f"**Alter bei Einstallung:** :gray[{stall_info['wochen']} Wochen, {stall_info['tage']} Tage]")

        if st.sidebar.button("❌ Stall löschen"):
            del st.session_state["staelle"][aktueller_stall]
            st.session_state["aktueller_stall"] = None
            st.rerun()
            return

# Hauptfunktionen nur anzeigen, wenn Stall gewählt ist
if st.session_state["aktueller_stall"]:
    st.subheader(f"Aktueller Stall: {st.session_state['aktueller_stall']}")
    stall = st.session_state["staelle"][st.session_state["aktueller_stall"]]
    start_datum = stall["datum"]
    start_alter_tage = stall["wochen"] * 7 + stall["tage"]
    einstalldatum = start_datum - timedelta(days=start_alter_tage)

    st.markdown("---")
    st.markdown("### 🧮 Berechnungen")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Alter zum Datum X berechnen**")
        ziel_datum = st.date_input("Datum wählen", key="alter_datum")
        if ziel_datum:
            differenz = (ziel_datum - einstalldatum).days
            if differenz >= 0:
                wochen = differenz // 7
                tage = differenz % 7
                st.success(f"Am {ziel_datum.strftime('%d.%m.%Y')} sind die Hennen **{wochen} Wochen und {tage} Tage** alt.")
            else:
                st.warning("Das Datum liegt vor dem Einstall-Datum.")

    with col2:
        st.markdown("**Datum für ein Alter X berechnen**")
        ziel_wochen = st.number_input("Alter in Wochen", min_value=0, step=1, key="ziel_wochen")
        ziel_tage = st.number_input("Zusätzliche Tage", min_value=0, max_value=6, step=1, key="ziel_tage")
        if ziel_wochen or ziel_tage:
            gesamt_tage = ziel_wochen * 7 + ziel_tage
            neues_datum = einstalldatum + timedelta(days=gesamt_tage)
            st.success(f"Die Hennen sind am **{neues_datum.strftime('%d.%m.%Y')}** genau {ziel_wochen} Wochen und {ziel_tage} Tage alt.")
