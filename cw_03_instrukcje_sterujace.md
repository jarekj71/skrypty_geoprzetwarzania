# Instrukcje sterujące w skrypty geoprzetwarzania i przetwarzanie wsadowe.

## Wiedza i umiejętności:
W ramach zajęć zostaną rozszerzone umiejętności pisania skryptów geoprzetwarzania o zastosowanie instrukcji sterujących (pętli i rozgałęzień) oraz posługiwania się poleceniami API środowiska QGIS odwołującymi się do interface i zawartości projektu. Integralną częścią projektu jest zapoznanie się z wbudowanymi w system procedurami wsadowego przetrzania algorytmów QGIS jako alternatywnym sposobem automatyzacji zadań.

## Zakres zajęć:
* wsadowe przetwarzanie algorytmów
* budowanie procedury
* sprawdzanie warunków wykonywalności polecenia
* instrukcje sterujące:
  * pętle i kontrola powtórzeń
  * rozgałęzienia i warunkowe wykonywanie poleceń
* automatyczne tworzenie nazw plików

## Cel geoinformacyjny ćwiczenia
Zbudować narzędzie, które użyje zbioru danych punktowych do wycięcia fragmentów rastra zapisanego w trybie *8bit z paletą kolorów* i zapisze fragmenty jako zbiór obrazów .png we wskazanym katalogu. Zadanie zostanie zrealizowane na dwa sposoby: jako połączenie modelu oraz narzędzia przetwarzania wsadowego oraz jako niezależny skrypt.

Osiągnięcie celu wymaga zbudowania narzędzia, które uwzględnia następujące oczekiwania

* możliwość wskazania pliku rastrowego i zbioru danych punktowych i wczytania danych z różnych źródeł (zarówno warstwy projektu i warstwy zewnętrzne)
* uwzględnić tylko te punkty, których zasięgi otoczenia nie wychodzą poza zakres warstwy rastrowej
* umożliwić wybów wielkości (zasięgów) obszaru cięcia
* możliwość kontroli nazw tworzonych wycinków poprzez możliwość wskazania atrybutu pliku punktowego z nazwą docelową
* ożliwość wskazania katalogu docelowego, gdzie zostaną zapisane wyniki

