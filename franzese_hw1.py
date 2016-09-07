## Import Statements
from __future__ import print_function # (needed for python2 vs. python3)

import graphspace_utils
import json_utils


def get_txt_data(filename):
    """
    reads a matrix off of an input txt file and parses it into a list of node names and a list of rows of values, both of which are returned in an enveloping list.
    """
    ret = []
    with open(str(filename), 'r') as input:        #gets the list of node names from the first line
        first = input.readline()
        names = first.split('\t')[1:]
        #print(names) UNCOMMENT THIS FOR TESTING PLS THX #####
        ret.append(names)
    
    with open(str(filename), 'r') as input:         #gets the values of the matrix from the subsequent lines
        row_ls = []
        input.readline()
        current_line = input.readline()
        while current_line != "":
            values = current_line.split('\t')[1:]
            row_ls.append(values)
            current_line = input.readline()
        ret.append(row_ls)
    print(len(ret[0]))                              #prints the number of badgers
    return ret
            
    

def get_badger_data(filename):
    """
    reads BadgerInfo.txt and returns a dictionary that has badgers as keys, and an ordered list containing sex, infection status, and social group as each value.
    """
    dict = {}
    with open(str(filename), 'r') as input:
        input.readline()
        current_line = input.readline()
        while current_line != "":
            badger = current_line.split('\t')[0]
            info = current_line.split('\t')[1:]
            dict[badger] = info
    return dict
    
    
def make_simplified_adj_matrix(names, row_ls):
    """
    takes the data from get_txt_data() and returns an adjacency matrix with only 1's and 0's
    """
    new_matrix = []
    for row in row_ls:
        new_row = []
        for item in row:
            if item == '0':
                new_row.append(0)
            else:
                new_row.append(1)
        new_matrix.append(new_row)
    return new_matrix

def make_adj_list(names, row_ls):
    """
    takes the data from get_txt_data() and returns an adjacency list in the form of a dictionary
    """
    dict = {}
    for i in range(len(names)):
        key = names[i]
        vals = []
        for j in range(len(row_ls[i])):
            if row_ls[i][j] != '0':
                vals.append(names[j])
        dict[key] = vals
    return dict
    
def give_matrix_and_adj_list(names, row_ls):
    """
    question 2.2 asks for a function that returns an adjacency matrix and an adjacency list so this just runs both of the appropriate functions and returns them bundled into a list
    it also does: for each node print the number of neighbors and the list of neighbors as question 2.2 asks for
    """
    a = make_simplified_adj_matrix(names,row_ls)
    b = make_adj_list(names,row_ls)
    for badger in b:
        print(len(b[badger]))
        print(b[badger])
    return [a,b]
    

def is_adjmat_symmetric(matrix):
    """
    checks if the supplied adjacency matrix is symmetric. If symmetric, the function prints True and then returns True. Otherwise, the function prints False and then returns False.
    """
    sym = True
    if len(matrix) != len(matrix[0]):         #assesses whether the matrix is square. this assumes that all the rows have equal length because if they don't then the thing isn't a matrix.
        sym = False
        print(sym)
        return sym
    
    for i in range(len(matrix)):               #traverses each value in the matrix and checks whether matrix(i,j) ?= matrix(j,i)
        for j in range(len(matrix[i])):
            if matrix[i][j] != matrix[j][i]
                sym = False
    print(sym)
    return sym


    

    
    
    
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



    
    
def get_undirected_edges(nodes, adj_mat):
    """
    get edges function for an undirected graph (e.g. an edge (A,B) is the same edge as (B,A). This function will have no duplicate edges in its output.)
    """
    edge_set = set()
    for i in range(len(adj_mat)):
        current_node = nodes[i]
        for j in range(len(adj_mat[i])):
            if adj_mat[i][j] == 1:
                edge_set.add({current_node, nodes[j]})     #adds the edge as a set to the set of edges, which prevents duplicate edges from being added
    edge_ls = []
    for element in edge_set:
        edge_ls.append(set_to_list(element))
    return edge_ls
    
    
def set_to_list(set):
    """
    helper function for get_undirected_edges() which turns a set into a list containing all the elements that the input set contained.
    """
    ls = []
    for element in set:
        ls.append(element)
    return ls
    
    

def get_edges(nodes, adj_mat, directed=True):
    """
    returns a list of edges constructed from a list of nodes and an adjacency matrix
    """
    edge_ls = []
    if directed == True:
        for row_num in range(len(adj_mat)):
            current_node = nodes[row_num]
            for e in range(len(adj_mat[row_num])):
                if adj_mat[row_num][e] == 1:
                    edge_ls.append([current_node, nodes[e]])
        return edge_ls
    else:
        return get_undirected_edges(nodes, adj_mat)


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
