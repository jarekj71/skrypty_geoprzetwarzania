# Symulacje i optymalizacje

## Wiedza i umiejętności
W ramach zajęć zostaną zaprezentowane wiedza i umiejętności niezbędne do wykorzystania algorytmów geoprzetwarzania do projektowania geoprzestrzennych symulacji i optymalizacji.  Oba zagadnienia różnią się, pomimo podobnej metodyki (podejście iteracyjne). Symulacja to proces iteracyjny, gdzie każdy krok reprezentuje jakiś stan systemu powstały pod wpływem zmieniajacych się danych i parametrów wejściowych i każdy krok jest jednakowo ważny. Optymalizacja to proces, w którym zarówno dane jak i parametry wejściowe zmieniają się iteracyjnie, ale liczą się tylko te kroki, które prowadzą do poprawy parametru zwanego funkcją kosztu. Ostatecznie w wynikiem symulacji jest osiągnięcie założonej warości funkcji kosztu, lub znalezienie jej akceptowalnego minimum. Projektowanie symulacji czy optymalizowanie procesów wymaga zaawansowanej wiedzy na temat symulowanych lub optymalizowanych zjawisk. W ramach ćwiczenia zostaną przedstawione jedynie ramy jak tego typu skrypty projektować w środowisku analiz geoprzestrzennych, ale ich praktyczna implementacja jest raczej zagadnieniem specyficznych problemów badawczych.


## Zakres zajęć
Zajęcia podzielone są na dwa osobne ćwiczenia, jedno poświęcone przykładowej symulacji, drugie optymalizacji. 

Umiejętności obejmują:

* opracowanie kroków symulacji
* losowy dobór podzbioru danych wejściowych
* wykonanie agregacji wyników
* wykorzystanie providera SAGA GIS
* użycie listy jako parametru wejściowego
* dobór optymalizowanych parametrów i zbudowanie optymalizatora
* dobór funkcji kosztu
* praca z tymczasowymi kolumnami
* dodatkowo zostanie zaprezentowana metoda budowania wyrażenia (*expresssion*) przy pomocy funkcji.


## Cele geoinformacyjne ćwiczeń
Wspólnym celem obu ćwiczeń jest zbudowanie iteracyjnego procesu, w ramach którego dla każdej iteracji będą zmieniane dane wejściowe i/lub parametry algorytmów wykorzystanych w skrypcie. Odmienne są cele obu ćwiczeń:

### Ćwiczenie 1
Celem ćwiczenia jest zbudowanie skryptu porównującego wyniki interpolacji danych ze zmieniającym się zestawem puntków, a następnie wskanie miejsc o największej niepewności wyniku. W każdej iteracji będzie losowany inny pozbiór punktów, a następnie wykonywana interpolacja. Każdy z wyników ma jednakowe znaczenie.

Interpolacja jest wykonywana przy pomocy algorytmów dostarczanych przez program *SAGA GIS*. Wykorzystanie algorytmów *SAGA* rozszerza znacząco możliwości analityczne środowiska QGIS i pozwala budować rozbudowane procedury analityczne w jednym środowisku. Sposób obsługi parametrów wejściowych *SAGA* różni się od *QGIS*, a jedną z różnic jest zwracanie przez *SAGA* kilku warstw wyjściowych z reguły o różnych nazwach, oraz sposób nazywania parametrów.

> **UWAGA 1**: provider *SAGA* nie zawsze dobrze współpracuje z systemem *QGIS*, głównie z powodu częstych zmian nazw parametrów wejściowych i zmian koncepcji rozwoju środowiska *SAGA GIS*

> **UWAGA 2**: Środowisko *SAGA GIS* generalnie nie jest wzorem stabilności, niezawodności i zgodności wyników z rzeczywistością. Stosować z ostrożnoscią. System pomocy jest również ograniczony i przestarzały.

