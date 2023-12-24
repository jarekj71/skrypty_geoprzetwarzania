# Tworzenie skryptów sekwencyjnych

## Wiedza i umiejętności
Celem ćwiczeń jest opanowanie mechanizmu geoprzetwarzania przy pomocy sekwencji poleceń tekstowych. Takie rozwiązanie pozwala nie tylko zapisać listę wykonanych działań w formie poleceń wraz z parametrami, ale również pozwala na powtórzenie procedury przy użyciu innych wartości parametrów wejściowych. Same skrypty sekwencyjne nie różnią się od modeli, poza tym że nie zależą od zawodnego interface graficznego. Są jednak wstępem do zrozumienia mechanizmu tworzenia skryptów, oraz budowy w przyszłości bardziej złożonych narzędzi, w tym z wykorzystaniem instrukcji sterujących i złożonych struktur danych. Nieoczywistą zaletą skrytów jest możliwość dodawania dowolnej ilości komentarzy dokumentujących pracę co nie jest możliwe w innych trybach. 

W ramach ćwiczenia zostanie przedstawiony mechanizm tworzenia słownika parametrów skryptu oraz jego poźniejsze modyfikacje. W ramach ćwiczenia przestawione zostaną zasady budowania skrytpów, pojęcie zmiennej oraz mechanizm przepływu danych, gdzie wyniki geoprzetwarzania uprzedniego algorytmu stają się danymi wejściowymi kolejnego. 

## Zakres zajęć: 
* środowisko pisania skryptów
* Działanie funkcji `processing.run()`
* posługiwanie się panelem geoprzetwarzania do generowania poleceń skrytpu
* Integracja poleceń jako skryptu


## Cel geoinformacyjny ćwiczenia
Cel geoinformacyjny ćwiczenia nie różni się od celu zaprezentowanym w cw_01_modele. 

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

## Podstawowe informacje o tworzeniu poleceń w trybie tekstowym

Każde narzędzie geoporocessingu można uruchomić w tyrbie graficznym, z oknem dialogowym lub jako polecenie w trybie tekstowym. Poza środowiskiem QGIS, każdy algorytm można uruchomić jako komendę linii poleceń, podobnie jak inne polecenia systemu operacyjnego, takie podejście sprawdza się w praktyce jedynie w systemach linuxowych i nie jest łatwe do powtórzenia na innych maszynach.

W środowisku QGIS można uruchamiać polecenia w konsoli Pythona. QGIS dostarcza własną konsolę tego języka z dostępem do własnego API oraz wybranych bibliotek systemowych i numerycznych. Oprócz konsoli, dostępny jest również prosty edytor, gdzie można zapisywać polecenia, a pojedyncze linie lub sekwencje linii można uruchamiać, a w praktyce przenosić do konsoli przy pomocy skrótu **ctrl+E**, po ich wcześniejszym zaznaczeniu. Można też uruchomić cały skrypt. 

Skrypt to rozdzaj kodu komputerowego, który jest uruchamiany w formie sekwencji kolejno wywołwywanych poleceń przez tzw. inteprpreter. Inteprereter, to narzędzie które nie kompiluje kodu do postaci binarnej, a jedynie interpretuje kolejne otrzymywane polecenia. W języku Python poleceniem jest ciąg znaków zawarty w jednej linii. Każda linia która może być zinterpretowana zostaje wykonana a wyniki jej wykonania dostępne są w środowisku uruchomieniowym (run-time). Jeżeli jakaś linia nie może być prawidłowo zinterepretowana, czyli zawiera błędy, interpreter informuje nas o tym oraz stara się określić na czym polega błąd. 

## Polecenie `processing.run()`

Do uruchamiania algorytów QGIS służy polecenie `run` z bilioteki `processing`. W praktyce, aby uniknąć możliwego nakładania się obiektów o podobnych nazwach, nie importujemy poleceń bezpośrednio do przestrzeni nazw i używamy składni `processing.run()`. Sama biblioteka processing nie jest do końca zgodna z właściwym API QGIS, gdzie nazwy klas rozpoczynają się od `QGS...` i jest przeznaczona głównie narzędzi do tworzenia i obsługi prostych skryptów. Samo polecenie `processing.run()` posiada dwa argumenty: nazwę algorytmu, poprzedzonego nazwą tzw. providera, czyli środowiska, z którego pochodzi algorytm oraz słownika parametrów przekazywanych do polecenia. 

