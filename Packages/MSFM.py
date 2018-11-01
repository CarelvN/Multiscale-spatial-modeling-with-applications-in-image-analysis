__title__   =  'Multiscale Spatial Feature Matching(MSFM)'
__author__  =  'Carel van Niekerk'
__contact__ =  'vniekerk.carel@gmail.com'
__date__    =  '2018-08-02'
__version__ =  0.1

#%% Load Packages
import numpy as np
from BunchDS import Bunch_DS as DS
from SignificantFeatures import DPTFeatures
from warnings import filterwarnings; filterwarnings("ignore")

#%% MSFM
N = [[0,1,0],[1,9,1],[0,1,0]]
class MSFM:
	def __init__(self, method = 'Euclid'):
		self.method = method

	def Match(self,Image1, Image2, alpha, beta, t, f, n, Neigh = N):
		Key1, Pulse1 = DPTFeatures(Image1, Neigh, alpha, beta); del Key1
		Key, Pulse2 = DPTFeatures(Image2, Neigh, alpha, beta)
		SG = Pulse2.copy().astype(np.int64)
		SG[Key] = 999
		DirSamp = DS(Pulse1, SG, self.method).Simulate(t, f, n)
		Matches = np.array(DirSamp.Matches); del DirSamp, SG
		Distance = Matches[:,-1].max()
		num = int(Matches.shape[0] * beta)
		Links = Matches[Matches[:,-1].argsort()[:num],:-1]

		return (Links, Distance)