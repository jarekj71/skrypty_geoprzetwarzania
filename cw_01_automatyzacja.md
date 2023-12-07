# Automatyzacja procesu geoprzetwarzania w środowisku QGIS

Celem ćwiczeń jest opanowanie podstaw automatyzacji geoprzetwarzania przy pomocy narzędzi programu QGIS wspomagająccyh automatyzację. Narzędzia te są mocno niedoskonałe i mogą być używane jedynie do niektórych czynności. 

Źródło danych: [https://uam-my.sharepoint.com/:u:/g/personal/jarekj_amu_edu_pl/EYUTROqLUtxMrXyakqTOHW8BoqLVLEq1rja3pnUz1kF8Ig?e=fsudQm]

### Zakres zajęć:
* metody automatyzacji geoprzetwarzania

## Przetwarzanie wsadowe

### Zadanie:
Użyć zbioru danych punktowych do wycięcia fragmentów rastra i zapisanie ich jako zbiór obrazów .png

> Proces wymaga następujących kroków. 

* Trzy pierwsze kroki można wykonać przy pomocy prostego modelera, który jako parametr przyjmie wielkość bufora.

* Zbudowania zbioru punktów dowolną metodą
* Zbudowanie bufora dookoła punktów
* Zbudowania bounding box dla każdego bufora

Następnie w trybie przetwarzania pojedynczych obiektów, wykonać maskowanie rastra na podstawie bounding box. 

Następnie zapisać otrzymane warstwy do plików .png w trybie przetwarzania wsadowego.

## Modeler

### Zadanie:
Przejdź od studium przypadku do modelu ogólnego przeznaczenia

#### Studium przypadku

Wykonać działania:
>  Wybrać obszar pod zabudowę mieszkalną według następujących krytieriów:
* obszar w granicach miasta Poznania
* położony na obszarach roliniczych i nieużytkach (Code
* do 200 metrów od obszarów zabudowanych
* powyżej 250 metrów od obszarów kolejowych
* minimalna wielkość poligonu 10 ha
      
Narzędzia i sekwencja działań:
* Clip - przycięcie UA do granicy Poznania
* Extract by expression (operator IN) - wydzielenie obszarów rolnych, zabudowy i kolejowych
* Bufer (dissolve) obszarów zabudowy i kolejowych
* Intersection - obszary rolne i zabudowa 200 metrów -> wIntersection
* Defference - wynik 1 - bufor obszarów kolejowych -> wDifference
* Mulitpart to single part wDifference -> single
* Extract by expression - single ($area/10000) 10

1. Zbudować model dokumentujący zadania (z prowadzącym)
2. Wskazać w modelu elementy które można modyfikować (wartości liczbowe)
3. Dodać możliwość wymiany warstw (dane + maska obszaru działania)
4. Wskazać możliwość wyboru wartości atrybutów (wyrażenia) w warstwie danych podlegających geoprzetwarzaniu

#### Wersja uogólniona:

> Pozwoli wskazać:
* obszary podlegające selekcji
* kryterium bliskości (obszary nie dalej niż wartość od)
* kryterium odległości (obszary nie bliżej niż wartość od)
* kryterium powierzchni (obszary nie mniejsze niż wartość)













