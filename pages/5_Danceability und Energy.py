import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from sklearn.linear_model import LinearRegression


st.set_page_config(page_title="Einlfuss der Speechiness",
                   page_icon="📈")


file_path = r'C:\Users\Privat\OneDrive\Dokumente\GitHub\DST-Documentation\data_exploration\spotify_angereichert_cleaned.csv'
df = pd.read_csv(file_path)

df.drop(['Unnamed: 0'], axis=1, inplace=True)


def show_distribution_plot(df, merkmal):
    column_name = ""
    title = ""
    color = ""
    if merkmal == "energy_%":
        column_name = "energy_range"
        title = "Energy"
        color = 'blue'
    if merkmal == "danceability_%":
        column_name = "danceability_range"
        title = "Danceability"
        color = 'orange'

    # calcaulate the mean of the song counts per energy range
    energy_grouped = df.groupby(pd.cut(df[merkmal], range(
        0, 101, 10))).size().reset_index(name='average_song_count')

    # Umbenennung der Spalte für die Energiebereiche
    energy_grouped.columns = [column_name, 'average_song_count']

    energy_grouped[column_name] = energy_grouped[column_name].apply(
        lambda x: f"{x.left}-{x.right}")

    energy_grouped_line_chart = alt.Chart(energy_grouped).mark_line(interpolate='monotone').encode(
        x=alt.X(column_name, axis=alt.Axis(title=title, labelFontSize=14)),
        y=alt.Y('average_song_count', axis=alt.Axis(
            title='Anzahl der Songs', titleFontSize=16, labelFontSize=14)),
        color=alt.value('red'),
        tooltip=[column_name, 'average_song_count']
    )

    energy_grouped_chart = alt.Chart(energy_grouped).mark_bar(opacity=0.7).encode(
        x=alt.X(column_name, axis=alt.Axis(title=title, labelFontSize=14)),
        y=alt.Y('average_song_count', axis=alt.Axis(
            title='Anzahl der Songs', titleFontSize=20, labelFontSize=14)),
        color=alt.Color(column_name,  scale=alt.Scale(
            scheme='viridis'), legend=alt.Legend(title=title)),
        tooltip=[column_name, 'average_song_count']
    )

    x = alt.layer(energy_grouped_chart, energy_grouped_line_chart).properties(
        title={'text': 'Durchschnittliche Anzahl der Songs nach {}'.format(
            title), 'dy': -20},
        width=600,
        height=400
    ).configure_title(
        fontSize=25,
        anchor='start',
        color=color
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

    return x


# sidebar um den user zwischen danceability und energy wählen zu lassen

st.sidebar.title("Tanzbarkeit oder Energy")

diagram = st.sidebar.radio(
    "Welchen Einfluss möchtest du dir anschauen?", ("Energy", "Danceability"), index=0)

st.title("Wie tanzbar und wie energetisch ein Song sein sollte")
st.write("""
         :blue[Energy] spiegelt die Intensität und Aktivität eines Songs wider, während :orange[Danceability] beschreibt, wie geeignet ein Song zum Tanzen ist. 
        
         Durch die Auswahl der Optionen in der Seitenleiste können Sie filtern welches Merkmal sie genauer betrachten möchten.
""")


if diagram == "Energy":
    st.altair_chart(show_distribution_plot(
        df, "energy_%"), use_container_width=True)

    st.write("""
        :point_right:
        :blue[Die meisten Songs haben einen Energy-Wert von 60-70 %] 
        """)

if diagram == "Danceability":
    st.altair_chart(show_distribution_plot(
        df, "danceability_%"), use_container_width=True)

    st.write("""
        :point_right:
        :orange[Die meisten Songs haben einen Danceability-Wert von 70-80%] 
        """)
