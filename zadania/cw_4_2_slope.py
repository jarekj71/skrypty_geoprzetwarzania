import os

folder= "raster_folder"
destination = "slopes"
path = os.path.join(os.path.expanduser("~"),"Documents","skrypty_geoprzetwarzania",folder)
os.chdir(path)

lista = os.listdir(".")
lista = [l for l in lista if l.endswith("tif")]

if not os.path.exists(destination):
    os.mkdir(destiantion)

    
for rast in lista:
    raster = QgsRasterLayer(rast)
    print(raster.dataProvider().dataType(1))
    print(raster.crs().authid())
    print(raster.crs().isGeographic())

slope_params = {
    'INPUT':'',
    'OUTPUT':''
}

repro_params = {'INPUT':'',
    'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:2180'),
    'RESAMPLING':1,
    'NODATA':None,
    'TARGET_RESOLUTION':30,
    'OUTPUT':'TEMPORARY_OUTPUT'}



for rast in lista:
    raster = QgsRasterLayer(rast)
    if raster.dataProvider().dataType(1) != Qgis.DataType.Byte:
        if raster.crs().isGeographic():
            repro_params['INPUT'] = rast
            reprojected = processing.run("gdal:warpreproject", repro_params)['OUTPUT']
            slope_params['INPUT'] = reprojected
        else:
            slope_params['INPUT'] = rast
        slope_params['OUTPUT'] = os.path.join(destination,"slope_"+rast)
        processing.run("native:slope", slope_params)