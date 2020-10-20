from app import app
from app import server
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import pyreadstat
import re



# load data
fpath = 'data/ATP W42.sav'

df, meta = pyreadstat.read_sav(fpath)

df_copy = pyreadstat.pyreadstat.set_value_labels(df, meta)


""" 
-----------------------------
DATA CLEANING, TRANSFORMATION
-----------------------------
"""

# regular expression that matches with every character up until the first whitespace character.
pattern = re.compile(r'.+?\.\s?')

label_dict = {}

for key, value in meta.column_names_to_labels.items():
    label_dict[key] = re.sub(pattern=pattern, string=value, repl=' ')

    
# helper function used to sort survey items according to thematic subject matter code (e.g. starts with 'RQ')
def list_helper(theme_code):
    return [i for i in df.columns if theme_code in i]


society = ['PAST_W42', 'FUTURE_W42', 'SC1_W42']
policy = list_helper('POLICY')
confidence = list_helper('CONF')
rq_form1 = list_helper('RQ')
pq_form2 = list_helper('PQ')
scm4 = list_helper('SCM4')
scm5 = list_helper('SCM5')
q = [i for i in df.columns if re.search("^Q[0-9]", i)] #regex to grab Q6, Q7, etc.
pop = list_helper('POP')
knowledge = list_helper('KNOW')
demographics = list_helper('F_')
weight = ['WEIGHT_W42']


# dictionary of column names to be used with the dcc.Dropdown() property 'options'
demo_dropdown = [{'label': v, 'value': k} for k,v in label_dict.items() if k in demographics]



# labels that are then zipped with column names, to be used as a dictionary for dcc.Dropdown
theme_categories = ['Social impact of scientific developments',
                    'Policy decisions on scientific issues',
                    'Confidence in public figures',
                    'Importance of scientific issues',
                    'Opinions on research scientists',
                    'Questions regarding scientific research',
                    'Solving the countires problems',
                    'General scientific knowledge']

theme_names = [society, policy, confidence, scm4, scm5, q, pop, knowledge]
theme_select_dropdown = dict(zip(theme_categories, theme_names))


# same as above
researchers_cat = ['Medical Research Scientists', 
                   'Environmental Research Scientists', 
                   'Nutrition Research Scientists']

med_scientists = [i for i in rq_form1 if re.search("(_F1A)", i)]
env_scientists = [i for i in rq_form1 if re.search("(_F1B)", i)]
nutr_scientists = [i for i in rq_form1 if re.search("(_F1C)", i)]

research_names = [med_scientists, env_scientists, nutr_scientists]
res_dropdown = dict(zip(researchers_cat, research_names))

#same as above
practitioners_cat = ['Medical Doctors', 
                     'Environmental Health Specialists', 
                     'Dietician']

md = [i for i in pq_form2 if re.search("(_F2A)", i)]
env_specialists = [i for i in pq_form2 if re.search("(_F2B)", i)]
dieticians = [i for i in pq_form2 if re.search("(_F2C)", i)]

pract_names = [md, env_specialists, dieticians]
pract_dropdown = dict(zip(practitioners_cat, pract_names))


""" 
--------------------------------------
DASH APP: LAYOUT, TABS, CALLBACKS
--------------------------------------
"""

app = JupyterDash(__name__, assets_ignore='.*bootstrap-journal.css.*')


""" 
------
LAYOUT
------
"""

app.layout = html.Div([
    dbc.Container([
        
# Navbar
        dbc.NavbarSimple(
            brand="Science and Society [In Development]",
            brand_href="#",
            color="primary",
            dark=True,
            fluid=True
        ),
        html.Br(),

# Intro
        html.Div([
            html.H4(children=['Introduction'], style={'font-family':'sans-serif'}),
            html.Hr(),
            html.P("""\
            In 2019, the Pew Research Center conducted a survey of 4,464 adults living within households
            in the United States. Part of their American Trends Panel, the survey measured respondent
            attitudes regarding a number of topics, from trust in researchers and the scientific process
            to whether or not scientists should be involved with guiding public policy decisions.
            This dashboard's purpose is to provide the user with the ability to examine theses trends for themselves.
            """)
        ],
            style={'background-color':'rgba(229, 237, 250, 0.5', 'padding': '5px'}
        ),
        html.Br(),

        html.H4(children=['Exploring by demographic']),
        html.Hr(),

        html.Div([
            html.P('''\
            The following frequency distributions represent the proportion of answers given by a particular demographic.
            Age category is provided as the default. The themes covered by the survey were pre-grouped according to 
            general similarities determined by the researchers, and within each group specific survey items can be selected.
            '''),
            html.P(html.Em('''
            Survey items regarding researchers (medical, environmental, nutrition) and practitioners 
            (doctors, env. health specialists, dieticians) have been separated into their own tabs to
            help simplify the options menu.
            ''')),
            html.P('Note: DK/REF stands for didn\'t know / refused to respond.')
        ]),

# Tabs

        html.Div([
            dbc.Tabs(
                [
                    dbc.Tab(label='Main', tab_id='tab-1'),
                    dbc.Tab(label='Researchers', tab_id='tab-2'),
                    dbc.Tab(label='Practitioners', tab_id='tab-3')
                ],
                id="tabs",
                active_tab="tab-1",
                ),
            html.Div(id="content"),
        ]),
        html.Br(),
        
        html.Div([
            dbc.Col(
                [html.Em(children=['A note on the data'], style={'font-family':'sans-serif'}),
                 html.P("""\
                 Weighted values are used to better represent the distribution of sociodemographic characteristics in 
                 the U.S. population. If not taken into account, the following tables and charts could over- or underrepresent
                 a given demographic's response.
                 """)
                ],
                    lg=12,
            )
        ]),
        html.Br(),
    ])
],
style={'background-color:': 'rgba(197, 220, 235, 0.9)',
       'margin':'2rem'}
)


