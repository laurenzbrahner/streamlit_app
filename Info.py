import streamlit as st


st.set_page_config(page_title="Spotify Analyse Dashboard",
                   page_icon=":musical_note:")

# Hauptüberschrift
st.title("Spotify Analyse Dashboard")

# Untertitel oder kurze Beschreibung
st.markdown("""
        Dieses interaktive Dashboard bietet detaillierte Einblicke in die Trends und Muster der erfolgreichsten Songs auf Spotify für das Jahr 2023. 
        Hier können Sie verschiedene Aspekte der Musikdaten erkunden, einschließlich Künstlerpopularität, Einfluss der Tonarten, Veröffentlichungsmonate, und vieles mehr.
    """)

col1, col2, col3 = st.columns([1, 1, 1])

image_path = "spotify_logo_black_new.png"
with col2:
    st.image(image_path,
             caption='Spotify', width=200)

# Abschnitt für den Autor
st.sidebar.header("Über den Autor")
st.sidebar.markdown("""
        **Name des Autors:**
        - Laurenz Brahner

        **Kontaktinformationen:**
        - [GitHub](https://github.com/laurenzbrahner)
        - lb184@hdm-stuttgart.de    

    """)

# Projektinformationen
st.header("Projektdetails")
st.markdown("""
    - **Datenquellen:** Die analysierten Daten stammen direkt von Kaggle. [Daten](https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023).
    - **Analyseziele:** Identifizierung von Mustern in Musikpräferenzen, Verständnis der Popularität verschiedener Musikgenres, Einfluss von verschiedenen Faktoren auf den Erfolg der Songs.
    - **Technologien:** Python, Pandas, Streamlit, Sklearn und Altair für visuelle Datenanalyse.
    """)

# Weitere Informationen
st.header("Weitere Informationen")
st.markdown("""
    Falls Sie weitere Informationen wünschen oder Fragen zum Dashboard haben, können Sie mich gerne über die oben genannten Kontaktdaten erreichen.
    """)

# Footer
st.markdown("---")
st.markdown("© 2023 Laurenz Brahner - Alle Rechte vorbehalten.")
