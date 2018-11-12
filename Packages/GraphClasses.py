""" Graph Data Structure Classes for the Roadmakers Pavage Algorithm """
__author__ = "Carel van Niekerk"
__copyright__ = "Copyright 2017, The University of Pretoria"
__version__ = "0.0.2"
__maintainer__ = "Carel van Niekerk"
__email__ = "vniekerk.carel@gmail.com"
__status__ = "1.0"

# Import Packages required
import numpy as np

# Create WorkingGraph class, this class will be used as a data type for the
# Working Graph (WG) in the Roadmakers Pavage Algorithm
class WorkingGraph:
    # Initialise the Working Graph (The working graph is a graph where the
    # nodes represents the original data sequence. The working graph always
    # contains a zero node of scale infinity, the theoretical reason for this
    # is that for the Discrete Pulse transform boundary elements are always
    # connected to zero elements which in turn are connected to zero elements,
    # and this continues endlessly).
    def __init__(self):
        # The graph data type is a class made up of dictionaries. Each
        # dictionary stores a attribute for each of the nodes. We have four
        # dictionaries, a node value dictionary, a node scale dictionary,
        # a node neighbours dictionary and finally a node pulses dictionary.
        # During initialisation the dictionaries are defined and the zero
        # node added.
        self.Value = {'0' : 0}
        self.Scale = {'0' : np.inf}
        self.Neighbours = {'0' : set()}
        self.Pulses = {'0' : set()}

    # Function to add a single node to the graph. (This function has
    # compulsory parameter value, which is the value of the node added. The
    # function also has parameters with default values, scale, neighbours
    # and pulses. The default scale is 1, the defualt neighbours is a empty
    # set and the defualt pulses is a set containing the node ID.)
    def add_node(self ,Value ,Scale = 1, Neighbours = None, Pulses = None):
        if Neighbours == None: Neighbours = set()
        ID = str(len(self.Value))
        if Pulses == None: Pulses = set([int(ID)])
        # Attributes of the new nodes added to the dictionaries
        self.Value.update({ID : Value})
        self.Scale.update({ID : Scale})
        self.Neighbours.update({ID : Neighbours})
        self.Pulses.update({ID : Pulses})

    # Function to add multiple nodes to the graph. (This function has
    # compulsory parameter Values, which is an array of values of the nodes
    # added. The function also has parameters with default values, scale,
    # neighbours and pulses.)
    def add_nodes(self, Values, Scales = None, Neighbours = None, Pulses = None):
        if not np.array(Scales).any(): Scales = [1] * len(Values)
        if not np.array(Neighbours).any(): Neighbours = [None] * len(Values)
        if not np.array(Pulses).any(): Pulses = [None] * len(Values)
        [self.add_node(Values[n], Scales[n], Neighbours[n], Pulses[n])
        for n in range(len(Values))]

    # Function to add a single edge to the graph. (This function has two
    # compulsory parameters, the ID's of the two nodes joined by the edge.)
    def add_edge(self, node1, node2):
        # Ensures a edge cannot exist between a node and itself.
        if node1 != node2:
            # Add the nodes to one anothers lists of neighbours.
            self.Neighbours[str(node1)].update([node2])
            self.Neighbours[str(node2)].update([node1])

    # Function to add multiple edges to the graph. (This function has two
    # compulsory parameters, the lists of edge tuples to be added to the
    # graph, where each tuple contains the ID's of the nodes to be joined by
    # a new edge.)
    def add_edges(self, edges):
        # Use a list comprehension together with the add_edge function to add
        # all the edges in the list.
        [self.add_edge(edge[0], edge[1]) for edge in edges]

    # Function to add new virtual edge from a node to a pulse in the pulse
    # graph. (This function has two compulsory parameters, the ID of the node
    # and the ID df the pulse in the Pulse graph.)
    def add_pulse(self, ID, pulse):
        # Add the pulse ID to the set of pulses in the pulse dictionary under
        # the desired node.
        self.Pulses[str(ID)].update([pulse])

    # Function to add new virtual edges. (This function has two compulsory
    # parameters, the list of ID's of the nodes and the list of corresponding
    # IDs of the pulses in the Pulse graph.)
    def add_pulses(self, ID, pulses):
        # Use a list comprehension together with the add_pulse function to add
        # all the pulses in the lists.
        [self.add_pulse(ID[n], pulses[n]) for n in range(len(ID))]

    # Function to delete a node from the graph. (This function only requires
    # the ID of the node to be removed.)
    def del_node(self, ID):
        # Remove the attributes of the node to be removed from all the
        # dictionaries.
        del self.Value[str(ID)]
        del self.Scale[str(ID)]
        del self.Pulses[str(ID)]
        # Remove the node ID from the neighbourhoods of all its neighbours.
        for node in self.Neighbours[str(ID)]:
            self.Neighbours[str(node)].remove(ID)
        del self.Neighbours[str(ID)]

    # Function to combine two nodes in the working graph. (This function has
    # two compulsory parameters, the ID's of the two nodes to be joined.
    # The node created by combining the two nodes will be stored at ID1 and
    # ID2 will be removed from the graph.)
    def join_nodes(self, ID1, ID2):
        # Calculate and store the scale of the joint node
        self.Scale[str(ID1)] += self.Scale[str(ID2)]
        # Add the edges of node ID2 to node ID1.
        self.add_edges([(i,ID1) for i in self.Neighbours[str(ID2)]])
        # Add the pulses associated with node ID2 to node ID1.
        self.add_pulses([ID1] * len(self.Pulses[str(ID2)]),
                               list(self.Pulses[str(ID2)]))
        # Remove node ID2.
        self.del_node(ID2)

