import streamlit as st
import pandas as pd
import altair as alt
import time


st.set_page_config(page_title="Einlfuss der Tonart",
                   page_icon="📈")


# Line Chart
file_path = './spotify_angereichert_cleaned.csv'
df = pd.read_csv(file_path)

df.drop(['Unnamed: 0'], axis=1, inplace=True)


# line plot Anzahl der Verföffenltichungen Monat im Jahr

monthly_releases = df.groupby(
    'released_month').size().reset_index(name='count')

month_labels = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}

monthly_releases['released_month'] = monthly_releases['released_month'].map(
    month_labels)


def monthly_rel_chart(df):
    chart = alt.Chart(df).mark_line(strokeWidth=3).encode(
        x=alt.X('released_month', axis=alt.Axis(title='Monat',
                                                labelFontSize=14), sort=list(month_labels.values())),
        y=alt.Y('count', scale=alt.Scale(domain=(30, 120)), axis=alt.Axis(
            title='Veröffentlichungen', titleFontSize=20, labelFontSize=14,)),
        tooltip=['released_month', 'count']
    ).properties(
        title={'text': 'Anzahl der Songveröffentlichungen nach Monat', 'dy': -20},
        width=600,
        height=400
    ).configure_title(
        fontSize=25,
        anchor='start'

    ).configure_axis(
        labelFontSize=14,
        titleFontSize=20,
        titleColor='gray',
        labelColor='gray',
        titlePadding=12
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
    return chart


st.title("Einfluss der Veröffentlichungsmonate")
st.write("""
Hier stellen wir uns die Frage, wann es am besten ist, einen Song zu veröffentlichen. Dazu schauen wir uns die Anzahl der Veröffentlichungen der beliebtesten Songs nach Veröffentlichungsmonat an.
""")


if 'diagramm_starten' not in st.session_state:
    st.session_state['diagramm_starten'] = False

if 'show_details' not in st.session_state:
    st.session_state['show_details'] = False


col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button('Diagrammdemo starten'):
        st.session_state['diagramm_starten'] = True

with col3:
    if st.button('Mehr Details anzeigen'):
        st.session_state['show_details'] = True


chart_placeholder = st.empty()

# Schleife, um das Diagramm schrittweise zu aktualisieren, nachdem der Button geklickt wurde
if st.session_state.get('diagramm_starten', False):
    for month in range(1, 13):
        # Filtern der Daten bis zum aktuellen Monat
        filtered_monthly_releases = monthly_releases.iloc[:month]

        # Anzeigen des Diagramms im Platzhalter
        chart_placeholder.altair_chart(monthly_rel_chart(
            filtered_monthly_releases), use_container_width=True)

        # Warten für 5 Sekunden vor dem Hinzufügen des nächsten Monats
        time.sleep(0.25)

        # Zurücksetzen des Zustands nach der Schleife
    st.session_state.diagramm_starten = False


def base_chart(df):
    chart = alt.Chart(df).mark_line(strokeWidth=3).encode(
        x=alt.X('released_month', axis=alt.Axis(title='Monat',
                                                labelFontSize=14), sort=list(month_labels.values())),
        y=alt.Y('count', scale=alt.Scale(domain=(30, 120)), axis=alt.Axis(
                title='Veröffentlichungen', titleFontSize=20, labelFontSize=14,)),
        tooltip=['released_month', 'count']
    )
    return chart


data_januar = pd.DataFrame({'count': [112], 'released_month': ['Jan']})
data_may = pd.DataFrame({'count': [112], 'released_month': ['May']})
data_Aug = pd.DataFrame({'count': [39], 'released_month': ['Aug']})

max_points = monthly_releases[monthly_releases['count']
                              == monthly_releases['count'].max()]
min_points = monthly_releases[monthly_releases['count']
                              == monthly_releases['count'].min()]

min_points_chart = base_chart(min_points).mark_point(
    size=100, color='red', opacity=0.8,  filled=True)
max_points_chart = base_chart(max_points).mark_point(
    size=100, color='green', opacity=0.8, filled=True)
min_points_chart_line = alt.Chart(data_Aug).mark_rule(strokeDash=[12, 6], size=1, color='red', fontSize=12, opacity=1).encode(
    y='count',
    x=alt.X('released_month', sort=list(month_labels.values())),
)
max_points_chart_line_jan = alt.Chart(data_januar).mark_rule(strokeDash=[12, 6], size=1, color='green', fontSize=12, opacity=0.8).encode(
    y='count',
    x=alt.X('released_month', sort=list(month_labels.values())),
)
max_points_chart_line_may = alt.Chart(data_may).mark_rule(strokeDash=[12, 6], size=1, color='green', fontSize=12, opacity=0.8).encode(
    y='count',
    x=alt.X('released_month', sort=list(month_labels.values())),
)

# Button, um das aktualisierte Diagramm mit Punkten und Linien anzuzeigen


if st.session_state['show_details']:

    # Zeigen Sie das aktualisierte Diagramm mit Punkten und Linien an
    final_chart = alt.layer(
        max_points_chart_line_jan,
        base_chart(monthly_releases),  # Basisliniendiagramm
        max_points_chart_line_may,     # Gestrichelte Linien und Punkte für Mai-Maximum
        min_points_chart,              # Minimumpunkte
        max_points_chart,              # Maximumpunkte
        min_points_chart_line          # Gestrichelte Linien für Minimumpunkte
    ).properties(
        title={'text': 'Anzahl der Songveröffentlichungen nach Monat', 'dy': -20},
        width=550,
        height=400
    ).configure_title(
        fontSize=25,
        anchor='start'
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=20,
        titleColor='gray',
        labelColor='gray',
        titlePadding=12
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

    chart_placeholder.altair_chart(final_chart, use_container_width=True)

    st.write("""
        :point_right:
        :green[Die meisten Top-Songs werden im Januar und im Mai released.]     
""")
    st.write(""":point_right: 
        :red[Die wenigsten Top-Songs werden im August released.] 
     """)

st.markdown("---")
st.write("© 2023 Laurenz Brahner - Alle Rechte vorbehalten.")
