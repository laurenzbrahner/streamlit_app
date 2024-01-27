import streamlit as st
import pandas as pd
import altair as alt
import sys


st.set_page_config(page_title="Inhalt", page_icon="📈", layout='wide')


file_path = r'C:\Users\Privat\OneDrive\Dokumente\GitHub\DST-Documentation\data_exploration\spotify_angereichert_cleaned.csv'
df = pd.read_csv(file_path)


df.drop(['Unnamed: 0'], axis=1, inplace=True)


# Griupieren nach Künstler und Summieren der Streams


df_top10_songs = df.sort_values(by='streams', ascending=False).head(10)

# only show track name and streams

df_top10_songs = df_top10_songs[['track_name', 'streams', 'artist(s)_name']]


# sort after the most streamed artists

df_top_artist = df.groupby('artist(s)_name')[
    'streams'].sum().sort_values(ascending=False)


# Anzeigen der Top-Künstler basierend auf Streams
top_artists_streams = df_top_artist.head(10)


# bar_chart top songs

top_artists_streams_chart = alt.Chart(df_top10_songs.reset_index()).mark_bar().encode(
    y=alt.Y('track_name', sort='-x',
            axis=alt.Axis(title='Songtitel', labelFontSize=12)),
    x=alt.X('streams', axis=alt.Axis(title='Streams (Milliarden)', titleFontSize=20,
            labelFontSize=12, format='.0s', tickCount=5, tickMinStep=1e9, labelExpr='datum.value / 1e9')),
    color=alt.Color('streams', scale=alt.Scale(scheme='viridis'), legend=None),
    tooltip=[
        alt.Tooltip('track_name', title='Songtitel'),
        alt.Tooltip('streams', title='Anzahl der Streams'),
        alt.Tooltip('artist(s)_name', title='Künstlername')
    ]
).properties(
    title={'text': 'Top 10 Songs nach Streams 2023', 'dy': -0},
    width=600,
    height=400
).configure_title(
    fontSize=25,
    anchor='start',
    color='#ffbd45'
).configure_axis(
    labelFontSize=12,
    titleFontSize=20,
    titleColor='gray',
    labelColor='gray',
    titlePadding=7,
    grid=False
).configure_view(
    strokeWidth=0,
).configure_axisX(
    labelAngle=0,
    titleAnchor='start'
).configure_axisY(
    grid=False,
    titleAnchor='middle',
    titleFontSize=20
)


# pie Chart To Artists


artist_streams_pie_chart = alt.Chart(top_artists_streams.reset_index()).mark_arc().encode(
    theta=alt.Theta(field='streams', type='quantitative'),
    color=alt.Color(field='artist(s)_name', type='nominal',
                    legend=alt.Legend(title='Künstler')),
    order=alt.Order('streams', sort='ascending'),
    tooltip=[
        alt.Tooltip('artist(s)_name', title='Künstlername'),
        alt.Tooltip('streams', title='Anzahl der Streams')
    ]
).properties(
    title={'text': 'Top Künstler nach Streams', 'dy': -0},
    width=600,
    height=300
).configure_title(
    fontSize=25,
    anchor='start',
    color='#60b4ff'
).configure_legend(
    titleFontSize=16,
    labelFontSize=12,
    padding=0
).configure_view(
    strokeWidth=0
)


# %%


st.title("Spotify Top-Songs und Künstler 2023")

st.write("""
Bevor wir tiefer in die Daten eindrigen, wollen wir uns erstmal einen Überblick verschaffen. :orange[**Welche Songs wurden am meisten gestreamt?**] und :blue[**Wer waren die Top-Künstler im Jahr 2023?**] 
    Die Grafiken unten zeigen einmal die Top 10 songs basierend auf der Gesamtzahl ihrer Spotify-Streams 
    und einmal die Top 10 Künstler basierend auf der Gesamtzahl ihrer Spotify-Streams.
""")

st.markdown("---")


col1, col2 = st.columns([1, 1])

with col1:
    st.altair_chart(top_artists_streams_chart, use_container_width=True)

with col2:
    st.altair_chart(artist_streams_pie_chart, use_container_width=True)


def aufteilen_streams(df, artist_column='artist(s)_name', streams_column='streams'):
    # Sicherstellen, dass die Künstler-Spalte als String behandelt wird
    df[artist_column] = df[artist_column].astype(str)

    # Erstellen einer neuen DataFrame, die die Künstlernamen aufsplittet
    new_df = df[artist_column].str.split(',').explode().reset_index()

    # Bereinigen der Künstlernamen und Zuweisung der Streams
    new_df[artist_column] = new_df[artist_column].str.strip()
    new_df = new_df.merge(df[[streams_column]],
                          left_index=True, right_index=True)

    # Streams gleichmäßig auf die Künstler aufteilen
    new_df[streams_column] = new_df[streams_column] / \
        new_df.groupby(level=0)[artist_column].transform('count')

    return new_df.reset_index(drop=True)


# Anwendung der Funktion auf den DataFrame
df_aufgeteilt = aufteilen_streams(df)

artist_list = df_aufgeteilt['artist(s)_name'].unique().tolist()
st.markdown("---")
st.subheader(
    "Hier kannst du selber Künstler auswählen!")

text = " Wähle einen oder mehrere Künstler aus der Liste aus und schaue dir an, wie sich die Streams auf die einzelnen Künstler verteilen. :point_down:"
# user soll einen oder mehrere Künstler auswählen können
selected_artists = st.multiselect(
    text, artist_list)

# Filtern des DataFrames nach den ausgewählten Künstlern

df_filtered = df_aufgeteilt[df_aufgeteilt['artist(s)_name'].isin(
    selected_artists)]


# Gruppieren nach Künstler und Summieren der Streams der user-spezifischen Auswahl
artist_streams_user = df_filtered.groupby('artist(s)_name')[
    'streams'].sum().sort_values(ascending=False)


# Chart für die user-spezifische Auswahl


artist_streams_user_chart = alt.Chart(artist_streams_user.reset_index()).mark_arc().encode(
    theta=alt.Theta(field='streams', type='quantitative'),
    color=alt.Color(field='artist(s)_name', type='nominal',
                    legend=alt.Legend(title='Künstler')),
    order=alt.Order('streams', sort='ascending'),
    tooltip=[
        alt.Tooltip('artist(s)_name', title='Künstlername'),
        alt.Tooltip('streams', title='Anzahl der Streams')
    ]
).properties(
    title={'text': 'Top Künstler nach Streams', 'dy': -0},
    width=400,
    height=300
).configure_title(
    fontSize=25,
    anchor='start'
).configure_legend(
    titleFontSize=16,
    labelFontSize=12
).configure_view(
    strokeWidth=0
)


if len(selected_artists) <= 12 and len(selected_artists) > 0:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.altair_chart(artist_streams_user_chart, use_container_width=False)
elif len(selected_artists) > 12:
    st.error("Bitte wähle nicht mehr als 12 Künstler aus!")


st.markdown("---")
st.write("© 2023 Laurenz Brahner - Alle Rechte vorbehalten.")
