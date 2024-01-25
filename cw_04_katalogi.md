# Iteracyjne przetwarzanie katalogów

## Wiedza i umiejętności
W ramach zajęć umiejętności iteracyjnego przetwarzania obiektów w warstwie zostaną rozbudowane o umiejętności przetwarzania zawartości folderów (katalogów). W ramach zajęć soztaną przedstawione metody warstw wektorowych i rastowych pozwalające na pozyskanie podstawowych informacji na temat zawartości danej warstwy. Ćwiczenie wymaga wcześniejszego zapozania się z narzędziami Pythona przeznaczonymi do obsługi scieżek, plików i katalogów (biblioteka `os`).

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
Zbudować skrypt, który dokona konwersji zbioru danych wektorowych do formatu rastrowego. Skrypt powinien przkształcać wyłącznie warstwy zawierające poligony o powierzchni nie mniejszej niż 1km<sup>2</sup>. Dodatkowo, skrypt powienien rozszerzyć zasięg pliku rastrowego.

### Ćwiczenie 2
Zbudować skrypt, który wyliczy nachylenie stoków z katalogu plików rastrowych. Skrypt powinien pomijać pliki, które zawierają dane kategoryzowane (Byte) oraz w przypadku wykrycia układu bez projekcji  geodezyjnej (geograficznego), np. wgs84 dokonać jego automatycznej konwersji do wybranego układu.

### Ćwiczenie 3
Zbudować skrypt, który pobierze podstawowe infromacje statystyczne na temat modeli wysokościowych z katalogu użytego w poprzednim ćwiczeniu u zapisze je w postaci tabeli. Dodatkowo skrypt powinien pominąć pliki zapisane w układzie geograficznym i zawierające dane kategoryzowane.

## Dane i algorytmy geoprzetwwarzania
Katalogi z danymi do wykonania ćwiczeń znajdują się pod adresem:
https://uam-my.sharepoint.com/:u:/r/personal/jarekj_amu_edu_pl/Documents/cwiczenia/foldery.zip?csf=1&web=1&e=ebrtYH

Do zrealizowania zadania będą potrzebne następujące narzędzia i algorytmy:

* biblioteka `os` do zarządzania plikami i katalogami
* biblioteka `core` Qgis, metody klas `QgsRasterLayer`, `QgsVectorLayer` i klasy nadrządnej `QgsMapLayer`. Dodatkowo, wykorzystane zostaną wybrane metody klasy `QgsRasterDataProvider` i `QgsRasterBandStats`
* `gdal:rasterize` do przekształcenia danych wektorowych w rastrowe
* `gdal:warpproject` do zamiany projekcji z jednego układu do drugiego
* `slope` do wyliczenia nachylenia stoków

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
minarea = 100
```

### Obszar roboczy
Następnie tworzymy sieżkę dostępu na katalog z danumi i ustawiamy go jako obszar roboczy. Listę plików pobieramy poleceniem `os.listdir` i filtrujemy tak, aby pozostawić tylko pliki z rozszerzeniem *.gpkg*. 

```Python
path = os.path.join(os.path.expanduser("~"),"Documents","skrypty_geoprzetwarzania",folder)
os.chdir(path)

lista = os.listdir(".")
lista = [l for l in lista if l.endswith("gpkg")]
```
### Podstawowe informacje
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
* wczytuje je jako warstwę wektorową
* sprawdza typ geometrii, jeżeli poligon:
* sprawdza powierzchnię poligonu, jeżeli większa niż 100:
* wylicza nowy extent
* Przypisuje parametry INPUT, EXTENT i OUTPUT.
* Uruchamiamy algorytm `gdal:rasterize` z aktualnymi parametrami.

Pętla wykonuje się tylko dla 7 z 9 plików. Pomijana jest linia oraz plik, gdzie poligon ma mniej niż 100km<sup>2</sup>

## Ćwiczenie 2 Wyliczenie nachylenia stoków dla wybranych plików