""" 
-----
TAB 1
-----
"""

tab1_content = html.Div([
        html.Br(),
       
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.H6(children=['Demographic'], style={'font-family':'sans-serif'}),
                    dcc.Dropdown(
                        id = 'xaxis-column1',
                        options = demo_dropdown,
                        value = 'F_AGECAT'
                    )
                ],
                    lg=8
                )
            ]),
            html.Br(),

            dbc.Row([
                dbc.Col([
                    html.H6(children=['Theme'], style={'font-family':'sans-serif'}),
                    dcc.Dropdown(
                        id = 'theme-selection',
                        options = [{'label': k, 'value': k} for k in theme_select_dropdown.keys()],
                        value = 'Social impact of scientific developments'
                    )
                ],
                    lg=8)
            ]),
            html.Br(),

            dbc.Row([
                 dbc.Col([
                    dcc.RadioItems(id='yaxis-column1',
                                  value = 'PAST_W42')
                ]),
            ]),

            dbc.Row([
                html.Br(),
                html.Br(),
                html.Br(),

                dbc.Col([
                    dcc.Graph(id='indicator-bar1',
                              config={'displayModeBar': False}
                    )
                ])
            ])
        ])
])


""" 
-----
TAB 2
-----
"""

tab2_content = html.Div([
        html.Br(),

        html.Div([
            dbc.Row([
                dbc.Col([
                    html.H6(children=['Please choose a demographic'], style={'font-family':'sans-serif'}),
                    dcc.Dropdown(
                        id = 'xaxis-column2',
                        options = demo_dropdown,
                        value = 'F_AGECAT'
                    )
                ],
                    lg=8
                )
            ]),
            html.Br(),

            dbc.Row([
                dbc.Col([
                    html.H6(children=['Researcher'], style={'font-family':'sans-serif'}),
                    dcc.Dropdown(
                        id = 'researcher-selection',
                        options = [{'label': k, 'value': k} for k in res_dropdown.keys()],
                        value = 'Medical Research Scientists'
                    )
                ],
                    lg=8)
            ]),
            html.Br(),

            dbc.Row([
                 dbc.Col([
                    dcc.RadioItems(id='yaxis-column2',
                                  value = 'RQ1_F1A_W42')
                ]),
            ]),

            dbc.Row([
                html.Br(),
                html.Br(),
                html.Br(),

                dbc.Col([
                    dcc.Graph(id='indicator-bar2',
                              config={'displayModeBar': False}
                    )
                ])
            ])
        ])
])


""" 
-----
TAB 3
-----
"""

tab3_content = html.Div([
        html.Br(),

        html.Div([
            dbc.Row([
                dbc.Col([
                    html.H6(children=['Please choose a demographic'], style={'font-family':'sans-serif'}),
                    dcc.Dropdown(
                        id = 'xaxis-column3',
                        options = demo_dropdown,
                        value = 'F_AGECAT'
                    )
                ],
                    lg=8
                )
            ]),
            html.Br(),

            dbc.Row([
                dbc.Col([
                    html.H6(children=['Practitioner'], style={'font-family':'sans-serif'}),
                    dcc.Dropdown(
                        id = 'practitioner-selection',
                        options = [{'label': k, 'value': k} for k in pract_dropdown.keys()],
                        value = 'Medical Doctors'
                    )
                ],
                    lg=8)
            ]),
            html.Br(),

            dbc.Row([
                 dbc.Col([
                    dcc.RadioItems(id='yaxis-column3',
                                  value = 'PQ1_F2A_W42')
                ]),
            ]),

            dbc.Row([
                html.Br(),
                html.Br(),
                html.Br(),

                dbc.Col([
                    dcc.Graph(id='indicator-bar3',
                              config={'displayModeBar': False}
                    )
                ])
            ])
        ])
])