### Ćwiczenie 2
Celem ćwiczenia jest zbudowanie skryptu, gdzie w każdej z iteracji będzie modelowany zasięg pracy "nadajników". Łączna moc nadajników jest ograniczona, a celem procesu jest znalezienie takiej konfiguracji mocy, aby objąć jak największą liczbę adresów. W optymalziacji liczy się jedynie najlepszy wynik.

Sama optymalizacja wymaga zdefiniowania kilku elementów: z reguły są to: strategię przeszukiwania, przestrzeń rozwiązań oraz funkcję celu. Dodatkowo można zdefiniować ograniczenia dla przestrzeni rozwiązań: twarde i miękkie.

* **Przestrzeń rozwiązań**, to zakres wartości jakie mogą przyjmować poszczególne parametry. Jest to jednocześnie ograniczenie twarde. Z reguły nie zakładamy że wartości parametrów mogą być całkowicie dowolne
* **Strategia przeszukiwania** określa w jaki sposób przeszukujemy przestrzeń rozwiązań. W sytuacji, gdy nie ma możliwości sprawdzenia wszystkich rozwiązań (*exahaustive search*), sprawdzamy jedynie ograniczony podzbiór. Pozdzbiór może być definiowany dla skończonej listy parametrów (*regular search*), losowego zestawu (*random search*) lub można stosować bardziej zaawansowane metody, gdzie każdy kolejny krok wykorzystuje wyniki kroku poprzedniego (*gradient descent search*). Dobór metod zależy od wielu czynników i optymalizowanego problemu.
* **Funkcja celu** to wartość jaką staramy się minimalizować  wtedy jest określana jako funnkcja kosztu (*loss function*) lub rzadziej, maksymalizować - wtedy określana jako funkcja zysku (*gain*) i wskazuje, najbardziej optymalne z punktu widzenia celu optymalizacji
* **Ograniczenia twarde** to takie, które nie mogą być przekroczone. Przestrzeń rozwiązań to jedno z ograniczeń twardych. W procesie optymalizacji warianty nie spełniające ograniczeń twardych nie są rozważane.
* **Ograniczenia miękkie** to takie, które wskazują w przestrzeni rozwiązań obszar gdzie chcielibyśmy zanaleść rozwiązanie. Ograniczenia miękkie są nadawane z reguły w postaci tak zwanych kar (penalties)na funkcję celu, zmiejszając zysk lub zwiększając koszt i utrudniajac akceptację wyniku jeżeli został osiągnięty zbyt dużym kosztem (lub stanowi zbyt mały zysk).

## Dane i algorytmy geoprzetwwarzania
Dane znajdują się...

Do zrealizowania zadań będą potrzebne następujące narzędzia i algorytmy:

* biblioteka `random`, będąca częścią pakietu `numpy`
* biblioteka `core` Qgis, metody klas `QgsProperty`, `QgsVectorLayer`, `QgsRasterLayer`, `QgsRectancle` 
* `native:randomextract` do losowego wyboru podzbioru punktów
* `saga:interpolatecubicspline` jako jeden z algorytmów interpolacji dostarczanych przez providera *SAGA GIS*
* `native:cellstatistics` do agregacji wyników symulacji
* `native:buffer` do wyznaczenia buforów o zmiennym zasięgu
* `native:fieldcalculator` do obliczenia zmieniających się wartości pól **distance** oraz obliczenia powierzchni buforów
* `native:extractbylocation` do wydobycia i policzenia punktów znajdujących się w buforze


## Ćwiczenie 1 Symulacja

Plik *próbkowanie.gpkg* zawiera kilkaset punktów z wartościami wysokości. Celem zadania jest określenie, które obszary zbioru danych cechują się największą niepewnością wyniku względem zastosowanego algorytmu interpolacji. Aby taki wynik osiągnąć z głównego zbioru danych usuwa się losowo część danych a następnie wykonuje interpolację. W wyniku utraty części danych wyniki lokalnie zmieniają się, ale skala zmian zależy od konfiguarcji punktów otoczenia (które nie zostały osiągnięte). Jeżeli utracone dane mogą być skutecznie zastąpione punktami otoczenia to niepewność wyniku w takim miejscu jest mała. Jeżeli jednak utrata danych powoduje drastyczną zmianę, oznacza to że wynik działania algorytmu jest w takim miejscu niepewny.

