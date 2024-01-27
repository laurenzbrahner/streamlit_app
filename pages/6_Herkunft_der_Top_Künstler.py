import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import geopandas as gpd
import json


st.set_page_config(page_title="Herkunft der Top Künstler",
                   page_icon="📈", layout="wide")


file_path = r'C:\Users\Privat\OneDrive\Dokumente\GitHub\DST-Documentation\data_exploration\spotify_angereichert_cleaned.csv'
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
            alt.Color('properties.artist_count:Q', scale=alt.Scale(scheme='blues', domain=[
                0, 95]), legend=alt.Legend(title='Anzahl der Künstler')),  # Farbe bei erfüllter Bedingung
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

    final_chart = base + points

    return final_chart


df['artist_country'] = df['artist_country'].replace(country_mapping)
unique_countries = df['artist_country'].unique()

st.sidebar.title(
    "Wähle Länder aus")
selected_countries = st.sidebar.multiselect(
    "Alle Länder sind Standartmäßig ausgewählt", unique_countries)


st.title("Aus welchem Land du Kommen solltest?")

if len(selected_countries) > 0:
    st.altair_chart(map(selected_countries), use_container_width=True)
else:
    st.altair_chart(map([]), use_container_width=True)


# Streamlit-Elemente