""" 
----------------
LAYOUT CALLBACKS
----------------
"""

# Switch tabs
@app.callback(
    Output('content', 'children'),
    [Input('tabs', 'active_tab')]
)
def switch_tab(at):
    if at == 'tab-1':
        return tab1_content
    elif at == 'tab-2':
        return tab2_content
    elif at == 'tab-3':
        return tab3_content
    return html.P("This shouldn't ever be displayed...")

""" 
---------------
TAB 1 CALLBACKS
---------------
"""
@app.callback(
    Output('yaxis-column1', 'options'),
    [Input('theme-selection', 'value')]
)
def set_theme_options(selected_theme):
        temp = [i for i in theme_select_dropdown[selected_theme]]
        temp_list = [{'label': label_dict[i], 'value': i} for i in temp]
        
        return temp_list


@app.callback(
    Output('indicator-bar1', 'figure'),
    [Input('xaxis-column1', 'value'),
     Input('yaxis-column1', 'value')]
)
def update_graph(x_axis, y_axis):
        new_df = pd.crosstab(df_copy[x_axis],
                             df_copy[y_axis],
                             df_copy.WEIGHT_W42, aggfunc = sum, dropna=True,
                             normalize='index'). \
                             loc[meta.variable_value_labels[x_axis].values()]. \
                             loc[:, meta.variable_value_labels[y_axis].values()]*100

        fig = px.bar(new_df, x=new_df.columns, y=new_df.index)

        fig.update_layout(
            font={'size':15},
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="Frequency (%)",
            yaxis_title=None,
            
            legend=dict(
                font=dict(size=16),
                title=None,
                yanchor="top",
                y=1.5,
                xanchor="left",
                x=0.01)
        ),
        
        fig.update_layout(
            hoverlabel = dict(
                bgcolor="white", 
                font_size=14, 
                font_family="sans-serif"
            )
        )

        return fig
    
""" 
---------------
TAB 2 CALLBACKS
---------------
"""
@app.callback(
    Output('yaxis-column2', 'options'),
    [Input('researcher-selection', 'value')]
)
def set_theme_options(selected_theme):
        temp = [i for i in res_dropdown[selected_theme]]
        temp_list = [{'label': label_dict[i], 'value': i} for i in temp]
        
        return temp_list

    
@app.callback(
    Output('indicator-bar2', 'figure'),
    [Input('xaxis-column2', 'value'),
     Input('yaxis-column2', 'value')]
)
def update_graph(x_axis, y_axis):
        new_df = pd.crosstab(df_copy[x_axis],
                             df_copy[y_axis],
                             df_copy.WEIGHT_W42, aggfunc = sum, dropna=True,
                             normalize='index'). \
                             loc[meta.variable_value_labels[x_axis].values()]. \
                             loc[:, meta.variable_value_labels[y_axis].values()]*100

        fig = px.bar(new_df, x=new_df.columns, y=new_df.index)

        fig.update_layout(
            font={'size':15},
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="Frequency (%)",
            yaxis_title=None,
            
            legend=dict(
                font=dict(size=16),
                title=None,
                yanchor="top",
                y=1.5,
                xanchor="left",
                x=0.01)
        ),
        
        fig.update_layout(
            hoverlabel = dict(
                bgcolor="white", 
                font_size=14, 
                font_family="sans-serif"
            )
        )

        return fig

""" 
---------------
TAB 3 CALLBACKS
---------------
"""
@app.callback(
    Output('yaxis-column3', 'options'),
    [Input('practitioner-selection', 'value')]
)
def set_theme_options(selected_theme):
        temp = [i for i in pract_dropdown[selected_theme]]
        temp_list = [{'label': label_dict[i], 'value': i} for i in temp]
        
        return temp_list

    
@app.callback(
    Output('indicator-bar3', 'figure'),
    [Input('xaxis-column3', 'value'),
     Input('yaxis-column3', 'value')]
)
def update_graph(x_axis, y_axis):
        new_df = pd.crosstab(df_copy[x_axis],
                             df_copy[y_axis],
                             df_copy.WEIGHT_W42, aggfunc = sum, dropna=True,
                             normalize='index'). \
                             loc[meta.variable_value_labels[x_axis].values()]. \
                             loc[:, meta.variable_value_labels[y_axis].values()]*100

        fig = px.bar(new_df, x=new_df.columns, y=new_df.index)

        fig.update_layout(
            font={'size':15},
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="Frequency (%)",
            yaxis_title=None,
            
            legend=dict(
                font=dict(size=16),
                title=None,
                yanchor="top",
                y=1.5,
                xanchor="left",
                x=0.01)
        ),
        
        fig.update_layout(
            hoverlabel = dict(
                bgcolor="white", 
                font_size=14, 
                font_family="sans-serif"
            )
        )

        return fig



if __name__ == '__main__':
    app.run_server(debug=True)