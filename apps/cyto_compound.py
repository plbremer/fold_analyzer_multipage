
import dash_bootstrap_components as dbc
from dash import html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
from dash import callback_context

from itertools import chain
import networkx as nx
import pathlib
import json
from pprint import pprint
import fnmatch

from app import app

cyto.load_extra_layouts()

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

compound_json_address=DATA_PATH.joinpath('cyto_format_compound.json')
temp_json_file=open(compound_json_address,'r')
compound_network_dict=json.load(temp_json_file)
temp_json_file.close()
for temp_element in compound_network_dict['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    try:
        temp_element['data']['label']='Bin: '+temp_element['data']['common_name']
    except KeyError:
        temp_element['data']['label']=temp_element['data']['name']
    
    temp_element['classes']='not_selected'


stylesheet=[
    {
        'selector':'node',
        'style':{
            'content':'data(label)',
            'text-wrap':'wrap',
            'text-max-width':100,
            'font-size':13
        }
        
    },
    # {
    #     'selector':'.selected',
    #     'style':{
    #         'background-color':'red'
    #     }
    # }
    #'text-wrap':'wrap'
    {
        'selector':'.selected',
        'style':{
            'background-color':'red'
        }
    },
    {
        'selector':'.not_selected',
        'style':{
            'background-color':'grey'
        }
    }
]

networkx_address=DATA_PATH.joinpath('compounds_networkx.bin')
networkx=nx.readwrite.gpickle.read_gpickle(networkx_address)

layout=html.Div(
    children=[
        dbc.Row(
            dbc.Col(
                children=[
                    html.Button('add compound cyto', id='button_add_cyto_compound', n_clicks=0),
                ],
                width='auto',
                align='center'
            )
        ),
        html.Div(
            id='div_cytoscape_compound_cyto',
            children=[]
        ),
        html.Div(    
            children=[
                dbc.Row(
                    dbc.Col(
                        children=[
                            html.Button('bs button', id='bs button', n_clicks=0),
                        ],
                        width='auto',
                        align='center'
                    )
                ),
            ]
        ),
    ]
)



@app.callback(
    [Output(component_id='div_cytoscape_compound_cyto',component_property='children')],
    #gets n_clicks=0 when app loads, thats why you get a cyto right off the bat
    [Input(component_id='button_add_cyto_compound',component_property='n_clicks')],
    [State(component_id='div_cytoscape_compound_cyto',component_property='children'),
    State(component_id='store_cyto_compound',component_property='data')],prevent_initial_callback=True
)
def add_cyto_compound(temp_n_clicks,temp_children,temp_store):

    if (callback_context.triggered[0]['prop_id']=='.'):
        for i,element in enumerate(temp_store):
            new_graph=dbc.Row(
                dbc.Col(
                    dbc.Card(
                        children=[
                            #compounds
                            cyto.Cytoscape(
                                id={
                                    'type':'cytoscape_compound',
                                    'key':i
                                },
                                layout={'name':'dagre'},
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


    #if (callback_context.triggered[0]['prop_id']=='.'):

    elif (callback_context.triggered[0]['prop_id']=='button_add_cyto_compound.n_clicks'):
        temp_children.append(new_graph)

    return [temp_children]

@app.callback(
    [Output(component_id={'type':'cytoscape_compound','key':MATCH},component_property='elements')],
    [Input(component_id={'type':'cytoscape_compound','key':MATCH},component_property='tapNodeData')],
    #Input(component_id='button_add_cyto_compound',component_property='n_clicks')],
    #Input(component_id='Compounds',component_property='href')],
    [State(component_id={'type':'cytoscape_compound','key':MATCH},component_property='elements'),
    State(component_id='store_cyto_compound',component_property='data')]#,prevent_initial_call=True
)
def update_node_selection(temp_tap,temp_elements,temp_store):

    if temp_tap is None:
        raise PreventUpdate

    elif callback_context.triggered[0]['prop_id']=='.':
        raise PreventUpdate

    try:
        child_nodes_and_self=nx.algorithms.dag.descendants(networkx,temp_tap['id'])
    except nx.NetworkXError:
        child_nodes_and_self=set()

    child_nodes_and_self.add(temp_tap['id'])

    child_nodes_and_self=set(map(str,child_nodes_and_self))

    for temp_node in temp_elements['nodes']:

        if temp_node['data']['id'] in child_nodes_and_self:


            if temp_node['classes']=='selected':
                temp_node['classes']='not_selected'
            elif temp_node['classes']=='not_selected':
                temp_node['classes']='selected'

    return [temp_elements]


def check_if_selected(temp_dict):

    if temp_dict['classes']=='selected':
        return str(temp_dict['data']['id'])


@app.callback(
    [Output(component_id='store_cyto_compound',component_property='data')],
    [Input(component_id={'type':'cytoscape_compound','key':ALL},component_property='elements')],
    [State(component_id='store_cyto_compound',component_property='data')]
    ,prevent_initial_call=True
)
def add_selections_to_store(temp_elements,temp_store):

    

    print('\nadd_selections_to_store')
    print(callback_context.triggered[0]['prop_id'])
    #print(temp_elements)

    if callback_context.triggered[0]['prop_id']=='.':
        raise PreventUpdate

    selected_ids_list=[list(map(check_if_selected,temp_cyto_dict['nodes'])) for temp_cyto_dict in temp_elements]

    
    return [selected_ids_list]


'''
@app.callback(
    [Output(component_id='bs button',component_property='n_clicks')],
    [Input(component_id='page_content',component_property='children')]
)
def display_page(temp_pathname):
    print('in bs button')
'''