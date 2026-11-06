# Ember–MI Kapcsolatok Kutatócsoport – honlap

Munkajegyzet a honlap karbantartásához. A fájlt a `_quarto.yml` `project: render:` beállítása zárja ki a renderelésből (csak a `*.qmd` fájlok fordulnak, a `CLAUDE.md` kifejezetten ki van zárva), így nem kerül ki a weboldalra. Ezt a beállítást nem szabad eltávolítani.

## Alapelvek

- **A Claude sehol nem jelenhet meg szerkesztőként vagy szerzőként** (author mező, lábléc, commit üzenet a weboldalon, metaadat stb.). A szerzői mezők a kutatócsoport tagjainak nevét vagy a „Kutatócsoport” megjelölést tartalmazzák.
- Az oldal mindig fordítható legyen az R-es Quarto környezetben (RStudio projekt: `human-ai.Rproj`, `quarto render`).
- Arculat: modern, visszafogott, elegáns, könnyen használható kutatócsoportos oldal; a világos és a sötét mód is legyen támogatott és tesztelt.
- A tartalom nyelve magyar (`lang: hu`); a Quarto felületi szövegei a `_quarto.yml` `language:` blokkjában vannak magyarítva.
- A forrásfájlok UTF-8 kódolásúak, CRLF sorvégekkel (Windows); szerkesztéskor ezt meg kell őrizni.

## Felépítés

- `_quarto.yml` – projekt, oldalsáv-menü, lábléc (nyers HTML), témák (`cosmo` + `theme-dark.scss`), `styles.css`.
- `styles.css` – saját tipográfia, színpaletta, lábléc, eseménykártyák, hírtáblák; a sötét módot a `body.quarto-dark` szelektor kezeli.
- `theme-dark.scss` – a sötét téma Bootstrap/Quarto változói.
- Listázó oldalak (`lp_*.qmd`) és a hozzájuk tartozó mappák:
  - `lp_mi_hirek_napi/` – napi MI-hírek (`mi_hirek_ÉÉÉÉHHNN.qmd`), automatikusan generált tartalom.
  - `lp_mi_hirek_heti_pszicho/` – heti MI–pszichológia hírek, automatikusan generált tartalom.
  - `lp_rovid_ismertetok/` – tagok rövid ismertetői (BibTeX + `apa.csl`, kapcsolódó HTML diasor).
  - `lp_szakmai_esemenyek/` – események; saját mezők: `datum`, `idopont`, `helyszin`, `szervezo`; képek az `images/` mappában.
- `tudastar/` – képek az MI-eszköz oldalakhoz (pl. `mi_eszkozok_iras.qmd`).
- A menüben a `href` nélküli tételek (Tudásmegosztás, Szakmai élet, Munkacsoportok, Kutatás) szakaszcímként jelennek meg.

## Publikálás

- `main` ágra pusholás → GitHub Actions (`.github/workflows/render.yml`) rendereli a `_site/` mappát, majd webhookkal szól a `psycho.unideb.hu` szerveren futó `deploy.php`-nek (rsync `--delete`). Részletek: `README.md`.
- A `_site/`, a `.quarto/` és a `.Rproj.user/` nincs verziókezelve (2026-11-06-tól a Git sem követi őket; ne kerüljenek vissza commitba).

## Karbantartási szabályok

- Képeket webre optimalizált méretben tegyünk fel (fotó: JPG, kb. 1500 px szélesség, néhány száz kB).
- Ne használjunk `date: today` mezőt olyan oldalon, ahol a dátumnak tartalmi jelentése van.
- Hírek beillesztése: YAML fejléc (`title`, `author: "OpenAI - ChatGpt"`, `date`), a forrásszöveg saját főcíme elhagyva; fájlnév `mi_hirek_ÉÉÉÉHHNN.qmd`. A honlap saját oldalaira mutató linkek relatívak legyenek.
- Új menüpontnál a menüfelirat és az oldal `title` mezője legyen összhangban.

## Változásnapló

- 2026-11-05: `about.qmd` sablonoldal eltávolítása; Tempus-eseménykép PNG → JPG (2,3 MB → 0,24 MB); a Linkek oldal címe egységesítve a menüvel, a `date: today` eltávolítva; ez a jegyzet létrehozva, és kizárva a renderelésből.
- 2026-11-05: napi MI-hírek pótolva (2026-10-28 – 2026-11-05), heti MI–pszichológia hír (2026-11-02) hozzáadva; új esemény: Abari Kálmán „A mesterséges intelligencia ma” online workshopja (2026-10-28, `lp_szakmai_esemenyek/honlap_20261028.qmd`, kép a diasor címlapjáról).
- 2026-11-05: workshop-esemény kiegészítve (12:00–13:00, beágyazott diasor, `resources:` a diasor HTML-jére); új esemény: IPCRF 2026, Hongkong (`lp_szakmai_esemenyek/ipcrf_20260728.qmd`), kép nélkül.
- 2026-11-06: a `.gitignore` által kizárt `_site/`, `.quarto/` és `.Rproj.user/` kivéve a Git követéséből (`git rm -r --cached`).
