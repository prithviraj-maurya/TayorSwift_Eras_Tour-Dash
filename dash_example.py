# Import packages
import numpy as np
import dash
import json
import random
from skimage import io
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_mantine_components as dmc
from dash_bootstrap_templates import load_figure_template

load_figure_template(["cyborg", "darkly"])

# Incorporate data
df = pd.read_csv('ts_data/taylor_swift_spotify.csv')
ts_setlist_spotify_merged = pd.read_csv("ts_data/ts_setlist_spotify_merged.csv")
ts_spotify_songs_setlist_count = pd.read_csv("ts_data/ts_spotify_songs_setlist_count.csv")
albums = pd.read_csv("ts_data/spotify_taylor_swift.csv")
venue = pd.read_csv("ts_data/venue_coordinates.csv")
tours = pd.read_csv("ts_data/lyrics_data.csv")
df["release_date"] = pd.to_datetime(df["release_date"])
df["year"] = df["release_date"].dt.year
year_counts = df.groupby('year',as_index=False).count().sort_values(by='name',ascending=False).sort_values(by='year')

# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

## 1. Popularity of albums over the years with album duration as size
grouped = ts_setlist_spotify_merged.groupby(['album', 'year']).agg({'popularity': 'mean', 'duration_m': 'sum'}).reset_index()
popularity_albums_years_duration_fig = px.scatter(grouped, x='year', y='popularity', size='duration_m', color='album',
                 labels={'popularity': 'Mean Popularity', 'duration_m': 'Total Duration (m)'},
                 title='Album Popularity Over the Years with Circle Size as Duration')

# Create a bar chart for popularity
bar_fig = go.Figure(data=[
    go.Bar(x=grouped['year'], y=grouped['popularity'], width=0.1, marker=dict(opacity=0.5))
])

popularity_albums_years_duration_fig.add_trace(bar_fig.data[0])
popularity_albums_years_duration_fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Mean Popularity',
    showlegend=False
)

# show image
random_row = albums.loc[random.choice(albums.index)]
url = json.loads(random_row.images.replace("'", "\""))[0]["url"]
img = io.imread(url)
album_image_fig = px.imshow(img)
album_image_fig.update_xaxes(showticklabels=False)
album_image_fig.update_yaxes(showticklabels=False)
album_image_fig.update_layout(xaxis_title=random_row["name"], showlegend=False)

## 2. Number of tracks per year and track each Era
tracks_per_era_fig = px.histogram(tours, x="Era", color="Era", title="Different Era's in the dataset")
tracks_per_era_fig.update_layout(showlegend=False)

## 3. Geolocation map
graph_map_figure = fig = go.Figure(data=go.Scattergeo(
    locationmode = 'USA-states',
    lat = venue.latitude.values,
    lon = venue.longitude.values,
    mode = 'lines',
    line = dict(width = 2, color = 'blue'),
    hoverinfo = 'text',
    text = venue['city'],
))

graph_map_figure.update_layout(
    title_text = 'TS concerts',
    showlegend = False,
    geo = dict(
        scope = 'north america',
        projection_type = 'azimuthal equal area',
        showland = True,
        landcolor = 'rgb(243, 243, 243)',
        countrycolor = 'rgb(204, 204, 204)',
    ),
)

## 4. Number of times song performed on Eras
times_performed_popularity_fig = px.scatter(
    ts_spotify_songs_setlist_count,
    title="Number of times performed in Eras vs Popularity on Spotify",
    x="popularity",
    y="times_performed_eras",
    hover_name="name",
)

## 5. Duration of albums over the year
year_album_duration = ts_setlist_spotify_merged.groupby(['year', 'album'])['duration_m'].sum().reset_index()
year_album_duration_fig = px.scatter(year_album_duration, y="duration_m", x="year", color="album", template='darkly')

## 6. Duration of songs over the year
year_duration = ts_setlist_spotify_merged.groupby(['year', 'setlist_id'])['duration_m'].sum().reset_index()
year_duration_fig = px.scatter(year_duration, y="duration_m", x="year", title="Duration of setlist over the years")

