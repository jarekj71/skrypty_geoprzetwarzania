# Automatyzacja procesu geoprzetwarzania w środowisku QGIS

Celem ćwiczeń jest opanowanie podstaw automatyzacji geoprzetwarzania przy pomocy narzędzi programu QGIS wspomagająccyh automatyzację. Narzędzia te są mocno niedoskonałe i mogą być używane jedynie do niektórych czynności. 

Źródło danych: 

Urban Atlas: [https://uam-my.sharepoint.com/:u:/g/personal/jarekj_amu_edu_pl/EYUTROqLUtxMrXyakqTOHW8BoqLVLEq1rja3pnUz1kF8Ig?e=fsudQm]

Raster: [https://uam-my.sharepoint.com/:i:/g/personal/jarekj_amu_edu_pl/ESbxLrd5NFJMlVPNEDS_I0MBHzxNxUmzRPPgu46LNInzdw?e=eEOdPf]

### Zakres zajęć:
* metody automatyzacji geoprzetwarzania



## Modeler

### Zadanie:
Przejdź od studium przypadku do modelu ogólnego przeznaczenia

#### Studium przypadku

Wykonać działania:
>  Wybrać obszar pod zabudowę mieszkalną według następujących krytieriów:
* obszar w granicach miasta Poznania
* położony na obszarach roliniczych i nieużytkach "code_2018" IN (21000, 22000, 23000, 24000, 13400)
* do 200 metrów od obszarów zabudowanych "code_2018" IN (11100, 11210, 11220, 11230, 11240)
* powyżej 250 metrów od obszarów kolejowych "code_2018" IN (12230)
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

#### [Zapis studium przypadku w postaci modelu](zadania/selekcjaI.model3)

#### [Możliwość modyfikowania modelu Dodanie parametrów ilościowych](zadania/selekcjaII.model3)


#### [Możliwość modyfikowania kategorii pól](zadania/selekcjaIII.model3)

> Wersja uogólniona umożliwia:
* wskazać obszary podlegające selekcji
* podać kryterium bliskości (obszary nie dalej niż wartość od)
* podać kryterium odległości (obszary nie bliżej niż wartość od)
* podać kryterium powierzchni (obszary nie mniejsze niż wartość)













