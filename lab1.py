## Lab1, Aug 29
#Labpartner: Karl




## Import Statements
from __future__ import print_function # (needed for python2 vs. python3)

import graphspace_utils
import json_utils

def str_rep(nodes, adj_mat):
    """
    helper function for print_mat which returns a string representation of the adjacency matrix
    """
    num_rows = len(nodes)
    top_str = ""
    current_str = ""
    total_str = ""
    i = 0
    
    top_str += "\t"
    while i < num_rows:
        top_str += nodes[i] + "\t"
        i += 1
    top_str += "\n"
    total_str += top_str
    
    for row in range(len(nodes)):
        current_str += nodes[row] + "\t"
        for n in adj_mat[row]:
            current_str += str(n) + "\t"
        current_str += "\n"
        total_str += current_str
        current_str = ""
    return total_str

    
def print_mat(nodes, adj_mat):
    """
    Prints the matrix in a nicely-formatted manner.
    Inputs: node names and adjacency matrix
    Returns: nothing
    """
    print(str_rep(nodes, adj_mat))

def get_edges(nodes, adj_mat):
    """
    returns a list of edges constructed from a list of nodes and an adjacency matrix
    """
    edge_ls = []
    for row_num in range(len(adj_mat)):
        current_node = nodes[row_num]
        for e in range(len(adj_mat[row_num])):
            if adj_mat[row_num][e] == 1:
                edge_ls.append([current_node, nodes[e]])
    return edge_ls


def getNodeAttributes(nodes):
    """
    Creates a dictionary of attributes for each node that corresponds to the GraphSpace API
    """
    attrs = {}
    for n in nodes:
        attrs[n] = {}
        attrs[n]['id'] = n
        attrs[n]['content'] = n
        attrs[n]['height'] = 60
        attrs[n]['width'] = 60
        print('Node Attribute for',n,':',attrs[n])
    return attrs

def customNodeAttributes(nodes):
    """
    Further modifies the node attributes
    """
    attrs = getNodeAttributes(nodes)
    attrs['A']['shape'] = 'star'
    attrs['A']['height'] = 600
    attrs['A']['width'] = 600
    attrs['A']['content'] = "Hello!"
    attrs['A']['background_color'] = "cyan"
    return attrs


def getEdgeAttributes(edges):
    """
    Creates a dictionary of attributes for each edge that corresponds to the GraphSpace API
    """
    attrs = {}
    for e in edges:
        source = e[0]
        target = e[1]
        if source not in attrs:
            attrs[source] = {}
        attrs[source][target] = {}
        attrs[source][target]['width'] = 2
        print('Edge Attribute for',source,'-',target,':',attrs[source][target])
    weird_edge = attrs['C']['D']
    weird_edge['line_style'] = 'dashed'
    weird_edge['target_arrow_shape'] = 'triangle-backcurve'
    weird_edge['width'] = 100
    weird_edge['line_color'] = 'magenta'
    return attrs


def upload_graph(nodes, adj_mat,GRAPHID,TITLE,TAGS=0,node_attrs=None,edge_attrs=None):
    """
    uploads the graph to the GraphSpace
    """
    if TAGS == 0:
        tag_ls = []
    else:
        tag_ls = TAGS
    edges = get_edges(nodes,adj_mat)
    #json_utils.test()
    data = json_utils.make_json_data(nodes,edges,node_attrs,edge_attrs,TITLE,'Desc.',tag_ls)
    json_utils.write_json(data,'lab1.json')
    graphspace_utils.postGraph(GRAPHID,'lab1.json','franzni@reed.edu','bio331')


def main(nodes,adj_mat):
    """
    Inputs to the main() function is a list of nodes and 
    a binary matrix of edges.  It will eventually post
    two graphs to GraphSpace.
    """
    ## print statements are now print FUNCTIONS (use parentheses)
    ## heads up to python 2.7 users.
    print('INPUTS:')
    print('nodes:',nodes)
    print('adj_mat:',adj_mat)    

    ## write your function calls here.
    print_mat(nodes,adj_mat)
    edges = get_edges(nodes,adj_mat)
    upload_graph(nodes,adj_mat,'lab1graph','Lab 1',['lab1'])
    node_attrs = getNodeAttributes(nodes)
    upload_graph(nodes,adj_mat,'lab1graphbigger','Lab 1', ['lab1'],node_attrs)
    node_attrs = customNodeAttributes(nodes)
    upload_graph(nodes,adj_mat,'lab1graphcustom','Lab 1', ['lab1'],node_attrs)
    edge_attrs = getEdgeAttributes(edges)
    upload_graph(nodes,adj_mat,'lab1-submission','Lab 1', ['lab1'],node_attrs,edge_attrs)
    graphspace_utils.shareGraph('lab1-submission','franzni@reed.edu','bio331','Lab1','aritz@reed.edu')
    return # done with main function

## start your functions here.





"""
 This is at the bottom of the file.  Once all functions are loaded, then 
 main() is called with nodes and adj_mat variables.
"""
if __name__ == '__main__':
    nodes = ['A','B','C','D','E','F']
    adj_mat = [[0,0,0,1,0,1],[1,0,0,0,1,0],[1,0,0,1,0,0],[0,1,1,0,0,0],[0,0,0,0,1,1],[0,1,1,0,0,0]]
    main(nodes,adj_mat)