## 7. Spotify metrics variation over Eras
cols = ['acousticness', 'danceability', 'energy', 'liveness']
era_metrics = ts_setlist_spotify_merged.dropna(subset=cols).groupby('era_name').agg({
    'acousticness': 'mean',
    'danceability': 'mean',
    'energy': 'mean',
    'loudness': 'mean',
    'liveness': 'mean'
}).reset_index()
spotify_metrics_Eras_fig = px.line(era_metrics, x='era_name', y=cols,
              line_shape='spline',
              labels={'era_name': 'Era', 'value': 'Metric Value'},
              title='Spotify Metrics Across Eras')
spotify_metrics_Eras_fig.update_layout(
    xaxis_title='Era',
    yaxis_title='Metric Value',
)

## 8. Spotify metrics grid
sptofiy_metrics_fig=make_subplots(rows=3,cols=3,subplot_titles=('<i>popularity', '<i>danceability', '<i>energy', '<i>loudness', '<i>log(speechiness)', '<i>acousticness', '<i>log(liveness)', '<i>valence', '<i>tempo'))
sptofiy_metrics_fig.add_trace(go.Histogram(x=df['popularity'],name='popularity'),row=1,col=1)
sptofiy_metrics_fig.add_trace(go.Histogram(x=df['danceability'],name='danceability'),row=1,col=2)
sptofiy_metrics_fig.add_trace(go.Histogram(x=df['energy'],name='energy'),row=1,col=3)
sptofiy_metrics_fig.add_trace(go.Histogram(x=df['loudness'],name='loudness'),row=2,col=1)
sptofiy_metrics_fig.add_trace(go.Histogram(x=np.log(df['speechiness']),name='log(speechiness)'),row=2,col=2)
sptofiy_metrics_fig.add_trace(go.Histogram(x=df['acousticness'],name='acousticness'),row=2,col=3)
sptofiy_metrics_fig.add_trace(go.Histogram(x=np.log(df['liveness']),name='log(liveness)'),row=3,col=1)
sptofiy_metrics_fig.add_trace(go.Histogram(x=df['valence'],name='valence'),row=3,col=2)
sptofiy_metrics_fig.add_trace(go.Histogram(x=df['tempo'],name='tempo'),row=3,col=3)
sptofiy_metrics_fig.update_layout(height=900,title_text='<b>Spotify Metrics',showlegend=False)

# App layout
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    withGlobalStyles=True,
    children=[
        dmc.Container([
            dmc.Title('How to Become Taylor Swift ?', color="blue", size="h1", align="center"),
            ## Row 1 - Album Popularity over Years and Album Image
            dmc.Title("Step 1: Album releases and Album cover ", size="sm"),
            dmc.Title("You need to release xx albums each year and look how dynamic album cover she makes", size="xs", color="gray"),
            dmc.Grid([
                dmc.Col([
                    dcc.Graph(figure=popularity_albums_years_duration_fig),
                ], span=8),
                dmc.Col([
                    dcc.Graph(figure=album_image_fig)
                ], span=4),
            ]),

            ## Row 2 - Tracks per year & tracks per Era
            dmc.Title("Step 2: Number of tours performed and tracks released ", size="sm"),
            dmc.Grid([
                dmc.Col(dcc.Graph(figure=px.area(year_counts, title="Number of songs vs year released", x="year", y="name")), span=6),
                dmc.Col(dcc.Graph(figure=tracks_per_era_fig), span=6)
            ]),

            ## Row 3 - Map & Name of Albums/Tracks
            dmc.Title("Step 3: Go to all states of US and choose smart Album titles", size="sm"),
            dmc.Grid([
                dmc.Col([
                    dcc.Graph(figure=graph_map_figure),
                ], span=6),
               dmc.Col([
                    dash_table.DataTable(df[["name"]].to_dict('records'), style_cell={'textAlign': 'left'}, page_size=13)
               ], span=6)
            ]),

            ## Row 4: Eras tour popularity & Duration of setlist
            dmc.Grid([
               dmc.Col([
                    dcc.Graph(figure=times_performed_popularity_fig),
               ], span=6),
                dmc.Col([
                    dcc.Graph(figure=year_duration_fig),
               ], span=6),
            ]),

            ## Row 5: Spotify Metrics Over Eras
            dcc.Graph(figure=spotify_metrics_Eras_fig),

            ## Row 6: Spotify metrics
            dcc.Graph(figure=sptofiy_metrics_fig)
        ], size=1200, px="xs")
    ]
)

# Run the App
if __name__ == '__main__':
    app.run(debug=True)