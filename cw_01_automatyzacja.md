# Automatyzacja procesu geoprzetwarzania w środowisku QGIS i OSG4W

Celem ćwiczeń jest opanowanie podstaw automatyzacji geoprzetwarzania przy pomocy narzędzi programu QGIS wspomagająccyh automatyzację. Narzędzia te są mocno niedoskonałe i mogą być używane jedynie do niektórych czynności

### Zakres zajęć:
* metody automatyzacji geoprzetwarzania
* środowisko 

## Modeler

### Zadanie:
Zbudować model przetwarzania, który zautomatyzuje proces wycinania rastra wokół sieci rzecznej w zadanym promieniu.

Model wymaga następujących kroków:

* Wczytanie zbioru danych wektorowych
* Wczytanie zbioru danych rastrowych
* Wskazania promienia
* Wyznaczenie bufora dla zbioru danych
* Zamaskowanie rastra otrzymanym buforem



## Przetwarzanie wsadowe

### Zadanie:
Użyć zbioru danych punktowych do wycięcia fragmentów rastra i zapisanie ich jako zbiór obrazów .png

Proces wymaga następujących kroków. Trzy pierwsze kroki można wykonać przy pomocy modelera, który jako parametr przyjmie wielkość bufora.

* Zbudowania zbioru punktów dowolną metodą
* Zbudowanie bufora dookoła punktów
* Zbudowania bounding box dla każdego bufora

Następnie w ==trybie przetwarzania pojedynczych obiektów==, wykonać maskowanie rastra na podstawie bounding box. 

Następnie zapisać otrzymane warstwy do plików .png w ==trybie przetwarzania wsadowego==.

## Wyrażenia



## Zaliczenie ćwiczenia
