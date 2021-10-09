
import dash_bootstrap_components as dbc
from dash import html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State, ALL

import pathlib
import json
from pprint import pprint

from app import app


cyto.load_extra_layouts()

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()



compound_json_address=DATA_PATH.joinpath('cyto_format_compound.json')
temp_json_file=open(compound_json_address,'r')
compound_network_dict=json.load(temp_json_file)
temp_json_file.close()
#the point of this is to add a property that we display.
##we could preprocess this once if we so desired
for temp_element in compound_network_dict['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    try:
        temp_element['data']['label']='Bin: '+temp_element['data']['common_name']
    except KeyError:
        temp_element['data']['label']=temp_element['data']['name']
    
    ##temp_element['selectable']=True
    ##temp_element['classes']='not_selected'
    #temp_element['data']['label']=replace_space_with_newline(temp_element['data']['label'])


stylesheet=[
    {
        'selector':'node',
        'style':{
            'content':'data(label)',
            'text-wrap':'wrap',
            'text-max-width':100,
            'font-size':13
        }
        
    }
    # {
    #     'selector':'.selected',
    #     'style':{
    #         'background-color':'red'
    #     }
    # }
    #'text-wrap':'wrap'
]





layout=html.Div(
    children=[
        dbc.Row(
            dbc.Col(
                #html.Div(
                children=[
                    html.Button('add compound cyto', id='button_add_cyto_compound', n_clicks=0),
                ],
                #),
                width='auto',
                align='center'
            )
        ),
        #dbc.Row(
        #    dbc.Col(
        #        children=[

        #        ]
        #    )
        #)
        html.Div(
            id='div_cytoscape_compound_cyto',
            children=[]
        )

    ]
)

        # dbc.Row(
        #     dbc.Col(
        #         dbc.Card(
        #             children=[
        #                 #compounds
        #                 cyto.Cytoscape(
        #                     id='cytoscape_compound',
        #                     layout={'name':'breadthfirst'},
        #                     elements=compound_network_dict['elements'],
        #                     stylesheet=stylesheet,
        #                     minZoom=0.3,
        #                     maxZoom=5
        #                 )
        #             ]
        #         ),
        #         width='auto',
        #         align='center'
        #     )

        # )

@app.callback(
    [Output(component_id='div_cytoscape_compound_cyto',component_property='children')],
    #gets n_clicks=0 when app loads, thats why you get a cyto right off the bat
    [Input(component_id='button_add_cyto_compound',component_property='n_clicks')],
    [State(component_id='div_cytoscape_compound_cyto',component_property='children')]
)
def add_cyto_compound(temp_n_clicks,temp_children):

    #pprint(temp_children)
    
    new_graph=dbc.Row(
        dbc.Col(
            dbc.Card(
                children=[
                    #compounds
                    cyto.Cytoscape(
                        id={
                            'type':'cytoscape_compound',
                            'key':temp_n_clicks
                        },
                        layout={'name':'breadthfirst'},
                        elements=compound_network_dict['elements'],
                        stylesheet=stylesheet,
                        minZoom=0.3,
                        maxZoom=5
                    )
                ]
            ),
            width='auto',
            align='center'
        )
    )

    temp_children.append(new_graph)

    return [temp_children]

@app.callback(
    [Output(component_id='store_cyto_compound',component_property='data')],
    [Input(component_id={'type':'cytoscape_compound','key':ALL},component_property='tapNodeData')],
    [State(component_id='store_cyto_compound',component_property='data')]
)
def test_store(temp_tap,temp_state):
    print('--------')
    print(temp_tap)
    print(temp_state)