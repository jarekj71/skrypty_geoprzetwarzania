import os
import matplotlib.pyplot as plt
os.chdir("/home/jarekj/Documents/skrypty_geoprzetwarzania")
pdist = 100
dem = 'dem.tif'
przekroj = 'przekroj.gpkg|layername=przekroj'

sample_params =  {'INPUT':przekroj,
    'DISTANCE':pdist,
    'OUTPUT':'TEMPORARY_OUTPUT'}

punkty = processing.run("native:pointsalonglines",sample_params)['OUTPUT']

sample_params = {
    'INPUT':punkty,
    'RASTERCOPY':dem,
    'COLUMN_PREFIX':'Z_',
    'OUTPUT':'TEMPORARY_OUTPUT'}

elevs = processing.run("native:rastersampling",sample_params)['OUTPUT']

distances = QgsVectorLayerUtils.getValues(elevs,'distance')
elevations = QgsVectorLayerUtils.getValues(elevs,'Z_1')


fig,ax = plt.subplots(figsize=(10,5))
ax.plot(distances[0],elevations[0],c="#DD1100",lw=2)
fig.show()