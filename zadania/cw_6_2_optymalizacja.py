import os
import numpy as np
path = os.path.join(os.path.expanduser("~"),"Documents","skrypty_geoprzetwarzania")
punkty_adresowe = QgsVectorLayer(os.path.join(path,"punkty_adresowe.gpkg")+"|layername=punkty_adresowe","punkty","ogr")
nadajniki = QgsVectorLayer(os.path.join(path,"punkty_adresowe.gpkg")+"|layername=nadajniki","nadajniki","ogr")

total = 6000
nsteps = 100
min_ = 0.2
max_ = 0.6

def constrains(r,total,min=0,max=1):
    r = np.random.rand(3) * (max-min) + min
    r *= total/r.sum()
    return r 

def penalty(r):
    return r.std()

calc_param = {'INPUT':nadajniki,
    'FIELD_NAME':'distance',
    'FIELD_TYPE':0,
    'FORMULA':'', 
    'OUTPUT':'TEMPORARY_OUTPUT'}

def formula(r):
    return 'array_get(array({},{},{}),@row_number)'.format(*r)

buffer_params = {'INPUT':'',
    'DISTANCE':QgsProperty.fromExpression('"distance"'),
    'DISSOLVE':True,
    'OUTPUT':'TEMPORARY_OUTPUT'}

select_params = {'INPUT':punkty_adresowe,
    'PREDICATE':[6],
    'INTERSECT':'',
    'METHOD':0,
    'OUTPUT':'TEMPORARY_OUTPUT'}

max_gain = -1 # mała liczba liczba
best_distances = NULL
   
  
for i in range(nsteps):
    dm = np.random.rand(3)
    constr = constrains(dm,total,min_,max_)
    calc_param['FORMULA'] = formula(constr)
    distances = processing.run("native:fieldcalculator",calc_param)['OUTPUT']
    buffer_params['INPUT'] = distances
    buffer = processing.run("native:buffer", buffer_params)['OUTPUT']
    select_params['INTERSECT'] = buffer
    selected = processing.run("native:extractbylocation", select_params)['OUTPUT']
    count = selected.featureCount()
    gain = count-penalty(constr)
    if gain > max_gain:
        max_gain = gain
        best_distances = distances
        print("    {:.3f}".format(max_gain))

buffer_params['INPUT']=best_distances
buffer = processing.run("native:buffer", buffer_params)['OUTPUT']
QgsProject.instance().addMapLayer(buffer)
