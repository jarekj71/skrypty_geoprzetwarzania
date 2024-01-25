import pandas as pd
folder= "raster_folder"
path = os.path.join(os.path.expanduser("~"),"Documents","skrypty_geoprzetwarzania",folder)
os.chdir(path)
lista = os.listdir(".")
lista = [l for l in lista if l.endswith("tif")]

means = []
stddevs = []
mins = []
maxes = []
rasts = []

for rast in lista:
    raster = QgsRasterLayer(rast)
    if (not raster.crs().isGeographic()) and (not raster.dataProvider().dataType(1) == Qgis.DataType.Byte):
        stats = raster.dataProvider().bandStatistics(1)
        means.append(stats.mean)
        stddevs.append(stats.stdDev)
        mins.append(stats.minimumValue)
        maxes.append(stats.maximumValue)
        rasts.append(rast[:-4]) # kropkę zostawiamy usuwamy tylko gpkg

stats = {'index':rasts,'means':means,'stddevs':stddevs,'mins':mins,'maxes':maxes}
pd.DataFrame(stats).to_csv(os.path.join("..","stats.csv"))