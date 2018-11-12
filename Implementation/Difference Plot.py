__title__   =  'Plot performance difference plots'
__author__  =  'Carel van Niekerk'
__contact__ =  'vniekerk.carel@gmail.com'

#%% Load Packages
import numpy as np
import pandas as pd
from os import chdir
from matplotlib import pyplot as plt
import matplotlib.cm as cm

#%%
Labs = ['Grass', 'Bark', 'Straw', 'Herringbone weave', 'Woolen cloth', 'Pressed calf leather', 'Beach sand', 'Water', 'Wood grain', 'Raffia', 'Pigskin', 'Brick wall', 'Plastic bubbles', 'Sand']
for n in [5,6,7,8]:
	chdir(r'...\DistComp\MSFM Euclidean')
	Data = pd.read_csv('DistComp(n={}).csv'.format(n))

	f_range = Data.f.unique()
	t_range = Data.t.unique()

	for f in f_range:
		fig = plt.figure(figsize = (12,5))
		ax = fig.add_subplot(111)
		for off,t in enumerate(t_range):
			off -= 2; off /= 7
			Subset = Data[(Data.t == t) & (Data.f == f)]
			Subset = Subset[[v in Labs for v in Subset.Label.values]]
			for i,obs in enumerate(Subset.values):
				vmax = max(Subset.Similar_Tex_Dist.max(), Subset.Random_Tex_Dist.max())
				Sim = obs[1] / vmax
				Ran = obs[2] / vmax
				Diff = Ran - Sim
				ax.scatter(i + off, Sim, c = 'Blue', s=15)
				ax.scatter(i + off, Ran, c = 'Black', s=15)
				col = 'green'
				if Diff < 0: col = 'red'
				ax.plot([i + off, i + off], [Sim, Ran], c = col)
		ax.vlines(np.arange(0.5, Subset.shape[0] - 1, 1), 0, 1.05, colors = 'grey')
		ax.set_ylim(0, 1.05)
		ax.set_xlim(-0.5, Subset.shape[0] - 0.5)
		Labels = Subset.Label.values
		Lab = list()
		for L in Labels:
			if len(L) > 8:
				L = L[:L.find(' ')] + '\n' + L[(L.find(' ')+1):]
			Lab += [L]
		plt.xticks(range(Subset.shape[0]), tuple(Lab), rotation = 'vertical')
		ax.set_ylabel('Standardised distance', fontsize = 14)
		chdir(r'...')
		fig.savefig('Compare(f={},n={}).png'.format(int(f*100),n), bbox_inches = 'tight', pad_inches = 0)