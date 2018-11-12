#!/usr/bin/env python
__title__   =  'Bunch Direct Sampling Function'
__author__  =  'Carel van Niekerk'
__contact__ =  'vniekerk.carel@gmail.com'
__date__    =  '2018-07-30'
__version__ =  1.0

#%% Load Packages
import numpy as np
from skimage.util.shape import view_as_windows
from scipy.spatial.distance import cdist

#%% Define Class
class Bunch_DS:
	def __init__(self, Image_Train: np.array, Sampling_Grid: np.array):
		self.TrainImg = Image_Train.copy()
		self.SampGrid = Sampling_Grid.copy()
		self.Matches = list()

	def Create_Windows(self):
		self.TI_Windows = view_as_windows(self.TrainImg, self.window)
		self.TIW_ind = [(i,j) for i in range(self.TI_Windows.shape[0])
									for j in range(self.TI_Windows.shape[1])]
		self.indmat = np.arange(len(self.TIW_ind))
		self.indmat = self.indmat.reshape(self.TI_Windows.shape[:2])

	def Compare(self, Twin: np.array, SGWin: np.array, Neigh: np.array):
		Dist = float(cdist(SGWin[Neigh].reshape(1,-1)/255,
					    Twin[Neigh].reshape(1,-1)/255)) / np.sqrt(Neigh.sum())
		return Dist

	def Simulate_Window(self, index: tuple, max_ite: int, t: float):
		indices = np.meshgrid(range(index[0], index[0] + self.window[0]),
	                          range(index[1], index[1] + self.window[1]))
		SGWin = self.SampGrid[tuple(indices)]
		if 999 in SGWin:
			Neigh = (SGWin != 999)
			min = np.inf
			for ind in np.random.choice(len(self.TIW_ind), max_ite):
				Twin = self.TI_Windows[self.TIW_ind[ind]]
				Dist = self.Compare(Twin, SGWin, Neigh)
				if Dist < min:
					TWin_min = Twin
					min = Dist
					TWin_index = ind
				if Dist < t: break
			row_col = np.where(self.indmat == TWin_index)
			N = np.where(~Neigh)
			Node = np.concatenate(((index[0] + N[0]).reshape(-1,1),
												  (index[1] + N[1]).reshape(-1,1),
												  (N[0] + row_col[0]).reshape(-1,1),
												  (N[1] + row_col[1]).reshape(-1,1),
												 np.full(N[0].shape, min).reshape(-1,1)),1)
			self.Matches += Node.tolist()
			self.SampGrid[indices[0][~Neigh], indices[1][~Neigh]] = TWin_min[~Neigh]

	def Simulate(self, t: float, f: float, window_size: int):
		self.window = (window_size, window_size)
		self.Create_Windows()
		SGind = [(i,j) for i in range(self.SampGrid.shape[0])
						for j in range(self.SampGrid.shape[1])
		          if i < (self.SampGrid.shape[0] - self.window[0] + 1)
				    and j < (self.SampGrid.shape[1] - self.window[1] + 1)]
		max_ite = int(len(self.TIW_ind) * f)
		[self.Simulate_Window(Ind, max_ite, t) for Ind in SGind]
		return self