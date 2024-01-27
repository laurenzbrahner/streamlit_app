import streamlit as st
import pandas as pd
import altair as alt


st.set_page_config(page_title="Einlfuss der Tonart",
                   page_icon="📈", layout='wide')

file_path = './spotify_angereichert_cleaned.csv'
df = pd.read_csv(file_path)

df.drop(['Unnamed: 0'], axis=1, inplace=True)

mode_streams = df.groupby('mode')['streams'].mean()


mode_streams_df = mode_streams.reset_index()

# Tonart bar chart


def mode_streams_chart(df, key):
    if len(key) == 0:
        key = ""
    else:
        inhalt = ", ".join(key)
        key = "Key: {}".format(inhalt)
    chart_mode_bar = alt.Chart(df).mark_bar(clip=True, size=50).encode(
        x=alt.X('mode', axis=alt.Axis(title='Tonart', labelFontSize=14)),
        y=alt.Y('streams', scale=alt.Scale(domain=[250000000, 650000000]), axis=alt.Axis(title='Streams (Millionen) Ø ', titleFontSize=20,
                                                                                         labelFontSize=14, format='.0s', tickCount=6, tickMinStep=1e9, labelExpr='datum.value / 1e6')),
        color=alt.Color('mode', legend=None, scale=alt.Scale(
            range=['#4ee2e6', 'white'])),

        tooltip=[
            alt.Tooltip('mode', title='Tonart'),
            alt.Tooltip('streams', title='Ø Streams')
        ]
    ).properties(
        title={'text': 'Ø Streams nach Tonart {}'.format(key), 'dy': -20},
        width=550,
        height=400
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
    return chart_mode_bar


# Key bar chart

key_streams = df.groupby('key')['streams'].mean()


key_streams_df = key_streams.reset_index()


def key_chart(df, title):
    if title == "Alle":
        title = ""
    else:
        title = "Tonart: {}".format(title)
    key_streams_chart = alt.Chart(df).mark_bar(clip=True, size=20).encode(
        x=alt.X('key',  axis=alt.Axis(title='Key', labelFontSize=14)),
        y=alt.Y('streams', scale=alt.Scale(domain=[250000000, 650000000]), axis=alt.Axis(title='Streams (Millionen) Ø ', titleFontSize=20,
                labelFontSize=14, format='.0s', tickCount=6, tickMinStep=1e9, labelExpr='datum.value / 1e6')),
        color=alt.Color('key', legend=None,),
        tooltip=['key', 'streams']
    ).properties(
        title={'text': 'Ø Streams nach Key {}'.format(
            title), 'dy': -20},
        width=550,
        height=400
    ).configure_title(
        fontSize=25,
        anchor='start',
        color='#60b4ff'
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

    return key_streams_chart


st.title(
    "Welchen Einfluss hat die :orange[Tonart] und die :blue[Keys] auf die Streamingzahlen?")

st.write("""
Diese Seite bietet einen Einblick in die Streaming-Dynamik von Dur (Major) und Moll (Minor) :orange[***Tonarten***],
          die als Schlüsselindikatoren für die Präferenzen von Hörern gelten. Während Dur ("Major") für seine helle und fröhliche Klangfarbe bekannt ist, bietet Moll ("Minor") eine tiefere, oft melancholischere Stimmung.
          Des weiteren werden die Tonstufen oder auch :blue[***keys***] auf ihre Beliebtheit untersucht.
""")

# Sidebar
# User soll die Tonart Major oder Minor Auswählen und keys auswählen können

st.sidebar.header("Filtermöglichkeiten")

st.markdown("---")

mode_list = df["mode"].unique().tolist()
mode_list.append("Alle")

key_list = df["key"].unique().tolist()


mode = st.sidebar.selectbox("Tonart", mode_list, index=2)
st.sidebar.markdown("---")

key = st.sidebar.multiselect("Key", key_list)


# filter df by only key and mode in seperate df

if mode == "Alle" and key == []:
    filtered_df = df
elif mode == "Alle" and key != []:
    filtered_df = df[df['key'].isin(key)]
elif mode != "Alle" and key == []:
    filtered_df = df[df['mode'] == mode]
else:
    filtered_df = df[(df['mode'] == mode) & (df['key'].isin(key))]


# sort filterd df by streams


col1, col2 = st.columns([1, 1])

with col1:
    mode_streams = filtered_df.groupby('mode')['streams'].mean()
    mode_streams_df = mode_streams.reset_index()
    st.altair_chart(mode_streams_chart(mode_streams_df, key),
                    use_container_width=True)

with col2:
    key_streams = filtered_df.groupby('key')['streams'].mean()
    key_streams_df = key_streams.reset_index()
    st.altair_chart(key_chart(key_streams_df, mode),
                    use_container_width=True)

# st.markdown("---")

col11, col22, col33 = st.columns([1, 1, 1])

# funktion zum dynmaischen Überschriften Anzeigen


def title(title, key):
    if title == "Alle":
        mode = ""
    else:
        mode = "Tonart: {}".format(title)
    if len(key) == 0:
        keys = ""
    elif len(key) >= 1:
        inhalt = ", ".join(key)
        keys = "Key(s): {}".format(inhalt)
    return mode, keys


with col22:
    # show top 5 track names and artist names as a text ranking
    inhalt = title(mode, key)
    top_songs = "Top 5 Songs"
    top_songs += " :orange[***{}***]".format(inhalt[0]) if inhalt[0] else ""
    top_songs += " :blue[***{}***]".format(inhalt[1]) if inhalt[1] else ""

    st.subheader(top_songs)
    filtered_df = filtered_df.sort_values(by='streams', ascending=False)
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df = filtered_df.head(5)
    filtered_df = filtered_df[['track_name', 'artist(s)_name', 'streams']]
    filtered_df = filtered_df.rename(
        columns={'track_name': 'Track Name', 'artist(s)_name': 'Artist Name', 'streams': 'Streams'})
    st.table(filtered_df)


st.markdown("---")
st.write("© 2023 Laurenz Brahner - Alle Rechte vorbehalten.")
