import dash
from dash import Dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px 
from dash.dependencies import Output,Input

app = Dash(__name__)

#################### DATA ##########################################################################
df = pd.read_csv("data_graph_def.csv")
df_sté = df[df['ville'] == 'SAINT ETIENNE']
df_sté = df_sté[['ville','type', 'latitude', 'longitude', 'lieu']]

#####################################################################################################

specFig = px.scatter_mapbox(df_sté, lat="latitude", lon="longitude", 
    hover_name="lieu", color_discrete_sequence=["blue"], 
    zoom=13, height=600, mapbox_style="stamen-terrain")
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app = Dash(__name__)

app.layout = html.Div([
    html.Div([html.H1('**Application tourisme**')], style={'textAlign': 'center'}),
    html.Div(dcc.Dropdown(id = 'page-2-dropdown',
                        options= [{'label': 'type', 'value': 'type'},
                                  {'label': 'ville', 'value': 'ville'}],
                        value= 'type'
  )),
dcc.Graph(id= 'Premier graphe',
                      figure= specFig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
