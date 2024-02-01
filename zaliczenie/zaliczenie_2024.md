# Zaliczenie programowanie geoinformacyjne 2024

W katalogu **zaliczenie** załączony jest spakowany plik z granicami gmin w układzie PUWG1992 i modelem wysokościowym o rozdzielczości 90m w układzie WGS84

## Ocena dostateczna plus:

   Utworzyć skrypt, który:

   1. Ujednolici układy odniesienia obu warstw do UWG1992
   2. Policzy średnią i odchylenie standardowe wysokości terenu dla każdej z gmin (statystyki strefowe)
   3. Wybrać gminy powyżej wartości progowej wysokości. Wartość progową przyjąć jako parametr skryptu (może być dowolnie zmieniana)
   4. Dla każdej wybranych gmin:
      1. zbudować bounding box granic
      2. zbudować bufor wokół bounding box o wartości zadanej parameterem
      3. bufory zapisać jako osobne pliki gpkg we wskazanym katalogu
      4. wykorzystać bufor do wycięcia obszarów z pliku rastrowego i zapisać w katalogu o nazwie zadanej parametrem skryptu. Katalog tworzymy w ramach skryptu 

Zadanie nie narzuca sposobu rozwiązania ani doboru wartości zadanych parametrów. Rozwiązaniem zadania jest skrypt w formie pliku .py oraz wynik jego działania w postaci katalogu wektorów. Jedynym elementem, który nie był omawiany na zajęciach są statystyki strefowe (zonal statistics), ale jest to zagadnienie znane. Skrypt nie wymaga instrukcji sterujących



## Ocena dobra plus:
1. Dla katalogu danych, pozyskanych w poprzednim kroku, każdy obszar zapisany w pliku gpkg użyć do wycięcia rastra. Wynik wycięcia zapisać w tym samym katalogu
2. Dla każdego rastra obliczyć statystyki: średnia, odchylenie standardowe, minimum, maximum, ilość komórek, powierzchnia rastra. Statystyki zapisać w formacie DataFrame oraz wyeksportować do pliku csv. 

Zadanie nie narzuca sposobu rozwiązania. Skrypt wymaga użycia pętli oraz w zależności od sposobu rozwiązania warunku. Niektóre statystyki do obliczeniawykraczają poza zakres zajęć.

## Ocena bardzo dobra:

WYkorzystać DataFrame z poprzedniego zadania i wyniki statystyk: średnia i odchylenie standardowe przedstawić w formie wykresu errorbar:

https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.errorbar.html

Wielkość rastra spróbować przedstawić jako wielkość punktu. Oś x powinna mieć etykiety numerów rastrów. Wykres powinien mieć tytuł oraz podpisy osi x i y.

Przykład wykresu:

https://matplotlib.org/stable/gallery/statistics/errorbar.html#sphx-glr-gallery-statistics-errorbar-py

Skrypt wymaga podstawowej wiedzy na temat posługiwania się grafiką prezentacyjną. Typ wykresu nie był omawiany na zajęciach i wymaga zapozania się z systemem pomocy, do którego linki zostały przekazane powyżej.