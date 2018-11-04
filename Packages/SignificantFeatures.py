__title__   =  'DPT graphical feature detector'
__author__  =  'Carel van Niekerk'
__contact__ =  'vniekerk.carel@gmail.com'
__date__    =  '2018-07-30'
__version__ =  1.0

#%% Load Packages
import numpy as np
from RoadmakersPavage import RP_DPT

#%% Significance feature detection class
class SignificantFeatures:
	# Initialise the class by loading in the Roadmakers pavage graphs
	def __init__(self, RP_Obj):
		self.RP = RP_Obj

    # Function which follows the route from a pulse down the graph and stores
	# all nodes (pulses) encountered on the way
	def find_Pulses(self, Node: int):
		Pulses = list()
		Neighbours = [None]
		while (len(Neighbours) != 0):
			Neighbours = [k
					  for k in self.RP.PG.Neighbours[str(Node)] if (k > Node)]
			if len(Neighbours) != 0:
				Node = Neighbours[0]
				Pulses += [Node]
		return Pulses

    # Function which uses the pulses found on the route down from a pixel
	# to calculate the saliency and sharpness of a pixel and ultimately
	# its significance
	def SigMap(self):
		self.Pulses = [self.find_Pulses(Node)
        for Node in range(1, self.RP.Image.shape[0]*self.RP.Image.shape[1]+1)]
		Saliency = [len(pulse) for pulse in self.Pulses]
		Sharp = [(np.abs(np.array([self.RP.PG.Value[str(key)]
		for key in pulse])) / np.sqrt(np.array([self.RP.PG.Scale[str(key)]
		for key in pulse]))).sum()
        for pulse in self.Pulses]
		self.Significance = np.array(Saliency) * np.array(Sharp)
		self.Map = self.Significance.reshape(self.RP.Image.shape)

	# Function which finds the locations of the alpha % most significant pixels
	def SigFeats(self, alpha: float):
		self.SigMap()
		Threshold = int(self.Significance.shape[0]*alpha)
		Threshold = np.argsort(self.Significance)[-Threshold]
		self.IsSig = self.Map >= self.Significance[Threshold]
		self.IsSig = np.where(self.IsSig)
		return self.IsSig