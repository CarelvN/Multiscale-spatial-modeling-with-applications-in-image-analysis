__title__   =  'Direct Sampling Feature Matching(DSFM)'
__author__  =  'Carel van Niekerk'
__contact__ =  'vniekerk.carel@gmail.com'
__date__    =  '2018-08-02'
__version__ =  0.1

#%% Load Packages
import numpy as np
from BunchDS import Bunch_DS as DS

#%% DSFM Match
def DSFM(Image1, Image2, Empty, alpha, t, f, n):
	SG = Image2.copy().astype(np.int64)
	SG[Empty] = 999
	DirSamp = DS(Image1, SG).Simulate(t, f, n)
	Matches = np.array(DirSamp.Matches); del DirSamp, SG
	Distance = Matches[:,-1].max()
	num = int(Matches.shape[0] * alpha)
	Links = Matches[Matches[:,-1].argsort()[:num],:-1]

	return (Links, Distance)