# Create PulseGraph class, this class will be used as a data type for the
# Pulse Graph (PG) in the Roadmakers Pavage Algorithm
class PulseGraph:
    # Initialise the Pulse Graph (The pulse graph is a graph where the
    # nodes represents the pulses extracted by the Discrete Pulse Transform.)
    def __init__(self):
        # The graph data type is a class made up of dictionaries. Each
        # dictionary stores a attribute for each of the nodes. We have three
        # dictionaries, a node value dictionary, a node scale dictionary
        # and finally a node neighbours dictionary. During initialisation the
        # dictionaries are defined.
        self.Value = {}
        self.Scale = {}
        self.Neighbours = {}

    # Function to add a single node to the graph. (This function has
    # compulsory parameter value, which is the value of the node added. The
    # function also has parameters with default values, scale and neighbours
    # The default scale is 1, the defualt neighbours is a empty
    # set.)
    def add_node(self ,Value ,Scale = 1, Neighbours = None):
        if Neighbours == None: Neighbours = set()
        if len(self.Value) == 0: ID = str(1)
        else: ID = str(len(self.Value) + 1)
        # Attributes of the new nodes added to the dictionaries
        self.Value.update({ID : Value})
        self.Scale.update({ID : Scale})
        self.Neighbours.update({ID : Neighbours})

    # Function to add multiple nodes to the graph. (This function has
    # compulsory parameter Values, which is an array of values of the nodes
    # added. The function also has parameters with default values, scale
    # and neighbours.)
    def add_nodes(self, Values, Scales = None, Neighbours = None):
        if not np.array(Scales).any(): Scales = [1] * len(Values)
        if not np.array(Neighbours).any(): Neighbours = [None] * len(Values)
        [self.add_node(Values[n], Scales[n], Neighbours[n])
        for n in range(len(Values))]

    # Function to add a single edge to the graph. (This function has two
    # compulsory parameters, the ID's of the two nodes joined by the edge.)
    def add_edge(self, node1, node2):
        # Ensures a edge cannot exist between a node and itself.
        if node1 != node2:
            # Add the nodes to one anothers lists of neighbours.
            self.Neighbours[str(node1)].update([node2])
            self.Neighbours[str(node2)].update([node1])

    # Function to add multiple edges to the graph. (This function has two
    # compulsory parameters, the lists of edge tuples to be added to the
    # graph, where each tuple contains the ID's of the nodes to be joined by
    # a new edge.)
    def add_edges(self, edges):
        # Use a list comprehension together with the add_edge function to add
        # all the edges in the list.
        [self.add_edge(edge[0], edge[1]) for edge in edges]