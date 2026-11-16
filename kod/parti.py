"""Birinci basamağın gönderim sırası ve partileri (işletim; ön kayda dokunmaz). Model ÇAĞIRMAZ.

Neden: Kota 5 saatlik pencerelerle dönüyor; birinci basamak tek pencereye sığmayabilir. İşler partiler halinde gönderilir.
Hiçbir istem, dosya, liste ya da analiz kuralı değişmez: istemler `isler.jsonl`'deki `istem` alanından aynen kopyalanır,
çağrı geçerliliğini `hakem_kosu.oku` denetler (istem karakter karakter, girdi dosyaları bayt bayt).

Sıra: ön kayıttaki kesme sırasının (§8) tersi. Kota biterse geride kalan, ön kaydın zaten keseceği şeydir:
  faz 1  hiç kesilmeyenler (MM denetleyicisi hariç): A {S,T,K,Co,C+,MMc}, B {S,K,Co,C+,MMc}, C {S,Co,MMc}, D sıkı 11 MMc
  faz 2  bu kayıtların MM denetleyicileri (madde dosyası `maddeler` ile yazıldıktan sonra)
  faz 3  D'nin sıkı 11 dışındaki kayıtları, MMc   (son çare kesimi)
  faz 4  aynı kayıtların MM denetleyicileri
  faz 5  T'nin B'si                               (kesme 3)
  faz 6  C+satır'ın C'si                          (kesme 2)
  faz 7  K'nın C'si                               (kesme 1)
Her fazın içi sabit tohumla (20261114) karıştırılır: ilk partiler maliyeti temsil eder ve zaman kol ile örtüşmez.

Yeniden gönderme (işletim kuralı): yalnızca cevabı olmayan iş yeniden gönderilir.
  - hiç gönderilmemiş ya da günlüğü olmayan iş;
  - gönderilmiş ama yanıt metni boş (kota ya da altyapı kesmesi) olan iş;
  - sınıflandırıcı durdurması: ön kayıt §8b'deki gibi bir kez.
  Cevabı olan bir iş asla yeniden gönderilmez.

Komutlar:
    python -I kod/parti.py sira                 # sonuclar/isler/b1_sonnet_sira.jsonl
    python -I kod/parti.py parti <no> <adet>    # önce hakem_kosu.oku; sonra sıradaki <adet> gönderilecek iş -> parti dosyası
    python -I kod/parti.py durum                # fazlara göre: bitti / gönderilecek / bekliyor / gönderilmez (yalnızca sayı)
"""
from __future__ import annotations

import collections
import datetime
import json
import pathlib
import random
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hakem_kosu as hk  # noqa: E402

KATMAN, HAKEM, TOHUM = "b1", "sonnet", 20261114
SIRA = hk.SONUC / "isler" / f"{KATMAN}_{HAKEM}_sira.jsonl"
PARTI_KAYIT = hk.SONUC / "isler" / f"{KATMAN}_{HAKEM}_partiler.jsonl"
FAZ_ADI = {1: "kesilmeyenler (MM hariç)", 2: "MM denetleyicileri", 3: "D sıkı dışı MMc", 4: "D sıkı dışı MM",
           5: "T/B", 6: "C+/C", 7: "K/C"}


def faz(i: dict) -> int:
    h, k = i["hucre"], i["kol"]
    if h == "D":
        return (1 if k == "MMc" else 2) if i["d_siki"] else (3 if k == "MMc" else 4)
    if (h, k) == ("B", "T"):
        return 5
    if (h, k) == ("C", "C+"):
        return 6
    if (h, k) == ("C", "K"):
        return 7
    return 2 if k == "MM" else 1


def liste() -> list[dict]:
    return [json.loads(l) for l in hk.is_listesi(KATMAN, HAKEM).read_text(encoding="utf-8").splitlines()]


def sira() -> None:
    gruplar = collections.defaultdict(list)
    for i in liste():
        gruplar[faz(i)].append(i)
    rnd = random.Random(TOHUM)
    out = []
    for f in sorted(gruplar):
        g = gruplar[f]
        rnd.shuffle(g)
        out += [{"is": i["is"], "faz": f, "hucre": i["hucre"], "kol": i["kol"], "kayit": i["kayit"]} for i in g]
    SIRA.write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in out), encoding="utf-8")
    print(f"{SIRA}: {len(out)} iş | " + ", ".join(f"faz {f} ({FAZ_ADI[f]}): {len(gruplar[f])}" for f in sorted(gruplar)))


