# %%
import pandas as pd
import altair as alt

# %%
file_path = r'C:\Users\Privat\OneDrive\Dokumente\GitHub\DST-Documentation\data_exploration\spotify_angereichert_cleaned.csv'
df = pd.read_csv(file_path)


# %%
df.set_index('track_id', inplace=True)

# %%
artist_streams = df.groupby('artist(s)_name')[
    'streams'].sum().sort_values(ascending=False)

# Anzeigen der Top-Künstler basierend auf Streams
top_artists_streams = artist_streams.head(10)


top_artists_streams_chart = alt.Chart(top_artists_streams.reset_index()).mark_bar().encode(
    y=alt.Y('artist(s)_name', sort='-x',
            axis=alt.Axis(title='Künstler', labelFontSize=12)),
    x=alt.X('streams', axis=alt.Axis(title='Streams (Milliarden)', titleFontSize=20,
            labelFontSize=12, format='.0s', tickCount=5, tickMinStep=1e9, labelExpr='datum.value / 1e9')),
    color=alt.Color('streams', scale=alt.Scale(scheme='viridis'), legend=None),
    tooltip=[
        alt.Tooltip('artist(s)_name', title='Künstlername'),
        alt.Tooltip('streams', title='Anzahl der Streams')
    ]
).properties(
    title={'text': 'Top 10 Künstler nach Streams', 'dy': -20},
    width=800,
    height=400
).configure_title(
    fontSize=25,
    anchor='start'
).configure_axis(
    labelFontSize=12,
    titleFontSize=20,
    titleColor='gray',
    labelColor='gray',
    titlePadding=0,
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
    titleAnchor='middle',
    titleFontSize=20
)


top_artists_streams_chart

# %%