### Losowanie podzbioru

Sam proces jest relatywnie prosty do implementacji. Do losowania punktów służy algorytm `native:randomextract`, który służy właśnie do wykonywania tego typu symulacji. Jedynym parametrem jest wielkość podzbioru, definiowana jako ilość lub odsetek zbioru głównego. Zaden z parametrów nie jest zmieniany w kolejnych krokach iteracji.

```Python
pparams = {'INPUT':points,
    'METHOD':1,
    'NUMBER':80,
    'OUTPUT':'TEMPORARY_OUTPUT'}

randomed = processing.run("native:randomextract", pparams)
```

### Interpolacja
Do wykonania interpolacji pozostawimy parametry domyślnie, które jednak muszą być wskazne jawnie. Wiele parametrów ma nazwy inne niż środowisko *QGIS*. **TARGET_USER_SIZE** to rozdzielczość; **SHAPES** to odpowiednik **INPUT**, wskazujący że dane wejściowe to plik wektorowy. Odpowiednikiem **EXTENT** jest **'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX'**. Parametr **FIELD_NAME** skrócony jest do **FIELD**. Nazwa warstwy wyjściowej jest różna dla różnych algorytmów; tu jest to **TARGET_OUT_GRID**. 

W kolejnych krokach iteracji ustawiane są SHAPES - z każdym razem wynik losowania punktów oraz nazwa pliku wyjściowego. Pozostałe parametry pozostawiamy bez zmian. Jako rozdzielczość przyjmiemy 100 (m) w celu realizacji zadania w trybie dydaktycznym. 

```Python
iparams = {'SHAPES':points,
    'FIELD':'SAMPLE_1',
    'NPMIN':5,
    'NPMAX':20,
    'NPPC':5,
    'K':140,
    'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX':ext,
    'TARGET_USER_SIZE':100,
    'TARGET_USER_FITS':0,
    'TARGET_OUT_GRID':''}
```

Tym samym główna pętla programu jest bardzo prosta:

```Python
for i in range(nsteps):
    randomed = processing.run("native:randomextract", pparams)

    iparams['SHAPES'] = randomed['OUTPUT']
    iparams['TARGET_OUT_GRID'] = os.path.join(destination,'s{:03d}.sdat'.format(i)) # musi być ścieżka bezwzględna
    dem = processing.run("saga:interpolatecubicspline",iparams)
```

### Agregacja wyników

Do agregacji wyników wykorzystamy algorytm  `native:cellstatistics`. Pierwszym krokiem jest zbudowanie listy plików w katalogu wyściowym z rozszerzeniem "`.sdat`" rozpoznawanym przez sterowniki biblioteki GDAL jako pliki programu *SAGA* oraz połączenia ich ze ścieżką dostępu:

```Python
lista = os.listdir(folder)
files = [l for l in lista if l.endswith(".sdat")]
files.sort()

fullpath_list = [os.path.join(folder,l) for l in files]
```

Lista wynikowa jest wartością parametru **INPUT**

Parametry algorytmu wymagają podania warstwy referencyjnej, z której zostanie pobrany zasięg i rozdzielczość warstwy wyjściowej, w tym wypadku możemy użyć pierwszego elementu listy. Parametr **STATISTIC** pozostawiamy pusty. Zostanie on ustawiony na 2 (średnia) i 4 (odchylenie standardowe) przed uruchomieniem algorytmu.

```Python 
listparam = {'INPUT':fullpath_list,
    'STATISTIC':'',
    'IGNORE_NODATA':True,
    'REFERENCE_LAYER':fullpath_list[0],
    'OUTPUT':'TEMPORARY_OUTPUT'}

listparam['STATISTIC'] = 2 # srednia
mean = processing.runAndLoadResults("native:cellstatistics",listparam)

listparam['STATISTIC'] = 4 # odchylenie 
std = processing.runAndLoadResults("native:cellstatistics",listparam)
```
Pełny kod skryptu znajduje się [tutaj](zadania/cw_6_1_symulacja.py).


