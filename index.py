from dash import dcc
from dash import html
from dash.dependencies import Input, Output
#had to import cyto here to use dagre...?
#import dash_cytoscape as cyto
#cyto.load_extra_layouts()

import dash_bootstrap_components as dbc
from dash import callback_context

# Connect to main app.py file
from app import app
#from app import server
from apps import cyto_compound
from apps import backend_dataset
from apps import additional_filters

#import dash_cytoscape as cyto
#cyto.load_extra_layouts()


app.layout = html.Div(
    [
        #storage_type='session',
        dcc.Store(id='store_cyto_compound'),
        
        dbc.Row(
            #for the moment, we put all in one column
            #but maybe later put in separate columns
            #just put one of each link into a different column
            dbc.Col(
                html.Div(
                    #id='link_list',
                    children=[
                        dcc.Location(id='url',pathname='',refresh=False),
                        dcc.Link('Compounds',href='/apps/cyto_compound'),
                        dcc.Link('Backend Dataset',href='/apps/backend_dataset'),
                        dcc.Link('Additional Filters',href='/apps/additional_filters')
                    ]
                ),

            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    id='page_content',
                    children=[]
                )
            )
        )
    ]
)

@app.callback(
    [Output(component_id='page_content',component_property='children')],
    [Input(component_id='url',component_property='pathname')]
)
def display_page(temp_pathname):
    if temp_pathname == '/apps/cyto_compound':
        #print('\n in link chooser')
        #print(callback_context.triggered)
        
        return [cyto_compound.layout]
    elif temp_pathname == '/apps/backend_dataset':
        return [backend_dataset.layout]
    elif temp_pathname == '/apps/additional_filters':
        return [additional_filters.layout]


    else:
        return 'under construction'


    # @dcc.Location(id='url', refresh=False),
    # html.Div([
    #     dcc.Link('Video Games|', href='/apps/vgames'),
    #     dcc.Link('Other Products', href='/apps/global_sales'),
    # ], className="row"),
    #    html.Div(id='page-content', children=[])
#])

'''
app.layout=html.Div(
    [
        #title
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        #a header
                        html.H1('Binvestigate Fold Analyzer'),
                        html.Br(),
                        html.Br(),
                        html.Br()
                    ]
                ),
                width='auto',
            ),
            justify='center'
        ),
'''

if __name__ == '__main__':
    app.run_server(debug=True)