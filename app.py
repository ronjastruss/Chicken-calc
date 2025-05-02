import streamlit as st
from datetime import date, datetime, timedelta

st.set_page_config(page_title="Hennen-Altersrechner", layout="centered")

st.title("🐔 Hennen-Altersrechner")

# SessionState initialisieren
if "ställe" not in st.session_state:
    st.session_state["ställe"] = {}

# Eingabefelder zum Stall anlegen
with st.sidebar:
    st.subheader("🛠️ Stall hinzufügen")
    stall_name_input = st.text_input("Stallname", placeholder="z. B. Hühnerstall 1", key="stall_name_input")
    einstalldatum_input = st.date_input("Einstall-Datum", key="einstalldatum_input", format="DD.MM.YYYY")
    wochen_alt_input = st.number_input("Alter bei Einstallung (Wochen)", min_value=0, max_value=100, step=1, key="wochen_input")
    tage_alt_input = st.number_input("Zusätzliche Tage", min_value=0, max_value=6, step=1, key="tage_input")
    speichern = st.button("➕ Stall speichern")

# Speichern eines neuen Stalls
if speichern:
    if stall_name_input and einstalldatum_input:
        st.session_state["ställe"][stall_name_input] = {
            "einstall_datum": einstalldatum_input,
            "wochen": wochen_alt_input,
            "tage": tage_alt_input
        }
        # Eingaben leeren
        for key in ["stall_name_input", "einstalldatum_input", "wochen_input", "tage_input"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    else:
        st.sidebar.warning("⚠️ Bitte alle Felder ausfüllen!")

# Wenn Ställe vorhanden sind, Stallauswahl anzeigen
if st.session_state["ställe"]:
    selected_stall = st.selectbox("📂 Wähle einen Stall", list(st.session_state["ställe"].keys()))
    
    # Stall löschen
    cols = st.columns([4, 1])
    with cols[1]:
        if st.button("🗑️ Löschen", key="delete_stall", help="Stall entfernen", type="secondary"):
            del st.session_state["ställe"][selected_stall]
            st.rerun()

    # Stall-Details anzeigen
    stall_data = st.session_state["ställe"][selected_stall]
    st.caption("**Einstall-Datum:** " + stall_data["einstall_datum"].strftime("%d.%m.%Y"))
    st.caption(f"**Alter bei Einstallung:** {stall_data['wochen']} Wochen, {stall_data['tage']} Tage")

    st.markdown("---")
    st.subheader("📅 Altersberechnung")

    # Möglichkeit 1: Alter zu einem bestimmten Datum X
    with st.expander("1️⃣ Alter der Hennen am Datum X", expanded=True):
        datum_x = st.date_input("Wähle ein Datum", key="datum_x")
        if datum_x:
            differenz = (datum_x - stall_data["einstall_datum"]).days
            gesamttage = differenz + (stall_data["wochen"] * 7 + stall_data["tage"])
            wochen = gesamttage // 7
            tage = gesamttage % 7
            st.success(f"Am {datum_x.strftime('%d.%m.%Y')} sind die Hennen **{wochen} Wochen und {tage} Tage alt**.")

    # Möglichkeit 2: Wann erreichen die Hennen ein bestimmtes Alter?
    with st.expander("2️⃣ Datum für gewünschtes Alter", expanded=True):
        ziel_wochen = st.number_input("Zielalter (Wochen)", min_value=0, max_value=100, step=1, key="zielwochen")
        ziel_tage = st.number_input("Zielalter (Tage)", min_value=0, max_value=6, step=1, key="zieltage")
        if ziel_wochen > 0 or ziel_tage > 0:
            start_tage = stall_data["wochen"] * 7 + stall_data["tage"]
            ziel_tage_gesamt = ziel_wochen * 7 + ziel_tage
            differenz = ziel_tage_gesamt - start_tage
            ziel_datum = stall_data["einstall_datum"] + timedelta(days=differenz)
            st.success(f"Die Hennen sind am **{ziel_datum.strftime('%d.%m.%Y')}** genau {ziel_wochen} Wochen und {ziel_tage} Tage alt.")
else:
    st.info("Noch kein Stall angelegt. Bitte einen Stall im Seitenmenü hinzufügen.")
