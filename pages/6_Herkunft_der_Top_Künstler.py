import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import geopandas as gpd
import json


st.set_page_config(page_title="Herkunft der Top Künstler",
                   page_icon=":earth_americas:", layout="wide")


file_path = './spotify_angereichert_cleaned.csv'
df = pd.read_csv(file_path)

df.drop(['Unnamed: 0'], axis=1, inplace=True)
country_mapping = {
    'England': 'United Kingdom',
    'Scotland': 'United Kingdom',
    'Buenos Aires': 'Argentina',
    'Guadalajara': 'Mexico',
    'Nashville': 'United States of America',
    'Downingtown': 'United States of America',
    'McAllen': 'United States of America',
    'Cabreúva': 'Brazil',
    'Monroe': 'United States of America',
    'Torrance': 'United States of America',
    'Los Angeles': 'United States of America',
    'Helsinki': 'Finland',
    'Manchester': 'United Kingdom',
    'Berlin': 'Germany',
    'Ipswich': 'United Kingdom',
    'Goiás': 'Brazil',
    'Mato Grosso do Sul': 'Brazil',
    'Las Palmas de Gran Canaria': 'Spain',
    'Providence': 'United States of America',
    'Orlando': 'United States of America',
    'New York': 'United States of America',
    'Austin': 'United States of America',
    'Türkiye': 'Turkey',
    'Punjab': 'India',
    'Boston': 'United States of America',
    'Amazonas': 'Brazil',
    'Rio de Janeiro': 'Brazil',
    'Sundsvall': 'Sweden',
    'Gujarat': 'India',
    'Philadelphia': 'United States of America',
    'United States': 'United States of America',
    'Oshawa': 'Canada'
}


def map(countries):
    # Zuordnung von Städten/Regionen zu Ländern
    country_mapping = {
        'England': 'United Kingdom',
        'Scotland': 'United Kingdom',
        'Buenos Aires': 'Argentina',
        'Guadalajara': 'Mexico',
        'Nashville': 'United States of America',
        'Downingtown': 'United States of America',
        'McAllen': 'United States of America',
        'Cabreúva': 'Brazil',
        'Monroe': 'United States of America',
        'Torrance': 'United States of America',
        'Los Angeles': 'United States of America',
        'Helsinki': 'Finland',
        'Manchester': 'United Kingdom',
        'Berlin': 'Germany',
        'Ipswich': 'United Kingdom',
        'Goiás': 'Brazil',
        'Mato Grosso do Sul': 'Brazil',
        'Las Palmas de Gran Canaria': 'Spain',
        'Providence': 'United States of America',
        'Orlando': 'United States of America',
        'New York': 'United States of America',
        'Austin': 'United States of America',
        'Türkiye': 'Turkey',
        'Punjab': 'India',
        'Boston': 'United States of America',
        'Amazonas': 'Brazil',
        'Rio de Janeiro': 'Brazil',
        'Sundsvall': 'Sweden',
        'Gujarat': 'India',
        'Philadelphia': 'United States of America',
        'United States': 'United States of America',
        'Oshawa': 'Canada'
    }

    df['artist_country'] = df['artist_country'].replace(country_mapping)

    # Erstellen des DataFrames 'artist_count_by_country'
    artist_count_by_country = df['artist_country'].value_counts().reset_index()
    artist_count_by_country.columns = ['name', 'artist_count']

    # schauen ob der parameter countries leer ist, dann alle länder auswählen sonst nur die ausgewählten

    if len(countries) == 0:
        artist_count_by_country = artist_count_by_country
    else:
        artist_count_by_country = artist_count_by_country[artist_count_by_country['name'].isin(
            countries)]

    # Laden der Weltkarte
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Zusammenführen der Daten
    world = world.merge(artist_count_by_country, on='name', how='left')
    world['artist_count'].fillna(0, inplace=True)

    json_data = json.loads(world.to_json())

    # Basis-Karte mit angepassten Eigenschaften
    base = alt.Chart(alt.Data(values=json_data['features'])).mark_geoshape(
        stroke='black'
    ).encode(
        color=alt.condition(
            'datum.properties.artist_count > 0',  # Bedingung
            alt.Color('properties.artist_count:Q', scale=alt.Scale(type="log", domain=[
                1, 368], scheme='blues',), legend=None),
            # Alternative Farbe, wenn Bedingung nicht erfüllt ist
            alt.value('lightgray')
        ),
        tooltip=[
            alt.Tooltip('properties.name:N', title='Land'),
            alt.Tooltip('properties.artist_count:Q',
                        title='Anzahl der Künstler')
        ]
    ).project('equirectangular').properties(
        width=800,
        height=500
    )

    # Konvertieren der Geometrie in Längen- und Breitengrade
    world['longitude'] = world.centroid.x
    world['latitude'] = world.centroid.y

    # Erstellen eines normalen Pandas DataFrame
    world_df = pd.DataFrame({
        'name': world['name'],
        'artist_count': world['artist_count'],
        'longitude': world['longitude'],
        'latitude': world['latitude']
    })

    # Altair-Diagramm erstellen
    points = alt.Chart(world_df).mark_circle(opacity=0).encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        size=alt.Size('artist_count:Q', title='Anzahl der Künstler',
                      legend=None),  # Legende für die Größe entfernen
        color=alt.Color('artist_count:Q', scale=alt.Scale(scheme='blues')),
        tooltip=[alt.Tooltip('name:N', title='Land'), alt.Tooltip(
            'artist_count:Q', title='Anzahl der Künstler')]
    ).properties(
        title='Weltkarte der Anzahl der Künstler nach Ländern',
        width=800,
        height=500
    )

    final_chart = alt.layer(base, points).configure_title(
        color='#60b4ff',
        fontSize=25,
        anchor='start'
    )

    return final_chart


