__title__   =  'Multiscale Spatial Feature Matching(MSFM)'
__author__  =  'Carel van Niekerk'
__contact__ =  'vniekerk.carel@gmail.com'
__date__    =  '2018-08-02'
__version__ =  0.1

#%% Load Packages
import numpy as np
from BunchDS import Bunch_DS as DS
from Extracter import Extracter
from warnings import filterwarnings; filterwarnings("ignore")

#%% MSFM
N = [[0,1,0],[1,9,1],[0,1,0]]
def MSFM(Image1, Image2, alpha, beta, t, f, n, Neigh = N):
		Pulse1, Key1 = Extracter(Image1, Neigh, alpha, beta); del Key1
		Pulse2, Key = Extracter(Image2, Neigh, alpha, beta)
		SG = Pulse2.copy().astype(np.int64)
		SG[Key] = 999
		DirSamp = DS(Pulse1, SG).Simulate(t, f, n)
		Matches = np.array(DirSamp.Matches); del DirSamp, SG
		Distance = Matches[:,-1].max()
		Links = Matches[Matches[:,-1].argsort(),:-1]

		return (Links, Distance)