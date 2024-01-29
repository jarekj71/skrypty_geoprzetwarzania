# Iteracyjne przetwarzanie katalogów

## Wiedza i umiejętności
W ramach zajęć umiejętności iteracyjnego przetwarzania obiektów w warstwie zostaną rozbudowane o umiejętności przetwarzania zawartości folderów (katalogów). W ramach zajęć zostaną przedstawione metody warstw wektorowych i rastowych pozwalające na pozyskanie podstawowych informacji na temat zawartości danej warstwy. Ćwiczenie wymaga wcześniejszego zapozania się z narzędziami Pythona przeznaczonymi do obsługi scieżek, plików i katalogów (biblioteka `os`).

## Zakres zajęć
Zajęcia są podzielone na trzy osobne ćwiczenia, dotyczące plików wektorowych, rastrowych oraz zapisu informacji do plików zewnętrznych. Umiejętności obejmują:
* przetwarzanie sekwencji plików (rastrowych i wektorowych)
* filtrowanie plików na podstawie nazw, rozszerzeń oraz właściwości geoprzestrzennych
* rozpozawanie typów danych dla których operacja nie może być wykonywana
  * filtrowanie danych
  * konwersja danych do formatów dla których operacja jest dozwolona
* łączenie inormacji o plikach i zapis do zewnętrznych formatów

## Cele geoinformacyjne ćwiczeń
Wspólnym celem wszystkich ćwiczeń jest zastosowanie zestawu operacji do sekwencji plików o dowolnej wielkości. Osiągnięcie celu wymaga zbudowania narzędzi, z których każdy będzie pozwalało na:

* wskazanie katalogu
* utworzenie nowego katalogu
* wskazania kryterium filtrowania danych
* zdefiniowanie nazwy wyjściowej na podstawie nazwy wejściowej

### Ćwiczenie 1
Zbudować skrypt, który dokona konwersji zbioru danych wektorowych do formatu rastrowego. Elementem skryptu jest filtrowanie na podstawie cech geoprzestrzennych i usuwanie danych nie spełniających wymogu. Skrypt powinien przkształcać wyłącznie warstwy zawierające poligony o powierzchni nie mniejszej niż 1km<sup>2</sup>. Dodatkowo, skrypt powienien rozszerzyć zasięg pliku rastrowego.

### Ćwiczenie 2
Zbudować skrypt, który wyliczy nachylenie stoków z katalogu plików rastrowych. Elementem sktyptu jest alternatywna scieżka realizacji w przypadku wykrycia problemów. Skrypt powinien pomijać pliki, które zawierają dane kategoryzowane (Byte) oraz w przypadku wykrycia układu bez projekcji  geodezyjnej (geograficznego), np. wgs84 dokonać jego automatycznej konwersji do wybranego układu.

### Ćwiczenie 3
Zbudować skrypt, który pobierze podstawowe infromacje statystyczne na temat modeli wysokościowych z katalogu użytego w poprzednim ćwiczeniu u zapisze je w postaci tabeli. Dodatkowo skrypt powinien pominąć pliki zapisane w układzie geograficznym i zawierające dane kategoryzowane.

## Dane i algorytmy geoprzetwwarzania
Katalogi z danymi do wykonania ćwiczeń znajdują się pod adresem:
https://uam-my.sharepoint.com/:u:/g/personal/jarekj_amu_edu_pl/EZq1fSAq8-1Hqwkijo8Wm6IByK7sEG6IGN-Yt7qGMv0Sqw?e=TVuvYr

Do zrealizowania zadań będą potrzebne następujące narzędzia i algorytmy:

* biblioteka `os` do zarządzania plikami i katalogami
* biblioteka `core` Qgis, metody klas `QgsRasterLayer`, `QgsVectorLayer` i klasy nadrządnej `QgsMapLayer`. Dodatkowo, wykorzystane zostaną wybrane metody klasy `QgsRasterDataProvider` i `QgsRasterBandStats`
* `gdal:rasterize` do przekształcenia danych wektorowych w rastrowe
* `gdal:warpproject` do zamiany projekcji z jednego układu do drugiego
* `native:slope` do wyliczenia nachylenia stoków
* biblioteka `pandas`, w celu exportu pliku tekstowego

### Wybrane metody klasy `QgsMapLayer`, wspólne dla obu typu danych.

Metody te można wywoływać zarówno dla warstwy wektorowej jak i rastrowej. Pozwalają na pozyskanie podstawowych informacji o warstwach:

