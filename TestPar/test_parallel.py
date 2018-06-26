_Author_ = "Karthik Vaidhyanathan and Mohammand Abouei Mehrizi"

# Parallelizing Test cases using PRADET approach
# Course project on Software Testing
# Gran Sasso Science Institute


import traceback
from Logging import logger
from ConfigParser import SafeConfigParser
from collections import defaultdict
import csv
import networkx as nx
import matplotlib.pyplot as plt

from threading import Lock

from Queue import Queue
from threading import Thread


# Impliment the algorithm to find the Strongly connected components from the fiven graph


# The main class comes here

CONFIG_FILE = "settings.conf"
CONFIG_SECTION = "settings"
lock = Lock()

class TesPar:
    data_path = ""  # Read the data path
    file_name = ""  # The file name from the conf

    def __init__(self):
        parser = SafeConfigParser()
        parser.read(CONFIG_FILE)
        self.data_path = parser.get(CONFIG_SECTION, "data")
        self.file_name = parser.get(CONFIG_SECTION, "fileName")

    def read_csv(self):
        fname = self.data_path + self.file_name
        file = open(fname, 'ra')
        csv_f = csv.reader(file, delimiter=',')
        return csv_f


    def label_genrator(self,csv_object):
        # Take the graph and give labels to each of the nodes
        label_map = {}
        key = 0 # This is the start value
        for row in csv_object:
            if row[0] not in label_map:
                label_map[row[0]] =key
                key = key + 1
            if row[1] not in label_map:
                label_map[row[1]] =key
                key = key+1

        return label_map

    def inverse_label_generator(self,label_map):
        # This inverses the total dictionary
        inv_map = {v: k for k, v in label_map.iteritems()}
        reverse_map = {}
        for key,value in label_map.iteritems():
            split_text = key.split('.')
            last_text = key.rsplit('.', 1)[0]
            #print last_text + "#" + split_text[-1]
            new_text = last_text + "#" + split_text[-1]
            reverse_map[value] = new_text
        return reverse_map


    def reverse_adjacency(self,adjacency_list):
        # This will pring the adjacency list in the reverse way so that it can be used to compute the parallel execution

        reverse_list = {}
        for node in adjacency_list:
            reverse_list[node] =[]

        for node in adjacency_list:
            for edge in adjacency_list[node]:
                reverse_list[edge].append(node)
        return  reverse_list

# This class represents a directed graph using adjacency list representation
class Graph:

    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = defaultdict(list)  # default dictionary to store graph

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # A function used by DFS
    def DFSUtil(self, v, visited):
        # Mark the current node as visited and print it
        visited[v] = True
        print v,
        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.DFSUtil(i, visited)

    def fillOrder(self, v, visited, stack):
        # Mark the current node as visited
        visited[v] = True
        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.fillOrder(i, visited, stack)
        stack = stack.append(v)

    # Function that returns reverse (or transpose) of this graph
    def getTranspose(self):
        g = Graph(self.V)
        # Recur for all the vertices adjacent to this vertex
        for i in self.graph:
            for j in self.graph[i]:
                g.addEdge(j, i)
        return g

    # The main function that finds and prints all strongly
    # connected components
    def printSCCs(self):

        stack = []
        # Mark all the vertices as not visited (For first DFS)
        visited = [False] * (self.V)
        # Fill vertices in stack according to their finishing
        # times
        for i in range(self.V):
            if visited[i] == False:
                self.fillOrder(i, visited, stack)

        # Create a reversed graph
        gr = self.getTranspose()

        # Mark all the vertices as not visited (For second DFS)
        visited = [False] * (self.V)

        # Now process all vertices in order defined by Stack
        while stack:
            i = stack.pop()
            if visited[i] == False:
                gr.DFSUtil(i, visited)
                print""





def draw_graph(graph):

    # extract nodes from graph
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph
    G=nx.Graph()

    # add nodes
    for node in nodes:
        G.add_node(node)

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # draw graph
    pos = nx.shell_layout(G)
    nx.draw(G, pos)

    # show graph
    plt.show()


