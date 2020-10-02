import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from util_functions import wind_dataframe, solar_dataframe
import base64
import io


def my_dash_app(server):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    wind_data = wind_dataframe()
    solar_data = solar_dataframe()

    trace1 = go.Bar(x=solar_data.index, y = solar_data['Power_Output_Predictions'],
              name = 'Solar Predictions')

    trace2 = go.Bar(x=wind_data.index, y = wind_data['Power_Output_Predictions'],
              name = 'Wind Predictions')

    layout1 = go.Layout(title = 'Solar Power Plant Predictions',
                        xaxis = {'title': 'Dates'},
                        yaxis = {'title': 'Power(MW)'})
    layout2 = go.Layout(title = 'Wind Farm Power Predictions',
                        xaxis = {'title': 'Dates'},
                        yaxis = {'title': 'Power(MW)'})
    app_dash = dash.Dash(__name__, server = server,
                        show_undo_redo=True,
                        routes_pathname_prefix = '/mydashboard/',
                        external_stylesheets=external_stylesheets)

    app_dash.layout = html.Div(children = [
                        html.Div([
                                html.H1('My Dashboard - AppDev Summatives!', style = {'textAlign': 'center'}),
                                html.Div('Solar Power Plant Predictions'),
                                dcc.Graph(
                                          id = 'solar-plot',
                                          figure = {'data': [trace1],
                                                    'layout':layout1}),
                                dcc.Upload(id='solar-upload-data',
                                           children=html.Button('Scale Prediction by Uploading Solar Maintenance CSV')),
                                html.Hr(),
                                ]),
                        html.Div([
                                html.Div('Wind Farm Predictions'),
                                dcc.Graph(
                                          id = 'wind-plot',
                                          figure = {'data': [trace2],
                                                    'layout':layout2}),
                                dcc.Upload(id='wind-upload-data',
                                           children=html.Button('Scale Prediction by Uploading Wind Maintenance CSV')),
                                html.Hr()
                                ]),
                            ])

    @app_dash.callback(Output('solar-plot', 'figure'),
            [Input('solar-upload-data', 'contents')],
            [State('solar-upload-data', 'filename')])
    def update_solar_plot(contents, filename):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')), header = 1)
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
                            ])
        merged_df = solar_data.merge(df, on = ['Date Of Month'], how = 'left') #merge exiting dataframe with maintenance dataframe
        merged_df.fillna(100, inplace = True) #100 capacity for days without maintenance
        merged_df['Scaled_Power_Output'] = (merged_df['Power_Output_Predictions'] * merged_df['Capacity Available'] / 100) #Scale Predictions
        trace3 = go.Bar(x=solar_data.index, y = merged_df['Scaled_Power_Output'],
                   name = 'Scaled Solar Predictions')
        traces = [trace1, trace3]
        return {'data': traces,
                'layout': go.Layout(title = 'Solar Power Plant Predictions - Combined',
                                    xaxis = {'title': 'Dates'},
                                    yaxis = {'title': 'Power(MW)'})}


    @app_dash.callback(Output('wind-plot', 'figure'),
            [Input('wind-upload-data', 'contents')],
            [State('wind-upload-data', 'filename')])
    def update_wind_plot(contents, filename):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')), header = 1)
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
                            ])
        merged_df = wind_data.merge(df, on = ['Date Of Month'], how = 'left') #merge exiting dataframe with maintenance dataframe
        merged_df.fillna(100, inplace = True) #100 capacity for days without maintenance
        merged_df['Scaled_Power_Output'] = (merged_df['Power_Output_Predictions'] * merged_df['Capacity Available'] / 100) #Scale Predictions
        trace4 = go.Bar(x=wind_data.index, y = merged_df['Scaled_Power_Output'],
                   name = 'Scaled wind Predictions')
        traces = [trace2, trace4]
        return {'data': traces,
                'layout': go.Layout(title = 'Wind Farm Power Predictions - Combined',
                                    xaxis = {'title': 'Dates'},
                                    yaxis = {'title': 'Power(MW)'})}

    return app_dash.server
