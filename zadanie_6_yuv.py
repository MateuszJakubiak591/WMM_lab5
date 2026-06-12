"""
Zadanie 6: skrypt konwertuje kolorowy obraz BGR/RGB do przestrzeni YUV,
zapisuje skladowe, ich histogramy i porownuje entropie RGB oraz YUV.
"""

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from wspolne import histogram_entropia, przygotuj_katalog, wczytaj_kolor


obraz_bgr = wczytaj_kolor()
obraz_yuv = cv2.cvtColor(obraz_bgr, cv2.COLOR_BGR2YUV)
rgb = {"R": obraz_bgr[:, :, 2], "G": obraz_bgr[:, :, 1], "B": obraz_bgr[:, :, 0]}
yuv = {"Y": obraz_yuv[:, :, 0], "U": obraz_yuv[:, :, 1], "V": obraz_yuv[:, :, 2]}
katalog = przygotuj_katalog("zadanie_6")

fig, osie = plt.subplots(1, 2, figsize=(14, 5))
entropie = {}
for os_, zbior, tytul in zip(osie, (rgb, yuv), ("RGB", "YUV")):
    for nazwa, skladowa in zbior.items():
        histogram, entropia, os_x = histogram_entropia(skladowa)
        entropie[nazwa] = entropia
        cv2.imwrite(str(katalog / f"skladowa_{nazwa}.png"), skladowa)
        os_.plot(os_x, histogram, label=nazwa)
    os_.set_title(f"Histogramy {tytul}")
    os_.set_xlabel("Wartosc")
    os_.set_ylabel("Liczba pikseli")
    os_.set_xlim(0, 255)
    os_.legend()
fig.tight_layout()
fig.savefig(katalog / "porownanie_histogramow_rgb_yuv.png", dpi=160)
plt.close(fig)

for nazwa in ("R", "G", "B", "Y", "U", "V"):
    print(f"Entropia {nazwa}: {entropie[nazwa]:.6f} bit/piksel")
print(f"Srednia entropia RGB: {sum(entropie[x] for x in 'RGB') / 3:.6f} bit/piksel")
print(f"Srednia entropia YUV: {sum(entropie[x] for x in 'YUV') / 3:.6f} bit/piksel")
