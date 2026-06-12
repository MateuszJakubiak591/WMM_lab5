"""
Zadanie 3: skrypt wykonuje jednopoziomowa transformacje DWT obrazu mono,
zapisuje cztery pasma, ich histogramy oraz oblicza entropie pasm.
"""

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from wspolne import dwt, histogram_entropia, normalizuj_do_zapisu, przygotuj_katalog, wczytaj_mono


obraz = wczytaj_mono()
pasma = dict(zip(("LL", "LH", "HL", "HH"), dwt(obraz)))
katalog = przygotuj_katalog("zadanie_3")
wyniki = {}

fig, osie = plt.subplots(2, 2, figsize=(12, 9))
for os_, (nazwa, pasmo) in zip(osie.ravel(), pasma.items()):
    if nazwa == "LL":
        histogram, entropia, os_x = histogram_entropia(pasmo)
    else:
        histogram, entropia, os_x = histogram_entropia(pasmo, -255, 256)
    wyniki[nazwa] = entropia
    cv2.imwrite(str(katalog / f"pasmo_{nazwa}.png"), normalizuj_do_zapisu(pasmo))
    os_.plot(os_x, histogram)
    os_.set_title(f"{nazwa}, H = {entropia:.4f}")
    os_.set_xlabel("Wartosc")
    os_.set_ylabel("Liczba wspolczynnikow")
fig.tight_layout()
fig.savefig(katalog / "histogramy_pasm_dwt.png", dpi=160)
plt.close(fig)

for nazwa, entropia in wyniki.items():
    print(f"Entropia {nazwa}: {entropia:.6f} bit/wspolczynnik")
print(f"Srednia entropia pasm DWT: {sum(wyniki.values()) / 4:.6f} bit/wspolczynnik")
