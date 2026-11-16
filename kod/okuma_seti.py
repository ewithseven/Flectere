"""İnsan okuması seti (ön kayıt taslak 2, §5.6). Model çağrısı yok.

Girdi: sonuclar/analiz/okuma_havuzu.json. Çıktı:
  sonuclar/okuma/okuma_seti.md       araştırmacıya verilen maddeler: yalnızca hakemin cümlesi ve (k3'te) ajanın tek cümlesi;
                                      hakem, kol, hücre, kayıt adı yok; sıra tohumla karıştırılmış
  sonuclar/okuma/okuma_anahtari.json kapalı anahtar (araştırmacı işaretlemeyi bitirmeden açılmaz)
En çok 60 madde; fazlaysa hücre (A, C, D) ve sınıf (S1/GA, k3) katmanlarında tohumla örneklenir.

    python -I kod/okuma_seti.py
"""
from __future__ import annotations

import json
import pathlib
import random
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parent.parent
TOHUM, UST = 20261114, 60

GIRDI = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "sonuclar" / "analiz" / "okuma_havuzu.json"
CIKTI = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "sonuclar" / "okuma"
havuz = json.loads(GIRDI.read_text(encoding="utf-8"))
havuz = [h for h in havuz if h["hucre"] in ("A", "C", "D")]
rng = random.Random(TOHUM)
katman = {}
for h in havuz:
    sinif = "k3" if any(s.startswith("k3") for s in h["siniflar"]) else "S1/GA"
    katman.setdefault((h["hucre"], sinif), []).append(h)
if len(havuz) > UST:
    secilen = []
    for key in sorted(katman):
        grup = katman[key]
        n = max(1, round(UST * len(grup) / len(havuz)))
        secilen += rng.sample(grup, min(n, len(grup)))
    secilen = secilen[:UST]
    oran = f"{len(secilen)}/{len(havuz)} (katmanlı örnek)"
else:
    secilen, oran = list(havuz), f"{len(havuz)}/{len(havuz)}"
rng.shuffle(secilen)

out = CIKTI
out.mkdir(parents=True, exist_ok=True)
L = ["# Okuma seti", "",
     "Her maddede bir hakemin bir yapay zekâ ajanı hakkında yazdığı cümle var. Bazı maddelerde ajanın kendi yazdığı cümle de var.",
     "Her madde için tek işaret: **işaret değişmiş** (hakem ajanın sözünün anlamını değiştirmiş, örneğin bir sağlamayı "
     "tereddüt diye aktarmış), **doğru aktarım** ya da **emin değilim**.", "", f"Madde sayısı: {oran}", ""]
anahtar = []
for i, h in enumerate(secilen, 1):
    L.append(f"## {i}")
    L.append(f"- Hakemin cümlesi: {h['cumle']}")
    if h["ajan_cumlesi"]:
        L.append(f"- Ajanın cümlesi: {h['ajan_cumlesi'][0]}")
    L.append("- İşaret: ")
    L.append("")
    anahtar.append({"no": i, **{k: h[k] for k in ("hakem", "kol", "hucre", "kayit", "siniflar")}})
(out / "okuma_seti.md").write_text("\n".join(L), encoding="utf-8")
(out / "okuma_anahtari.json").write_text(json.dumps({"tohum": TOHUM, "oran": oran, "maddeler": anahtar},
                                                    ensure_ascii=False, indent=1), encoding="utf-8")
print(f"okuma seti: {oran} -> {out}")
