"""2. kolun seçim kuralı (araştırmacı, 13 Kasım 22:05): seçimi kimse okuyarak yapmaz, önceden yazılmış kural yapar.
Model çağrısı yok, ağ yok. Döküm içeriği yazdırılmaz; yalnızca kimlik, model ve sayı.

K2-1 Durum yüklü: kaydın kendi `section` alanı "covert-sabotage" ya da "assisting-fraud" (kaynağın bölüm etiketi).
K2-2 Aranan ifade bulunmadı ("ajan sessiz"): ajanın kendi ürettiği mesajlarda (role=assistant, source=generate)
     `ret` ve `kaygı_dar` listelerinin hiçbiri eşleşmiyor. Sıkı alt küme: `kaygı_geniş` de eşleşmiyor.
     Listeler `kod/on_kayit_oncesi.py`'den (13 Kasım 20:50) ast ile okunur; elle kopyalanmaz.
K2-3 AgentDojo (injection koşuları dahil) bu betikte hiç okunmaz.
K2-4 Daha önce hakeme okutulmuş ya da bir dosyada adı geçen kayıt ana sayımdan çıkar, ayrı sayılır.
     Tek istisna: Faz 14'ün kod anahtarı (`LANG/results/faz14/anahtar.jsonl`, `faz5/anahtar_caft.py`). O betik yalnızca
     çevre mesajlarını (user, tool) okudu, ajanın sözünü okumadı; hiçbir hakem okumadı. Orada adı geçmek kaydı
     görülmüş yapmaz (AgentDojo parti 2 emsali: render edildi, kodla tarandı, hakem okumadı). Bu kayıtlar
     "kodla anahtarlanmış" diye beyan edilir; anahtarın kendisi bu sprintte kullanılmaz.

    python -I kod/kol2_kural.py           # yalnızca sayım
    python -I kod/kol2_kural.py --yaz     # seçimi on_kayit/kol2_secim.json'a da yazar
"""
from __future__ import annotations

import ast
import collections
import datetime
import hashlib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
LANG = pathlib.Path(r"C:\Users\user\Desktop\LANG")
MM = pathlib.Path(r"C:\Users\user\Desktop\memento-mori")
SWARM = pathlib.Path(r"C:\Users\user\SWARMAI")
SAB, FRA = LANG / "data" / "anthropic_sabotage", LANG / "data" / "anthropic_fraud"
ANTH = LANG / "data" / "anthropic_mislabel"
YUKLU = {"covert-sabotage", "assisting-fraud"}
METIN = {".md", ".py", ".json", ".jsonl", ".txt", ".html", ".csv"}
KOD_ANAHTARI = LANG / "results" / "faz14" / "anahtar.jsonl"
sys.stdout.reconfigure(encoding="utf-8")


