"""C hücresi: AgentDojo'nun görülmemiş bütün user_task koşuları (araştırmacı, 14 Kasım 07:48). Model çağrısı yok.
Döküm içeriği yazdırılmaz; yalnızca ad, utility ve uzunluk.

Kural:
  - adında `injection_task` geçen koşu hiç alınmaz (K2-3 ile aynı koruma);
  - user_task koşusu, Faz 17 seçiminde parti 2'deyse ya da seçimde yoksa ve adı hiçbir dosyada geçmiyorsa alınır
    (LANG'in data klasörü dışı, memento-mori, SWARMAI).
  Beklenen (VERI §2): 80 koşu, utility=True 58, utility=False 22.

Ayrıca dört hücrenin (A, B, C, D) uzunluklarını basar (maliyet tablosu için; karakter, bütün mesajlar).

    python -I kod/c_kume.py           # yalnızca sayım
    python -I kod/c_kume.py --yaz     # listeyi on_kayit/c_secim.json'a yazar
"""
from __future__ import annotations

import datetime
import json
import pathlib
import statistics
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
LANG = pathlib.Path(r"C:\Users\user\Desktop\LANG")
MM = pathlib.Path(r"C:\Users\user\Desktop\memento-mori")
SWARM = pathlib.Path(r"C:\Users\user\SWARMAI")
DOJO, ANTH, SAB, FRA = (LANG / "data" / d for d in ("agentdojo", "anthropic_mislabel", "anthropic_sabotage",
                                                     "anthropic_fraud"))
METIN = {".md", ".py", ".json", ".jsonl", ".txt", ".html", ".csv"}

dojo = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in DOJO.glob("*.json")}
secim = {s["name"]: s["batch"] for s in json.loads((MM / "results" / "faz17" / "secim.json").read_text(encoding="utf-8"))}
user = {n for n in dojo if "injection_task" not in n}
assert all("user_task" in n for n in user)

anilmis = set()
for base in (LANG, MM, SWARM):
    for f in base.rglob("*"):
        if not f.is_file() or f.suffix not in METIN or f.stem in dojo:
            continue
        if (LANG / "data") in f.parents:
            continue
        try:
            if f.stat().st_size > 50_000_000:
                continue
            t = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        anilmis |= {n for n in user if n in t}

C = sorted(n for n in user if secim.get(n) == 2 or (n not in secim and n not in anilmis))
ut = {n: bool(dojo[n].get("utility")) for n in C}
print(f"C: {len(C)} koşu | utility=True {sum(ut.values())} | utility=False {len(C) - sum(ut.values())} | "
      f"parti 2'den {sum(secim.get(n) == 2 for n in C)} | dokunulmamış {sum(n not in secim for n in C)}")
print(f"   seçimde olmayıp adı bir dosyada geçen user_task: {sorted(n for n in user if n not in secim and n in anilmis)}")


def boy(msgs):
    return sum(len(str(m.get("content") or "")) for m in msgs)


kol2 = json.loads((ROOT / "on_kayit" / "kol2_secim.json").read_text(encoding="utf-8"))
D = [r["kayit"] for r in kol2["D_birincil"]]


def d_msgs(stem):
    p = (SAB / f"{stem}.json") if (SAB / f"{stem}.json").exists() else (FRA / f"{stem}.json")
    return json.loads(p.read_text(encoding="utf-8"))["target_messages"]


hucre = {
    "A": [boy(json.loads(p.read_text(encoding="utf-8"))["target_messages"]) for p in sorted(ANTH.glob("*.json"))],
    "B": [boy(json.loads(p.read_text(encoding="utf-8"))["target_messages"]) for p in sorted(SAB.glob("opus48-*.json"))],
    "C": [boy(dojo[n]["messages"]) for n in C],
    "D": [boy(d_msgs(s)) for s in D],
}
print("\nUzunluk (karakter, bütün mesajlar; yaklaşık token = karakter / 4):")
for k, v in hucre.items():
    print(f"   {k}: {len(v):>3} kayıt | en az {min(v):>7,} | ortanca {int(statistics.median(v)):>7,} | "
          f"en çok {max(v):>7,} | toplam {sum(v):>9,}")

if "--yaz" in sys.argv:
    out = ROOT / "on_kayit" / "c_secim.json"
    out.write_text(json.dumps({
        "uretildi": datetime.datetime.now().isoformat(timespec="minutes"),
        "betik": "kod/c_kume.py",
        "kural": "user_task; Faz 17 parti 2 ya da seçimde yok ve adı hiçbir dosyada geçmiyor; injection_task hiç yok",
        "C": [{"kayit": n, "utility": ut[n], "parti2": secim.get(n) == 2} for n in C],
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nyazıldı: {out}")
