# CISC352
# Assignment2 Alpha-beta Problem
# Christina Hu  
# Derek Huang   
# Jie Niu       
# Wansi Liang   
# Xing Wang     

# import the library we need
import math

'''
A reference for implementation of the node structure
node[] 0      1           2     3      4     5         6
       value, neighbours, type, alpha, beta, LeafNode, rootNode
'''

# An initialization for a Node structure
def init_node(value, type, rootNode):
    neighbours = []
    alpha = -float(math.inf)
    beta = float(math.inf)
    if(value.isdigit()):
        LeafNode = True
        value = int(value)
    else:
        LeafNode = False
    return [value, neighbours, type, alpha, beta, LeafNode, rootNode]


# The Alpha-beta pruning algorithm for n-player game
def alpha_beta(current_node, alpha, beta, numOfLeafNodes):
    # Set alpha and beta to positive and negative infinity when the current node is the root node
    if current_node[6]:
        alpha = -float(math.inf)
        beta = float(math.inf)
    
    # Returns the current node and the number of leaf nodes if the current node is a leaf node
    if current_node[5]:
        numOfLeafNodes += 1
        return (current_node[0], numOfLeafNodes)
    
    # Returns value of alpha/beta and the number of leaves if the type is MAX
    if current_node[2] == "MAX":
        values = []
        for i in current_node[1]:
            value, numOfLeafNodes = alpha_beta(i, alpha, beta, numOfLeafNodes)
            values.append(value)
            alpha = max(alpha, max(values))
            current_node[3] = max(alpha, max(values))
            if alpha>=beta:
                return (beta, numOfLeafNodes)
        return (alpha, numOfLeafNodes)

    # Returns value of alpha/beta and the number of leaves if the type is MIN
    if current_node[2] == "MIN":
        values = []
        for i in current_node[1]:
            value, numOfLeafNodes = alpha_beta(i, alpha, beta, numOfLeafNodes)
            values.append(value)
            beta = min(beta, min(values))
            current_node[4] = min(beta, min(values))
            if beta<=alpha:
                return (alpha, numOfLeafNodes)
        return (beta, numOfLeafNodes)
        

# Given a certain format of string (i.e. Input file), this function splits the string to a nested list
# of strings
def splitSet(string):
    tmp = string[2:-2].split("),(")
    newString=[]
    for i in tmp:
        newString.append(i.split(','))
    return newString


# Given a list-like string, this function splits the string to the set of nodes and edges.
# Then the function returns the root node of a dictionary of linked-list with edges and nodes
def init_graph(lst):
    givenSet = lst.split()
    nodes, edges = splitSet(givenSet[0]), splitSet(givenSet[1])

    graph_dict = {}
    root = graph_dict[nodes[0][0]] = init_node(nodes[0][0], nodes[0][1], True)

    for n in nodes[1:]:
        graph_dict[n[0]] = init_node(n[0], n[1], False)
    for e in edges:
        if e[1] not in graph_dict:
            graph_dict[e[1]] = init_node(e[1], 'None', False)
        graph_dict[e[0]][1].append(graph_dict[e[1]])
        
    return root


# Given a file name, the function reads lines of the file and strips it to two parts, one node set and one edge set
def fileIn(txt):
    file = open(txt, 'r')
    content = file.readlines()
    input = []
    for c in content:
        input.append(c.strip())
    file.close()
    return input


# The main function for Alpha-beta pruning algorithm given sets of nodes and edges of a graph
def main(file_input, file_output):
    f_in = fileIn(file_input)
    f_out = open(file_output, 'a')

    graph_num = 1
    
    for line in range(0, len(f_in)):
        newLine = f_in[line]
        rootNode = init_graph(newLine)
        solution = (alpha_beta(rootNode, 0, 0, 0))
        
        f_out.write("Graph " + str(graph_num) + ": Score: " + str(solution[0]) +
               "; Leaf Nodes Examined: " + str(solution[1]) + "\n")
               
        graph_num += 1
        
    f_out.close()
    
    
main('alphabeta.txt', 'alphabeta_out.txt')
