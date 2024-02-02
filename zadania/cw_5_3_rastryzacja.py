import os
import math
path = os.path.join(os.path.expanduser("~"),"Documents","skrypty_geoprzetwarzania")
os.chdir(path)
folder= "vector_folder"
os.chdir(folder)

lista = os.listdir(".")
lista = [l for l in lista if l.endswith("gpkg")]


vect_params = {'INPUT':'',
    'BURN':1,
    'UNITS':1,
    'WIDTH':'', #wyliczane
    'HEIGHT':'',
    'EXTENT':'',
    'NODATA':0,
    'OUTPUT':''}


type = QgsWkbTypes.PolygonGeometry

for vect in lista:
    vector = QgsVectorLayer(vect)
    if vector.geometryType() == type: # tylko poligony
        # extent
        poly_area = vector.getFeature(1).geometry().area()
        bbox = vector.getFeature(1).geometry().boundingBox()
        bbox_size = (bbox.width()+bbox.height())/4 # średnia przez 2
        bbox_area = bbox.area()
        size = bbox_size * (poly_area/bbox_area)
        extent = bbox.buffered(size)
    else:
        extent = vector.getFeature(1).geometry().boundingBox()
    # resolution
    res = round(math.sqrt(extent.area()/1000000))
    # params
    vect_params['WIDTH'] = res
    vect_params['HEIGHT'] = res
    vect_params['EXTENT'] = extent
    # input and output 
    vect_params['INPUT'] = vect
    vect_params['OUTPUT'] = vect[:-4]+"tif"
    processing.run("gdal:rasterize",vect_params)
        

