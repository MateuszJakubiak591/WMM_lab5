"""
Zadanie 2: skrypt tworzy poziomy obraz roznicowy z predykcja od lewego
sasiada, zapisuje jego wizualizacje, porownuje histogramy i entropie.
"""

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from wspolne import (
    histogram_entropia,
    normalizuj_do_zapisu,
    obraz_roznicowy_poziomy,
    przygotuj_katalog,
    wczytaj_mono,
)


obraz = wczytaj_mono()
roznice = obraz_roznicowy_poziomy(obraz)
hist_mono, entropia_mono, os_mono = histogram_entropia(obraz)
hist_roznice, entropia_roznice, os_roznice = histogram_entropia(roznice, -255, 256)
katalog = przygotuj_katalog("zadanie_2")

cv2.imwrite(str(katalog / "obraz_roznicowy.png"), normalizuj_do_zapisu(roznice))

fig, osie = plt.subplots(2, 1, figsize=(11, 8))
osie[0].plot(os_mono, hist_mono, color="black")
osie[0].set_title("Histogram obrazu oryginalnego")
osie[0].set_xlim(0, 255)
osie[1].plot(os_roznice, hist_roznice, color="darkred")
osie[1].set_title("Histogram obrazu roznicowego")
osie[1].set_xlim(-255, 255)
for os_ in osie:
    os_.set_xlabel("Wartosc")
    os_.set_ylabel("Liczba pikseli")
fig.tight_layout()
fig.savefig(katalog / "porownanie_histogramow.png", dpi=160)
plt.close(fig)

print(f"Zakres obrazu roznicowego: [{roznice.min()}, {roznice.max()}]")
print(f"Entropia obrazu oryginalnego: {entropia_mono:.6f} bit/piksel")
print(f"Entropia obrazu roznicowego: {entropia_roznice:.6f} bit/piksel")
print(f"Zmiana entropii: {entropia_roznice - entropia_mono:+.6f} bit/piksel")
