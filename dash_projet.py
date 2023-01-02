import dash
from dash import Dash, dash_table, State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px 
from dash.dependencies import Output,Input
from V2_NoSqlDataAccess import NoSqlDataAccess


app = Dash(__name__)

#################### INITIALISATION DE LA DATA ##########################################################################
nsql = NoSqlDataAccess()
result = nsql.recherche_distance(lat = 45.4380 , longi = 4.3862)
df = pd.DataFrame (result, columns = ['Record Distance', 'latitude', 'longitude','Lieu'])
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

#####################################################################################################

specFig = px.scatter_mapbox(df, lat="latitude", lon="longitude", 
    hover_name="Lieu", color_discrete_sequence=["blue"], 
    zoom=13, height=600, mapbox_style="stamen-terrain")

app = Dash(__name__)

app.layout = html.Div([
    html.Label('Latitude :'),
    dcc.Input(id='latitude', type='number', value=0),
    html.Label(' Longitude :'),
    dcc.Input(id='longitude', type='number', value=0),
    html.Div([html.H1('**Application tourisme**')], style={'textAlign': 'center'}),
    html.Div(id='output'),
    html.Button(id='submit-button', children='Valider'),

#    html.Div(dcc.Dropdown(id = 'page-2-dropdown',
#                        options= [{'label': 'type', 'value': 'type'},
#                                  {'label': 'Record Distance', 'value': 'Record Distance'}],
#                        value= 'type'
#
#  )),
    

    dcc.Graph(id= 'Premier graphe',
                      figure= specFig),
    
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
])
@app.callback(
    [Output('Premier graphe', 'figure'),
    Output('table', 'data')],
    [Input('latitude', 'value'),
     Input('longitude', 'value'),
     Input('submit-button', 'n_clicks')]
)

def update_output(latitude, longitude, n_clicks):
    if n_clicks is not None :
        nsql = NoSqlDataAccess()
        lat = latitude
        longi = longitude
        result = nsql.recherche_distance(lat, longi)
        df = pd.DataFrame (result, columns = ['Record Distance', 'latitude', 'longitude','Lieu'])
        df['latitude'] = df['latitude'].astype(float)
        df['longitude'] = df['longitude'].astype(float)
        return px.scatter_mapbox(df, lat="latitude", lon="longitude", 
        hover_name="Lieu", color_discrete_sequence=["blue"], 
        zoom=13, height=600, mapbox_style="stamen-terrain"), df.to_dict('records')
    if n_clicks is None:
        nsql = NoSqlDataAccess()
        result = nsql.recherche_distance(lat = 45.4380 , longi = 4.3862)
        df = pd.DataFrame (result, columns = ['Record Distance', 'latitude', 'longitude','Lieu'])
        df['latitude'] = df['latitude'].astype(float)
        df['longitude'] = df['longitude'].astype(float)
        return specFig, df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
