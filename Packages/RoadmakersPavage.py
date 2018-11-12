""" Roadmakers Pavage Algorithm Class (Used to extract Discrete Pulse
    Transform pulses using the Roadmakers Pavage Algorithm """
__author__ = "Carel van Niekerk"
__copyright__ = "Copyright 2017, The University of Pretoria"
__version__ = "0.2.0"
__maintainer__ = "Carel van Niekerk"
__email__ = "vniekerk.carel@gmail.com"
__status__ = "1.0"

# Import Packages required
import numpy as np
from scipy.ndimage import generic_filter as imfilt
import GraphClasses as Graph
from timeit import default_timer as timer
from warnings import filterwarnings; filterwarnings('ignore')

# Create Roadmakers_Pavage class, a class which contains the 2-dimensional
# sequence and all the functions to perform the discrete pulse transform
# using the Roadmakers Pavage algorithm.
class Roadmakers_Pavage:
    # Initialise the Roadmakers Pavage process with an image. (This image
    # should be a numpy 2 dimensional array of type int64)
    def __init__(self, Image):
        # Store the image in the class.
        self.Image = np.array(Image,"int64")
        # Reshape the image into a 1 dimensional data set by stacking the
        # rows of the image.
        Data = self.Image.reshape(Image.shape[0]*Image.shape[1])

        # Initialise the working graph.
        self.WG = Graph.WorkingGraph()
        # Add all the data nodes to the working graph.
        self.WG.add_nodes(Data)

        # Initialise the pulse graph.
        self.PG = Graph.PulseGraph()
        # Add all the initial data nodes to the pulse graph.
        self.PG.add_nodes(np.zeros(len(Data)), [1] * len(Data))

    # Function to define the neighbourhoods of all the nodes and add the
    # corresponding edges to the graph. (This function requires a single
    # parameter which is a list indicating the neighbourhood of a data point,
    # eg. for four connectivity we use the neighbourhood [[0,1,0],
    #                                                     [1,9,1],
    #                                                     [0,1,0]], which
    # indicates that the four data points surrounding the data point is it's
    # neighbours.
    def Define_Neighbours(self, Neighbourhood):
        # Boundary widths.
        Neighbourhood = np.array(Neighbourhood)
        BWl = np.where(Neighbourhood == 9)[1][0]
        BWr = Neighbourhood.shape[1] - np.where(Neighbourhood == 9)[1][0] - 1
        BWt = np.where(Neighbourhood == 9)[0][0]
        BWb = Neighbourhood.shape[0] - np.where(Neighbourhood == 9)[0][0] - 1
        Neighbourhood[np.where(Neighbourhood == 9)] = 0

        # Define a zero matrix with the same dimensions as the original 2-D
        # aswell as zero rows and columns on the edges. These zeros rows and
        # columns links the edge nodes to the zero node.
        Indices = np.zeros((self.Image.shape[0] + BWl + BWr,
                        self.Image.shape[1] + BWt + BWb), 'int64')

        # Array of node indices.
        Node_Index = np.array(list(self.WG.Value.keys())[1:])
        # Store the index of each data point at its position in the Indices
        # matrix.
        Indices[BWl:-BWr, BWt:-BWb] = Node_Index.reshape(self.Image.shape)

        # Initialise a list to store the edge tuples to be added to the graph.
        Edges = list()
        # For each of the neighbours defined in the neighbourhood list do
        # the following.
        for i in range(Neighbourhood.sum()):
            # Use the imfilt(ndimage.generic_filter) function loaded from the
            # Scipy library to scan through the image andd find the i-th
            # neighbour for each node.
            Neighbours = imfilt(Indices,lambda x:x[i],footprint=Neighbourhood)
            # Extract the Neighbours from the results of the filter
            Neighbours = Neighbours[BWl:-BWr, BWt:-BWb]
            # Reshape the Neighbours array to one dimension.
            New_size = (Neighbours.shape[0]*Neighbours.shape[1])
            Neighbours = Neighbours.reshape(New_size)
            # Add the edges corresponding to these Neighbours to the edges
            # list.
            Edges += [(i+1, int(Neighbours[i]))
                        for i in range(len(Neighbours))]

        # Use the graph add edges funtion to add the edges to the graph.
        self.WG.add_edges(Edges)

    # Function to combine a specific node with a neighbour which as has the
    # same value as that node. (This function requires a single parameter
    # which is the ID of the node to be checked).
    def Combine_Connected(self, ID):
        # Find the ID's of all the neighbours of the sepcified node which has
        # the same value as this node.
        J = [i for i in self.WG.Neighbours[str(ID)]
            if self.WG.Value[str(i)] == self.WG.Value[str(ID)]]
        # If the node has a neighbour with the same value as itself then
        # combine it with that neighbour using the join_nodes function from
        # the Working Graph class.
        if len(J) != 0:
            J = int(J[0])
            self.WG.join_nodes(J, ID)
            # Return true if two nodes where combined.
            return True
        else: return False

    # Function to combine all the neighbouring nodes with the same values in
    # the working graph. (This function has no parameters)
    def Find_ConnectedRegions(self):
        # Use list comprehension and the Combine_Connected function to combine
        # all the neighbouring nodes with the same values in the working
        # graph.
        [self.Combine_Connected(ID) for ID in range(1,len(self.WG.Value))]

    # Function to determine whether a node is a Max Feature. (This function
    # has one parameter which is the ID of the node to be checked)
    def MaxFeature(self, Node):
        # Run a list comprehension which checkes whether the value of a node
        # is larger than the value of a single one of its neighbours. If
        # a False value is not in this list returned then the node has a value
        # larger than all of its neighbours and hence it is a max feature.
        return False not in [self.WG.Value[str(Node)] > self.WG.Value[str(i)]
                            for i in self.WG.Neighbours[str(Node)]]

    # Function to determine whether a node is a Min Feature. (This function
    # has one parameter which is the ID of the node to be checked)
    def MinFeature(self, Node):
        # Run a list comprehension which checkes whether the value of a node
        # is smaller than the value of a single one of its neighbours. If
        # a False value is not in this list returned then the node has a value
        # smaller than all of its neighbours and hence it is a min feature.
        return False not in [self.WG.Value[str(Node)] < self.WG.Value[str(i)]
                            for i in self.WG.Neighbours[str(Node)]]

    # Function to add a node as a pulse in the Pulse Graph. (This function
    # has a single parameter, which is the ID of the node to be added)
    def Add_Pulse(self, Node):
        # Find the ID of the neighbour with the smallest distance in terms
        # of value from the specified node.
        J = np.array([abs(self.WG.Value[str(Node)] - self.WG.Value[str(n)])
                    for n in self.WG.Neighbours[str(Node)]]).argmin()
        J = list(self.WG.Neighbours[str(Node)])[J]

        # Add a new node to the Pulse Graph. The value of this node is the
        # difference in value between the specified node and node J defined
        # above.
        self.PG.add_node(self.WG.Value[str(Node)] - self.WG.Value[str(J)],
                        self.WG.Scale[str(Node)])
        # Add edges from this new Pulse node to all the pulse Nodes linked to
        # the specified node.
        self.PG.add_edges([(len(self.PG.Value), p)
                        for p in self.WG.Pulses[str(Node)]])
        # Add the new pulse to the set of pulses linked to the above defined
        # node J.
        self.WG.add_pulse(J, len(self.PG.Value))

        # Calculate and store the scale of the new joint node J.
        self.WG.Scale[str(J)] += self.WG.Scale[str(Node)]

        # Add the edges of the specified node to node J.
        self.WG.add_edges([(i,J) for i in self.WG.Neighbours[str(Node)]])
        # Delete the specified node.
        self.WG.del_node(Node)

    # Function which performs the discrete pulse transform using the
    # Roadmakers Pavage algorithm.
    def Discrete_Pulse_Transform(self):
        # Set the initial scale to 1.
        Scale = 1

        # Continue performing the process until only the zero node remains
        # in the working graph.
        while (len(self.WG.Value) != 1):
            # Find all the nodes of the current scale.
            Nodes = [int(i) for i in self.WG.Value.keys()
                    if self.WG.Scale[i] == Scale]

            # Initialise the list of Min Features.
            MinFs = list()
            # Create all the Max Feature Pulses first. This does the same as
            # the roadmakers algorithm bump removal operator.
            for Node in Nodes:
                # Ensure the node of still of the current scale.
                if self.WG.Scale[str(Node)] == Scale:
                    # Combine the node with a neighbour if neccesary.
                    Removed = self.Combine_Connected(Node)
                    MinF = False
                    Pulse = Removed
                    if not Removed:
                        # If the node is a max feature it is a pulse.
                        Pulse = self.MaxFeature(Node)
                        # If the node is a pulse add it to the pulse graph.
                        if Pulse: self.Add_Pulse(Node)
                    # Check if a node is a min feature when it is not a pulse.
                    if not Pulse: MinF = self.MinFeature(Node)
                    # Add the min features to the list of min features.
                    if MinF: MinFs.append(Node)

            # Now create all the Min Feature Pulses. This does the same as
            # the roadmakers algorithm pit removal operator.
            for Node in MinFs:
                # Ensure the node of still of the current scale.
                if self.WG.Scale[str(Node)] == Scale:
                    # Combine the node with a neighbour if neccesary.
                    Removed = self.Combine_Connected(Node)
                    if not Removed:
                        # If the node is a min feature it is a pulse.
                        Pulse = self.MinFeature(Node)
                        # If the node is a pulse add it to the pulse graph.
                        if Pulse: self.Add_Pulse(Node)

            # Increase the current scale.
            Scale += 1

    # Function to extract a pulse from the pulse graph.
    def Extract_Pulse(self, ID):
        N = self.PG.Neighbours[str(ID)]
        Pixels = set()
        last_pixel = self.Image.shape[0] * self.Image.shape[1]
        while (len(Pixels) < self.PG.Scale[str(ID)]):
            [Pixels.update([p]) for p in N if p <= last_pixel]
            N1 = set()
            [N1.update(self.PG.Neighbours[str(n)]) for n in N
             if last_pixel < n < ID]
            N = N1

        Pulse = np.zeros(last_pixel)
        Pulse[np.array(list(Pixels)) - 1] = self.PG.Value[str(ID)]
        Pulse = Pulse.reshape(self.Image.shape)

        return Pulse

    def Extract_Pulses_ofscale(self, Scale):
        last_pixel = self.Image.shape[0] * self.Image.shape[1]
        keys = [int(key) for key,scale in self.PG.Scale.items()
                if (scale == Scale) and (int(key) > last_pixel)]

        Pulses = np.zeros(self.Image.shape)
        for key in keys:
            Pulses += self.Extract_Pulse(key)

        return Pulses

    def Extract_Pulses_ofscales(self, Scales):
        Scales = list(Scales)
        Pulses = np.zeros(self.Image.shape)
        for scale in Scales:
            Pulses += abs(self.Extract_Pulses_ofscale(scale))
        return Pulses

def RP_DPT(x, Neigh):
    RP = Roadmakers_Pavage(x)
    RP.Define_Neighbours(Neigh)
    RP.Find_ConnectedRegions()
    RP.Discrete_Pulse_Transform()
    return RP