# Automatyzacja sekwencji geoprzetwarzania w środowisku QGIS przy pomocy modeli

## Wiedza i umiejętności
Celem ćwiczeń jest opanowanie podstaw automatyzacji geoprzetwarzania przy pomocy narzędzi programu QGIS wspomagająccyh automatyzację. Narzędzia te są mocno niedoskonałe i mogą być używane w ograniczonym zakresie. Pozwalają jednak zautomatyzować pracę w przypadku sekwencji powtażalnych czynności. W ramach zajęć student zapozna się jak proces geoprzetwarzania realizowany jako sekwencja kolejnych poleceń zamienić w model automatyzujący proces a następnie rozbudować model o możliwość powtarzania procesu dla różnych parametrów modelu i innych danych.

## Zakres zajęć:
* Środowisko budowania modeli
* algorytmy geoprzetwarzania jako składowe modelu
* pozyskiwanie parametrów wejściowych algorytmów
* przepływ danych
* opcje wejścia i wyjścia
* wyrażenia (expression)

## Cel geoinformacyjny ćwiczenia
Zbudować narzędzie które pozowoli wykonać zaawansowaną selekcję obszarów z uzględnieniem zarówno kryteriów atrybutowych jak i przestrzennych. Kryteria atrybutowe określają jaka kategoria danych ma być wybrana a kryteria przestrzenne jakie obszary mają znajdować się w pobliżu a jakie nie powinny. Ćwiczenie zostanie zrealizowane na podstawie studium przypadku wyboru terenów budowlanych zlokalizowanych na polach ornych i nieużytkach a zlokalizowanych w odległości nie większej niż 200 m od istniejącej zabudowy i co najmniej 250 metrów od linii kolejowej. Wybrane obszary nie mogą być mniejsze niż 10 ha.

Osiągnięcie celu wymaga zbudowania narzędzia, które spełni następujące oczekiwania

* możliwość wskazania warstwy zawierającej dane geoprzestrzenne na których zostanie wykonana analiza
* możliwość wskazania warstwy maski, ograniczającej obszar analizy
* możliwość wskazania więcej niż jednej kategorii w procesie selekcji, zarówno dla obszarów wybieranych jak i obszarów ograniczających przestrzennie wybór, tj. wymaganych w pobliżu i zabronionych w pobliżu
* możliwość określenia zasięgu dla obszarów wymaganych i zabronionych
* możliwość określenia minimalnej wielkości obszaru


