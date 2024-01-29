# Wtykorzystanie skryptów do tworzenia grafiki prezentacyjnej

## Wiedza i umiejętności
W ramach zająć umiejętności przetwarzania danych geoprzestrzennych przy pomocy skryptów zostaną wykorzystane do tworzenia grafiki prezentujące zarówno dane atrybutowe (wartości) jak i informację przestrzenną zapisaną w geometrii obiektów. Ćwiczenie wymaga podstawowej wiedzy na temat metod tworzenia grafiki prezentacyjnej w Pythonie (matplotlib) i przetwarzania danych (pandas)

## Zakres zajęć
Zajęcia podzielone są na trzy ćwiczenia: praca z danymi rastrowymi i wektorowymi, przetwarzanie wieloatrybutowych danych wektorowych i przetwarzanie wielowarstwowych danych rastrowych. Umiejętności obejmują:
* próbkowanie danych wektorowych
* pozyskiwanie wartości atrybutowych
* pozyskiwanie wartości rastra (próbkowanie)
* tworzenie DataFrame z różnych źródeł danych
* tworzenie grafik prezentacyjnych na podstawie danych 

## Cel geoinformacyjny ćwiczeń
Współnym celem wszyskich ćwiczeń jest przygotowanie danych geoprzestrzennych do tworzenia grafiki prezentacyjnych. QGis nie jest narzędziem przystosowanym do przetwarzania danych tabelarycznych i ich wizualizacji, w przypadku zaawansowanych wizualizacji należy wykorzystywać dedykowane narzędzia. Stosowanie wizualizacji bezpośrendio w plikach geoprzetwarzania ma sens jedynie, gdy wizualizaja jest częścią procesu decyzyjnego i nie ma sensu zmieniać środowiska jedynie w celu przeprowadzenia prostej wizualizacji.  W przypadku plików wektorowych tabele atrybutów można wczytywać bezpośrednio do środowisk obliczeniowych, natomiast przygotowanie danych rastrowych, ze względu na ich rozmiar wymaga redukcji rozmiaru np. przez próbkowanie. Tym samym ćwiczenie skupia się głównie na wstępnym przetwarzania danych (preprocessingu). Zagadnienia tworzenia grafik jest osobnym zagadnieniem. Osiągnięcie celu wymaga narzędzia, które:

* pozwala pozyskać wartości dowolnego atrybutu
* próbkować warstwę rastrową lub sekwencję warstw rastrowych
* przekształcić wydobyte dane do postaci akceptowanej przez algorytmy tworzenia grafiki


### Ćwiczenie 1
Zbudować skrypt, który wykona wykres zależności pomiędzy wartościami atrybutowymi pliku wektorowego lub atrybutami geometrycznymi obiektów (powierzchnia, obwód). Skrypt musi uwzględnić filtowanie wyników w celu usunięcia obiektów o nieprawidłowych wartościach np. zerowej powierzchni lub ujemnych dochodach.

### Ćwiczenie 2
Zbudować skrypt, który wykona przekrój geomorfologiczny wzdłuż wskazanej linii. Skrypt wymaga wygenerowania wzduż linii serii punktów o stałej, znanej odległości oraz pobraniu wartości rastra w lokalizacji punktów. Ostatnim krokiem jest pozyskanie warości wysokości i odległości między punktami i narysowanie wykresu.

### Ćwiczenie 3
Zbudować skrypt który obróbkuje serię danych rastrowych i zintegruje wyniki w jednym pliku. Następnie z użyciem pętli dokona wizualizacji rozkładu wartości poszczególnych rastrów w postaci serii wykresów.

## Dane i algorytmy geoprzetwarzania
Katalog z danymi do wykonania ćwiczenia znajduje się pod adresem: https://uam-my.sharepoint.com/:u:/g/personal/jarekj_amu_edu_pl/EarsKfJaOntOvDx5W79u0tMB9m0fVs2yoVRC262wC2JtDA?e=MJ7nlh 

Dane obejmują model wysokościowy, linię przekrojową w zasięgu modelu oraz plik z krajami świata i wybranymi atrybutami dotyczącymi tych krajów.

Do zrealizowania zadań będą potrzebne następujące narzędzia i algorytmy:

* biblioteka `matplotlib` do wizualizacji danych
* biblioteka `pandas` do zarządzania strukturami danych tabelarycznych
* algorytm `points along lines` do wygenerowania punktów regularnie rozłożonych wzduż linii
* algorytm `rastersampling` do pozyskania wartości rastra w lokalizacji punktu
* algorytm `randompointsinextent` do wynenerowania losowych punktów w zasięgu zbioru rastrowego
* wybrane algorytmy providera `saga` do wygenerowania serii danych rastrowych z modelu wyskościowego.
* metoda `.getValues()` klasy `QgsVectorLayerUtils` do pozyskania wartości atrybutów i geometrii plików wektorowych

