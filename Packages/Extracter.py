__title__   =  'DPT detail extractor'
__author__  =  'Carel van Niekerk'
__contact__ =  'vniekerk.carel@gmail.com'
__date__    =  '2018-07-30'
__version__ =  1.0

#%% Load Packages
import numpy as np
from SignificantFeatures import SignificantFeatures
from TextureExtraction import Textures
from RoadmakersPavage import RP_DPT

def Extracter(Image, Neigh, alpha, beta):
	RP = RP_DPT(Image, Neigh)
	KeyPoints = SignificantFeatures(RP).SigFeats(alpha)
	PulseMap = Textures(RP).DetectDetails(beta)

	return(PulseMap, KeyPoints)