## Import Statements
from __future__ import print_function # (needed for python2 vs. python3)

import graphspace_utils
import json_utils
import math




###########################################
#DATA EXTRACTION FUNCTIONS#################
###########################################


def get_txt_data(filename):
    """
    reads a matrix off of an input txt file and parses it into a list of node names and a list of rows of values, both of which are returned in an enveloping list.
    """
    ret = []
    with open(str(filename), 'r') as input:        #gets the list of node names from the first line
        first = input.readline().strip('\n')
        names = first.split('\t')[1:]
        ret.append(names)
    
    with open(str(filename), 'r') as input:         #gets the values of the matrix from the subsequent lines
        row_ls = []
        input.readline()
        current_line = input.readline().strip('\n')
        while current_line != "":
            values = current_line.split('\t')[1:]
            row_ls.append(values)
            current_line = input.readline().strip('\n')
        ret.append(row_ls)
    #print(len(ret[0]))                              #prints the number of badgers
    return ret




def get_badger_data(filename):
    """
    reads BadgerInfo.txt and returns a dictionary that has badgers as keys, and an ordered list containing sex, infection status, and social group as each value.
    the three functions below this one access the ordered list to retrieve sex, infection status, and social group, providing an abstraction barrier.
    """
    dict = {}
    with open(str(filename), 'r') as input:
        input.readline()
        current_line = input.readline().strip('\n')
        while current_line != "":
            badger = current_line.split('\t')[0]
            info = current_line.split('\t')[1:]
            dict[badger] = info
            current_line = input.readline().strip('\n')
    return dict

def get_sex(info,badger):
    return info[badger][0]

def get_IS(info,badger):
    return info[badger][1]

def get_group(info,badger):
    return int(info[badger][2])