Narzędzia i zastosowania bibliotek matplotlib i pandas są tematyką osobnych zajęć.

## Ćwiczenie 1 Zależności między atrybutami
Jedynym atrybutem skrpytu jest źródło danych wektorowych, które trzeba przekształcić w warstwę wektorową.

```Python
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
os.chdir("/home/jarekj/Documents/skrypty_geoprzetwarzania")
vect = "countries.gpkg"
vect_layer = QgsVectorLayer(vect)
```

### Pobranie atrybutów
To wykonania teog ćwiczenie nie potrzeba żadnych algorytmów geoprzetwarzania, a jedynie pomocnicza metoda klasy `QgsVectorLayerUtils.getValues()`, która jako parametry przyjmuje źródło danych oraz nazwę atrybutu lub wyrażenie. Z zestawu danych pozyskamy zarówno dane atrybutowe **POP_EST** i **GDP_MD** oraz parametry geometryczne obiektów: **area** i **perimeter**. Te ostatnie są możliwe do szybkiego wydobycia dzięki obsłudze wyrażeń (expressions) przez funkcję `getValues()`. Wyrażenia podajemy zgodnie ze składnią środowiska QGis.

```Python
pops = QgsVectorLayerUtils.getValues(vect_layer,'POP_EST')
gdps = QgsVectorLayerUtils.getValues(vect_layer,'GDP_MD')
areas = QgsVectorLayerUtils.getValues(vect_layer,'$area')
perimeters = QgsVectorLayerUtils.getValues(vect_layer,'$perimeter')
```

Alternatywną metodą jest pobieranie atrybutów porzez iterowanie po obiekatach warstwy. Nie jest to metoda zalecania o ile `QgsVectorLayerUtils.getValues()` może być zastosowana. Dodatkowo, pozyskanie atrybutów geometrycznych wymaga dostępu do geometrii obiektu.

```Python
features = vect_layer.getFeatures()
areas = [feature.geometry().area() for feature in features]
pops = [feature['POP_EST'] for feature in features]
```

### Integracja danych w postaci pandas DataFrame.
Zagadnienie obslugi pandas jest zagadnieniem przedstawianym na innych zajęciach. Tu do przekształcenia list w ramkę danych wykorzystamy słownik. Meteda `getValues()`  zwraca krotkę, której pierwszym elementem jest lista danych a drugim wartość logiczna True/False o nieznanym przeznaczeniu. tym samym dostęp dodanych wymaga użycia indeksu [0]. Ostatnim krokiem jest usunięcie tych rekordów, które mają nieprawidłowe wartości: GDP lub licznę ludności mniejszą lub równą 0.

```Python
stats = {'GDPS':gdps[0],'POPS':pops[0],'AREAS':areas[0],'PERIMETERS':perimeters[0]}
stats = pd.DataFrame(stats)
select = (stats['POPS'] > 0) & (stats['GDPS'] > 0)
selected_stats = stats[select]
```

### Wizualizacja danych
Sam proces wizualizacji to użycie narzędzi biblioteki `matplotlib` i utworzonej `DataFrame`. Wizualizacja w Pythonie to temat osobnych zajęć. W ramach ćwiczenia:

1. utworztymy figurę  w postaci dwóch paneli, 
2. w którym jeden wyświetli zależność pomiędzy powierzchnią a obwodem krajów, 
3. a drugi pomiędzy liczbą ludności a GDP. 
4. Oba wykresy zostaną przedstawione na skali logarytmicznej 
5. oraz zostaną dodane etykiety do osi wykresów.

Środowisko pracy Qgis python nie jest interaktywne, tym samym, należy wywołać figurę metodą `.show()`.

```Python
fig,axes = plt.subplots(ncols=2,figsize=(10,5))
axes[0].scatter(selected_stats.PERIMETERS,selected_stats.AREAS,c="#DD1100")
axes[1].scatter(selected_stats.POPS,selected_stats.GDPS,c="#DD1100")
axes[0].set_xlabel("area")
axes[0].set_ylabel("perimeter")
axes[0].set_xscale('log',base=10)
axes[0].set_yscale('log',base=10)
axes[1].set_xscale('log',base=10)
axes[1].set_yscale('log',base=10)
axes[1].set_xlabel("population")
axes[1].set_ylabel("GDP")
fig.tight_layout()
fig.show()
```

Cały skrypt można znaleść [tu](zadania/cw_7_1_atrybuty.py) 

## Ćwiczenie 2 Tworzenie przekroju
Do zrealizowania ćwiczenia potrzebujemy plik rastrowy *dem.tif* oraz linię przekrojową *przekroj.gpkg*. Dodatkowym parametrem jest odległość pomiędzy punktami generowanymi wzdłuż linii.