## Ćwiczenie 2

W przykładzie zastosujemy strategię przeszukiwania losowego. Ograniczeniem twardym będzie wymóg nieprzekraczalnej sumy mocy "nadajników", a ograniczeniem miękkim (penalty) będzie  zróżnicowanie mocy poszczególnych nadajników - im większe zróżnicowanie tym większa kara nakładana na funkcję celu. Przestrzeń rozwiązań (określaną jako domenaa) zdefiniujemy zakresem od 0.2 do 0.6 maksymalnej mocy dla każdego nadajnika. Ograniczenie twarde wyrazimy sumą mocy wszystkich nadajników a ograniczenie miękkie będzie wyrażone odchyleniem standardowym mocy nadajników. Wszystkie te elementy zostaną zdefiniowane jako osobne funkcje języka Python. Operacje geoprzestrzenne będą służyły jedynie obliczeniu funkcji celu. Łączną moc nadajników zdefiniujemy na 6000, a liczbę kroków symulacji na 100.

### Zdefiniowanie parametrów i ograniczeń

Ograniczenia są wyliczane w taki sposób, że zestaw parametrów - czyli trzy losowe liczby [0,1] są przeliczane na przedział określony wartościami min i max a następnie mnożone przez parametr skalujący, tak aby suma wynosiła *total*. W tym celu wystarczy dowolny ciąg liczb przemnożyć przez iloraz oczekiwanej sumy i sumy wartości liczb w wektorze: `r *= total/r.sum()`. Funkcja kary wraca po prostu odchylenie standardowe. 

```Python
total = 6000
nsteps = 100
min_ = 0.2
max_ = 0.6

def constrains(r,total,min=0,max=1):
    r = r * (max-min) + min
    r *= total/r.sum()
    return r 

def penalty(r):
    return r.std()
```

Fukcja celu to liczba punktów adresowych objętych nadajnikami. Przyjmujemy, że im więcej nadajników tym lepiej, a więc funkcję celu musimy maksymalizować (staje się w tej sytuacji funkcją zysku) a kara w takiej sytuacji jest odejmowana a nie dodawana. Do obliczenia funkcji celu potrzebujemy kilka algorytmów. 

### Dodanie parametrów buforowania nadajników
Najważniejszym jest `native:fieldcalculator`, dla którego ustawiamy kilka parametrów: warstwę z nadajnikami oraz nazwę dodawanego pola (*distance*). Nie ustawiamy pola **FORMULA**, które będzie zmieniane w każdej iteracji.

Formułę tworzy expression wykorzystujące funkcję `array_get` pozwalającą wstawić do danego pola wartość z tablicy określoną indeksem. Indeksem jest numer wiersza `@row_number`, który nie jest jednak zdefiniowany w kreatorze wyrażeń (w wesji 2.0 był jako `$row_num`). Do wstawienia wartości do pól funkcji `array` służy operator rozwijania krotki, który może być stosowany również do tablic numpy.

```Python
calc_param = {'INPUT':nadajniki,
    'FIELD_NAME':'distance',
    'FIELD_TYPE':0,
    'FORMULA':'', 
    'OUTPUT':'TEMPORARY_OUTPUT'}

def formula(r):
    return 'array_get(array({},{},{}),@row_number)'.format(*r)

distances = processing.run("native:fieldcalculator",calc_param)['OUTPUT']
```
Wynikiem działania algorytmu jest nowa warstwa zawierająca punkty z przypisanymi wartościami bufora do obliczenia w następnym kroku

