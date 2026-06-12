"""
Zadanie 4: skrypt oblicza przeplywnosc pliku PNG dla obrazu mono i porownuje
ja z entropia oryginalu, obrazu roznicowego oraz srednia entropia pasm DWT.
"""

from wspolne import (
    ROOT,
    dwt,
    histogram_entropia,
    obraz_roznicowy_poziomy,
    przeplywnosc,
    wczytaj_mono,
)


obraz = wczytaj_mono()
_, h_mono, _ = histogram_entropia(obraz)
_, h_roznice, _ = histogram_entropia(obraz_roznicowy_poziomy(obraz), -255, 256)
ll, lh, hl, hh = dwt(obraz)
h_pasma = [
    histogram_entropia(ll)[1],
    histogram_entropia(lh, -255, 256)[1],
    histogram_entropia(hl, -255, 256)[1],
    histogram_entropia(hh, -255, 256)[1],
]
h_dwt = sum(h_pasma) / 4
r_png = przeplywnosc(ROOT / "monarch_mono.png", *obraz.shape)

print(f"Przeplywnosc PNG mono: {r_png:.6f} bit/piksel")
print(f"Entropia oryginalu: {h_mono:.6f} bit/piksel")
print(f"Entropia obrazu roznicowego: {h_roznice:.6f} bit/piksel")
print(f"Srednia entropia pasm DWT: {h_dwt:.6f} bit/wspolczynnik")
