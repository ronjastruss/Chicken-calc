Last login: Wed Apr 30 19:33:30 on ttys000
ronjastruss@AirvonRonja447 ~ % >....                                            

    ausgewaehlter_stall = st.selectbox("Wähle einen Stall", list(st.session_state["staelle"].keys()))
    selected_datum = st.date_input("Für welches Datum möchtest du das Alter berechnen?", datetime.today())

    if st.button("Alter berechnen"):
        stall = st.session_state["staelle"][ausgewaehlter_stall]
        tage_seit_einstallung = (selected_datum - stall["einstalldatum"]).days
        aktuelles_alter = stall["alter_start"] + tage_seit_einstallung

        if aktuelles_alter < 0:
            st.error("⚠<fe0f> Das gewählte Datum liegt vor dem Einstall-Datum!") 
        else:
            st.success(f"<0001f7e2> Alter der Hennen am {selected_datum.strftime('%d.%m.%Y')} im Stall '{ausgewaehlter_stall}': **{aktuelles_alter} Tage**")

else:
    st.info("🔸 Aktuell sind keine Ställe gespeichert. Lege zuerst einen neuen Stall an.")


