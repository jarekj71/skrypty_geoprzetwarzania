import os
folder= "vector_folder"
buf = 1000
res=50
minarea = 100

path = os.path.join(os.path.expanduser("~"),"Documents","skrypty_geoprzetwarzania",folder)
os.chdir(path)

lista = os.listdir(".")
lista = [l for l in lista if l.endswith("gpkg")]

### NOT RUN
''' 
for vect in lista:
    vector = QgsVectorLayer(vect)
    print(vect,vector.geometryType())
    print(vector.getFeature(1).geometry().area()/1000000)
''' # END NOT RUN    


vect_params = {'INPUT':'',
    'BURN':1,
    'UNITS':1,
    'WIDTH':res,
    'HEIGHT':res,
    'EXTENT':'',
    'NODATA':0,
    'OUTPUT':''}


type = QgsWkbTypes.PolygonGeometry

for vect in lista:
    vector = QgsVectorLayer(vect)
    if vector.geometryType() == type: # tylko poligony
        area = vector.getFeature(1).geometry().area()/1000000 # km2
        if area > 100: # tylko duże
            e = vector.extent()
            extent ="{},{},{},{}".format(
                e.xMinimum()-buf,
                e.xMaximum()+buf,
                e.yMinimum()-buf,
                e.yMaximum()+buf)
            vect_params['INPUT'] = vect
            vect_params['EXTENT'] = extent
            vect_params['OUTPUT'] = vect[:-4]+"tif" # usunięcie rozszerzenia i kropki
            processing.run("gdal:rasterize",vect_params)
