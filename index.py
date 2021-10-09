from dash import dcc
from dash import html
from dash.dependencies import Input, Output
#had to import cyto here to use dagre...?
#import dash_cytoscape as cyto
#cyto.load_extra_layouts()

import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
#from app import server
from apps import cyto_compound

#import dash_cytoscape as cyto
#cyto.load_extra_layouts()


app.layout = html.Div(
    [
        dcc.Store(id='store_cyto_compound',data={}),
        
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
                        dcc.Link('Backend Dataset',href='/apps/backend_dataset')
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
        return [cyto_compound.layout]
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