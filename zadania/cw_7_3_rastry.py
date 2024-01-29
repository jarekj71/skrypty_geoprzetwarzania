import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
os.chdir("/home/jarekj/Documents/skrypty_geoprzetwarzania")

npoints = 1000
DEM = "dem.tif"

slope_pos_params = {'DEM':DEM,
              'HO':'TEMPORARY_OUTPUT', # slope height
              'HU':'TEMPORARY_OUTPUT', #valley depth
              'NH':'TEMPORARY_OUTPUT', #normalized height
              'SH':'TEMPORARY_OUTPUT', #standarized height
              'MS':'TEMPORARY_OUTPUT'} #midslope position

# to jest słownik
slopes = processing.run("saga:relativeheightsandslopepositions",slope_pos_params)
slopes.keys()

tmp_rast = QgsRasterLayer(slopes['HO'])
e = tmp_rast.extent()
crs = tmp_rast.crs() ##

random_params = {'EXTENT':e,
    'POINTS_NUMBER':npoints,
    'TARGET_CRS':crs,
    'OUTPUT':'TEMPORARY_OUTPUT'}

random_points = processing.run("native:randompointsinextent",random_params)['OUTPUT']

sample_params = {
    'INPUT':random_points,
    'RASTERCOPY':'',
    'COLUMN_PREFIX':'',
    'OUTPUT':'TEMPORARY_OUTPUT'}

for key in slopes.keys():
    sample_params['RASTERCOPY']=slopes[key]
    sample_params['COLUMN_PREFIX']='{}_'.format(key)
    tmp = processing.run("native:rastersampling",sample_params)
    sample_params['INPUT'] = tmp['OUTPUT']
    
#QgsProject.instance().addMapLayer(tmp['OUTPUT'])
vect_layer = tmp['OUTPUT']


slopes_df = {}
for f in vect_layer.fields(): # pomijamy id
    if f.name() !='id':
        slopes_df[f.name()]= QgsVectorLayerUtils.getValues(vect_layer,f.name())[0]
slopes_df = pd.DataFrame(slopes_df)

fig, axes = plt.subplots(nrows=5,figsize=(4,10))
for n, column in enumerate(slopes_df.columns):
    slopes_df.plot(y=column,kind='kde',ax=axes[n])
    axes[n].set_xlabel(column)

fig.tight_layout()
fig.show()
