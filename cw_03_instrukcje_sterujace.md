# Przetwarzanie wsadowe



## Zadanie:
Użyć zbioru danych punktowych do wycięcia fragmentów rastra i zapisanie ich jako zbiór obrazów .png

> Proces wymaga następujących kroków. 

* Trzy pierwsze kroki można wykonać przy pomocy prostego modelera, który jako parametr przyjmie wielkość bufora.
* Zbudowania zbioru punktów dowolną metodą
* Zbudowanie bufora dookoła punktów
* Zbudowania bounding box dla każdego bufora

Następnie w trybie przetwarzania pojedynczych obiektów, wykonać maskowanie rastra na podstawie bounding box. 

Następnie zapisać otrzymane warstwy do plików .png w trybie przetwarzania wsadowego.


### Zadanie:
Zbudować skrypt wycinający fragmenty rastra z użyciem instrukcji sterujących:

Jak dodać if?

* Wczytanie zbioru danych wektorowych
* Wczytanie zbioru danych rastrowych
* Wskazania promienia
* Wyznaczenie bufora dla zbioru danych
* Zamaskowanie rastra otrzymanym buforem

Wykorzystanie pętli po obiektach z użyciem modułu `extract_by_expression`

### Zadanie:
Zbudować skrypt tnący obszar ... nazwa pliku musi zawierać nazwę obszaru przechowywaną w tabeli atrybutów