```Python
import os
import matplotlib.pyplot as plt
os.chdir("/home/jarekj/Documents/skrypty_geoprzetwarzania")
pdist = 100
dem = 'dem.tif'
przekroj = 'przekroj.gpkg|layername=przekroj'
```

### Generowanie punktów
Do wygenerowania punktów użyjemy algorytmu `native:pointsalonglines`, odległość **DISTANCE** ustawimy na 100, źródłem linii **INPUT** jest **przekrój.gpkg** a wynikiem warstwa tymczasowa. Użyty algorytm nie jest jedyną opcją, podobne możliwości foeruje analogiczny algorytm z biblioteki `GDAL`. Zaletą obu rozwiązań jest to że podają również odległość punktu od początku linii, co oznacza że są przystosowane do generowania przekrojów.

```Python
sample_params =  {'INPUT':przekroj,
    'DISTANCE':pdist,
    'OUTPUT':'TEMPORARY_OUTPUT'}

punkty = processing.run("native:pointsalonglines",sample_params)['OUTPUT']
```

### Próbkowanie punktów
Do próbkowania punktów użyjemy warstwy tyczasowej i algorytmu `native:rastersampling`. Algorytm ten dodaje kolumnę z próbkowanymi wartościami i zwraca wynik w postaci nowego pliku wektrowego. Atrybuty już istniejące w pliku zostają zachowane. 

```Python
sample_params = {
    'INPUT':punkty,
    'RASTERCOPY':dem,
    'COLUMN_PREFIX':'Z_',
    'OUTPUT':'TEMPORARY_OUTPUT'}

elevs = processing.run("native:rastersampling",sample_params)['OUTPUT']
```
### Pozyskanie atrybutów
Do pozyskania atrybutów poznana już metoda `QgsVectorLayerUtils.getValues()`, która jako parametry przyjmue źródło danych oraz nazwę atrybutu lub wyrażenie. Nazwy atrybutów to **distance**, który jest generowany automatycznie w czasie tworzenia sekwencji punktów oraz **Z_1**, który został dodany w trakcie próbkowania.

```Python
distances = QgsVectorLayerUtils.getValues(elevs,'distance')
elevations = QgsVectorLayerUtils.getValues(elevs,'Z_1')
```

### Tworzenie grafiki
Do utworzenia grafiki użyjemy najprostrzej metody `.plot()` biblioteki `matplotlib`. 

```Python
fig,ax = plt.subplots(figsize=(10,5))
ax.plot(distances[0],elevations[0],c="#DD1100",lw=2)
fig.show()
```

Cały skrypt można znaleść [tu](zadania/cw_7_2_przekroje.py) 


## Ćwiczenie 3 Wizualizacja sekwencji danych rastrowych
W ramach tego ćwiczenia skupimy się na zagadnieniach związanych z próbkowaniem sekwencji danych rastrowych i integracji danych w postaci ujednoliconego zbioru danych. Do wygenerowania sekwencji użyjemy algorytmu `saga:relativeheightsandslopepositions` w celu zbudowania 5 warstw rastrowych zawierających informację na temat wysokości stoków, głębokości dolin, normalizowanej i standaryzowanej wysokości oraz pozycji środka stoków. Wyniki działania algorytmu nie są tematem ćwiczenia, a zaproponownay algorytm można zstąpić dowlonym innym, tworzącym wiele warstw rastrowych. Tym samym jedynym paramterem skryptu jest liczba generowanych punktów **npoints**.

```Python
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
os.chdir("/home/jarekj/Documents/skrypty_geoprzetwarzania")

npoints = 1000
```

### Algorytm geoprzetwarznia

```Python
slope_pos_params = {'DEM':"dem.tif",
              'HO':'TEMPORARY_OUTPUT', # slope height
              'HU':'TEMPORARY_OUTPUT', #valley depth
              'NH':'TEMPORARY_OUTPUT', #normalized height
              'SH':'TEMPORARY_OUTPUT', #standarized height
              'MS':'TEMPORARY_OUTPUT'} #midslope position

# to jest słownik
slopes = processing.run("saga:relativeheightsandslopepositions",slope_pos_params)
```
Wynikiem algorytmu jest słownik, którego klucze to nazwy parametrów warstw rastrowych tworzonych przez algorytm. Wartościami słownika są ścieżki dostępu do plików tymczasowych programu `SAGA GIS`. Format ten jest obsługiwany przez GDAL i może być bezpośrednio wczytywany do QGis.

