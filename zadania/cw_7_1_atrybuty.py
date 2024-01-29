import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
os.chdir("/home/jarekj/Documents/skrypty_geoprzetwarzania")
vect = "countries.gpkg"
vect_layer = QgsVectorLayer(vect)

'''
features = vect_layer.getFeatures()
areas = [feature.geometry().area() for feature in features]
pops = [feature['POP_EST'] for feature in features]
'''

pops = QgsVectorLayerUtils.getValues(vect_layer,'POP_EST')
gdps = QgsVectorLayerUtils.getValues(vect_layer,'GDP_MD')
areas = QgsVectorLayerUtils.getValues(vect_layer,'$area')
perimeters = QgsVectorLayerUtils.getValues(vect_layer,'$perimeter')

stats = {'GDPS':gdps[0],'POPS':pops[0],'AREAS':areas[0],'PERIMETERS':perimeters[0]}
stats = pd.DataFrame(stats)
select = (stats['POPS'] > 0) & (stats['GDPS'] > 0)
selected_stats = stats[select]

fig,axes = plt.subplots(ncols=2,figsize=(10,5)) #1
axes[0].scatter(selected_stats.PERIMETERS,selected_stats.AREAS,c="#DD1100") #2
axes[1].scatter(selected_stats.POPS,selected_stats.GDPS,c="#DD1100") #3
axes[0].set_xlabel("area") #5
axes[0].set_ylabel("perimeter")
axes[0].set_xscale('log',base=10) #4
axes[0].set_yscale('log',base=10)
axes[1].set_xscale('log',base=10)
axes[1].set_yscale('log',base=10)
axes[1].set_xlabel("population") #5
axes[1].set_ylabel("GDP")
fig.tight_layout()
fig.show()