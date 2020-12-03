import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import pyreadstat

from apps import explore

fig1 = explore.make_freq_distr('F_EDUCCAT2', 'SCM5a_W42')
fig2 = explore.make_freq_distr('F_EDUCCAT2', 'SCM5f_W42')
fig3 = explore.make_freq_distr('F_EDUCCAT2', 'SCM5b_W42')
fig4 = explore.make_freq_distr('F_EDUCCAT2', 'SCM5g_W42')


layout = html.Div([
    dbc.Container([
        
        html.Br(),
        
        html.H4(children=['Introduction']),
        html.Hr(),
        
        html.P('''
            In 2019, the Pew Research Center conducted a survey of 4,464 adults living within households 
            in the United States. Part of their American Trends Panel, the survey measured respondent 
            attitudes regarding a number of topics, from trust in researchers and the scientific process 
            to whether or not scientists should be involved with guiding public policy decisions. 
            This dashboard's purpose is to provide the user with the ability to examine theses trends for themselves.
            '''
              ),
        html.P('The opinions expressed herein, including any implications for policy, are those of the author and not of Pew Research Center.')
    ]),
    
    dbc.Container([
        
        html.Hr(),
        html.Br(),
        
        html.H4(
            children=[
                'Example: In general, would you say each of the following statements describes most RESEARCH SCIENTISTS well?'
            ], 
            style={'font-size':'20px'}
        ),
        
        html.Br(),
        
        html.H5(children=['Intelligent'], style={'text-align':'center', 
                                                 'background-color':'rgba(229, 237, 250, 0.5',
                                                 'padding': '5px',
                                                 'font-size':'18px'}
               ),
        dcc.Graph(figure=fig1),
        html.Br(),

        html.H5(children=['Honest'], style={'text-align':'center', 
                                            'background-color':'rgba(229, 237, 250, 0.5',
                                            'padding': '5px',
                                            'font-size':'18px'}
               ),
        dcc.Graph(figure=fig2),
        html.Br(),
        
        html.H5(children=['Good communicators'], style={'text-align':'center', 
                                                        'background-color':'rgba(229, 237, 250, 0.5',
                                                        'padding': '5px',
                                                        'font-size':'18px'}
               ),
        dcc.Graph(figure=fig3),
        html.Br(),
        
        html.H5(children=['Skilled at working in teams'], style={'text-align':'center', 
                                                                 'background-color':'rgba(229, 237, 250, 0.5',
                                                                 'padding': '5px',
                                                                 'font-size':'18px'}
               ),
        dcc.Graph(figure=fig4),
        html.Br()
    ])
])