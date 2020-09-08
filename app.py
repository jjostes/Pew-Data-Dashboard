# load data
fpath = 'data/ATP W42.sav'

df, meta = pyreadstat.read_sav(fpath)

df_copy = pyreadstat.pyreadstat.set_value_labels(df, meta)


""" 
data cleaning, transformation

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
pw_form2 = list_helper('PQ')
scm4 = list_helper('SCM4')
scm5 = list_helper('SCM5')
q = [i for i in df.columns if re.search("^Q[0-9]", i)] #regex to grab Q6, Q7, etc.
pop = list_helper('POP')
knowledge = list_helper('KNOW')
demographics = list_helper('F_')
weight = ['WEIGHT_W42']


# dictionary of column names to be used with the dcc.Dropdown() property 'options'
policy_dropdown = [{'label': v, 'value': k} for k,v in label_dict.items() if k in policy]

demo_dropdown = [{'label': v, 'value': k} for k,v in label_dict.items() if k in demographics]


# creating labels to be used with dropdown menu
theme_categories = ['Social impact of scientific developments',
                    'Policy decisions on scientific issues',
                    'Confidence in public figures',
                    'Opinions on Medical, Environmental & Nutrition research scientists',
                    'Opinions on Medical Doctors, Environmental Health Specialists & Dieticians',
                    'Importance of scientific issues',
                    'Opinions on research scientists',
                    'Questions regarding scientific research',
                    'Solving the countires problems',
                    'General scientific knowledge']

theme_labels = [society, policy, confidence, rq_form1, pw_form2, scm4, scm5, q, pop, knowledge]

theme_select_dropdown = dict(zip(theme_categories, theme_labels))


"""
Dash app

"""

app = dash.Dash(__name__, assets_ignore='.*bootstrap-journal.css.*')

layout = html.Div([
    dbc.Container([
            dbc.NavbarSimple(
                brand="Science and Society",
                brand_href="#",
                color="primary",
                dark=True,
                fluid=True
            ),
            html.Br(),
        
            html.Div([
                html.H4(children=['Introduction'], style={'font-family':'sans-serif'}),
                html.Hr(),
                html.P("""\
                In 2019, the Pew Research Center conducted a survey of 4,464 adults living in households
                in the United States. Part of their American Trends Panel, the survey measured respondent
                attitudes regarding a number of topics, from trust in researchers and the scientific process
                to whether or not scientists should be involved with guiding public policy decisions.
                This dashboard's purpose is to provide the user with the ability to examine theses trends for .themselves.
                """)
            ],
                style={'background-color':'rgba(229, 237, 250, 0.5', 'padding': '5px'}
            ),
            html.Br(),

        
            html.Br(),
            html.H4(children=['Exploring by demographic']),
            html.Hr(),
            
            html.Div([
                html.P('''\
                The following frequency distributions represent the proportion of answers given by a particular demographic.
                Age category is provided as the default. The topics, or themes, covered by the survey were pre-grouped according to 
                general similarities determined by the researchers, and within each group specific survey items can be selected.
                \n \n
                Note: DK/REF stands for didn't know / refused to respond.
                ''')
            ]),
            
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.H6(children=['Please choose a demographic'], style={'font-family':'sans-serif'}),
                        dcc.Dropdown(
                            id = 'xaxis-column',
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
                        html.H6(children=['Please choose a theme'], style={'font-family':'sans-serif'}),
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
                        dcc.RadioItems(id='yaxis-column',
                                      value = 'PAST_W42')
                    ]),
                ]),
                
                dbc.Row([
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    dbc.Col([
                        dcc.Graph(id='indicator-bar',
                                  config={'displayModeBar': False}
                        )
                    ])
                ])
            ]),
        dbc.Row([
            dbc.Col(
                [html.H5(children=['A note on the data'], style={'font-family':'sans-serif'}),
                 html.P("""\
                 Weighted values are used to better represent the distribution of sociodemographic characteristics in 
                 the U.S. population. If not taken into account, the following tables and charts could over- or underrepresent
                 a given demographic's response. The graphs below provide a quick illustration of this. (Weights were provided in the original dataset.)
                 """)
                ],
                    lg=12,
            )
        ])
    ])

],
style={'background-color:': 'rgba(197, 220, 235, 0.9)',
       'margin':'2rem'}
)


app.layout = layout


@app.callback(
    Output('yaxis-column', 'options'),
    [Input('theme-selection', 'value')]
)
def set_theme_options(selected_theme):
        temp = [i for i in theme_select_dropdown[selected_theme]]
        temp_list = [{'label': label_dict[i], 'value': i} for i in temp]
        
        return temp_list



@app.callback(
    Output('indicator-bar', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value')]
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