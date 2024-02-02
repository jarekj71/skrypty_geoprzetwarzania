import os
path = os.path.join(os.path.expanduser("~"),"Documents","skrypty_geoprzetwarzania")
os.chdir(path)

point_layer = "random.gpkg"


matrix_params = {'INPUT':point_layer,
'TARGET':point_layer,
'MATRIX_TYPE':2, # statystyki
'INPUT_FIELD':'fid',
'TARGET_FIELD':'fid',
'OUTPUT':'TEMPORARY_OUTPUT'}

stats = processing.run("qgis:distancematrix", matrix_params)['OUTPUT']

buffer_params = {'INPUT':stats,
'DISTANCE':QgsProperty.fromExpression('"MIN"'),
'OUTPUT':'TEMPORARY_OUTPUT'}

buffers = processing.run("native:buffer",buffer_params)['OUTPUT']

QgsProject.instance().addMapLayer(buffers)