import os

destination = os.path.join(os.path.expanduser("~"),"Documents","sym")
point_layer = "probkowanie.gpkg"

path = os.path.join(os.path.expanduser("~"),"Documents","skrypty_geoprzetwarzania")
os.chdir(path)
points = QgsVectorLayer(point_layer)

ext = points.extent()

iparams = {'SHAPES':points,
    'FIELD':'SAMPLE_1',
    'NPMIN':5,
    'NPMAX':20,
    'NPPC':5,
    'K':140,
    'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX':ext,
    'TARGET_USER_SIZE':100,
    'TARGET_USER_FITS':0,
    'TARGET_OUT_GRID':''}
    
pparams = {'INPUT':points,
    'METHOD':1,
    'NUMBER':80,
    'OUTPUT':'TEMPORARY_OUTPUT'}

for i in range(20):
    randomed = processing.run("native:randomextract", pparams)
    iparams['SHAPES'] = randomed['OUTPUT']
    iparams['TARGET_OUT_GRID'] = os.path.join(destination,'s{:03d}.sdat'.format(i)) # musi być ścieżka bezwzględna
    dem = processing.run("saga:interpolatecubicspline",iparams)
    
lista = os.listdir(folder)
files = [l for l in lista if l.endswith(".sdat")]
files.sort()

fullpath_list = [os.path.join(folder,l) for l in files]


listparam = {'INPUT':fullpath_list,
    'STATISTIC':'',
    'IGNORE_NODATA':True,
    'REFERENCE_LAYER':fullpath_list[0],
    'OUTPUT':'TEMPORARY_OUTPUT'}


listparam['STATISTIC'] = 2 # srednia
mean = processing.runAndLoadResults("native:cellstatistics",listparam)

listparam['STATISTIC'] = 4 # odchylenie 
std = processing.runAndLoadResults("native:cellstatistics",listparam)