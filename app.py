import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

import pandas as pd
import numpy as np
import pyreadstat
import re

# load data
fpath = 'data/ATP W42.sav'

df, meta = pyreadstat.read_sav(fpath)


""" 
data cleaning, transformation

"""

# regular expression that matches with every character up until the first whitespace character.
pattern = re.compile(r'.+?\.\s?')

label_dict = {}

for key, value in meta.column_names_to_labels.items():
    label_dict[key] = re.sub(pattern=pattern, string=value, repl='')


# helper function used to sort survey items according to thematic subject matter code (e.g. starts with 'RQ')
def list_helper(theme_code):
    return [i for i in df.columns if theme_code in i]

past_future = ['PAST_W42', 'FUTURE_W42']
society = ['SC1_W42']
policy = list_helper('POLICY')
confidence = list_helper('CONF')
rq_form1 = list_helper('RQ')
pw_form2 = list_helper('PQ')
scm = list_helper('SCM')
q = [i for i in df.columns if re.search("^Q[0-9]", i)] #regex to grab Q6, Q7, etc.
pop = list_helper('POP')
knowledge = list_helper('KNOW')
demographics = list_helper('F_')
weight = ['WEIGHT_W42']


# changes the values in the dataframe according to the value formats in the metadata.
df_copy = pyreadstat.pyreadstat.set_value_labels(df, meta)


# dictionary of column names to be used with dcc.Dropdown()
meta_list = zip(meta.column_names, meta.column_labels)
policy_dropdown = [{'label': y, 'value': x} for x, y in meta_list if x in policy]


# note: had to redeclare meta_list for second list comprehension. Returns empty list otherwise
meta_list = zip(meta.column_names, meta.column_labels)
demo_dropdown = [{'label': y, 'value': x} for x, y in meta_list if x in demographics]

# function generates a static bar chart to be used as visuals
def frequency_chart(array1, array2):
    temp_df = pd.crosstab(df_copy[array1],
                       df_copy[array2],
                       df_copy.WEIGHT_W42, aggfunc = sum, dropna=True,
                       normalize='index').\
                       loc[meta.variable_value_labels[array1].values()].\
                       loc[:, meta.variable_value_labels[array2].values()]*100
    
    fig = px.bar(temp_df, x=temp_df.index, y=temp_df.columns )

    fig.update_layout(
        title={
            'text': label_dict[array2],
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font':dict(
                size=18)},
        
        xaxis_title="Frequency (%)",
        yaxis_title=None,
        legend=dict(
            title=label_dict[array2],
            yanchor="bottom",
            y= .9,
            xanchor="center",
            x=0)
        )
    
    fig.show(config={'displayModeBar': False})
    
    return fig

# used in introduction to demonstrate the frequency distribution of survey respondents
intro_chart1 = frequency_chart(demographics[0], policy[2])


"""
Dash app

"""

app = dash.Dash(__name__, assets_ignore='.*bootstrap-journal.css.*')

layout = html.Div([
    dbc.Container([
        dbc.NavbarSimple(
            children=[
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("Page 2", href="#"),
                    dbc.DropdownMenuItem("Page 3", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="Science and Society",
        brand_href="#",
        color="primary",
        dark=True,
        fluid=True
        )
    ]),

    dbc.Container([
        dbc.Row([
            dbc.Col(
                [html.H4("Introduction"),
                 html.P("""\
                 In 2019, the Pew Research Center conducted a survey of 4,464 adults living in households
                 in the United States. Part of their American Trends Panel, the survey measured respondent
                 attitudes regarding a number of topics, from trust in researchers and the scientific process
                 to whether or not scientists should be involved with guiding public policy decisions.
                 This dashboard's purpose is to provide the user with the ability to examine theses trends themselves.
                """)
                ],
                lg=8,
            )
        ]),
        dbc.Row([
            dbc.Col(
                [html.H2("Highlighted Graphs"),
                dcc.Graph(
                    figure=example_graph1,
                    config={'displayModeBar': False}
                )],
                lg=6,
            )
        ]),
    ]),

    html.Div([
        dbc.Container([
                dcc.Dropdown(
                    id = 'xaxis-column',
                    options = demo_dropdown,
                    value = 'F_AGECAT'
                ),
                dcc.Dropdown(
                    id = 'yaxis-column',
                    options = policy_dropdown,
                    value = 'POLICY1_W42'
                ),
                html.Div([dcc.Graph(id='indicator-bar',
                                   config={'displayModeBar': False})
                         ])
        ]),

    ]),
])


app.layout = layout

@app.callback(
    Output('indicator-bar', 'figure'),
    [Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value')])
def update_graph(x_axis, y_axis):
    new_df = pd.crosstab(df_copy[x_axis],
                         df_copy[y_axis],
                         df_copy.WEIGHT_W42, aggfunc = sum, dropna=True,
                         normalize='index'). \
                         loc[meta.variable_value_labels[x_axis].values()]. \
                         loc[:, meta.variable_value_labels[y_axis].values()]*100
    
    fig = px.bar(new_df, x=new_df.columns, y=new_df.index )

    fig.update_layout(
        title={
            'text': label_dict[y_axis],
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font':{
                'size':18}},
        
        margin=dict(l=20, r=20, t=20, b=20),
        
        xaxis_title="Frequency (%)",
        yaxis_title=None,
        legend=dict(
            title=None,
            yanchor="top",
            y= .9,
            xanchor="right",
            x=0
        ))
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)