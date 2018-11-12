__title__   =  'DSFM Distance comparison'
__author__  =  'Carel van Niekerk'
__contact__ =  'vniekerk.carel@gmail.com'

#%% Load Packages
from os import chdir
chdir(r'...')
from sys import path
path.insert(0, 'Packages')
from DSFM import DSFM; del path
import pandas as pd
import numpy as np

def DistComp(Image, Similar, Random, t, f, n):
	Sim_Dist = list()
	for img in Similar[Similar.keys()[2:90002]].values:
		img = img.reshape(300,-1)
		L, Dist = DSFM(img, Image, Empty, 1, t, f, n)
		Sim_Dist += [Dist]
	Sim_Dist = np.mean(Sim_Dist)

	Ran_Dist = list()
	for img in Random[Random.keys()[2:90002]].values:
		img = img.reshape(300,-1)
		L, Dist = DSFM(img, Image, Empty, 1, t, f, n)
		Ran_Dist += [Dist]
	Ran_Dist = np.mean(Ran_Dist)

	return [Sim_Dist, Ran_Dist, t, f, n]

#%% Run
SIPIStore = pd.HDFStore('Data\\SIPIStore.h5')
TextureDB = SIPIStore.get('TextureDB')
SIPIStore.close()

Res = list()
print('DSFM Distance compare n=5')
Classes = ['Grass', 'Bark', 'Straw', 'Herringbone weave', 'Woolen cloth']
Classes += ['Pressed calf leather', 'Beach sand', 'Water', 'Wood grain']
Classes += ['Raffia', 'Pigskin', 'Brick wall', 'Plastic bubbles', 'Sand']
for Label in Classes:
	K = int(0.5 * 90000) #Select the same number of random pixels as features selected for MSFM
	Image = TextureDB[TextureDB.Label == Label].sample(1)
	Empty = (np.random.choice(Image.shape[0], K),
		  np.random.choice(Image.shape[0], K))
	Image = Image[Image.keys()[2:90002]].values.reshape(300,-1)

	Similar = TextureDB[TextureDB.Label == Label].sample(3, replace = True)
	Random = TextureDB[TextureDB.Label != Label].sample(3)

	print('Running {}'.format(Label))
	Res += [[Label] + DistComp(Image, Similar, Random, 0.4, 0.8, 5)]
	print('{} Completed at t=0.4,f=0.8,n=5'.format(Label))
	Res += [[Label] + DistComp(Image, Similar, Random, 0.35, 0.8, 5)]
	print('{} Completed at t=0.35,f=0.8,n=5'.format(Label))
	Res += [[Label] + DistComp(Image, Similar, Random, 0.3, 0.8, 5)]
	print('{} Completed at t=0.3,f=0.8,n=5'.format(Label))
	Res += [[Label] + DistComp(Image, Similar, Random, 0.25, 0.8, 5)]
	print('{} Completed at t=0.25,f=0.8,n=5'.format(Label))
	Res += [[Label] + DistComp(Image, Similar, Random, 0.2, 0.8, 5)]
	print('{} Completed at t=0.2,f=0.8,n=5'.format(Label))

	Res += [[Label] + DistComp(Image, Similar, Random, 0.4, 0.85, 5)]
	print('{} Completed at t=0.4,f=0.85,n=5'.format(Label))
	Res += [[Label] + DistComp(Image, Similar, Random, 0.35, 0.85, 5)]
	print('{} Completed at t=0.35,f=0.85,n=5'.format(Label))
	Res += [[Label] + DistComp(Image, Similar, Random, 0.3, 0.85, 5)]
	print('{} Completed at t=0.3,f=0.85,n=5'.format(Label))
	Res += [[Label] + DistComp(Image, Similar, Random, 0.25, 0.85, 5)]
	print('{} Completed at t=0.25,f=0.85,n=5'.format(Label))
	Res += [[Label] + DistComp(Image, Similar, Random, 0.2, 0.85, 5)]
	print('{} Completed at t=0.2,f=0.85,n=5'.format(Label))

	Res += [[Label] + DistComp(Image, Similar, Random, 0.4, 0.9, 5)]
	print('{} Completed at t=0.4,f=0.9,n=5'.format(Label))
	Res += [[Label] + DistComp(Image, Similar, Random, 0.35, 0.9, 5)]
	print('{} Completed at t=0.35,f=0.9,n=5'.format(Label))
	Res += [[Label] + DistComp(Image, Similar, Random, 0.3, 0.9, 5)]
	print('{} Completed at t=0.3,f=0.9,n=5'.format(Label))
	Res += [[Label] + DistComp(Image, Similar, Random, 0.25, 0.9, 5)]
	print('{} Completed at t=0.25,f=0.9,n=5'.format(Label))
	Res += [[Label] + DistComp(Image, Similar, Random, 0.2, 0.9, 5)]
	print('{} Completed at t=0.2,f=0.9,n=5'.format(Label))

pd.DataFrame(Res,
columns = ['Label', 'Within_Class_Dist', 'Alternate_Class_Dist', 't', 'f', 'n']).to_csv('Output\\DistComp(MSFM).csv')