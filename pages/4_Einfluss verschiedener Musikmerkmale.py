import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from sklearn.linear_model import LinearRegression


st.set_page_config(page_title="Einlfuss der Speechiness",
                   page_icon="📈", layout='wide')


file_path = r'C:\Users\Privat\OneDrive\Dokumente\GitHub\DST-Documentation\data_exploration\spotify_angereichert_cleaned.csv'
df = pd.read_csv(file_path)

df.drop(['Unnamed: 0'], axis=1, inplace=True)


def mrkmal_streams_chart(merkmal, anzeige):
    title = ""
    color = ""
    if merkmal == 'speechiness_%':
        title = 'Speechiness'
        color = 'blue'
    elif merkmal == 'liveness_%':
        title = 'Liveness'
        color = 'orange'
    elif merkmal == 'instrumentalness_%':
        title = 'Instrumentalness'
        color = 'green'
    elif merkmal == 'acousticness_%':
        title = 'Acousticness'
        color = 'gray'

    agg_df = df.groupby(merkmal).agg({'streams': 'mean'}).reset_index()

    X = agg_df[merkmal].values.reshape(-1, 1)
    y = agg_df['streams'].values
    reg = LinearRegression().fit(X, y)

    # Erstellen Sie eine DataFrame für die Regressionslinie
    regression_df = pd.DataFrame({merkmal: np.linspace(
        df[merkmal].min(), df[merkmal].max(), 100)})
    regression_df['streams_predicted'] = reg.predict(
        regression_df[[merkmal]])

    regression_line = alt.Chart(regression_df).mark_line(color='red').encode(
        x=alt.X(merkmal, axis=alt.Axis(title=title, labelFontSize=14)),
        y=alt.Y('streams_predicted', scale=alt.Scale(domain=[0, 1500000000]), axis=alt.Axis(title='Streams (Milliarden)', titleFontSize=16,
                labelFontSize=14, format='.0s', tickCount=5, tickMinStep=1e9, labelExpr='datum.value / 1e9')),
    )

    custom_legend_values = [0, 1500000000]

    scatter_plot = alt.Chart(agg_df).mark_circle(size=60, opacity=0.7).encode(
        x=alt.X(merkmal, axis=alt.Axis(
            title=title, labelFontSize=14)),
        y=alt.Y('streams', axis=alt.Axis(title='Streams (Milliarden)', titleFontSize=16,
                labelFontSize=14, format='.0s', tickCount=5, tickMinStep=1e9, labelExpr='datum.value / 1e9')),
        color=alt.Color('streams', scale=alt.Scale(
            scheme="viridis", domain=custom_legend_values), legend=None),
        tooltip=[merkmal, 'streams']
    )

    if anzeige == 'Beides':
        final_plot = alt.layer(scatter_plot, regression_line)
    elif anzeige == 'Regressions Linie':
        final_plot = regression_line
    elif anzeige == 'Scatter Points':
        final_plot = scatter_plot

    scatter_plot_1 = final_plot.properties(
        title={'text': '{}'.format(title), 'dy': -20},
        width=475,
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

    return scatter_plot_1


def mrkmal_streams_chart_with_song_amount(merkmal, anzeige):
    title = ""
    color = ""
    if merkmal == 'speechiness_%':
        title = 'Speechiness'
        color = 'blue'
    elif merkmal == 'liveness_%':
        title = 'Liveness'
        color = 'orange'
    elif merkmal == 'instrumentalness_%':
        title = 'Instrumentalness'
        color = 'green'
    elif merkmal == 'acousticness_%':
        title = 'Acousticness'
        color = 'gray'

    song_count_df = df.groupby(
        merkmal).size().reset_index(name='song_count')

    X = song_count_df[merkmal].values.reshape(-1, 1)
    y = song_count_df['song_count'].values
    reg = LinearRegression().fit(X, y)

    # Erstellen Sie eine DataFrame für die Regressionslinie
    regression_df = pd.DataFrame(
        {merkmal: np.linspace(df[merkmal].min(), df[merkmal].max(), 100)})

    regression_df['song_count_predicted'] = reg.predict(
        regression_df[[merkmal]])

    regression_df['song_count_predicted'] = regression_df['song_count_predicted'].clip(
        lower=0)
    y_max = song_count_df['song_count'].max()

    regression_line = alt.Chart(regression_df).mark_line(color='red').encode(
        x=alt.X(merkmal, axis=alt.Axis(title=title, labelFontSize=14)),
        y=alt.Y('song_count_predicted', scale=alt.Scale(domain=[0, y_max]), axis=alt.Axis(title='Anzahl der Songs', titleFontSize=16,
                labelFontSize=14, tickCount=5, )),
    )

    custom_legend_values = [0, y_max]

    scatter_plot = alt.Chart(song_count_df).mark_circle(size=60, opacity=0.7).encode(
        x=alt.X(merkmal, axis=alt.Axis(
            title=title, labelFontSize=14)),
        y=alt.Y('song_count', axis=alt.Axis(title='Anzahl der Songs', titleFontSize=16,
                labelFontSize=14,)),
        color=alt.Color('song_count', scale=alt.Scale(
            scheme="viridis", domain=custom_legend_values), legend=None),
        tooltip=[merkmal, 'song_count']
    )

    if anzeige == 'Beides':
        final_plot = alt.layer(scatter_plot, regression_line)
    elif anzeige == 'Regressions Linie':
        final_plot = regression_line
    elif anzeige == 'Scatter Points':
        final_plot = scatter_plot

    scatter_plot_1 = final_plot.properties(
        title={'text': '{}'.format(title), 'dy': -20},
        width=475,
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

    return scatter_plot_1


st.title('Analyse des Einflusses von Audio-Merkmalen auf die Songpopularität')

st.write("""
Diese Visualisierung bietet einen tiefgreifenden Einblick in den Einfluss verschiedener Audio-Merkmale wie :blue[Speechiness],
          :orange[Liveness], :green[Instrumentalness] und :gray[Acousticness] auf die Popularität von Songs, gemessen an Streams und Songanzahl. 
         Nutzer können zwischen verschiedenen Darstellungen wählen, einschließlich Streudiagrammen und Regressionslinien,
          um die Beziehungen zwischen den Audio-Merkmalen und der Popularität der Songs zu verstehen.
""")


# side bar for removing the regression line and the Scatter points

remove_regression = st.sidebar.radio(
    'Was möchten sie Anzeigen lassen', ('Beides', 'Regressions Linie', 'Scatter Points'), index=0)

y_axis_user_option = st.sidebar.radio(
    'Welche Y-Achse möchten Sie verwenden?', ('Streams', 'Anzahl der Songs'), index=0)


if remove_regression == 'Beides':
    col1, col2 = st.columns([1, 1])

    with col1:
        if y_axis_user_option == 'Streams':
            st.altair_chart(mrkmal_streams_chart(
                'speechiness_%', remove_regression))

        elif y_axis_user_option == 'Anzahl der Songs':
            st.altair_chart(mrkmal_streams_chart_with_song_amount(
                'speechiness_%', remove_regression))

    with col2:
        if y_axis_user_option == 'Streams':
            st.altair_chart(mrkmal_streams_chart(
                'liveness_%', remove_regression))

        elif y_axis_user_option == 'Anzahl der Songs':
            st.altair_chart(mrkmal_streams_chart_with_song_amount(
                'liveness_%', remove_regression))

    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    with col1:
        if y_axis_user_option == 'Streams':
            st.altair_chart(mrkmal_streams_chart(
                'instrumentalness_%', remove_regression))

        elif y_axis_user_option == 'Anzahl der Songs':
            st.altair_chart(mrkmal_streams_chart_with_song_amount(
                'instrumentalness_%', remove_regression))

    with col2:
        if y_axis_user_option == 'Streams':
            st.altair_chart(mrkmal_streams_chart(
                'acousticness_%', remove_regression))

        elif y_axis_user_option == 'Anzahl der Songs':
            st.altair_chart(mrkmal_streams_chart_with_song_amount(
                'acousticness_%', remove_regression))

    st.markdown("---")

 #   col1, col2 = st.columns([1, 1])
 #   with col1:
 #       if y_axis_user_option == 'Streams':
 #           st.altair_chart(mrkmal_streams_chart(
 #               'danceability_%', remove_regression))
#
#        elif y_axis_user_option == 'Anzahl der Songs':
#            st.altair_chart(mrkmal_streams_chart_with_song_amount(
#                'danceability_%', remove_regression))

#    with col2:
#        if y_axis_user_option == 'Streams':
#            st.altair_chart(mrkmal_streams_chart(
#                'energy_%', remove_regression))
#
#        elif y_axis_user_option == 'Anzahl der Songs':
#            st.altair_chart(mrkmal_streams_chart_with_song_amount(
#                'energy_%', remove_regression))


elif remove_regression == 'Regressions Linie':
    col1, col2 = st.columns([1, 1])

    with col1:
        if y_axis_user_option == 'Streams':
            st.altair_chart(mrkmal_streams_chart(
                'speechiness_%', remove_regression))

        elif y_axis_user_option == 'Anzahl der Songs':
            st.altair_chart(mrkmal_streams_chart_with_song_amount(
                'speechiness_%', remove_regression))

    with col2:
        if y_axis_user_option == 'Streams':
            st.altair_chart(mrkmal_streams_chart(
                'liveness_%', remove_regression))

        elif y_axis_user_option == 'Anzahl der Songs':
            st.altair_chart(mrkmal_streams_chart_with_song_amount(
                'liveness_%', remove_regression))

    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    with col1:
        if y_axis_user_option == 'Streams':
            st.altair_chart(mrkmal_streams_chart(
                'instrumentalness_%', remove_regression))

        elif y_axis_user_option == 'Anzahl der Songs':
            st.altair_chart(mrkmal_streams_chart_with_song_amount(
                'instrumentalness_%', remove_regression))

    with col2:
        if y_axis_user_option == 'Streams':
            st.altair_chart(mrkmal_streams_chart(
                'acousticness_%', remove_regression))

        elif y_axis_user_option == 'Anzahl der Songs':
            st.altair_chart(mrkmal_streams_chart_with_song_amount(
                'acousticness_%', remove_regression))

#    st.markdown("---")
#
#    col1, col2 = st.columns([1, 1])
#    with col1:
#        if y_axis_user_option == 'Streams':
#            st.altair_chart(mrkmal_streams_chart(
#                'danceability_%', remove_regression))
#
#        elif y_axis_user_option == 'Anzahl der Songs':
#            st.altair_chart(mrkmal_streams_chart_with_song_amount(
#                'danceability_%', remove_regression))
#
#    with col2:
#        if y_axis_user_option == 'Streams':
#            st.altair_chart(mrkmal_streams_chart(
#                'energy_%', remove_regression))
#
#        elif y_axis_user_option == 'Anzahl der Songs':
#            st.altair_chart(mrkmal_streams_chart_with_song_amount(
#                'energy_%', remove_regression))


elif remove_regression == 'Scatter Points':
    col1, col2 = st.columns([1, 1])

    with col1:
        if y_axis_user_option == 'Streams':
            st.altair_chart(mrkmal_streams_chart(
                'speechiness_%', remove_regression))

        elif y_axis_user_option == 'Anzahl der Songs':
            st.altair_chart(mrkmal_streams_chart_with_song_amount(
                'speechiness_%', remove_regression))

    with col2:
        if y_axis_user_option == 'Streams':
            st.altair_chart(mrkmal_streams_chart(
                'liveness_%', remove_regression))

        elif y_axis_user_option == 'Anzahl der Songs':
            st.altair_chart(mrkmal_streams_chart_with_song_amount(
                'liveness_%', remove_regression))

    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    with col1:
        if y_axis_user_option == 'Streams':
            st.altair_chart(mrkmal_streams_chart(
                'instrumentalness_%', remove_regression))

        elif y_axis_user_option == 'Anzahl der Songs':
            st.altair_chart(mrkmal_streams_chart_with_song_amount(
                'instrumentalness_%', remove_regression))

    with col2:
        if y_axis_user_option == 'Streams':
            st.altair_chart(mrkmal_streams_chart(
                'acousticness_%', remove_regression))

        elif y_axis_user_option == 'Anzahl der Songs':
            st.altair_chart(mrkmal_streams_chart_with_song_amount(
                'acousticness_%', remove_regression))

        st.markdown("---")

#    col1, col2 = st.columns([1, 1])
#    with col1:
#        if y_axis_user_option == 'Streams':
#            st.altair_chart(mrkmal_streams_chart(
#                'danceability_%', remove_regression))
#
#        elif y_axis_user_option == 'Anzahl der Songs':
#            st.altair_chart(mrkmal_streams_chart_with_song_amount(
#                'danceability_%', remove_regression))
#
#    with col2:
#        if y_axis_user_option == 'Streams':
#            st.altair_chart(mrkmal_streams_chart(
#                'energy_%', remove_regression))
#
#        elif y_axis_user_option == 'Anzahl der Songs':
#            st.altair_chart(mrkmal_streams_chart_with_song_amount(
#                'energy_%', remove_regression))
