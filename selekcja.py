# GPKG - plik zawiera kilka warstw. 

#parametry przekazywane do skryptu. Mogą być dowolnie zmieniane
source_file = '/home/jarekj/BACKUP/geodata/Poznan/dane_skrypty_przetwarzania/POLSKA/urban_atlas_espg3035/poznan_ua2018/Data/PL005L2_POZNAN_UA2018_v013.gpkg'
data_layer = 'PL005L2_POZNAN_UA2018'
mask_layer = 'PL005L2_POZNAN_UA2018_UrbanCore'

selected_areas_codes = '21000, 22000, 23000, 24000, 13400' # jako tekst
attached_areas_codes = '11100, 11210, 11220, 11230, 11240'
detached_areas_codes = '12230'
attached_buffer = 200
detached_buffer = 250
min_area=10

######


# słownik wykorzystuje mechanizmy przekazywania paremetrów **
params = {'INPUT':"{}|layername={}".format(source_file,data_layer),
'OVERLAY':"{}|layername={}".format(source_file,mask_layer),
'OUTPUT':'TEMPORARY_OUTPUT'}

clipped = processing.run("native:clip", params)

# Jeżli utworzyliśmy temporary_output, wyniki są przechowywane w słowniku,w polu 'OUTPUT'
# możemy go wyświelić, aby sprawdzić wyniki:

## NOT RUN:
# QgsProject.instance().addMapLayer(clipped['OUTPUT'])
###

#Extract by parameters: ten słownik można użyć kilka razy
params =  {'INPUT':clipped['OUTPUT'],
'EXPRESSION':' "code_2018" IN ({})'.format(selected_areas_codes),
'OUTPUT':'TEMPORARY_OUTPUT'}

selected_areas = processing.run("native:extractbyexpression",params)

params['EXPRESSION'] = ' "code_2018" IN ({})'.format(attached_areas_codes)
attached_areas = processing.run("native:extractbyexpression",params)

params['EXPRESSION'] = ' "code_2018" IN ({})'.format(detached_areas_codes)
detached_areas = processing.run("native:extractbyexpression",params)

#Buforowanie.Ponownie słownik można użyć kilka razy

params = {'INPUT':attached_areas['OUTPUT'],
'DISTANCE':attached_buffer,
'DISSOLVE':True,
'OUTPUT':'TEMPORARY_OUTPUT'}
attached_buffer = processing.run("native:buffer",params)

params['DISTANCE'] = detached_buffer
params['INPUT'] = detached_areas['OUTPUT']
detached_buffer = processing.run("native:buffer",params)

#overlays

params = {'INPUT':selected_areas['OUTPUT'],
'OVERLAY':attached_areas['OUTPUT'],
'OUTPUT':'TEMPORARY_OUTPUT'}

interesection = processing.run("native:intersection",params)

params['INPUT'] = intersection['OUTPUT']
params['OVERLAY'] = detached_areas['OUTPUT']

difference = processing.run("native:difference",params)

params = {'INPUT':difference['OUTPUT'],
'OUTPUT':'TEMPORARY_OUTPUT'}

single = processing.run("native:multiparttosingleparts",params)

params =  {'INPUT':single['OUTPUT'],
'EXPRESSION':'($area/10000) > {}'.format(min_area),
'OUTPUT':'TEMPORARY_OUTPUT'}

result = processing.run("native:extractbyexpression",params)
QgsProject.instance().addMapLayer(result['OUTPUT'])