# Automatyczny dobór parametrów algorytmów

## Wiedza i umiejętności
W ramach zajęć wiedza i umiejętności na temat pisania skryptów zostaną rozszerzone o automatyczny dobór parametrów wybranych algorytmów. Wybrane parametry nie będą ustawiane wyłącznie na podstawie zmiennych wskazanych przez użytkownika ale wpływ na wartości paramterów będą miały wyniki przetwarzania wstępnego danych. Innymi słowy, zamiast ustawiać parametry globalnie, tak że w każdym kroku będą działały tak samo, jako dane wejściowe do skryptu można podać zestaw reguł, które pozwolą wyznaczyć parametry algorytmu dla każdego przypadku danych indywidualnie. Tego typu zadania nie są zreguły smodzielnymi skryptami, ale częścią większych zadań. Ćwiczenie wymaga podstawowej wiedzy na temat metod wykonywania obliczeń w języku Python.

## Zakres zajęć
Zajęcia podzielone są na trzy osobne ćwiczenia dotyczące obliczenia i wykorzystania indywidualnych wartości zapisanych w pliku, doboru wielkości oczek siatki do zakresu danych oraz doboru parametrów rastryzacji

Umiejętności obejmują:

* zstosowanie klasy QgsProperty do wykorzystywania wyrażeń jako parametrów algorytmu
* pozyskiwanie danych z zasięgu warstwy do wyliczania parametrów algorytmu
* zmiana zasięgu nowej warstwy na podstawie danych
* pozyskiwania innych parametrów statysytcznych do wyliczania parametrów algorytmu

## Cele geoinformacyjne ćwiczeń
Wspólnym celem wszystkich ćwiczeń jest wykorzystanie możliwości indywidualnego dostosowania parametrów poszczególnych algorytmów dla każdego kroku iteracji. Osiągnięcie celu wymaga zbudowania narzędzi, z których każde będzie pozwalało na uzyskanie wyników zależnych od danych wejściowych.

### Ćwicznie 1
Zbudować sktypt, który dla zbioru danych punktowych, wyznaczy bufory dla każdego punktu, tak aby w obrębie buforów nie było innych punktów

### Ćwiczenie 2
Zbudować skrypt, który dokona próbkowania ilości punktów w oczkach siatki i przypisze wyniki do poszczwególnych oczek. Skrypt musi zbudować siatkę na podstawie zasięgu warstwy punktowej, ale do zdefiniowania siatki używamy informacji na temat ilości wierszy i kolumn, co nie jest możliwe w standardowym algorytmie

### Ćwiczenie 3
Zbudować skrypt, który dokona rastryzacji danych wektorowych (użytych w poprzednim ćwiczeniu). Proces rastryzacji będzie wymagał automatycznego doboru zasięgu nowej warstwy wyliczaniej na podstawie złożoności rastryzowanego obiektu oraz rozdzielczości dostosowanej do wielkości nowo tworzonej warstwy.

## Dane i algorytmy geoprzetwwarzania
Dane znajdują się...

Do zrealizowania zadań będą potrzebne następujące narzędzia i algorytmy:

* biblioteka `math` (obliczenie pierwiastka)
* biblioteka `core` Qgis, metody klas `QgsProperty`, `QgsVectorLayer`, `QgsRasterLayer`, `QgsRectancle` (zasięg warstwy)
* `native:distancematrix` do obliczenia odległości miedzy punktami
* `native:buffer` do wyznaczenia buforów o zmiennym zasięgu
* `native:creategrid`, do utworzenia siatki
* `native:countpointsinpolygon`, do policzenia ilości punktów w każdym z oczek siatki
* `gdal:rasterize`, do zamiany pliku wektorowego na rastrowy

## Ćwiczenie 1 
 
Plik *random.gpkg* zawiera 20 losowo rozmieszczonych punktów. Celem zadania jest wykonanie indywidualnych buforów dookoła każdego z punktów, tak aby w każdym z nich nie było innych punktów. Oznacza to, że parametr **DISTANCE** dla każdego z buforów musi być dobrany indywidualnie, a dokładnie jest to minimalna odległość do pozostałych punktów. Samo zadanie nie wymaga osobnego skryptu a jedynie użycia dwóch algorytmów: `native:distancematrix ` i `native:buffer`. 

