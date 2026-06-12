"""
Zadanie 5: skrypt rozdziela obraz monarch_col.png na skladowe RGB,
zapisuje skladowe i wspolny histogram oraz oblicza ich entropie.
"""

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from wspolne import histogram_entropia, przygotuj_katalog, wczytaj_kolor


obraz_bgr = wczytaj_kolor()
skladowe = {
    "R": obraz_bgr[:, :, 2],
    "G": obraz_bgr[:, :, 1],
    "B": obraz_bgr[:, :, 0],
}
kolory = {"R": "red", "G": "green", "B": "blue"}
katalog = przygotuj_katalog("zadanie_5")
entropie = {}

plt.figure(figsize=(10, 5))
for nazwa, skladowa in skladowe.items():
    histogram, entropia, os_x = histogram_entropia(skladowa)
    entropie[nazwa] = entropia
    cv2.imwrite(str(katalog / f"skladowa_{nazwa}.png"), skladowa)
    plt.plot(os_x, histogram, color=kolory[nazwa], label=nazwa)
plt.title("Histogramy skladowych RGB")
plt.xlabel("Wartosc")
plt.ylabel("Liczba pikseli")
plt.xlim(0, 255)
plt.legend()
plt.tight_layout()
plt.savefig(katalog / "histogramy_rgb.png", dpi=160)
plt.close()

for nazwa, entropia in entropie.items():
    print(f"Entropia {nazwa}: {entropia:.6f} bit/piksel")
print(f"Srednia entropia RGB: {sum(entropie.values()) / 3:.6f} bit/piksel")
