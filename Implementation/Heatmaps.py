__title__   =  'Plot Heatmap performance'
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

	t_range = Data.t.unique()
	f_range = Data.f.unique()

	Res = list()
	for t in t_range:
		for f in f_range:
			Subset = Data[(Data.t == t)&(Data.f == f)]
			Subset = Subset[[v in Labs for v in Subset.Label.values]]
			Acc = (Subset.Similar_Tex_Dist < Subset.Random_Tex_Dist).sum() / Subset.shape[0]
			Res += [[t, f, Acc]]
	Res = np.array(Res)[:,-1].reshape(-1,3)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	p = ax.imshow(Res, cmap = cm.get_cmap(name='coolwarm'), vmin = 0.4, vmax = 0.8)
	plt.yticks((0,1,2,3,4), (0.4, 0.35, 0.3, 0.25, 0.2))
	plt.xticks((0,1,2), (0.8, 0.85, 0.9))
	ax.set_ylabel('t', fontsize = 16)
	ax.set_xlabel('f', fontsize = 16)
	chdir(r'...')
	plt.savefig('Heat(n={}).png'.format(n), bbox_inches = 'tight', pad_inches = 0)