### Obliczenie bufora i wybór punktów adresowych
Do obliczenia liczby punktów adresowych w zasięgu nadajników potrzebujemy obszaru objętego nadajnikami. Obszar ten wyznaczony zostanie buforem `native:buffer`, gdzie parametr **DISTANCE** będzie pobierany indywidualnie z pola *distance* obliczonego w poprzedni kroku. Aby pozyskać parametry dla każdego kroku iteracji użyjemy poznaną już metodę `fromExpression()` klasy `QgsProperty`. W tym wypadku ograniczoną do podania nazwy pola *'distance'*. Jako **INPUT** stosujemy warstwę utworzoną przy pomocy `native:fieldcalculator` w poprzednim kroku.

Obliczenie ilości punktów adresowych użyjemy metody `native:extractbylocation` gdzie jako warstwy wejściowej użyjemy warstwy *punkty_adresowe*, a jako warstwy przecięcia **INTERSECT** bufora utworzonego w poprzednim kroku.

```Python
buffer_params = {'INPUT':'',
    'DISTANCE':QgsProperty.fromExpression('"distance"'),
    'DISSOLVE':True,
    'OUTPUT':'TEMPORARY_OUTPUT'}

buffer_params['INPUT'] = distances
buffer = processing.run("native:buffer", buffer_params)['OUTPUT']

select_params = {'INPUT':punkty_adresowe,
    'PREDICATE':[6],
    'INTERSECT':'',
    'METHOD':0,
    'OUTPUT':'TEMPORARY_OUTPUT'}

select_params['INTERSECT'] = buffer
selected = processing.run("native:extractbylocation", select_params)['OUTPUT']
```

### Główna pętla programu - obliczenie funcji kosztu

1. Główna pętla rozpoczyna się wylosowaniem 3 liczb,  
2. następnie nałożenia na nich ograniczeń (zakresu wartości i ograniczenia sumy). 
3. Obliczone wartości buforów zostają dołączone do formuły i użyte do dodania jako nowe pole warstwy z "nadajnikami.
4. Kolejne trzy kroki to obliczenie:
   1. Warstwy z paramerami buforów *distances*
   2. Warstwy z buforem *buffer*
   3. Warstwy z punktami znajdującymi się w buforze
5. Liczba punktów objętych nadajnikami zostaje pozyskana przez metodą `featureCount()`
6. A funkcja zysku zostaje obliczona poprzez odjęcie od liczby odchylenia standardowego różnicy promieni buforów
7. Następnie testujemy czy funkcja zysku jest większa od maksymalnej wartości obliczonej w pierwszym kroku 
   1. i jeśli tak, to wartość funkcji wysku zastępuje poprzednią wartość maksymalną 
   2. a warstwa punktowa z promieniamu buforów zostaje zachowana
   3. Dodatkowo wypisujemy wartość aktualną funkcji zysku

```Python
for i in range(nsteps):
    dm = np.random.rand(3) #1
    constr = constrains(dm,total,min_,max_) #2
    calc_param['FORMULA'] = formula(constr) #3
    distances = processing.run("native:fieldcalculator",calc_param)['OUTPUT'] #4.1
    buffer_params['INPUT'] = distances
    buffer = processing.run("native:buffer", buffer_params)['OUTPUT'] #4.2
    select_params['INTERSECT'] = buffer
    selected = processing.run("native:extractbylocation", select_params) #4.3['OUTPUT']
    count = selected.featureCount() #5
    gain = count-penalty(constr) #6
    if gain > max_gain: #7
        max_gain = gain #7.1
        best_distances = distances #7.2
        print("    {:.3f}".format(max_gain)) #7.3
```
### Dodanie warstwy do mapy

Ostatnim krokiem jest ponowne wyliczenie buforów dla najlepszego zestawu parametrów i dodanie bufora do mapy QGIS.

Pełny kod skryptu znajduje się [tutaj](zadania/cw_6_2_optymalizacja.py)

Wielokrotne uruchomienie skryptu pokazuje, że przy takich samych ograniczeniach optymalne rozwiązania są prawie identyczne, co oznacza że skrypt znajduje wartości suboptymalne.