* `layer.id()` - zwraca identyfikator warstwy
* `layer.name()` - zwraca nazwę warstwy
* `layer.crs()` - zwraca układ osniesienia
  * `.crs().isGeographic()` - zwraca informację czy nadana jest projekcja geodezyjna (False) czy nie (True)
  * `.crs().authid()` - zwraca nazwę bazy danych projekcji i jej identyfikator
* `layer.type()` - zwraca typ warstwy (wektor lub raster)
* `layer.source()` - źródło warstwy (np. nazwa pliku)
* `layer.extent()` - obiekt `QgsRectangle` opisujący zakres warstwy
  * `.xMinimum()`, `.xMaximum()`, `.yMinimum()`, `.xMaximum()` - odpowiednio wartości zasięgu

### Wybrane metody klasy `QgsVectorLayer`, niedostępne dla warstw rastrowych

Metody wywoływane dla warstwy wektorowej jak i obiektów wektorowych (features), pozyskanych wcześniej z warstwy wektorowej

* `vect_layer.featureCount()` - liczba obiektów
* `vect_layer.geometryType()` - zwraca typ geometrii: 0 point 1 linia 2 poligon
* `vect_layer.fields()`[0] - zwraca atrybut obiektu o indeksie 0
  * `field.name()`, `field.type()` - nazwa i typ pola
* `vect_layer.getFeatures()` - zwraca iterator obiektów warstwy wektorowej
* `vect_layer.getFeature(1)` - zwraca obiekt (feature) o indeksie 1. Obiekty są indeksowane od 1
  * `feature['LANDUSE']` - wartość pola o znanej nazwie w danym obiekcie
  * `feature[vect_layer.fields()[0].name()]` - wartość pola o znanym położeni w danym obiekcie
  * `feature.id()` - zwraca identyfikator obiektu. Obiekty są indeksowane od 1
  * `feature.geometry()` - zwraca geometrię obiektu
    * `geometry.area()` - powierzchnia obiektu
    * `geometry.length()` - długość obiektu

### Wybrane metody klasy `QgsRasterLayer`, niedostępne dla warstw wektorowych

Metody wywoływane dla warstwy rastrowej jak i obiektu dataProvider warstwy. Te ostatnie dotyczą poszczególnych pasm w pliku, gdyż typy pasm są od siebie niezależne.

`rast_layer.bandCount()` - liczba warstw w pliku
`rast_layer.width()`,`layer2.height()` - odpowiednio wysokość i szerokość
`rast_layer.dataProvider().dataType(1)` - typ danych warstwy pierwszej. Warstwy  liczymy od 1
`rast_layer.dataProvider().bandStatistics(1)` - statystyki warstwy pierwszej, dostępne mn: mean, stddev, minimumValue, maximumValue, 


## Ćwiczenie 1 Rastryzacja katalogu danych wektorowych
Katalog *vector_folder* zawiera 8 plików z poligonami oraz 1 plik z linią. Powierzchnia jednego z poligonów jest bardzo mała i ten plik również powinien być pominięty. Zasięg pliku rastrowego powinien być zwiększony o pewien bufor (1000m)  względem pliku wektorowego


### Parametry
Skrypt przyjmuje następujące parametry:
* folder z danymi
* zasięg bufora (m)
* rozdzielczość rastra
* minimalny obszar (km) dla którego robiona jest konwersja

```Python
import os
folder= "vector_folder"
buf = 1000
res=50
min_area = 100
```

### Obszar roboczy
Następnie tworzymy sieżkę dostępu na katalog z danumi i ustawiamy go jako obszar roboczy. Listę plików pobieramy poleceniem `os.listdir` i filtrujemy tak, aby pozostawić tylko pliki z rozszerzeniem *.gpkg*. 

```Python
path = os.path.join(os.path.expanduser("~"),"Documents","skrypty_geoprzetwarzania",folder)
os.chdir(path)

lista = os.listdir(".")
lista = [l for l in lista if l.endswith("gpkg")]
```
### Kryteria filtrowania
Aby można było pozyskać jakiekolwiek informacje na temat pliku geoprzestrzennego, musi on zostać wczytany jako obiekt geoprzestrzenny. Służy do tego klasa `QgsVectorLayer(vect)`, gdzie atrybutem (vect) jest scieżka dostępu do pliku.  Ponieważ aktywny jest nasz katalog roboczy zawarty w zmiennej *path* nazwa pliku jest jednocześnie ścieżką dostępu. 
Podstawą filtrowania na podstawie własności jest: 
* informacja na temat typu geometrii pliku, co możemy metodą:  `vector.geometryType()` 
* powierzchna pierwszego i jednyego obiektu w warstwie. (Dla uproszczenia pomijamy sprawdzanie liczbny features). Tę ostanią pozyskujemy złożoną scieżką obejmującą feature, jego geometrię oraz powierzchnię tej geometrii: vector.`getFeature(1).geometry().area()`, dla ułatwienia dzielmy przez 1000000 do km<sup>2</sup>.

