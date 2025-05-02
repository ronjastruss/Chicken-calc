import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Hühner Altersrechner", layout="centered")

# Hinweis für mobile Nutzer
st.info("📱 Auf dem Smartphone? Tippe oben links auf das ☰ Menü, um einen Stall hinzuzufügen.")

st.title("🐔 Hühner Altersrechner")

# Session State initialisieren
if "ställe" not in st.session_state:
    st.session_state["ställe"] = {}

if "stall_name_input" not in st.session_state:
    st.session_state["stall_name_input"] = ""

if "wochen_input" not in st.session_state:
    st.session_state["wochen_input"] = 0

if "tage_input" not in st.session_state:
    st.session_state["tage_input"] = 0

if "einstall_datum_input" not in st.session_state:
    st.session_state["einstall_datum_input"] = datetime.today()

# --- Sidebar: Stallverwaltung ---
st.sidebar.title("🐥 Stallverwaltung")

with st.sidebar.form("stall_form"):
    stall_name = st.text_input("🆕 Stallname", placeholder="z. B. Hühnerstall 1", key="stall_name_input")
    einstall_datum = st.date_input("📅 Einstalldatum", key="einstall_datum_input")
    wochen = st.number_input("🗓️ Alter bei Einstallung – Wochen", min_value=0, step=1, key="wochen_input")
    tage = st.number_input("🗓️ Alter bei Einstallung – Tage", min_value=0, max_value=6, step=1, key="tage_input")

    if st.form_submit_button("💾 Stall speichern"):
        if stall_name and einstall_datum:
            st.session_state["ställe"][stall_name] = {
                "einstall_datum": einstall_datum,
                "wochen": wochen,
                "tage": tage
            }
            # Felder zurücksetzen
            st.session_state["stall_name_input"] = ""
            st.session_state["wochen_input"] = 0
            st.session_state["tage_input"] = 0
            st.success(f"✅ {stall_name} wurde gespeichert!")
        else:
            st.warning("⚠️ Bitte alle Felder ausfüllen!")

# Stall auswählen
if st.session_state["ställe"]:
    st.subheader("📂 Stall auswählen")
    selected_stall = st.selectbox("Wähle einen Stall", list(st.session_state["ställe"].keys()))
    stall_data = st.session_state["ställe"][selected_stall]

    # Stallinfo anzeigen
    with st.expander("📋 Stall-Informationen", expanded=True):
        st.markdown(
            f"""
            <p style='color: grey; font-size: 0.9em'>
            <b>Einstall-Datum:</b> {stall_data["einstall_datum"].strftime("%d.%m.%Y")}<br>
            <b>Alter bei Einstallung:</b> {stall_data["wochen"]} Wochen, {stall_data["tage"]} Tage
            </p>
            """, unsafe_allow_html=True
        )

        # Stall löschen
        if st.button("🗑️ Löschen", key="delete_stall", help="Diesen Stall löschen"):
            del st.session_state["ställe"][selected_stall]
            st.rerun()

    st.markdown("---")

    # --- Abschnitt 1: Alter zu bestimmtem Datum ---
    st.subheader("📆 Alter zum Datum X")
    datum_x = st.date_input("Zu welchem Datum möchtest du das Alter wissen?", datetime.today())
    saved_date = stall_data["einstall_datum"]
    saved_wochen = stall_data["wochen"]
    saved_tage = stall_data["tage"]

    diff_tage = (datum_x - saved_date).days
    gesamttage = saved_wochen * 7 + saved_tage + diff_tage

    if gesamttage < 0:
        st.error("🚫 Das gewählte Datum liegt vor dem Einstall-Datum!")
    else:
        alter_wochen = gesamttage // 7
        rest_tage = gesamttage % 7
        st.success(f"🟢 Die Hennen sind am {datum_x.strftime('%d.%m.%Y')} genau {alter_wochen} Wochen und {rest_tage} Tage alt.")

    st.markdown("---")

    # --- Abschnitt 2: Datum für gewünschtes Alter ---
    st.subheader("📅 Datum für gewünschtes Alter")
    ziel_wochen = st.number_input("In welcher Woche möchtest du das Datum wissen?", min_value=0, step=1)
    ziel_tage = st.number_input("Und wie viele zusätzliche Tage?", min_value=0, max_value=6, step=1)

    tage_für_wochen = ziel_wochen * 7 + ziel_tage
    neues_datum = saved_date + timedelta(days=tage_für_wochen)
    st.success(f"🟢 Die Hennen sind am {neues_datum.strftime('%d.%m.%Y')} genau {ziel_wochen} Wochen und {ziel_tage} Tage alt.")

else:
    st.info("ℹ️ Lege zunächst einen Stall in der Sidebar an, um mit den Berechnungen zu beginnen.")