Pierwszy algorytm pozwala na obliczenie wzajemnych odległości między punktami, w tej wersji są to głowne satystyki rozkładu **MATRIX_TYPE** = 2. Wskazać jedynie należy że wersja skryptowa algorytmu wymaga jawnego podania pola grupującego, względem którego obliczne są statystyki, w tym wypadku będzie to unikalne pole *"fid"*. 

 ```Python
 matrix_params = {'INPUT':point_layer,
'TARGET':point_layer,
'MATRIX_TYPE':2, # statystyki
'INPUT_FIELD':'fid',
'TARGET_FIELD':'fid',
'OUTPUT':'TEMPORARY_OUTPUT'}

stats = processing.run("qgis:distancematrix", matrix_params)['OUTPUT']
 ```

Drugim algorytmem jest poznany już `native:buffer`. Jedyną różnicą względem stosowanych dotychczas metod jest sposób definiowania parametru distance jako metody `fromExpression()` klasy `QgsProperty`. W tym wypadku ograniczoną do podania nazwy pola *'MIN'*. Może tam być stosowane dowolne wyrażenie, również odwołujące się do innych warstw. Jako warstwy wejściowej użyjemy pozyskanej w poprzednim kroku warstwy *stats*.

 ```Python
 buffer_params = {'INPUT':stats,
'DISTANCE':QgsProperty.fromExpression('"MIN"'),
'OUTPUT':'TEMPORARY_OUTPUT'}

buffers = processing.run("native:buffer",buffer_params)['OUTPUT']
 ```

Pełny kod skryptu znajduje się [tutaj](zadania/cw_5_1_odleglosci.py).

## Ćwiczenie 2 Utworzenie siatki wektorowej na podstawie zadanej ilości oczek

Algorytm tworzenia siatki wektorowej wymaga podania wielkości oczka w jednostkach długości. Jeżeli tworzona siatka ma być dostosowana do zasięgu innej warstwy a jej rozmiar ma być podany w ilości oczek, należy ręcznie przeliczyć oczekiwaną wielkość na wymiary oczek. Do wykoania ćwiczenia zostanie użyty plik *punkty_adresowe.gpkg*, dla kórego ma zostać utworzona siatka o wymiarach 21 na 30 oczek w zasięgu większym o 100 metrów od istniejącego. 

```Python
point_layer = "punkty_adresowe.gpkg"
buffer = 100
ncols = 21
nrows=30
```
Aby zwięszyć zasięg można utworzyć nową warstwę z zasiegu punktów a następnie warstwę buforową, z której zostanie pobrany zasięg (*extent*). Wymaga to jednak utworzenia dwóch warstw tymczasowych. Zadanie zostanie uproszczone poprzez pobranie zasięgu z warstwy punktowej, a następnie buforowanie samego zasięgu. Do pracy ze strukturą danych niezbędne jest wczytanie danych jako warstwy wektorowej.

```Python
points = QgsVectorLayer(point_layer)
e = points.extent()
e_buf_ = e.buffered(100)
```

W następnym kroku nowy zasięg zostanie użyty to wyliczenia wielkości oczek siatki, poprzez podzielenie długości i szerokości zasięgu przez oczekiwaną liczbę kolumn i wierszy.

```Python
xsize = e_buf.width()/ncols
ysize = e_buf.height()/nrows
```
Przygotowane parametry pozwalają na utworzenie siatki, gdzie zasięg oraz rozmiar oczek został pozyskany z danych innej warstwy. Dodatkowo układ współrzędnych zostanie pobrany z utworzonej wcześniej warstwy wektorowej.

```Python
grid_params = {'TYPE':2,
    'EXTENT':e_buf,
    'HSPACING':xsize,'VSPACING':ysize,
    'CRS':points.sourceCrs(),
    'OUTPUT':'TEMPORARY_OUTPUT'}

grid = processing.run("native:creategrid", grid_params)
```
Tak utworzoną siatkę można wykorzystać na przykład do policzenia liczby punktów w każym z oczek.

```Python
point_params = {'POLYGONS':grid['OUTPUT'],
    'POINTS':points,
    'FIELD':'NUMPOINTS',
    'OUTPUT':'TEMPORARY_OUTPUT'}

counted = processing.run("native:countpointsinpolygon", point_params)
```