```Python
for vect in lista:
    vector = QgsVectorLayer(vect)
    print(vect,vector.geometryType())
    print(vector.getFeature(1).geometry().area()/1000000)
```

Widzimy że jeden z plików posiada geometry type 1 (*QgsWkbTypes.LineGeometry*) a pozostałe 2 (*QgsWkbTypes.PolygonGeometry*). Również powierzchnia jednego z pliku jest o dwa rzędy wielości mniejsza niż pozostałych.


### Parametry rastryzacji
Do rastryzacji użyjemy algorytmu `gdal:rasterize`, który nie należy do natywnych algorytmów Qgis ale pochodzi od providera GDAL. Do procesu rastryzacji wystarczą następujące parametry:

```Python
vect_params = {'INPUT':'',
    'BURN':1,
    'UNITS':1,
    'WIDTH':res,
    'HEIGHT':res,
    'EXTENT':'',
    'NODATA':0,
    'OUTPUT':''}
```
W kolejnych krokach zmieniać się będą *INPUT*, *EXTENT*, zwiększany o stałą wartość oraz *OUTPUT*


### Zmiana zasięgu
W ramach przetwarzania katalogu założyliśmy że zasięg warstwy rastrowej będzie rozszerzony o stałą wartość względem zasięgu warstwy wektorowej. Niestety, Qgis nie dostarcza klasy do zarządzania zasięgiem a jedynie obiekt QgsRectangle. aby uzyskać zasięg jako łańcuch znaków, operację trzeba trzeba przeprowadzić ręcznie jako część pętli. Obiekt *e* to `QgsRectangle`, z którego trzeba pobrać współrzędne i odpowiednio dodać lub odjąć bufor.

```Python
e = vector.extent()
    extent ="{},{},{},{}".format(
        e.xMinimum()-buf,
        e.xMaximum()+buf,
        e.yMinimum()-buf,
        e.yMaximum()+buf)
```

### Wejście i wyjście
Jako wejścia używamy nazwy pliku gpkg, zawartej w zmiennej *vect*,  a nie wewnętrznej warstwy wetktorowej. Nazwę pliku wyjściowego uzyskujemy poprzez wycięcie z łańcucha nazwy pliku wejściowegowszystkich znaków za wyjątkiem ostatnich 4 czyli rozszerzenia *gpkg*. Kropkę pozostawiamy. Następnie dodajemy rozszerzenie *tif*, w jaki zostanie zapisany plik wyściowy. Jest to metoda uproszczona, gdyż skrypt zakłada jedynie działanie z plikami *gpkg*.

```Python
vect_params['OUTPUT'] = vect[:-4]+"tif"
```


### Pętla główna
Pętla główna przechodzi przez wszystkie pliki *gpkg*,  
1. wczytuje je jako warstwę wektorową
2. sprawdza typ geometrii, jeżeli poligon:
3. sprawdza powierzchnię poligonu, jeżeli większa niż 100:
4. wylicza nowy extent
5. Przypisuje parametry INPUT, EXTENT i OUTPUT.
6. Uruchamiamy algorytm `gdal:rasterize` z aktualnymi parametrami.

Pętla wykonuje się tylko dla 7 z 9 plików. Pomijana jest linia oraz plik, gdzie poligon ma mniej niż 100km<sup>2</sup>

Kod głównej pętli skryptu:

```Python
for vect in lista:
    vector = QgsVectorLayer(vect) #1
    if vector.geometryType() == type: #2 tylko poligony
        area = vector.getFeature(1).geometry().area()/1000000 # km2
        if area > min_area: #3 tylko duże
            e = vector.extent() #4
            extent ="{},{},{},{}".format(
                e.xMinimum()-buf,
                e.xMaximum()+buf,
                e.yMinimum()-buf,
                e.yMaximum()+buf)
            vect_params['INPUT'] = vect #5
            vect_params['EXTENT'] = extent
            vect_params['OUTPUT'] = vect[:-4]+"tif" # usunięcie rozszerzenia i kropki
            processing.run("gdal:rasterize",vect_params) #6
```

