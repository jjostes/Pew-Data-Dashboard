import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.Br(),
    
    html.H4('Dataset (an account is required to download)'),
    html.Ul(
        html.Li(
            dcc.Link('Pew Research Center, American Trends Panel 42', 
                     href='https://www.pewresearch.org/science/dataset/american-trends-panel-wave-42/',
                     target='_blank')
        )
    ),
    
    html.Hr(),
    
    html.H4('Releases from this survey'),
    html.Ul([
        html.Li(
            dcc.Link('Most Americans are wary of industry-funded research', 
                     href='https://tinyurl.com/y2ywl8l3',
                     target='_blank')
        ),
        
        html.Li(
            dcc.Link('Most Americans say science has brought benefits to society and expect more to come',
                     href='https://tinyurl.com/yyzojwqw',
                     target='_blank')
        ),
        
        html.Li(
            dcc.Link('Most Americans have positive image of research scientists, but fewer see them as good communicators', 
                     href='https://tinyurl.com/y6bngclv',
                     target='_blank')
        ),
        
        html.Li(
            dcc.Link('Democrats and Republicans differ over role and value of scientists in policy debates',
                     href='https://tinyurl.com/yct9ep43',
                     target='_blank')
        ),
        
        html.Li(
            dcc.Link('5 key findings about public trust in scientists in the U.S.',
                     href='https://tinyurl.com/yxqc7ezb',
                     target='_blank')
        ),
        
        html.Li(
            dcc.Link('Science knowledge varies by race and ethnicity in U.S.',
                     href='https://tinyurl.com/yxmdobwj',
                     target='_blank')
        ),
        
        html.Li(
            dcc.Link('Trust and mistrust in Americans\' view of scientific experts',
                     href='https://tinyurl.com/y5yrplfr',
                     target='_blank')
        ),
        
        html.Li(
            dcc.Link('What Americans know about science',
                     href='https://tinyurl.com/y33n2bof',
                     target='_blank')
        ),

        html.Hr(),
        
        html.Li(
            dcc.Link('Github Repository',
                     href='https://github.com/jjostes/Pew-Data-Dashboard',
                     target='_blank')
        )
        
    ])

])