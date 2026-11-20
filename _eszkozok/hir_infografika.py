# -*- coding: utf-8 -*-
"""Infografikák beillesztése egy napi vagy heti MI-hírbe.

Használat:
    python _eszkozok/hir_infografika.py <hír.qmd> <adatok.json>

Az adatok.json szerkezete:
{
  "datum": "2026. november 20.",
  "nemzetkozi": {
    "tanulsag": "Egy mondat a szakasz fő tanulságáról.",
    "tetelek": [
      {"kategoria": "MI-gazdaság", "adat": "+17,1%",
       "adat_cimke": "első napi árfolyam-emelkedés",
       "cim": "Anthropic: történelmi tőzsdei bemutatkozás"}
    ]
  },
  "magyar": { ... ugyanígy ... }
}

A tételek sorrendje a szakasz számozott hírcímeinek sorrendje; a szkript
minden csempét a hozzá tartozó hírcímre linkeli (Pandoc-azonosító).
A beillesztés megismételhető: a korábbi infografikát lecseréli.
A fájl UTF-8 kódolású, CRLF sorvégű marad.
"""
import html
import json
import re
import sys
import unicodedata

SZAKASZOK = {
    "nemzetkozi": ("Nemzetközi MI-hírek", re.compile(r"nemzetk[öo]zi", re.I)),
    "magyar": ("Magyar MI-hírek", re.compile(r"magyar", re.I)),
}
FEJLEC = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
SZAMOZOTT = re.compile(r"^\d{1,2}\.\s")
BLOKK = re.compile(r"```\{=html\}\n<!-- emi-infografika:(\w+) -->\n.*?\n```\n\n?", re.S)


def pandoc_azonosito(szoveg):
    """A Pandoc auto_identifiers szabálya (nem GFM)."""
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", szoveg)
    s = re.sub(r"[*_`]{1,3}(\S(?:.*?\S)?)[*_`]{1,3}", r"\1", s)
    s = unicodedata.normalize("NFC", s)
    s = "".join(c for c in s if c.isalnum() or c in "_-. \t\n")
    s = "-".join(s.split()).lower()
    i = 0
    while i < len(s) and not s[i].isalpha():
        i += 1
    s = s[i:]
    return s or "section"


def fejlecek(sorok):
    """(sorindex, szint, szöveg, azonosító) – a kódblokkokon kívül."""
    eredmeny, latott, kod = [], {}, False
    for i, sor in enumerate(sorok):
        if sor.startswith("```"):
            kod = not kod
            continue
        if kod:
            continue
        m = FEJLEC.match(sor)
        if not m:
            continue
        szoveg = m.group(2)
        alap = pandoc_azonosito(szoveg)
        azon = alap
        if alap in latott:
            latott[alap] += 1
            azon = f"{alap}-{latott[alap]}"
        else:
            latott[alap] = 0
        eredmeny.append((i, len(m.group(1)), szoveg, azon))
    return eredmeny


def szakasz_keres(fej, minta):
    for k, (i, szint, szoveg, _) in enumerate(fej):
        if szint <= 2 and not SZAMOZOTT.match(szoveg) and minta.search(szoveg):
            tetelek = []
            for j, sz2, t2, az2 in fej[k + 1:]:
                if sz2 <= szint:
                    break
                if sz2 == szint + 1 and SZAMOZOTT.match(t2):
                    tetelek.append(az2)
            return i, tetelek
    return None, []


def e(s):
    return html.escape(str(s), quote=True)


def blokk(kulcs, nev, datum, adat, horgonyok):
    tetelek = adat["tetelek"]
    sor = [
        "```{=html}",
        f"<!-- emi-infografika:{kulcs} -->",
        f'<figure class="emi-infografika" aria-labelledby="emi-ig-{kulcs}">',
        '<figcaption class="emi-ig-fej">',
        f'<span class="emi-ig-felcim">Infografika · {e(datum)}</span>',
        f'<span class="emi-ig-cim" id="emi-ig-{kulcs}">{e(nev)} egy pillantásra</span>',
        f'<span class="emi-ig-alcim">{len(tetelek)} hír – a csempére kattintva a részletes hírhez ugorhat.</span>',
        "</figcaption>",
        '<ol class="emi-ig-racs">',
    ]
    for n, t in enumerate(tetelek, 1):
        href = f"#{horgonyok[n - 1]}" if n <= len(horgonyok) else None
        nyito = f'<a class="emi-ig-tetel" href="{e(href)}">' if href else '<div class="emi-ig-tetel">'
        zaro = "</a>" if href else "</div>"
        sor += [
            f"<li>{nyito}",
            f'<span class="emi-ig-teteltetej"><span class="emi-ig-szam" aria-hidden="true">{n}</span>'
            f'<span class="emi-ig-kat">{e(t["kategoria"])}</span></span>',
            f'<span class="emi-ig-adat">{e(t["adat"])}</span>',
            f'<span class="emi-ig-adat-cimke">{e(t["adat_cimke"])}</span>',
            f'<span class="emi-ig-tetel-cim">{e(t["cim"])}</span>',
            f"{zaro}</li>",
        ]
    sor.append("</ol>")
    if adat.get("tanulsag"):
        sor.append(f'<p class="emi-ig-tanulsag"><span class="emi-ig-tanulsag-cimke">Fő tanulság</span> {e(adat["tanulsag"])}</p>')
    sor += ["</figure>", "```", ""]
    return "\n".join(sor) + "\n"


def main(qmd, spec):
    nyers = open(qmd, encoding="utf-8").read()
    szoveg = BLOKK.sub("", nyers.replace("\r\n", "\n"))
    adatok = json.load(open(spec, encoding="utf-8"))
    hibak = []
    beszurasok = []
    sorok = szoveg.split("\n")
    fej = fejlecek(sorok)
    for kulcs, (nev, minta) in SZAKASZOK.items():
        if kulcs not in adatok:
            continue
        idx, horgonyok = szakasz_keres(fej, minta)
        if idx is None:
            hibak.append(f"Nincs „{nev}” szakasz a hírben.")
            continue
        tetelek = adatok[kulcs]["tetelek"]
        if len(tetelek) != len(horgonyok):
            hibak.append(f"{nev}: {len(tetelek)} csempe, de {len(horgonyok)} számozott hír.")
        for t in tetelek:
            for mezo, hossz in (("kategoria", 28), ("adat", 14), ("adat_cimke", 60), ("cim", 90)):
                if not str(t.get(mezo, "")).strip():
                    hibak.append(f"{nev}: hiányzó „{mezo}” mező.")
                elif len(t[mezo]) > hossz:
                    hibak.append(f"{nev}: túl hosszú „{mezo}” ({len(t[mezo])} > {hossz}): {t[mezo]}")
        beszurasok.append((idx, blokk(kulcs, nev, adatok["datum"], adatok[kulcs], horgonyok)))
    if hibak:
        print("\n".join(hibak))
        sys.exit(1)
    for idx, b in sorted(beszurasok, reverse=True):
        # a szakaszcím után egy üres sor, majd az infografika
        j = idx + 1
        while j < len(sorok) and not sorok[j].strip():
            j += 1
        sorok[j:j] = b.rstrip("\n").split("\n") + [""]
        sorok[idx + 1:j] = [""]
    kimenet = "\n".join(sorok).rstrip("\n") + "\n"
    open(qmd, "w", encoding="utf-8", newline="").write(kimenet.replace("\n", "\r\n"))
    print(f"Kész: {len(beszurasok)} infografika -> {qmd}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