`processing.run("algorithm_id", {parameter_dictionary})`

gdzie: *algorithm_id* to nazwa polecenia poprzedzona nazwą providera a *{parameter_dictionary}* to słownik parametrów.

QGIS domyślnie obsługuje następujące:

* *native:* własne świdowisko
* *gdal:* polecenia biblioteki GDAL/OGR
* *SAGA:*  polecenia środowiska programu SAGA
* *GRASS:*  polecenia środowiska programu GRASS

Możliwe jest dodanie kilku innych środowisk. Każde z nich będzie również dostępne jako narzędzie w algorytmach geoprocessingu.

Parametry przekazywane są jako słowniki. Same parametry dzielą się na dwie grupy: *wymagane*, czyli takie, których podanie jest niezbędne do uruchomienia skryptu oraz *opcjonalne*, których podanie wymagane nie jest. Opcjonalność parametrów jest realizowana poprzez nadanie im wartości domyślnych. Jeżeli użytkownik nie wskaże parametru, zostanie użyty taki, jaki zaproponował autor algorytmu. Koncepcja parametrów opcjonalnych nie jest do końca spójna. Niektóre z nich mają znaczenie drugorzędne i są wykorzystywane wyłącznie w bardzo specyficznych sytuacjach (na przykład parametr określający sposób rysowania zakończeń linii w buforze) inne są kluczowe dla działania algorytmów, jak na przykład zasięg bufora i są w praktyce zawsze zmieniane.

Polecenie algorytmu można zbudować na dwa sposoby: korzystając z systemu pomocy lub kopiując algorytm jako polecenie Pythona. Aby skorzystać z systemu poleceń, należy uruchomić system pomocy (niedostępny dla providera saga) lub znaleść nazwę algorytmu na [stronie:](https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/index.html)

### System pomocy

Każdy algorytm poza opisem działania informację o *Algorithm ID:* czyli składni nazwy polecenia oraz posiada tabelę parametrów. W tabeli są podane:

* *etykieta parametru*: czyli jak parametr jest określany w oknie dialogowym, 
* *nazwa*: (zawsze dużymi literami), czyli jak parametr nazywa się w linii poleceń, 
* *typ parametru*: wraz z wartością domyślną (*DEFAULT:*). Jeżeli *DEFAULT:* nie występuje, oznacza że parametr jest wymagany. 
* *Opis parametru*: zawiera doposzczalne wartości lub zakres jaki parametr może przyjąć, oraz dodatkowe informacje.

W praktyce parametry wymagane są na początku listy a opcjonalne za nimi. Również kolejność parametrów opcjonalnych może być pomocna co do ich znaczenia. Specjalnym parametrem na końcu listy jest **OUTPUT**, który określa co zrobić z wynikiem działania algorytmu. 

Przykład z buffer

### Kopiowanie polecenia z okna dialogowego (wersja 3.22 i wyższe)

Alternatywą dla budowania polecenia na podstawie systemu pomocy jest skopiowanie polecenia z okna dialogowego (*Advanced -> Copy as Python command*). Jest to jednak metoda przeznaczona (wbrew pozorom) dla zaawansowanych użytkowników, gdyż skopiowane polecenie jest mocno zaśmiecone, przede wszystkim w słowniku parametrów, gdzie przekazana jest struktura warstw wejściowych oraz wszystkie parametry domyślne co sprawia że polecenie nie jest czytelne i wymaga oczyszczenia.

```Python

# wersja otrzymana
processing.run("native:buffer", {'INPUT':'/home/jarekj/Documents/lubrza/sites.shp','DISTANCE':1000,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'OUTPUT':'TEMPORARY_OUTPUT'})

# wersja oczekiwana
params = {'INPUT': path + sites.shp',
    'DISTANCE':1000, # tylko ten parametr był zmieniany
    'OUTPUT':'TEMPORARY_OUTPUT'}

processing.run("native:buffer", params)
```
W celu uczytelnienia skryptu najczęściej osobno zarządza się parametrami algorytmu i samym algorytmem.


## Zadanie:

W ramach zadania model wykonany w poprzednim ćwiczeniu zostanie zamieniony na sekwencyjny skrypt języka Python. 


### Ścieżka dostępu