def _kayit() -> dict[str, dict]:
    p = hk.SONUC / f"{KATMAN}_{HAKEM}" / "kayit.jsonl"
    if not p.exists():
        return {}
    return {r["is"]: r for r in map(json.loads, p.read_text(encoding="utf-8").splitlines())}


def _yanitli(r: dict | None) -> bool:
    """Cevabı olan iş: yeniden gönderilmez. Sınıflandırıcı durdurması bir kez yeniden denendiyse de bitmiştir."""
    if not r or r["gonderilmedi"] or not r["metin"]:
        return False
    return not r["siniflandirici"] or r["deneme"] >= 2


def durumlar() -> list[tuple[dict, str]]:
    ler = {i["is"]: i for i in liste()}
    kay = _kayit()
    mmc = {i["rid"]: kay.get(i["is"]) for i in ler.values() if i["kol"] == "MMc"}
    out = []
    for s in map(json.loads, SIRA.read_text(encoding="utf-8").splitlines()):
        i, r = ler[s["is"]], kay.get(s["is"])
        if _yanitli(r):
            d = "bitti"
        elif i["kol"] != "MM" or (pathlib.Path(i["klasor"]) / hk.DOSYA["madde"]).exists():
            d = "gönder"
        else:
            c = mmc.get(i["rid"])
            if not _yanitli(c):
                d = "çıkarıcı bekliyor"
            elif c["siniflandirici"] or c["gecersiz"]:
                d = "gönderilmez"  # ön kayıt §8b: çıkarıcı durduysa ya da geçersizse denetleyici gönderilmez
            else:
                d = "maddeler bekliyor"
        out.append(({**s, **i}, d))
    return out


def durum() -> None:
    say = collections.defaultdict(collections.Counter)
    for s, d in durumlar():
        say[s["faz"]][d] += 1
    for f in sorted(say):
        print(f"faz {f} ({FAZ_ADI[f]}): {dict(say[f])}")


def parti(no: int, adet: int, yalniz_faz: int | None = None) -> None:
    """yalniz_faz: yalnızca o fazın gönderilebilir işleri (15 Kasım 22:05; araştırmacı kararı: D'nin kalanından yalnızca
    çıkarıcısı biten kayıtların MM'si). Verilmezse davranış öncekiyle aynı."""
    hk.oku(KATMAN, HAKEM)
    secilen, engel = [], None
    for s, d in durumlar():
        if len(secilen) >= adet:
            break
        if yalniz_faz is not None:
            if s["faz"] == yalniz_faz and d == "gönder":
                secilen.append(s)
            continue
        if d == "gönder":
            secilen.append(s)
        elif d in ("maddeler bekliyor", "çıkarıcı bekliyor") and engel is None:
            engel = (s["faz"], d)
            break  # sıra korunur: bir faz bekliyorsa sonraki fazlara geçilmez
    if not secilen:
        print(f"gönderilecek iş yok | engel: {engel}")
        return
    hedef = hk.grup_dizini(KATMAN, HAKEM) / f"parti_{no:02d}.jsonl"
    if hedef.exists():
        raise SystemExit(f"{hedef} zaten var; yeni numara ver")
    hedef.write_text("\n".join(json.dumps({"is": s["is"], "model": s["model"], "istem": s["istem"]}, ensure_ascii=False)
                               for s in secilen), encoding="utf-8")
    with PARTI_KAYIT.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"parti": no, "zaman": datetime.datetime.now().isoformat(timespec="seconds"),
                            "isler": [s["is"] for s in secilen]}, ensure_ascii=False) + "\n")
    sayi = collections.Counter((s["faz"], s["hucre"], s["kol"]) for s in secilen)
    print(f"{hedef}: {len(secilen)} iş | {dict(sayi)} | engel: {engel}")


if __name__ == "__main__":
    k = sys.argv[1]
    {"sira": sira, "durum": durum, "parti": lambda: parti(int(sys.argv[2]), int(sys.argv[3]),
                                                           int(sys.argv[4]) if len(sys.argv) > 4 else None)}[k]()
