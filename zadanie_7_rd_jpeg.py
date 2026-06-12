"""
Zadanie 7: skrypt kompresuje obraz kolorowy JPEG dla wielu poziomow quality,
oblicza bitrate, MSE i PSNR, zapisuje obrazy oraz gladkie krzywe R-D.
"""

import csv

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from wspolne import ROOT, mse_psnr, przygotuj_katalog, przeplywnosc, wczytaj_kolor


obraz = wczytaj_kolor()
katalog = przygotuj_katalog("zadanie_7")
katalog_jpeg = przygotuj_katalog("zadanie_7/jpeg")
jakosci = list(range(5, 101, 5))
wyniki = []

for jakosc in jakosci:
    sciezka = katalog_jpeg / f"monarch_q{jakosc:03d}.jpg"
    cv2.imwrite(str(sciezka), obraz, [cv2.IMWRITE_JPEG_QUALITY, jakosc])
    zrekonstruowany = cv2.imread(str(sciezka), cv2.IMREAD_COLOR)
    mse, psnr = mse_psnr(obraz, zrekonstruowany)
    bitrate = przeplywnosc(sciezka, obraz.shape[0], obraz.shape[1])
    wyniki.append((jakosc, bitrate, mse, psnr))

with (katalog / "wyniki_rd.csv").open("w", newline="", encoding="utf-8") as plik:
    zapis = csv.writer(plik)
    zapis.writerow(("quality", "bitrate_bit_na_piksel", "MSE", "PSNR_dB"))
    zapis.writerows(wyniki)

posortowane = sorted(wyniki, key=lambda x: x[1])
bitrate = [x[1] for x in posortowane]
mse = [x[2] for x in posortowane]
psnr = [x[3] for x in posortowane]

for wartosci, etykieta, nazwa in (
    (mse, "MSE", "krzywa_rd_mse.png"),
    (psnr, "PSNR [dB]", "krzywa_rd_psnr.png"),
):
    plt.figure(figsize=(9, 5))
    plt.plot(bitrate, wartosci, "-o", markersize=3)
    plt.title(f"Krzywa R-D: {etykieta}(R)")
    plt.xlabel("R [bit/piksel]")
    plt.ylabel(etykieta)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(katalog / nazwa, dpi=160)
    plt.close()

r_png_kolor = przeplywnosc(ROOT / "monarch_col.png", obraz.shape[0], obraz.shape[1])
print("quality | bitrate [bit/piksel] | MSE | PSNR [dB]")
for jakosc, r, mse_, psnr_ in wyniki:
    print(f"{jakosc:3d} | {r:9.6f} | {mse_:9.4f} | {psnr_:9.4f}")
print(f"Przeplywnosc kolorowego PNG: {r_png_kolor:.6f} bit/piksel")