Dane znajdują się w pliku **'PL005L2_POZNAN_UA2018_v013.gpkg'**, który powinien zostać umieszczony w katalogu **'Documents'**. Należy ustawić katalog roboczy, na **'Documents'**. Dane znajdują się w pliku `gpkg`, który zawiera kilka warstw, interesującą nas warstwą jest maska, **'PL005L2_POZNAN_UA2018_UrbanCore'**. Odczytując dane zbudowane w ten sposób należy wskazać zarówno plik jak i maskę. Wszystkie elementy składające się na ścieżkę dostępu do danych warto przechowywać w osobnych zmiennych. Dostęp do warstw w `gpkg` realizowany jest poprze składnię: `plik|layername=layer_name`

```python
import os
import porocessing

current_path = os.getcwd()
file = 'PL005L2_POZNAN_UA2018_v013.gpkg'
data_layer = 'PL005L2_POZNAN_UA2018'
mask_layer = 'PL005L2_POZNAN_UA2018_UrbanCore'
source_file = os.path.join(os.path.expanduser("~"),'Documents',file)
data = "{}|layername={}".format(source_file,data_layer)
mask = "{}|layername={}".format(source_file,mask_layer)
```
### Krok clip

Do wykonania instrukcji `clip` użyjemy metody kopiowania.

```python
processing.run("native:clip", {'INPUT':'/home/jarekj/Documents/PL005L2_POZNAN_UA2018_v013.gpkg|layername=PL005L2_POZNAN_UA2018','OVERLAY':'/home/jarekj/Documents/PL005L2_POZNAN_UA2018_v013.gpkg|layername=PL005L2_POZNAN_UA2018_UrbanCore','OUTPUT':'TEMPORARY_OUTPUT'})
```
Wynik kopiowania zawiera  bezwględne ścieżki dostępu, również słownik parametrów jest zintegrowany z poleceniem. W celu poprawy czytelności słownik zostanie oddzielony od polecenia, a bezwzględne ścieżki zostaną zamienione na zbędne, utworzone w poprzednim kroku. Nazwy parametrów jak widać w skopiowanym fragmencie to' INPUT' i 'OVERLAY'. W parametrach znajduje się spcjalny parametr 'OUTPUT', który określa jak ma być utworzona warstwa wyjściowa. W tym wypadku jest to warstwa tymczasowa.

```python
params = {'INPUT':data,
'OVERLAY':mask,
'OUTPUT':'TEMPORARY_OUTPUT'}

clipped = processing.run("native:clip", params)
```

#### Podgląd warstwy geoprzestrzennej

Warstwa tymczasowa nie jest dostępna do obserwacji, gdyż nie została dodana do obszaru projektu. Aby zobaczyć warstwę, należy zastosować metodę `.addMapLayer` obiektu `QgsProject`, który, jak sama nazwa wskazuje przechowuje elementy projektu QGIS. Sama zmienne `clipped` przechowuje słownik, którego jednym z elementów (w tym wypadku jedynym) jest ['OUTPUT'], przechowujący warstwę danych. Tę warstwę możemy wyświetlić lub dodać do projektu. Obiekt `QgsProject` nie jest częścią API processing, ale głównego API systemu QGIS.

```python
QgsProject.instance().addMapLayer(clipped['OUTPUT'])
```
W trakcie pisania skryptów warto sprawdzać pośrednie wyniki działania, szczególnie na etapie początkowym. Ten krok nie będzie już ponawiany w dalszej części.

### Kroki selectbyexpression
Są to trzy kroki, gdzie słownik parametrów wykorzystamy kilka razy, za każdym razem zmieniając jedynie parametr 'EXPRESSIONS'. Jako `INPUT` zostanie użyta warstwa `clipped` utworzona w poprzednim kroku. W pierwszym kroku jednak zbudujemy zmienne zawierające łańcuchy tekstowe zawierające kody typów pokrycia terenu, które powinny zostać wybrane w każdym z trzech kroków. Takie podejście upraszcza pisanie kodu. 

```python
selected_areas_codes = '21000, 22000, 23000, 24000, 13400' # jako tekst
attached_areas_codes = '11100, 11210, 11220, 11230, 11240'
detached_areas_codes = '12230'

# pierwsza selekcja
params =  {'INPUT':clipped['OUTPUT'], 
'EXPRESSION':' "code_2018" IN ({})'.format(selected_areas_codes),
'OUTPUT':'TEMPORARY_OUTPUT'}
selected_areas = processing.run("native:extractbyexpression",params)

# druga selekcja
params['EXPRESSION'] = ' "code_2018" IN ({})'.format(attached_areas_codes)
attached_areas = processing.run("native:extractbyexpression",params)

# trzecia selekcja
params['EXPRESSION'] = ' "code_2018" IN ({})'.format(detached_areas_codes)
detached_areas = processing.run("native:extractbyexpression",params)
```