### Zakres przestrzenny próbkowania
Aby wyznaczyć zakres przestrzenny próbkowania należy pobrać zasięg z dowolnej warstwy. Utworzymy warstwę tymczasową, na podstawie pierwszej warstwy ze słownika wyników poprzedniego algorytmu.  Zasięg może być przekazany bezpośrednio do algorytmu jako QgsRectangle lub jako tekst zawierający 4 liczby. Parametr **TARGET_CRS** przekazywany jest jako obiekt klasy `QgsCoordinateReferenceSystem`, pozyskany z tymczasowej warstwy rastrowej, użytej do zdefiniowania zasięgu. Wynik w postaci zbioru punktów, przechowujemy jako obiekt tymczasowy, gdyż będzie on wykorzystany tylko do próbkowania i pobrania próbkowanych wartości.

```Python
tmp_rast = QgsRasterLayer(slopes['HO'])
e = tmp_rast.extent()
crs = tmp_rast.crs() ##

random_params = {'EXTENT':e,
    'POINTS_NUMBER':npoints,
    'TARGET_CRS':crs,
    'OUTPUT':'TEMPORARY_OUTPUT'}

random_points = processing.run("native:randompointsinextent",random_params)['OUTPUT']
```
### Próbkowanie

Do próbkowania zostanie użyty algorytm `native:rastersampling`. Algortym pozwala na próbkowanie tylko jednej warstwy rastrowej a w wyniku zwraca nową warstwę wektorową, z zachowanymi atrybutami z warstwy wejściowej. Oznacza to że dla pozyskania jednolitego pliku proces próbkowania trzeba przeprowadzić tyle razy ile jest warstw, za każdym razem warstwę wyściową z poprzedniego kroku traktujemy jako warstwę wejściową w kroku następnym. Tym samym, kedynym niezmiennym atrybutem algorytmu jest **OUTPUT**: 'TEMPORARY_OUTPUT'; pozostałe parametry będą zmieniane w kolejnych krokach. Iniclajnie jako input ustawiany jest ranom_points.

```Python
sample_params = {
    'INPUT':random_points,
    'RASTERCOPY':'',
    'COLUMN_PREFIX':'',
    'OUTPUT':'TEMPORARY_OUTPUT'}
```
Pętla wykorztstuje klucze słownika slopes, zwróconego przez algorytm providera SAGA i 

1. na podstawie klucza 
2. ustawia zarówno parameter **RASTERCOPY** jaki i **COLUMN_PREFIX**. 
3. Dopiero po uruchomieniu algorytmu `native:rastersampling`, 
4. wynik jego działania jest ustawiany jako **INPUT** dla następnego kroku. 
5. Po zakończeniu pętli ostatni wynik jest zapisany jako *vect_layer*.

```Python
for key in slopes.keys(): #1
    sample_params['RASTERCOPY']=slopes[key] #2
    sample_params['COLUMN_PREFIX']='{}_'.format(key)
    tmp = processing.run("native:rastersampling",sample_params) #3
    sample_params['INPUT'] = tmp['OUTPUT'] #4

vect_layer = tmp['OUTPUT'] #5
```

### Pozyskanie wyników próbkowania
Utworznie DataFrame zawierającej wyniki danych w formie tabelarycznej wykonujemy:
1. tworzymy pusty słownik
2. w pętli przechodzącej przez wszystkie nazwy pól warstwy wektorowej, 
3. pole 'id' jest pomijane (aby nie tworzyć zbędnej kolumny)
4. Dodajemy listę atrybutów do słownika gdzie kluczem jest nazwa pola
5. Słownik zamieniamy w DataFrame 

```Python
slopes_df = {} #1
for f in vect_layer.fields(): #2 
    if f.name() !='id': #3
        slopes_df[f.name()]= QgsVectorLayerUtils.getValues(vect_layer,f.name())[0] #4
slopes_df = pd.DataFrame(slopes_df) #5
```

### Tworzenie grafiki
Samo utworzenie grafiki również wykonujemy w pętli. Figura składa się z pięciu wykresów, ustaiwonych w wierszach jeden pod drugim/
1. Przed uruchomieniem pętli tworzymy figurę zawierającą 5 wierszy
2. Pętlę wykonujemy dla nazw kolumn DataFrame. Funkcja `enumerate` zwraca liczby porządkowe
3. Dla każdej kolumny wykonujemy metodę `.plot()` dla DataFrame. Jest to metoda, która pozwala utworzyć wykres matplotlib dla 1 lub więcej kolumn DataFrame.
4. Do każdego wykresu dodajemy etykietę osi x
5. Wyświetlamy wykres

```Python
fig, axes = plt.subplots(nrows=5,figsize=(4,10))
for n, column in enumerate(slopes_df.columns):
    slopes_df.plot(y=column,kind='kde',ax=axes[n])
    axes[n].set_xlabel(column)

fig.tight_layout()
fig.show()
```
Cały skrypt można znaleść [tu](zadania/cw_7_3_rastry.py) 