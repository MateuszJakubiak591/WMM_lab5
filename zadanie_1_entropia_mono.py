"""
Zadanie 1: skrypt oblicza histogram i entropie monochromatycznego obrazu
monarch_mono.png, a nastepnie zapisuje histogram do katalogu wyniki.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from wspolne import histogram_entropia, przygotuj_katalog, wczytaj_mono


obraz = wczytaj_mono()
histogram, entropia, os_x = histogram_entropia(obraz)
katalog = przygotuj_katalog("zadanie_1")

plt.figure(figsize=(10, 5))
plt.plot(os_x, histogram, color="black")
plt.title("Histogram obrazu monarch_mono")
plt.xlabel("Wartosc piksela")
plt.ylabel("Liczba pikseli")
plt.xlim(0, 255)
plt.tight_layout()
plt.savefig(katalog / "histogram_mono.png", dpi=160)
plt.close()

print(f"Wymiary: {obraz.shape[1]} x {obraz.shape[0]}")
print(f"Entropia obrazu monochromatycznego: {entropia:.6f} bit/piksel")