### Kroki buffer
Podobnie jak w poprzednich krokach zmieniane są tylko wybrane paprametry algorytmu `buffer`: warstwa wejściowa ('INPUT') oraz 'DISTANCE'. Warstwami wejściowymi są wyniki działania algorytmu `extractbyexpression`, natomiast odległości to parametry, które definijemy sami. Pozostałe parametry zostały albo pominięte i pozostawione ich domyślne wartości, albo zostają ustawione raz i nie zmieniane w kolejnych wywołaniach.

```python
attached_buffer = 200
detached_buffer = 250

params = {'INPUT':attached_areas['OUTPUT'],
'DISTANCE':attached_buffer,
'DISSOLVE':True,
'OUTPUT':'TEMPORARY_OUTPUT'}
attached_buffer = processing.run("native:buffer",params)

params['DISTANCE'] = detached_buffer
params['INPUT'] = detached_areas['OUTPUT']
detached_buffer = processing.run("native:buffer",params)
```

### Kroki  intersection i difference
Są to dwa osobne algorytmy, jednakże korzystają z tego samego słownika parametrów. Z tego powodu podonie jak w poprzednich krokach użyjemy tego samego słownika. Wejściem dla intersection są wyniki selekcji obszarów do zabudowy `selected_areas` oraz `attached_buffer` dla algorytmu `difference` odpowiednio wyniki `interection` i `detached_buffer`.

```python
#overlays

params = {'INPUT':selected_areas['OUTPUT'],
'OVERLAY':attached_buffer['OUTPUT'],
'OUTPUT':'TEMPORARY_OUTPUT'}
interesection = processing.run("native:intersection",params)

params['INPUT'] = intersection['OUTPUT']
params['OVERLAY'] = detached_buffer['OUTPUT']
difference = processing.run("native:difference",params)
```

### Krok multiparttosinglepart

To prosty krok a algorytm nie zawiera żadnych parametrów poza 'INPUT' i 'OUTPUT'

```python
params = {'INPUT':difference['OUTPUT'],
'OUTPUT':'TEMPORARY_OUTPUT'}
single = processing.run("native:multiparttosingleparts",params)
```

### Krok extractbyexpression

Ostatni krok ponownie wymaga ustawienia parametru, w tym wypadku `min_area=10`. W przeciwieństwie jednak do rozwiązania przy pomocy modelera, nie używamy składni `expression`, ale budujemy wyrażenie używając metod pracy pythona z łańcuchami tekstu.

```Python
min_area=10
params =  {'INPUT':single['OUTPUT'],
'EXPRESSION':'($area/10000) > {}'.format(min_area),
'OUTPUT':'TEMPORARY_OUTPUT'}

result = processing.run("native:extractbyexpression",params)
```
### Zakończenie skryptu i dodanie wyniku do mapy projektu
Jeżeli wszystkie polecenia zostały wykonane można sprawdzić warstwę wynikową  dodając ją do projektu poznaną wcześniej metodą:

```Python
QgsProject.instance().addMapLayer(result['OUTPUT'])
```
Jeżeli skrypt działa prawidłowo, warto wszystkie modyfikowane przez użytkownika parametry wejściowe umieścić na początku skrytpu w jednym miejscu. Uodporni to skrypt na błędy spowodowane zmianami kodu przez użytkownika, który mógłby przypadkowo zmienić newralgiczne części kodu.

Na koniec warto jeszcze raz przetestować cały skrypt uruchamiając go w całości poleceniem **Run...** z belki narzędziowej.

Pełna wersja skryptu znajduje się [tutaj](zadania/cw_2_selekcja.py)


## Zadanie:
Rozszerzyć skrypt o kryterium odległości względem lotniska - działki nie mogą być bliżej niż 1 km do lotniska

## Zadanie:
Zmodyfikować skrypt tak, aby poszczególne narzędzia geoprocessingu opakować w funkcje, a parametry przekazywać jako argumenty funkcji