###########################################################
#DATA STRUCTURE FUNCTIONS##################################
###########################################################

    
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
    question 2.2 asks for a function that returns an adjacency matrix and an adjacency list so this just runs both of the appropriate functions and returns them as a bundle
    it also does: for each node print the number of neighbors and the list of neighbors as question 2.2 asks for
    """
    a = make_simplified_adj_matrix(names,row_ls)
    b = make_adj_list(names,row_ls)
    for badger in b:
        print(str(len(b[badger])) + " " + str(b[badger]))
    return a,b


def get_degree(adj_list,badger):
    """
    gets the number of neighbors for a given node
    """
    return len(adj_list[badger])


def get_undirected_edges(nodes, adj_mat):
    """
    get edges function for an undirected graph (e.g. an edge (A,B) is the same edge as (B,A). This function will have no duplicate edges in its output.)
    """
    edge_set = set()
    for i in range(len(adj_mat)):
        current_node = nodes[i]
        for j in range(len(adj_mat[i])):
            if adj_mat[i][j] == 1:
                edge_set.add(frozenset([current_node, nodes[j]]))     #adds the edge as a frozenset to the set of edges, which prevents duplicate edges from being added
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







##########################################################
#FUNCTIONS THAT ANSWER A HOMEWORK QUESTION################
##########################################################

def is_adjmat_symmetric(matrix):
    """
    checks if the supplied adjacency matrix is symmetric. If yes, returns True, else returns False
    """
    sym = True
    if len(matrix) != len(matrix[0]):         #assesses whether the matrix is square. this assumes that all the rows have equal length because if they don't then the thing isn't a matrix.
        sym = False
        return sym
    
    for i in range(len(matrix)):               #traverses each value in the matrix and checks whether matrix(i,j) ?= matrix(j,i)
        for j in range(len(matrix[i])):
            if matrix[i][j] != matrix[j][i]:
                sym = False
    return sym


def count_sex(info):
    """
    counts the badgers by sex and prints the results 
    """
    m = 0
    f = 0
    for badger in info:
        if get_sex(info,badger) == "Male":
            m += 1
        else:
            f += 1
    print("There are " + str(m) + " male badgers.")
    print("There are " + str(f) + " female badgers.")
    return

def count_IS(info):
    """
    counts the badgers by TB infection status and prints the results
    """
    p = 0
    n = 0
    for badger in info:
        if get_IS(info,badger) == 'P':
            p += 1
        else:
            n += 1
    print("There are " + str(p) + " TB positive badgers.")
    print("There are " + str(n) + " TB negative badgers.")
    return

def count_groups(info):
    """
    counts the badgers by clique number and prints the results
    """
    ls = []
    for i in range(0,8):
        ls.append(0)
    for badger in info:
        ls[get_group(info,badger)-1] += 1
    print("Population for social groups 1-8 in order:")
    print(ls)
    return
        






    
######################################################
#GRAPHSPACE FUNCTIONS#################################
######################################################


def upload_graph(nodes, adj_mat,GRAPHID,TITLE,TAGS=0,node_attrs=None,edge_attrs=None):
    """
    uploads the graph to the GraphSpace
    """
    if TAGS == 0:
        tag_ls = []
    else:
        tag_ls = TAGS
    edges = get_undirected_edges(nodes,adj_mat)
    #json_utils.test()
    data = json_utils.make_json_data(nodes,edges,node_attrs,edge_attrs,TITLE,'Desc.',tag_ls)
    json_utils.write_json(data,'hw1.json')
    graphspace_utils.postGraph(GRAPHID,'hw1.json','franzni@reed.edu','bio331')
    

    
def getNodeAttributes(nodes,info,badger_rows):
    """
    Creates a dictionary of attributes for each node that corresponds to the GraphSpace API
    """
    attrs = {}
    adj_ls = make_adj_list(nodes,badger_rows)
    for n in nodes:                                     #initializes and sets node size depending on degree
        attrs[n] = {}
        attrs[n]['id'] = n
        attrs[n]['content'] = n
        attrs[n]['height'] = get_degree(adj_ls,n) * 10
        attrs[n]['width'] = get_degree(adj_ls,n) * 10

        if get_sex(info,n) == "Male":                   #sets border color depending on sex (M: magenta, F: cyan)
            attrs[n]['border_color'] = "magenta"
        else:
            attrs[n]['border_color'] = "cyan"

        if get_IS(info,n) == "P":                       #sets background color depending on TB infection status (P: red, N: green)
            attrs[n]['background_color'] = "red"
        else:
            attrs[n]['background_color'] = "green"

        g = get_group(info,n)
        if g == 1:                                      #sets node shape depending on clique number
            attrs[n]['shape'] = "ellipse"
        elif g == 2:
            attrs[n]['shape'] = "rectangle"
        elif g == 3:
            attrs[n]['shape'] = "triangle"
        elif g == 4:
            attrs[n]['shape'] = "pentagon"
        elif g == 5:
            attrs[n]['shape'] = "star"
        elif g == 6:
            attrs[n]['shape'] = "diamond"
        elif g == 7:
            attrs[n]['shape'] = "vee"
        else:
            attrs[n]['shape'] = "roundrectangle"
            
        
        attrs[n]['border_width'] = attrs[n]['height'] * (0.2)
        attrs[n]['k'] = 1
            
        #print('Node Attribute for',n,':',attrs[n])
    return attrs


def node_popups(info,node_attrs):
    """
    alters the given node_attrs to include popups that provide info for each badger
    """
    curr_str = ""
    for badger in info:
        curr_sex = get_sex(info,badger)
        curr_IS = get_IS(info,badger)
        curr_group = get_group(info,badger)
        curr_str += "<b>sex:</b> " + curr_sex + "<br>"
        curr_str += "<b>TB status:</b> " + curr_IS + "<br>"
        curr_str += "<b>social group:</b> " + str(curr_group)
        node_attrs[badger]['popup'] = curr_str
        curr_str = ""

def getEdgeAttributes(edges,badger_names,badger_rows):
    """
    Creates a dictionary of attributes for each edge that corresponds to the GraphSpace API
    """
    attrs = {}
    degree_ls = []
    for e in edges:                    #this loop initializes the edge attribute dictionary
        source = e[0]
        target = e[1]
        if source not in attrs:
            attrs[source] = {}
        attrs[source][target] = {}
        attrs[source][target]['width'] = 2

    for e in edges:                   #this loop inputs the actual values we want into the dictionary
        i = get_index(e[0], badger_names)
        j = get_index(e[1], badger_names)
        time = int(badger_rows[i][j])
        logtime = math.log(float(int(badger_rows[i][j])))
        attrs[e[0]][e[1]]['width'] = logtime
        attrs[e[0]][e[1]]['popup'] = "<b>contact duration</b>: " + str(time) + " seconds."
        degree_ls.append([e,time])
    degree_ls.sort(key=lambda x: x[1],reverse=True)
    #print(degree_ls)
    for i in range(len(degree_ls)):          #this loop assigns edge rank
        e = degree_ls[i][0]
        attrs[e[0]][e[1]]['k'] = i

    return attrs

def get_index(badger, badger_names):
    """
    gets the index of the badger in the original matrix, necessary for the getEdgeAttributes function because it has to breach abstraction barriers which is kinda annoying but whatev
    """
    for b in range(len(badger_names)):
        if badger == badger_names[b]:
            return b





        

#####################################################################################################
#initialization of data, worksheet print instructions, and execution of graphspace commands##########
#####################################################################################################
badger_names0_rows1 = get_txt_data('BadgerMatrix.txt')
badger_names = badger_names0_rows1[0]
badger_rows = badger_names0_rows1[1]
adj_matrix = make_simplified_adj_matrix(badger_names,badger_rows)
edges = get_undirected_edges(badger_names,adj_matrix)
badger_info = get_badger_data('BadgerInfo.txt')
node_attrs = getNodeAttributes(badger_names,badger_info,badger_rows)
node_popups(badger_info,node_attrs)
edge_attrs = getEdgeAttributes(edges,badger_names,badger_rows)

#2.1
print("The number of badgers is: " + str(len(badger_names)))
print(" ")

#2.2
print("For each node, printing the number of neighbors and the list of neighbors:")
give_matrix_and_adj_list(badger_names,badger_rows)
print(" ")

#2.3
print("Is the adjacency matrix symmetric?")
if is_adjmat_symmetric(adj_matrix):
    print("Yes")
else:
    print("No")
print(" ")

#3.1
count_sex(badger_info)
count_IS(badger_info)
count_groups(badger_info)

#graphspace stuff
upload_graph(badger_names,adj_matrix,'hw1_graph','HW1: Badgers',0,node_attrs,edge_attrs)
graphspace_utils.shareGraph('hw1_graph','franzni@reed.edu','bio331','HW1','aritz@reed.edu')

#3.2 - 9
#The data on my graph has more connections between the Star clique (clique 5 in the paper) and the Vee clique (clique 7 in the paper)
