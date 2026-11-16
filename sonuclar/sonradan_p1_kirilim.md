# P1'in utility etiketine göre kırılımı (SONRADAN; ön kayıtta yok; betimleyici)

16 Kasım 00:25, `analiz.dogru` ve `analiz.kodla` ile, `sonuclar/b1_sonnet/kayit.jsonl` üzerinde. C hücresi, Sonnet 5.5, S ve MM; aynı 80 kayıt.

| utility (AgentDojo) | S doğru, MM doğru | S yanlış, MM doğru | S doğru, MM yanlış | ikisi yanlış | S doğru | MM doğru |
|---|---|---|---|---|---|---|
| True (58) | 40 | 10 | 1 | 7 | 41/58 | 50/58 |
| False (22) | 14 | 2 | 0 | 6 | 14/22 | 16/22 |

Okuma: farkın çoğu utility=True kayıtlarda. S görevi başaran 58 kaydın 17'sinde "uymadı" ya da teslim etmedi; MM'de bu 8. utility=False'ta MM S'den geri değil (16 / 14).
