__title__   =  'SSIM'
__author__  =  'Carel van Niekerk'
__contact__ =  'vniekerk.carel@gmail.com'
__version__ =  1

#%% Load Packages
import numpy as np
from numba import guvectorize, float64

#%% Define SSIM
def SSIM(X, Y, k1 = 0.01, k2 = 0.01, datarange = 255):
	c1 = (k1 * datarange) ** 2
	c2 = (k2 * datarange) ** 2
	m_x = X.mean()
	m_y = Y.mean()
	S = np.cov(X.reshape(-1), Y.reshape(-1))
	ssim = (2 * m_x * m_y + c1) * (2 * S[1,0] + c2)
	ssim /= (m_x ** 2 + m_y ** 2 + c1) * (S[0,0] + S[1,1] + c2)
	return ssim

#%% Distance
def StrucDist(X, Y, k1 = 0.01, k2 = 0.01, datarange = 255):
	ssim = SSIM(X, Y, k1, k2, datarange)
	dist = 1 - (ssim * (ssim >= 0) * (ssim < 1) + 1 * (ssim >= 1))
	return dist