## Dane i algorytmy geoprzewarzania
Dane zawierające Urban Atlas dla powiatu poznańskiego można znaleść pod adresem:
[https://uam-my.sharepoint.com/:u:/g/personal/jarekj_amu_edu_pl/EYUTROqLUtxMrXyakqTOHW8BoqLVLEq1rja3pnUz1kF8Ig?e=fsudQm]

Do zrealizowania zadanie będą potrzebne następujące algorytmy:
`clip` służy do przycięcia warstwy danych *URBAN ALTALS* do mniejszego zasięgu w celu przyspieszenia obliczeń
`extractbyexpression` służy do selekcji obiektów na podstawie przekazanego wyrażenia. Narzędzie będzie wykorzystywane wielokrotnie.
`buffer` służy do wyznaczenia otoczek, zarówno dla obszarów wymaganych jak i zabroninionych w pobliżu
`intersection` służy do wyboru obszarów, spełniających wymóg kategorii, i przecinających się z otoczką obszarów wymaganych
`difference` służy do usunięcia z wyboru obszarów zabronionych
`multiparttosinglepart` narzędzie postprocessingu, ma na celu podział obszarów rozbitych w wyniku operacji różnicy i intereskcji

Algorytmy zostaną uzupełnione o typy wejścia i wyjścia modelu:
`vector layer` pozwala wprowadzić do modelu warstwę wektorową. Dodatkowo pozwala wprowadzić sprawdzenie typu geometrii
`expression` pozwala wprowadzić dowolne wyrażenie. Powinno być powiązane z warstwą
`number` pozwala wprowadzić wartość. Można określić typ liczby (całkowita, rzeczywista) oraz zakres wartości
`OUTPUT` wskazanie warstwy będącej efektem działania modelu

Dodatkowo, do rozwiązania zadania samodzielnego narzędzie:
`conditional branch` pozawala na warunkowe wykonanie algorytmu, jeżeli zwrócona została wartość `True`.

## Rozwiązanie ćwiczenia w formie kolejnych kroków realizowanych w środowisku QGIS

> **UWAGA** jest to studium przypadku, które pozwoli zorientować się jakie kroki muszą być wykonane. Sama procedura nie jest częścią ćwiczenia. Kursywą nazwy robocze warstw wynikowych w kolejnych krokach

1. Przyciąć `clip` warstwę *poznan_UA* przy pomocy maski *poznan_urbancore*. Działanie w celu usunięcia obszarów nie będących częścią analizy -> *clip*
2. Wybrać `extractbyexpression` z wyniku poprzedniej operacji (*clip*) obszary spełniające kryteria obszarów rolnych i nieużytków: `"code_2018" IN (21000, 22000, 23000, 24000, 13400)` -> *expressionS*
3. Wybrać `extractbyexpression`z wyniku poprzedniej operacji (*clip*) obszary spełniające kryteria obszarów zabudowanych: `"code_2018" IN (11100, 11210, 11220, 11230, 11240)` -> *expressionA*
4. Wybrać `extractbyexpression` z wyniku poprzedniej operacji (*clip*) obszary spełniające kryteria terenów kolejowych: `"code_2018" IN (12230)` -> *expressionD*
5. Zbudować bufor `buffer` 200 metrów dookoła obszarów zabudowanych *expressionA* z użyciem parametru `dissolve` -> *bufferA* 
6. Zbudować bufor `buffer` 250 metrów dookoła obszarów kolejowych *expressionD* z użyciem parametru `dissolve` -> *bufferD*
7. Dokonać przecięcia `intersection` warstwy *expressionS* z warstwą *expressionA* -> *intersection*
8. Dokonać odjęcia od warstwy *intersection* warstwy *bufferD* -> *difference*
9. Warstwę *difference* `difference` przekształcić algorytmem `multiparttosinglepart` -> *singlepart*
10. Z warstwy *singlepart* wybrać `extractbyexpression` obszary o powierzchni powyżej 10 ha, przy pomocy wyrażenia: `($area/10000) >  10`, gdzie podział przez 10000 oznacza przeliczenie metrów kwadratowych na hektary. 

## Rozwiązanie ćwiczenia w postaci zamkniętego modelu
> **UWAGA** w tym kroku jedynie zamieniamy sekwencję poleceń w model. Realizuje on tylko te zadania, które omówione w poprzednim zadaniu:

Praca polega dodawaniu kolejnych algorytmów z listy algorytmów dostępnych w panelu modelera. Są to w większości te same algorytmy, które dostępne są w menu processing. Jedyną trudność stanowi dodanie *expression*, gdyż nie można tu skorzystać z wyrażenia a trzeba wkleić kod taki sam jak w poceniu geoprocessingu. Różnica pomiędzy poleceniami geoprocessingu a modelerem polega na wprowadzaniu parametrów do modelu. Interesujące nas opcje to:

* `value` - wprowadzamy warość stałą, która nie zmienia się w trakcie pracy modelera
* `pre-calculated value` - wprowadzamy wyrażenie wyliczające wartość na podstawie innych parametrów
* `model input` - wprowadzamy wartość po uruchomieniu modelu
* `algorithm output` - jest to wynik dzialania innego, wprowadzonego wcześniej do modelu algorytmu

Na obecnym etapie będziemy korzystać dwóch typów wejść: `value` i `algorithm output`. Wersji `value`, gdzie wprowadzamy warstwy wejściowe (krok 1) oraz wszystkie parametry modelu nie będące warstwami, w tym również kod wyrażeń w krokach 2,3 i 4; wartości wbuforów w krokach 5 i 6 oraz wartość powierzchni w kroku 10. Wersji `algorithm output` używamy jako wejścia dla pozostałych warstw we wszyskich korkach za wyjątkiem 1. 

> **UWAGA** Każdemu algorytmowi nadajemy nazwę, nie dłuższą niż 10 znaków bez spacji (ze względu na problemy w niektórych wersjach QGIS)

W ostatnim kroku - 10, dla wyjścia nadajemy nazwę, tak aby została ona rozpoznana jako wyjście całego modelu.

[Gotowy model można zobaczyć tu](zadania/selekcjaI.model3)


## Rozbudowa modelu o możliwość sterowania parametrami odległości i powierzchni

Do modelu dodamy dodatkowe pola wejścia. Są to proste parametry numeryczne, pozwalające na testowanie różnych wartości buforów i powierzchni pól.

* Dodajemy 3 pola numeryczne, a ich typ ustawiamy na `numeric`. Każdemu z pól nadajemy nazwę, taką jaką chcemy, aby była wyświetlana w oknie dialogowym modelu.
* W algorytmach 5 i 6 zmieniamy typy wejścia dla parametru `distance` na `model input`, i jako wejścia wybieramy z listy te pola, które mają odpowiadać za zasięg bufora
* W algorytmie 10 zmieniamy wyrażenie z `($area/10000) >  10` na `($area/10000) >  @input`, gdzie zamiast 'input' wstawiamy nazwę pola zawierającego wielkość poligonu w ha. 

[Gotowy model można zobaczyć tu](zadania/selekcjaII.model3)

## Rozbudowa modelu o możliwość zmiany warstw danych i wyboru kategorii pól

W ostatnim kroku zostaną dodane pola wejścia dla dwóch warstw wektorowych. Dla danych (plik Urban Atlas) oraz dla maski obszaru (granice miasta). Pola te zostaną powiązane z polami pozwalającymi na wprowadzenie wyrażeń, określających kategorie pól użytych w selekcji. 

* Dodajemy dwa pola model input typu `vector layer`. Dopuszczalne warstwy ustawiamy na `polygon` i określamy nazwy tych pól
* W algorytmie `clip` zmieniamy typy wejścia dla warst wektorowych na `model input` i wybieramy nazwy odpowiednich pól wejścia
* Dodajemy trzy pola wejścia `expression` i jako `parent layer` dla każdego wskazujemy pole input, które będzie zawierać warstwę Urban atlas. Każdemu z pól nadajemy odpowiednią nazwę.
* Dla algorytmów 2, 3 i 4 zmieniamy typ pola w którym znajduje się wyrażenie z `value` na `model input` i jako jako pola wskazujemy odpowiednie pola wejścia modelu. Od tej pory okno dialogowe modelu pozwoli zbudować wyrażenie i dokona sprawdzenia jego poprawności.

Ostatnim krokiem jest uporządkowanie pól wejścia. Z menu *Model* wybieramy *Reorder model inputs* i zmieniamy kolejność pól wejścia, na taki układ, jaki uznamy za najbardziej logiczny.

[Gotowy model można zobaczyć tu](zadania/selekcjaIII.model3)

---

Tak wykonany model staje się narzędziem ogólnego przeznaczenia realizującym cele projektu. Model pozwala na:

* wskazać obszary podlegające selekcji
* podać kryterium bliskości (obszary nie dalej niż wartość od)
* podać kryterium odległości (obszary nie bliżej niż wartość od)
* podać kryterium powierzchni (obszary nie mniejsze niż wartość)

## Zadanie do samodzielnego wykonania:

> **UWAGA** zadanie nie jest ocenianie, jest przeznaczone dla studenów, którzy chcą podnieść swoje umiejętności
> 
Ostatnią wersję modelu rozbudować o narzędzie `conditional branch` w celu umożliwienia rezygnacji z przycinania warstwy danych maską i przeprowadzenia analizy na całym zbiorze *dane*. 

Poniżej przykład użycia i dokumentacja conditional branch:
[Tutorial](https://courses.spatialthoughts.com/advanced-qgis.html#using-conditions-in-modeler)
[Dokumentacja](https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/modelertools.html)






