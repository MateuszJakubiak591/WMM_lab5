"""
Wspolne funkcje wykorzystywane w zadaniach laboratorium: obliczanie
entropii, przeplywnosci, DWT, MSE/PSNR oraz przygotowanie katalogu wynikow.
"""

from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parent
WYNIKI = ROOT / "wyniki"


def przygotuj_katalog(nazwa=None):
    katalog = WYNIKI if nazwa is None else WYNIKI / nazwa
    katalog.mkdir(parents=True, exist_ok=True)
    return katalog


def wczytaj_mono():
    obraz = cv2.imread(str(ROOT / "monarch_mono.png"), cv2.IMREAD_GRAYSCALE)
    if obraz is None:
        raise FileNotFoundError("Nie znaleziono monarch_mono.png")
    return obraz


def wczytaj_kolor():
    obraz = cv2.imread(str(ROOT / "monarch_col.png"), cv2.IMREAD_COLOR)
    if obraz is None:
        raise FileNotFoundError("Nie znaleziono monarch_col.png")
    return obraz


def histogram_entropia(obraz, minimum=0, maksimum=256):
    wartosci = obraz.astype(np.int64).ravel()
    histogram = np.bincount(
        wartosci - minimum, minlength=maksimum - minimum
    ).astype(np.float64)
    prawdopodobienstwa = histogram[histogram > 0] / histogram.sum()
    entropia = -np.sum(prawdopodobienstwa * np.log2(prawdopodobienstwa))
    os_x = np.arange(minimum, maksimum)
    return histogram, float(entropia), os_x


def przeplywnosc(sciezka, wysokosc, szerokosc):
    return 8 * Path(sciezka).stat().st_size / (wysokosc * szerokosc)


def obraz_roznicowy_poziomy(obraz):
    roznice = np.empty(obraz.shape, dtype=np.int16)
    roznice[:, 0] = obraz[:, 0].astype(np.int16) - 127
    roznice[:, 1:] = (
        obraz[:, 1:].astype(np.int16) - obraz[:, :-1].astype(np.int16)
    )
    return roznice


def dwt(obraz):
    mask_l = np.array(
        [
            0.02674875741080976,
            -0.01686411844287795,
            -0.07822326652898785,
            0.2668641184428723,
            0.6029490182363579,
            0.2668641184428723,
            -0.07822326652898785,
            -0.01686411844287795,
            0.02674875741080976,
        ]
    )
    mask_h = np.array(
        [
            0.09127176311424948,
            -0.05754352622849957,
            -0.5912717631142470,
            1.115087052456994,
            -0.5912717631142470,
            -0.05754352622849957,
            0.09127176311424948,
        ]
    )
    ll = cv2.sepFilter2D(obraz, -1, mask_l, mask_l)[::2, ::2]
    lh = cv2.sepFilter2D(obraz, cv2.CV_16S, mask_l, mask_h)[::2, ::2]
    hl = cv2.sepFilter2D(obraz, cv2.CV_16S, mask_h, mask_l)[::2, ::2]
    hh = cv2.sepFilter2D(obraz, cv2.CV_16S, mask_h, mask_h)[::2, ::2]
    return ll, lh, hl, hh


def normalizuj_do_zapisu(obraz):
    minimum = float(obraz.min())
    maksimum = float(obraz.max())
    if maksimum == minimum:
        return np.zeros(obraz.shape, dtype=np.uint8)
    wynik = (obraz.astype(np.float64) - minimum) * 255.0 / (maksimum - minimum)
    return np.round(wynik).astype(np.uint8)


def mse_psnr(obraz_1, obraz_2):
    roznica = obraz_1.astype(np.float64) - obraz_2.astype(np.float64)
    mse = float(np.mean(roznica**2))
    psnr = float("inf") if mse == 0 else float(10 * np.log10(255.0**2 / mse))
    return mse, psnr
