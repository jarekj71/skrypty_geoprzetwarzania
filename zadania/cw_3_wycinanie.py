import os

# import values
points = iface.mapCanvas().layers()[0] # index warstwy może ulec zmianie.
rastermap = '/home/jarekj/Documents/lubrza/landcover.tif'
distance = 1000
field = 'ID'
katalog=os.path.expanduser('~')+"/Documents"

extent_params = {'INPUT':rastermap,'OUTPUT':'TEMPORARY_OUTPUT'}
extent = processing.run("native:polygonfromlayerextent",extent_params)['OUTPUT']

# algorithm parameters
attribute_params = {'INPUT':points,
    'FIELD':field,
    'OPERATOR':0,
    'VALUE':'',
    'OUTPUT':'TEMPORARY_OUTPUT'}

location_params = {'INPUT':'',
    'PREDICATE':[6],
    'INTERSECT':extent,
    'OUTPUT':'TEMPORARY_OUTPUT'}

buffer_params = {'INPUT':'','DISTANCE':distance,
'SEGMENTS':1,'END_CAP_STYLE':2,'OUTPUT':'TEMPORARY_OUTPUT'}

clip_params = {'INPUT':rastermap,
    'MASK':'',
    'CROP_TO_CUTLINE':True,
    'DATA_TYPE':0,
    'OUTPUT':''}

# main loop
for feature in points.getFeatures():
    attribute_params['VALUE']=feature.id()
    buffer_params['INPUT'] = processing.run("native:extractbyattribute",attribute_params)['OUTPUT']
    location_params['INPUT']  = processing.run("native:buffer",buffer_params)['OUTPUT']
    extracted = processing.run("native:extractbylocation", location_params)['OUTPUT']
    if extracted.featureCount() ==1:
        clip_params['MASK'] = extracted
        clip_params['OUTPUT'] = "{}/{:03d}.png".format(katalog,feature.id())
        processing.run("gdal:cliprasterbymasklayer",clip_params)