def strongly_connected_components_iterative(vertices, edges):
    """
    This is a non-recursive version of strongly_connected_components_path.
    See the docstring of that function for more details.

    Examples
    --------
    Example from Gabow's paper [1]_.

    >>> vertices = [1, 2, 3, 4, 5, 6]
    >>> edges = {1: [2, 3], 2: [3, 4], 3: [], 4: [3, 5], 5: [2, 6], 6: [3, 4]}
    >>> for scc in strongly_connected_components_iterative(vertices, edges):
    ...     print(scc)
    ...
    set([3])
    set([2, 4, 5, 6])
    set([1])

    Example from Tarjan's paper [2]_.

    >>> vertices = [1, 2, 3, 4, 5, 6, 7, 8]
    >>> edges = {1: [2], 2: [3, 8], 3: [4, 7], 4: [5],
    ...          5: [3, 6], 6: [], 7: [4, 6], 8: [1, 7]}
    >>> for scc in  strongly_connected_components_iterative(vertices, edges):
    ...     print(scc)
    ...
    set([6])
    set([3, 4, 5, 7])
    set([8, 1, 2])

    """
    identified = set()
    stack = []
    index = {}
    boundaries = []

    for v in vertices:
        if v not in index:
            to_do = [('VISIT', v)]
            while to_do:
                operation_type, v = to_do.pop()
                if operation_type == 'VISIT':
                    index[v] = len(stack)
                    stack.append(v)
                    boundaries.append(index[v])
                    to_do.append(('POSTVISIT', v))
                    # We reverse to keep the search order identical to that of
                    # the recursive code;  the reversal is not necessary for
                    # correctness, and can be omitted.
                    to_do.extend(
                        reversed([('VISITEDGE', w) for w in edges[v]]))
                elif operation_type == 'VISITEDGE':
                    if v not in index:
                        to_do.append(('VISIT', v))
                    elif v not in identified:
                         while index[v] < boundaries[-1]:
                            boundaries.pop()
                else:
                    # operation_type == 'POSTVISIT'
                    if boundaries[-1] == index[v]:
                        boundaries.pop()
                        scc = set(stack[index[v]:])
                        del stack[index[v]:]
                        identified.update(scc)
                        yield scc

global thread_node_list  # A boolean map to keep track if the edge has been visited or not
thread_node_list={}

def parallel_test(q,adjacency_list,index):

    print index
    # This is the function that takes the queue, what ever test is there, it will be executed and the corresponding neigbours will be added
    while True:
        #lock.acquire()
        current_node = q.get() # Gets the current test node

        thread_node_list[current_node] = False
        #print thread_node_list

        #
        print str(current_node) + "\n"
        #if len(adjacency_list[current_node])>0:
        #    for edges in adjacency_list[current_node]:
         #         if edges not in thread_node_list:
        #           q.put(edges)

        #print list(q.queue)

        #lock.release()
        q.task_done()




if __name__ == '__main__':
    test_par_object = TesPar()
    csv_obj = test_par_object.read_csv()
    label_map = test_par_object.label_genrator(csv_obj)
    print label_map
    graph = Graph(len(label_map))
    # Add all the edges to the graph as per they are processed from the file
    graph_list = []
    csv_obj = test_par_object.read_csv()
    node_list = [] # For vertices
    edge_list = defaultdict(list)
    adjacency_map = {}
    print edge_list
    for row in csv_obj:
        node_list.append(label_map[row[0]])
        node_list.append(label_map[row[1]])
        adjacency_map[label_map[row[0]]] = []
        adjacency_map[label_map[row[1]]] = []
        edge_list[label_map[row[0]]].append(label_map[row[1]])

    print adjacency_map



    #print list(set(node_list))
    #print edge_list
    graph_list = []
    for scc in strongly_connected_components_iterative(node_list,edge_list):
        print scc
    csv_obj = test_par_object.read_csv()

    for row in csv_obj:

        #edge_list[label_map[row[0]]] =  edge_list[label_map[row[0]]].append(label_map[row[1]])
        node_list.append(label_map[row[0]])
        adjacency_map[label_map[row[0]]].append(label_map[row[1]])
        graph_list.append(tuple((label_map[row[0]],label_map[row[1]])))
        #print tuple((label_map[row[0]],label_map[row[1]]))
        graph.addEdge(label_map[row[0]],label_map[row[1]])

    print adjacency_map

    #print graph_list
    #draw_graph(graph_list)
    #graph.printSCCs()
    reverse_list = test_par_object.reverse_adjacency(adjacency_map)
    #print reverse_list
    inverse_map = test_par_object.inverse_label_generator(label_map)
    #print inverse_map
      # Initialize the queue and send the test cases to others