## Dane i algorytmy geoprzetwwarzania
Dane rastrowe do realizacji zadania znajdują się pod adresem:
Raster: [https://uam-my.sharepoint.com/:i:/g/personal/jarekj_amu_edu_pl/ESbxLrd5NFJMlVPNEDS_I0MBHzxNxUmzRPPgu46LNInzdw?e=eEOdPf]

Do zrealizowania zadania będą potrzebne następujące algorytmy:
* `polygonfromlayerextent` do wydobycia zasięgu rastra i zapisu go w formie poligonu
* `exctractbyattribute` do wydobycia poszczególnych punktów, na podstawie ich wartości 'ID' (tylko skrypt geoprzetwarzania)
* `buffer` do zbudowania kwadratów dookoła punktów. Funkcję buffer należy wykonać z parametrem: *.. square* i *.. 1*, aby uzyskać kwadrat.
* `extractbylocation` do wyboru tych buforów, których zasięgi leżą w całości w zasięgu rastra (opcja *is within*)
* `split vector layer` w celu zapisu poszczególnych buforów w formie osobnych plików (tylko tryb wsadowy)
* `cliprasterbylayermask` do wycięcia fragmentów rastra na podstawie zasięgu bufora (provider: gdal)

## Algorytm skryptu

## Rozwiązanie ćwiczenia w trybie wsadowym
Zadanie można zrealizować poprzez zbudowanie modelu, w którym wskażemy warstwę rastrową i zbiór danych punktowych. Dodatkowo, należy wybrać zasięg bufora (w metrach) oraz pole ID. Wszystkie te elementy dodajemy jako model input. Wskazujemy również katalog do którego zapiszemy wyniki podziału pliku buforowego na pojedyncze poligony.

W ramach modelu wykonujemy następujące kroki. Wyznaczamy poligon zasięgu, wyznaczmy bufory dookoła punktów, wybieramy tylko te poligony w buforze, które znajdują się w całości w obrębie poligonu zasięgu. Ostatnim krokiem zadania jest wskazanie kaltalogu, do którego zostaną zapisane wyniki oraz pole (ID), z którego zostanie pobrana nazwa. 

Model zawierający całą procedurę można pobrać [tutaj](zadania/cw_3_wycinanie.model3)

Zadanie wycięcia fragmentów rastra zrealizowane zostanie przy pomocy algorytmu extract by layer mask w trybie wsadowym. Przygotowanie zadania wsadowego wymaga wskazania katalogu z maskami oraz wskazania sposobu nadawania nazw kolejnych plików; w tym wypadku zostanie wykorzystana nazwa pliku poligony

Plik wsadowy całą procedurę można pobrać [tutaj](zadania/cw_3_wycinanie_batch.json)

## Rozwiązanie ćwiczenia w trybie skryptu geoprzetwarzania z użyciem instrukcji sterujących (pętli i warunków)
 
 > **UWAGA**: w celu zilustrowania wykorzystania różnych instrukcji sterujacych, zrezygnujemy z jednorazowego sprawdzenia czy poligony buforów znajdują się z zasięgu warstwy. Zasięg każdego z poligonów będzie sprawdzany osobno.

 ### Pozyskanie informacji o warstwach i obiektach warstwy
 Procedury wsadowe mogą być zastępowane pętlami `for...`, gdzie każda iteracja to lista kroków do wykonania. Zaletą podejścia skryptowego jest większa swoboda zarządzania poszczególnymi krokami skryptu.

 Podstawą skryptu jest pętla główna:

``` python
 for feature in points.getFeatures(): 
    ...
```
gdzie na feature to pojedyczny obiekt wektorowy pobierany z warstwy points metodą getFeatures(). Warstwa points w tym przykładzie pobierana jest ze środowiska pracy (mapCanvas).

```python 
points = iface.mapCanvas().layers()[2] # w tym wypadku jest to druga warstwa w mapCanvas
```
### Zmienne skryptu
Na początku skryptu warto wprowadzić zmienne, do których przypiszemy wartości parametrów poszczególnych algorytmów. Pozwoli to oddzielić proces ustawiania parametrów od pisania właściwego skryptu, którego kod powinien być niezmienny. Są to źródła danych (points i raster) distance do zbudowania bufora oraz nazwa pola z którego pobierany dane.

Wrstwa wektorowa zostanie pozyskana z osbszaru roboczego, gdyż jest to warstwa tymczasowa i dostęp do niej nie jest możliwy w inny sposób.

```python
points = iface.mapCanvas().layers()[2]
rastermap = os.path.join(os.path.expanduser("~"),'/Documents/lubrza/landcover.tif')
distance = 1000
field = 'ID'
katalog="os.path.expanduser("~")/Documents"
```

### Parametry algorytmów
Każde z poleceń uruchamiających kolejne algorytmy składa się z nazwy algorytmów i słownika zawierającego parametry danego algorytmu. W celu uczytelnienia kodu skyptu wszystkie słowniki warto zdefiniować przed uruchomieniem pętli. W sytuacji, gdy do algorytmu przypisujemy warości zdefniowane jako zmienne wpisujemy nazwę zmiennej a nie wartość. W miejscach, gdzie parametr algorytmu jest wyjściem poprzedniego algorytmu, a wartość jest wymagana, wstawiamy pustą linię ''.

```python
attribute_params = {'INPUT':points,
    'FIELD':field,
    'OPERATOR':0,
    'VALUE':'',
    'OUTPUT':'TEMPORARY_OUTPUT'}

location_params = {'INPUT':'',
    'PREDICATE':[6],
    'INTERSECT':extent,
    'OUTPUT':'TEMPORARY_OUTPUT'}

buffer_params = {'INPUT':'','DISTANCE':distance,
'SEGMENTS':1,'END_CAP_STYLE':2,'OUTPUT':'TEMPORARY_OUTPUT'}

clip_params = {'INPUT':rastermap,
    'MASK':'',
    'CROP_TO_CUTLINE':True,
    'DATA_TYPE':0,
    'OUTPUT':''}

```
Po zdefiniowaniu parametrów algorytmów przechodzimy do głównej części skryptu. Poza pętlą znajduje się polecenie wydobycia zasięgu warstwy rastrowej do postaci poligonu. Wynik działania algorytmu przypisujemy do pola `'INTERESECT'` słownika `extract_params`. 

```python
exctrac_params['INTERSECT'] = processing.run('native:exctractbylocation'exctract_params)['OUTPUT']
```

### Pętla główna
W samej pętli, dane wyjściowe (['OUTPUT']) kolejnych algorytmów, przypisywane są do wybranych pól słowników, parametrów tak aby mogły być użyte jako parametry wejściowe do kolejnych algorytów. Pętla przetwarza każdy punkt osobno: 

* Pętla zwraca wartości 'ID' kolejnych punktów
* ID jest przypisywany do parametrów `extract by attribute`
* wydobyty punkt jest przypisywane jako 'INPUT' do parametrów bufora
* dookoła punktu wyznaczana jest kwadratowy bufor, który jako warstwa tymczasowa staje się parametrem wejściowym 'INPUT' dla parametru extract by location

```python
for feature in points.getFeatures():
    attribute_params['VALUE']=feature.id()
    buffer_params['INPUT'] = processing.run("native:extractbyattribute",attribute_params)['OUTPUT']
    location_params['INPUT']  = processing.run("native:buffer",buffer_params)['OUTPUT']
    extracted = processing.run("native:extractbylocation", location_params)['OUTPUT']

```
Celem algorytmu extract by location jest sprawdzenie, czy poligon buforu leży w całości w obrębie zasięgu warstwy. Wynik przypisywany jest do zmiennej `extracted`. Ponieważ analizie podlega tylko jeden poligon bufora (tworzony jest dla jednego punktu), testem oceny czy jest znajduje sie w obrębie wartwy czy nie jest liczba features w zwróconej warstwie. jeśli jest to 0 to znaczy że polygon nie spełnił warunku, jeżeli 1 to znaczy że spełnił.  

### Zastosowanie instrukcji rozgałęzienia
Sprawdzenie warunku jest testowane przy pomocy warunku `if..` sprawdzającego liczbę features w warstwie.

```python
if extracted.featureCount() ==1:
```
Jeżeli warunek zwrócił `False`, to punkt jest pomijany, jeżeli zwórcone zostało `True`, wykonywane są kolejne kroki: przypisanie poligony jako 'MASK' oraz nazwa pliku jako 'OUTPUT'. Nazwa pliku tworzona jest na podstawie wartości atrybutu 'ID' przypisanego do punktu i wydobywanego w nagłówków pętli. Ostatnim krokiem jest zapis wydzielonej warstwy do pliku, z nazwą zdefiniowaną w poprzednim kroku. Stosowanie skryptu pozwala stosować całą gamę jezyka Python, zamiast nie zawsze przejrzystych *expressions*.

```python
if extracted.featureCount() ==1:
        clip_params['MASK'] = extracted
        clip_params['OUTPUT'] = "{}/{:03d}.png".format(katalog,feature.id())
        processing.run("gdal:cliprasterbymasklayer",clip_params)
```
Kompletny skrypt można pobrać tutaj: [tutaj](zadania/cw_3_wycinanie.py)

## Zadanie zaliczeniowe:
Zbudować skrypt tnący Corine Land Cover o rozdzielczości 100m na powiaty. Nazwa pliku musi zawierać nazwę powiatu przechowywaną w tabeli atrybutów. Dodać parametr pozwalający na wybór minimalnej powierzchni powiatu, dla którego robiona jest mapa.

Dodatkowe wymogi: Dodać możliwość wyboru powiatów w formie listy zawierającej jej nazwę.

Co podlega ocenie: 
* poprawność wykonania skryptu
* zarządzanie parametrami i danymi wejściowymi
* ocenę bardzo dobrą z zadania można otrzymać jeżeli spełni się dodatkowe wymogi lub zaproponuje własne rozwiązania, nie omawiane na zajęciach