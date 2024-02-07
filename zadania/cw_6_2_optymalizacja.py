import os
import numpy as np
path = os.path.join(os.path.expanduser("~"),"Documents","skrypty_geoprzetwarzania")
punkty_adresowe = QgsVectorLayer(os.path.join(path,"punkty_adresowe.gpkg")+"|layername=punkty_adresowe","punkty","ogr")
nadajniki = QgsVectorLayer(os.path.join(path,"punkty_adresowe.gpkg")+"|layername=nadajniki","nadajniki","ogr")

total = 5000
nsteps = 100

calc_param = {'INPUT':nadajniki,
    'FIELD_NAME':'distance',
    'FIELD_TYPE':0,
    'FORMULA':'rand(500,2000)', # prosta wartość losowa
    'OUTPUT':'TEMPORARY_OUTPUT'}

buffer_params = {'INPUT':'',
    'DISTANCE':QgsProperty.fromExpression('"distance"'),
    'DISSOLVE':True,
    'OUTPUT':'TEMPORARY_OUTPUT'}

buffer_area_params = {'INPUT':'',
    'FIELD_NAME':'area',
    'FIELD_TYPE':0,
    'FORMULA':'$area',
    'OUTPUT':'TEMPORARY_OUTPUT'}

select_params = {'INPUT':punkty_adresowe,
    'PREDICATE':[6],
    'INTERSECT':'',
    'METHOD':0,
    'OUTPUT':'TEMPORARY_OUTPUT'}

min_cost = 100000000000 # duża liczba
best_distances = NULL


def formula(total):
    r = np.random.rand(3)
    r *= total/r.sum()
    return 'array_get(array({},{},{}),@row_number)'.format(*r)
   
for i in range(nsteps):
    calc_param['FORMULA'] = formula(total)
    distances = processing.run("native:fieldcalculator",calc_param)['OUTPUT']
    buffer_params['INPUT'] = distances
    buffer = processing.run("native:buffer", buffer_params)['OUTPUT']
    buffer_area_params['INPUT'] = buffer
    buffer = processing.run("native:fieldcalculator",buffer_area_params)['OUTPUT']
    select_params['INTERSECT'] = buffer
    selected = processing.run("native:extractbylocation", select_params)['OUTPUT']
    count = selected.featureCount()
    area = buffer.getFeature(1)['area']
    cost = area/count
    print(count,area,cost)
    if cost < min_cost:
        min_cost = cost
        best_distances = distances
        print("    {:.3f}".format(min_cost*1000))

buffer_params['INPUT']=best_distances
buffer = processing.run("native:buffer", buffer_params)['OUTPUT']
QgsProject.instance().addMapLayer(buffer)