import os
path = os.path.join(os.path.expanduser("~"),"Documents","skrypty_geoprzetwarzania")
os.chdir(path)

buffer = 100
point_layer = "punkty_adresowe.gpkg"
ncols = 21
nrows=30

points = QgsVectorLayer(point_layer)

e = points.extent()
e_buf = e.buffered(100)

xsize = e_buf.width()/ncols
ysize = e_buf.height()/nrows

grid_params = {'TYPE':2,
    'EXTENT':e_buf,
    'HSPACING':xsize,'VSPACING':ysize,
    'CRS':points.sourceCrs(),
    'OUTPUT':'TEMPORARY_OUTPUT'}

grid = processing.run("native:creategrid", grid_params)

point_params = {'POLYGONS':grid['OUTPUT'],
    'POINTS':points,
    'FIELD':'NUMPOINTS',
    'OUTPUT':'TEMPORARY_OUTPUT'}

counted = processing.run("native:countpointsinpolygon", point_params)
QgsProject.instance().addMapLayer(counted['OUTPUT'])