## Ćwiczenie 2 Wyliczenie nachylenia stoków dla wybranych plików
Katalog *raster_folder* zawiera 10 plików: 8 z cyfrowym modelem wysokości, 1 z kategoryzowaną mapą geologiczną i 1 z cyfrowym modelem wysokości ale w układzie WGS84. Zadaniem skryptu jest przetworzyć modele wysokościowe do map stoków. W przypadku modelu WGS84 należy wcześniej dokonać reprojekcji do układu '92.

### Parametry: katalog docelowy
Plik zawiera tylko dwa parametry: katalog z danymi i katalog docelowy. Katalog docelowy musi być utworzony, jeżeli nie istnieje. Pozostałe kroki nie różnią się od poprzedniego zadania, poza tym, że kryterium filtrowania jest rozszerzenie *tif*.

```Python
import os

folder= "raster_folder"
destination = "slopes"
path = os.path.join(os.path.expanduser("~"),"Documents","skrypty_geoprzetwarzania",folder)
os.chdir(path)

lista = os.listdir(".")
lista = [l for l in lista if l.endswith("tif")]

if not os.path.exists(destination):
    os.mkdir(destiantion)
```

### Kryteria filtrownia
Podobnie jak w przypadku warstwy wektorowej, podstawą uzyskania informacji przestrzennej jest wczytanie jej jako warstwy rastrowej, służy do tego klasa `QgsRasterLayer()`. Zastosowane zostaną dwa kryteria filtrowania: typ danych oraz projekcja.

* Typ danych. Celem filtra jest oddzielenie danych zawierających kategorie (type Byte) od danych zawierających wartości. Informacja na temat typu danych jest pozyskiwana dla każdego pasma (*band*). Numeracja pasm zaczyna się od 1. Informacja o typie danych nie jest metodą `QgsRasterLayer` ale klasy `QgsRasterDataProvider`, którą pozyskujemy metodą `.dataProvider()` dla warstwy rastrowej.

  > dataProvider to struktura danych odpowiedzialna za obsługę źródła danych. W przypadku danych rastrowych jest to biblioteka **GDAL**. 

* Projekcja. Celem filtra jest identyfikacja warstw nie posiadających projekcji geodezyjnej (w jednostkach długości) tylko geograficzną (w stopniach). Służy do tego metoda `.crs()`, zwracająca obiekt `QgsCoordinateReferenceSystem`. Informację na temat kodu EPSG można pozyskać metodą `.crs().authid()`, ale lepiej stosować metodę `.crs().isGeographic()`, która zwraca *True*, jeżeli warstwa posiada projekcę geograficzną. 

Poniższy kod pozwala na przegląd właściwości poszczególnych plików.
  
```Python
for rast in lista:
    raster = QgsRasterLayer(rast)
    print(raster.dataProvider().dataType(1))
    print(raster.crs().authid())
    print(raster.crs().isGeographic())
```

Typem danych właściwym dla danych kategoryzowanych jest typ `Byte`. Jest on przechowywany w stałej ```Qgis.DataType.Byte```. Inne typy całkowite to Int16, Int32, UInt16, UInt32 oraz Float32 i Float64. Ponadto stosowane są typy urojone (complex), które nas nie interesują.


### Parametry algorytmów slope i warpreproject
Głównym algorytmem geoprzetwarzania skryptu jest `native:slope`, który posiada tylko dwa parametry: INPUT i OUTPUT. Parametr INPUT to nazwa pliku wejściowego, OUTPUT to nazwa pliku wyjściowego, tworzona na podstawie wejściowego, z dodaniem katalogu docelowego (zdefiniowanego w zmiennej *destination*) oraz przdrostka slope:

```Python
output = os.path.join(destination,"slope_"+rast)
```