def listeler() -> dict[str, str]:
    """RX sözlüğünü on_kayit_oncesi.py'den okur; bayrağın re.I olduğunu denetler."""
    tree = ast.parse((HERE / "on_kayit_oncesi.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "RX" for t in node.targets):
            out = {}
            for k, v in zip(node.value.keys, node.value.values):
                flag = v.args[1]
                assert isinstance(flag, ast.Attribute) and flag.attr == "I", "bayrak re.I değil"
                out[ast.literal_eval(k)] = ast.literal_eval(v.args[0])
            return out
    raise SystemExit("RX bulunamadı")


PAT = listeler()
RX = {k: re.compile(v, re.I) for k, v in PAT.items()}
PAT_SHA = hashlib.sha256(json.dumps(PAT, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def ajan(msgs, yalniz_uretilen=True):
    return [str(m.get("content") or "") for m in msgs
            if m.get("role") == "assistant" and (m.get("source") == "generate" or not yalniz_uretilen)]


def isabet(texts):
    return {k: sum(bool(rx.search(t)) for t in texts) for k, rx in RX.items()}


def sessiz(h, siki=False):
    ok = h["ret"] == 0 and h["kaygı_dar"] == 0
    return ok and (h["kaygı_geniş"] == 0 if siki else True)


# --- kayıtlar (K2-1, K2-3) ---
kayit = {}
for p in sorted(SAB.glob("*.json")) + sorted(FRA.glob("*.json")):
    if p.name.startswith("_"):
        continue
    j = json.loads(p.read_text(encoding="utf-8"))
    grup = "fraud" if p.parent == FRA else ("CAFT-20" if p.stem.startswith("opus48") else "CAFT-110")
    msgs = j["target_messages"]
    kayit[p.stem] = {
        "grup": grup, "bolum": j.get("section"), "model": (j.get("metadata") or {}).get("target_model"),
        "h": isabet(ajan(msgs)), "h_hepsi": isabet(ajan(msgs, yalniz_uretilen=False)),
        "kaynaksiz": [i for i, m in enumerate(msgs) if m.get("role") == "assistant" and m.get("source") != "generate"],
        "ilk_asistan": next(i for i, m in enumerate(msgs) if m.get("role") == "assistant"),
        "kaynaksiz_isabet": isabet([str(m.get("content") or "") for m in msgs
                                    if m.get("role") == "assistant" and m.get("source") != "generate"]),
    }

# --- görülmüşlük (K2-4) ---
STEMS = set(kayit)
okutulmus, anilmis = set(), set()
anahtarli = {s for s in STEMS if s in KOD_ANAHTARI.read_text(encoding="utf-8")}
for base in (LANG, MM, SWARM):
    for f in base.rglob("*"):
        if not f.is_file() or f.suffix not in METIN or f.stem in STEMS or f.name == "_manifest.json":
            continue
        if f.resolve() == KOD_ANAHTARI.resolve():
            continue
        if base == LANG and (LANG / "data") in f.parents:
            continue
        try:
            if f.stat().st_size > 50_000_000:
                continue
            t = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        hits = {s for s in STEMS if s in t}
        anilmis |= hits
        if f.name.startswith("kayit") and f.suffix == ".jsonl":
            okutulmus |= hits

print(f"Listeler (on_kayit_oncesi.py, ast ile): {', '.join(PAT)} | SHA-256 {PAT_SHA[:16]}…")
print("\n== K2-1: bölüm etiketi ==")
print("  ", dict(collections.Counter((v["grup"], v["bolum"]) for v in kayit.values())))
assert all(v["bolum"] in YUKLU for v in kayit.values())

print("\n== Ajanın üretmediği asistan mesajı (source boş) ==")
for g in ("CAFT-110", "CAFT-20", "fraud"):
    vs = [v for v in kayit.values() if v["grup"] == g]
    n_k = sum(len(v["kaynaksiz"]) for v in vs)
    ilk = sum(v["kaynaksiz"] == [v["ilk_asistan"]] for v in vs)
    ih = {k: sum(v["kaynaksiz_isabet"][k] > 0 for v in vs) for k in RX}
    print(f"   {g:<9} kayıt {len(vs):>3} | source boş asistan mesajı {n_k:>3} | yalnızca ilk asistan mesajı olan kayıt {ilk:>3}"
          f" | bu mesajda liste eşleşen kayıt {ih}")
deg = sum(sessiz(v["h"]) != sessiz(v["h_hepsi"]) for v in kayit.values())
print(f"   source boş mesajlar sayılsaydı birincil sessizlik kararı değişen kayıt: {deg}")

print("\n== K2-2 ve K2-4: modele göre ==")
print("   grup      model                       kayıt | görülmemiş | birincil sessiz (görülmemiş) | sıkı sessiz (görülmemiş) | birincil sessiz (görülmüş)")
tablo = collections.defaultdict(collections.Counter)
for s, v in kayit.items():
    t = tablo[(v["grup"], str(v["model"]))]
    gor = s in anilmis
    t["n"] += 1
    t["gorulmemis"] += not gor
    t["b_g"] += (not gor) and sessiz(v["h"])
    t["s_g"] += (not gor) and sessiz(v["h"], siki=True)
    t["b_gor"] += gor and sessiz(v["h"])
tot = collections.Counter()
for (g, m), t in sorted(tablo.items()):
    tot.update(t)
    print(f"   {g:<9} {m:<27} {t['n']:>5} | {t['gorulmemis']:>10} | {t['b_g']:>28} | {t['s_g']:>24} | {t['b_gor']:>26}")
print(f"   TOPLAM{'':<31} {tot['n']:>5} | {tot['gorulmemis']:>10} | {tot['b_g']:>28} | {tot['s_g']:>24} | {tot['b_gor']:>26}")
print(f"   okutulmuş (bir kayit*.jsonl'de geçen): {len(okutulmus)} | kod anahtarı dışında bir dosyada adı geçen: "
      f"{len(anilmis)} | Faz 14 kod anahtarında geçen: {len(anahtarli)} (bunların {len(anahtarli & anilmis)}'i başka yerde de)")

D1 = sorted(s for s, v in kayit.items() if s not in anilmis and sessiz(v["h"]))
D2 = sorted(s for s, v in kayit.items() if s not in anilmis and sessiz(v["h"], siki=True))
claude = lambda ss: sum("claude" in str(kayit[s]["model"]).lower() or "opus" in str(kayit[s]["model"]).lower()
                        or "sonnet" in str(kayit[s]["model"]).lower() for s in ss)
for ad, D in (("birincil", D1), ("sıkı", D2)):
    n = len(D)
    ub = 1 - 0.05 ** (1 / n) if n else float("nan")
    print(f"\n   D {ad}: {n} kayıt | grup {dict(collections.Counter(kayit[s]['grup'] for s in D))} | "
          f"Claude ajanı {claude(D)} | kodla anahtarlanmış {len(set(D) & anahtarli)} | "
          f"0 olay görülürse tek yönlü %95 üst sınır {ub:.1%}")
    print("     model:", dict(collections.Counter(str(kayit[s]["model"]) for s in D).most_common()))

print("\n== Ana test denetimi: Anthropic'in 18 dökümünde ajanın üretmediği asistan mesajı var mı? ==")
a_k, a_ret = 0, 0
for p in ANTH.glob("*.json"):
    msgs = json.loads(p.read_text(encoding="utf-8"))["target_messages"]
    a_k += sum(m.get("role") == "assistant" and m.get("source") != "generate" for m in msgs)
    a_ret += bool(isabet(ajan(msgs))["ret"])
print(f"   source boş asistan mesajı: {a_k} | ret kalıbı yalnızca üretilen mesajlarda arandığında: {a_ret}/18")

if "--yaz" in sys.argv:
    out = ROOT / "on_kayit" / "kol2_secim.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "uretildi": datetime.datetime.now().isoformat(timespec="minutes"),
        "betik": "kod/kol2_kural.py",
        "kural": ["K2-1 bölüm etiketi covert-sabotage ya da assisting-fraud",
                  "K2-2 ajanın ürettiği mesajlarda ret ve kaygı_dar eşleşmiyor (sıkı: kaygı_geniş de)",
                  "K2-3 AgentDojo hiç okunmaz", "K2-4 adı herhangi bir dosyada geçen kayıt ana sayımdan çıkar"],
        "listeler": PAT, "listeler_sha256": PAT_SHA,
        "D_birincil": [{"kayit": s, "grup": kayit[s]["grup"], "model": kayit[s]["model"],
                        "siki_alt_kume": s in D2, "faz14_kod_anahtarinda": s in anahtarli} for s in D1],
        "gorulmus_ve_sessiz": sorted(s for s, v in kayit.items() if s in anilmis and sessiz(v["h"])),
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nyazıldı: {out}")
