"""
Skrypt pomocniczy uruchamiajacy po kolei wszystkie siedem zadan
laboratorium i zapisujacy ich tekstowe wyniki w katalogu wyniki.
"""

import subprocess
import sys
from pathlib import Path


root = Path(__file__).resolve().parent
katalog = root / "wyniki"
katalog.mkdir(exist_ok=True)

for numer in range(1, 8):
    skrypt = next(root.glob(f"zadanie_{numer}_*.py"))
    wynik = subprocess.run(
        [sys.executable, str(skrypt)],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    (katalog / f"zadanie_{numer}_wyniki.txt").write_text(wynik.stdout, encoding="utf-8")
    print(f"Wykonano {skrypt.name}")