Lista parametrów `gdal:warpreproject` jest dłuższa. Istotne są TARGET_RESOLUTION (rozdzielczość) oraz TARGET_CRS. pierwszy ustawimy na 30 (m) drugi na `QgsCoordinateReferenceSystem('EPSG:2180')`. Parametr RESAMPLING można pozostawić domyślny (0) lub ustawić na dowolny inny (1-11). Więcej na temat metod resamplingu. Więcej: [https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/gdal/rasterprojections.html] oraz: [https://gdal.org/programs/gdalwarp.html] w sekcji resampling_methods.

Jako output użyjemy 'TEMPORARY_OUTPUT', gdyż pośredniego wyniku reprojekcji nie zamierzamy zachowywać.

```Python
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
```

### Główna pętla skryptu.
Główna pętla przechodzi przez wszystkie pliki *tif* i wykonuje następujące zadania:
1. wczytuje je jako warstwy rastrowe
2. sprawdza typ danych jeżeli i jeżeli nie jest to *Byte*:
3. Dokonuje rozgałęzienia:
4. Jeżeli projekcja jest geograficzna:
   1. plik staje się wejściem dla parametrów reprojekcji
   2. wykonuje reprojekcję
   3. wynik reprojekcji jest wejściem do obliczenia nachylenia stoków
5. Jeżeli projekcja nie jest geograficzna:
  1. plik staje się wejściem dla parametrów rnachylenia stoków.
6. Wyznacza scieżkę i nazwę pliku docelowego
7. Wylicza nachylenie stoków
   
```Python
for rast in lista:
    raster = QgsRasterLayer(rast) #1
    if raster.dataProvider().dataType(1) != Qgis.DataType.Byte: #2
        if raster.crs().isGeographic(): #3
            repro_params['INPUT'] = rast #4.1
            reprojected = processing.run("gdal:warpreproject", repro_params) ['OUTPUT'] #4.2
            slope_params['INPUT'] = reprojected #4.3
        else:
            slope_params['INPUT'] = rast #5.1
        slope_params['OUTPUT'] = os.path.join(destination,"slope_"+rast) #6
        processing.run("native:slope", slope_params) #7
```

## Ćwiczenie 2 Wyliczenie podstawowych statystyk i zapis do zewnętrznego pliku
Zadanie wykorzystuje katalog *raster_folder* z poprzedniego ćwiczenia. W ramach zadania pomijamy zarówno plik z danymi kategoryzowanymi jak i ten z projekcją WGS84, zawierający dane typu Int16. 

Podobnie jak w poprzednich zadaniach należy ustawić ścieżkę do katalogu roboczego oraz przefiltrować listę w celu pozostawienia plików z rozszerzeniem *tif*. Dodatkowo, zostanie zaimportowana biblioteka `pandas`, która ostanie użyta w celu exportu wyników do pliku *csv*

```Python
import pandas as pd
import os
folder= "raster_folder"
path = os.path.join(os.path.expanduser("~"),"Documents","skrypty_geoprzetwarzania",folder)
os.chdir(path)
lista = os.listdir(".")
lista = [l for l in lista if l.endswith("tif")]
```

### Wyliczenie statystyk
Kolejnym krokiem jest zainicjowanie pustych list, do których będą dodwane statyski rastrów.

```Python
means = []
stddevs = []
mins = []
maxes = []
rasts = []
```

Statystki rastra wymagają utworzenia obiektu `QgsRasterBandStats`, który przechowuje podstawowe statstyki: mean, stddev, minimumValue, maximumValue czy range. Statystyki nie są metodami, ale atrybutami klasy, czyli do ich wywołania nie stosujemy nawiasów: ```stats.minimumValue```.

Obiekt `QgsRasterBandStats` jest tworzony metodą `.dataProvider().bandStatistics(1)`, gdzie 1 to numer pasma. Numeracja pasm zaczyna się od 1. 

> **UWAGA:** metoda `.bandStatistics()`, nie jest metodą klasy `QgsRasterDataProvider`, ale klasy `QgsRasterInterface` i tam jest też opisana.

### Główna pętla skryptu
Główna pętla przechodzi przez wszystkie pliki *tif* i wykonuje następujące zadania:

1. wczytuje je jako warstwy rastrowe
2. sprawdza czy projekcję plików i typ danych
3. Tworzy obiekt `QgsRasterBandStats` ze statystykami
4. dodaje do list odpowiednie statystyki...
5. ...oraz nazwę pliku bez rozszerzenia i kropki

```Python
for rast in lista:
    raster = QgsRasterLayer(rast) #1
    if (not raster.crs().isGeographic()) and (not raster.dataProvider().dataType(1) == Qgis.DataType.Byte): #2
        stats = raster.dataProvider().bandStatistics(1) #3
        means.append(stats.mean) #4
        stddevs.append(stats.stdDev)
        mins.append(stats.minimumValue)
        maxes.append(stats.maximumValue)
        rasts.append(rast[:-4]) #5 usuwamy tif i kropkę, dlatego -4
```


Po zakończeniu pętli głównej tworzony jest słownik, gdzie kluczem jest nazwa statystyki a wartościami lista ze statystykami. Kolumna index zawiera nazwy pliku. W ostatnim krokiem słownik konwertowany jest do struktury *DataFrame* biblioteki `pandas` i eksporowany do pliku csv, w katalogu nadrzędym *".."* względem katalogu z którego wczytywane są rastry. 

```Python
stats = {'index':rasts,'means':means,'stddevs':stddevs,'mins':mins,'maxes':maxes}
pd.DataFrame(stats).to_csv(os.path.join("..","stats.csv"))
```
