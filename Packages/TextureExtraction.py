__title__   =  'DPT texture extractor'
__author__  =  'Carel van Niekerk'
__contact__ =  'vniekerk.carel@gmail.com'
__date__    =  '2018-07-30'
__version__ =  1.0

#%% Load Packages
import numpy as np
from RoadmakersPavage import RP_DPT

#%% Significance feature detection class
class Textures:
	# Initialise the class by loading in the Roadmakers pavage graphs
	def __init__(self, RP_Obj):
		self.RP = RP_Obj

	def DetectDetails(self, beta):
		Scales = [self.RP.PG.Scale[i] for i in self.RP.PG.Scale
					if int(i) > self.RP.Image.reshape(-1).shape[0]]
		Counts = {S : Scales.count(S) for S in Scales}
		Scales = np.array([s for s in Counts])
		Counts = np.array([Counts[s] for s in Scales])
		Freq = np.cumsum(Counts) / sum(Counts)
		MaxScale = Scales[np.where(Freq > beta)[0][0]]
		PulseMap = self.RP.Extract_Pulses_ofscales(range(MaxScale))

		return PulseMap