df['artist_country'] = df['artist_country'].replace(country_mapping)
unique_countries = df['artist_country'].unique()

st.sidebar.title(
    "Wähle Länder aus")
selected_countries = st.sidebar.multiselect(
    "Alle Länder sind standardmäßig ausgewählt", unique_countries)


st.title("Aus welchem Land der Künstler kommen sollte")

st.write("""Die :blue[Weltkarte] zeigt die Anzahl der Künstler pro Land an. Sie können die Länder auswählen, die Sie interessieren.
          Wenn Sie mit der Maus über ein Land fahren, sehen Sie die Anzahl der Top-Künstler im Land.""")

st.write(
    """Wenn Sie in der Sidebar Länder auswählen, wird ein :orange[Barplot] mit den Top 10 Ländern der Top-Künstler angezeigt und die :blue[Weltkarte] wird aktualisiert, um nur die ausgewählten Länder anzuzeigen.""")

if len(selected_countries) > 0:
    st.altair_chart(map(selected_countries), use_container_width=True)

else:
    st.altair_chart(map([]), use_container_width=True)

if len(selected_countries) >= 1 and len(selected_countries) <= 10:
    st.write("Barchart mit den Top Künstlern aus den ausgewählten Ländern")

    artist_country_count = df.groupby('artist_country')[
        'artist(s)_name'].count().sort_values(ascending=False)

    # filer nach den ausgewählten Ländern
    artist_country_count = artist_country_count[artist_country_count.index.isin(
        selected_countries)]

    top_artist_country_count_chart = alt.Chart(artist_country_count.reset_index()).mark_bar(size=60).encode(
        x=alt.X('artist_country', sort='-y',
                axis=alt.Axis(title='Land', labelAngle=-45)),
        y=alt.Y('artist(s)_name', axis=alt.Axis(
            title='Anzahl der Künstler')),
        color=alt.Color('artist(s)_name',  scale=alt.Scale(
            domain=[1, 400], type="log", scheme='blues'), legend=None),
        tooltip=['artist_country', 'artist(s)_name']
    ).properties(
        title={'text': 'Top 10 Herkunftsländer der Top-Künstler', 'dy': 0},
        width=800,
        height=500
    ).configure_title(
        fontSize=25,
        anchor='start',
        color='#ffbd45'
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=20,
        titleColor='gray',
        labelColor='gray',
        titlePadding=12,
        grid=False
    ).configure_legend(
        titleFontSize=16,
        labelFontSize=14
    ).configure_view(
        strokeWidth=0,
    ).configure_axisX(
        labelAngle=0,
        titleAnchor='start'
    ).configure_axisY(
        grid=False,
        titleAnchor='end',
        titleFontSize=20
    )
    st.altair_chart(top_artist_country_count_chart, use_container_width=True)

elif len(selected_countries) > 10:
    st.error(
        "Zu viele Länder ausgewählt, bitte wähle maximal 10 Länder aus um den Barplot anzuzeigen")


# Streamlit-Elemente


st.markdown("---")
st.write("© 2023 Laurenz Brahner - Alle Rechte vorbehalten.")