Pełny kod skryptu znajduje się [tutaj](zadania/cw_5_2_siatka.py).

## Ćwiczenie 3 Indywidualny dobór parametrów rastryzacji.

Ćwiczenie wykorzystuje dane z zadania [4_1](zadania/cw_4_1_rastryzacja.py). W ramach zadania parametry rastryzacji: **WIDTH**, **HEIGHT**, **EXTENT** będą dobierane indywidualnie dla każdego obiektu w pętli. Zakładamy że:

* zasięg warstwy rastrowej ma być większy niż warstwy wektorowej proporcjonalnie do powierzchni zajmowanej przez obiekt w jego *bounding box*. 
* rozdzielczość ma być proporcjonalna do powierzchni nowo tworzonego rastra

Dodatkowym ograniczeniem jest zastosowanie dynamicznego bufora wyłącznie dla poligonów. Dla linii nie możemy obliczyć powierzchni, a więc wielkość bufora nie może być obliczona.

> **UWAGA:** dla większości danych takich zabiegów się nie stosuje. Zaproponowane wymogi mają wyłącznie cel dydaktyczny.

### Metoda obliczenia parametrów

Podstawą zwiększenia zasięgu jest połowa uśrednionionej wysokości i szerokości otoczki obiektu (`bbox_size`) zmodyfikowana relacją pomiędzy powierzchnią poligonu a powierzchnią bboxa: `(bbox_size/2) * (poly_area/bbox_area)`

Podstawą określenia rozdzielczości jest powierzchnia nowego zasięgu (w km<sup>2</sup>), z której zostanie wyciągnięty pierwiastek: `round(math.sqrt(extent.area()/1000000))`. Funkcję pierwiastka pozyskujemy z biblioteki `math`.

Obliczenie parametrów wymaga pozyskania informacji o powierzchni rastryzowanego poligonu oraz jego otoczki. 

```Python
poly_area = vector.getFeature(1).geometry().area()
bbox = vector.getFeature(1).geometry().boundingBox()
bbox_size = (bbox.width()+bbox.height())/2 # średnia
bbox_area = bbox.area()
```
Zmienne te pozwalają obliczyć zasięg bufora a następnie *extent* i  z zasięgu obliczna jest gemometria:

```Python
size = (bbox_size/2) * (poly_area/bbox_area)
extent = bbox.buffered(size)
res = round(math.sqrt(extent.area()/1000000))
```

### Sprawdzenie typu geometrii

Skrypt sprawdza typ geometrii i w zależności czy jest to poligon czy nie oblicza nowy zasięg dynamicznie (poligon) lub pobiera go z zasięgu linii.

```Python

    if vector.geometryType() == type: # tylko poligony
        # extent
        # ...
        extent = bbox.buffered(size)
    else:
        extent = vector.getFeature(1).geometry().boundingBox()
```

### Główna pętla programu

W pierwszej kolejności tworzymy plik parametrów rastryzacji, gdzie ustawiamy wyłącznie wartość rastryzowanego poligonu **BURN** (1) **UNITS** (m) oraz **NODATA** (0). Parametry te są poza pętlą. Ustawiamy również zmienną: `type = QgsWkbTypes.PolygonGeometry`, gdzie `QgsWkbTypes.PolygonGeometry = 2`.

```Python
vect_params = {'INPUT':'',
    'BURN':1,
    'UNITS':1,
    'WIDTH':'', #wyliczane
    'HEIGHT':'',
    'EXTENT':'',
    'NODATA':0,
    'OUTPUT':''}
type = QgsWkbTypes.PolygonGeometry
```

Pętla główna wymaga ustawienia parametrów rastryzacji indywidualnie dla każdej warstwy poligonowej indywidualnie dla każdej iteracji pętli. **INPUT** to nazwa aktualnie przetwarzanego pliku a **OUTPUT** wyznaczany jest na podstawie tej nazwy i uruchomienie algorytmu.

```Python
vect_params['WIDTH'] = res
vect_params['HEIGHT'] = res
vect_params['EXTENT'] = extent
    # input and output 
vect_params['INPUT'] = vect
vect_params['OUTPUT'] = vect[:-4]+"tif"
processing.run("gdal:rasterize",vect_params)
```
Pełny kod skryptu znajduje się [tutaj](zadania/cw_5_3_rastryzacja.py).


