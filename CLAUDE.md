# Ember–MI Kapcsolatok Kutatócsoport – honlap

Munkajegyzet a honlap karbantartásához. A fájlt a `_quarto.yml` `project: render:` beállítása zárja ki a renderelésből (csak a `*.qmd` fájlok fordulnak, a `CLAUDE.md` kifejezetten ki van zárva), így nem kerül ki a weboldalra. Ezt a beállítást nem szabad eltávolítani.

## Alapelvek

- **A Claude sehol nem jelenhet meg szerkesztőként vagy szerzőként** (author mező, lábléc, commit üzenet a weboldalon, metaadat stb.). A szerzői mezők a kutatócsoport tagjainak nevét vagy a „Kutatócsoport” megjelölést tartalmazzák.
- Az oldal mindig fordítható legyen az R-es Quarto környezetben (RStudio projekt: `human-ai.Rproj`, `quarto render`).
- Arculat: modern, elegáns, könnyen használható kutatócsoportos oldal – „A” irány (akadémiai, intézményi): intézményi sötétkék (#1E3A5F) + arany kiemelés (#A16207, sötét módban #E9C78B), Crimson Pro címek, Atkinson Hyperlegible szövegtörzs (Google Fonts). A világos és a sötét mód is legyen támogatott és tesztelt (a Quarto saját színmód-váltójával).
- Quarto-kompatibilitás: csak a Quarto saját eszközei (SCSS-téma, `styles.css`, listák, EJS-listasablonok, `_quarto.yml`); nincs npm/build-lépés; JavaScript legfeljebb kis kiegészítés.
- A tartalom nyelve magyar (`lang: hu`); a Quarto felületi szövegei a `_quarto.yml` `language:` blokkjában vannak magyarítva.
- A forrásfájlok UTF-8 kódolásúak, CRLF sorvégekkel (Windows); szerkesztéskor ezt meg kell őrizni.

## Felépítés

- `_quarto.yml` – projekt, felső navigációs sáv (`website: navbar:`, logóval, kereséssel, lenyíló „Tudásmegosztás” menüvel), lábléc (nyers HTML), témák (`cosmo` + `theme-light.scss` / `theme-dark.scss`), `styles.css`.
- `styles.css` – saját tipográfia, színpaletta (`--emi-*` változók, világos `:root` / sötét `body.quarto-dark`), navigációs sáv, sötétkék lábléc, eseménykártyák, hírtáblák, valamint a kezdőlap elemei (`.emi-hero`, `.emi-teruletek`, `.emi-ketoszlop`, `.emi-sav`, `.emi-szemely`).
- `index.qmd` – kezdőlap cím-blokk nélkül (`pagetitle`, `page-layout: full`): sötétkék bemutató sáv a legutóbbi eseménnyel, kutatási területek kártyái, legfrissebb hírek és események (Quarto-listák), vezetők. A hírek és események maguktól frissülnek.
- `_templates/` – a kezdőlap listáinak EJS-sablonjai (`hero-esemeny.ejs`, `friss-hirek.ejs`, `friss-esemenyek.ejs`); az aláhúzással kezdődő mappát a Quarto nem rendereli. A sablonok sorai ne legyenek behúzva (különben a Markdown kódblokknak veszi őket).
- `ember-mi-logo.svg` – logó (kék vonalak, arany pont; mindkét színmódban látható).
- `theme-light.scss` / `theme-dark.scss` – a világos és a sötét téma Bootstrap/Quarto változói (a navigációs sáv színei is: ebből kapják színüket a keresés, a színmód-váltó és a mobilmenü ikonjai).
- Listázó oldalak (`lp_*.qmd`) és a hozzájuk tartozó mappák:
  - `lp_mi_hirek_napi/` – napi MI-hírek (`mi_hirek_ÉÉÉÉHHNN.qmd`), automatikusan generált tartalom.
  - `lp_mi_hirek_heti_pszicho/` – heti MI–pszichológia hírek, automatikusan generált tartalom.
  - `lp_rovid_ismertetok/` – tagok rövid ismertetői (BibTeX + `apa.csl`, kapcsolódó HTML diasor).
  - `lp_szakmai_esemenyek/` – események; saját mezők: `datum`, `idopont`, `helyszin`, `szervezo`; képek az `images/` mappában.
- `tudastar/` – képek az MI-eszköz oldalakhoz (pl. `mi_eszkozok_iras.qmd`), webre méretezett WebP formátumban (max. 800 px széles); minden kép képleírása a kártya szövegét adja vissza.
- Nincs bal oldali menü (sidebar). A lenyíló menüben a `href` nélküli tétel csoportcímként, a `text: "---"` elválasztóként jelenik meg.

## Publikálás

- `main` ágra pusholás → GitHub Actions (`.github/workflows/render.yml`) rendereli a `_site/` mappát, majd webhookkal szól a `psycho.unideb.hu` szerveren futó `deploy.php`-nek (rsync `--delete`). Részletek: `README.md`.
- A `_site/`, a `.quarto/` és a `.Rproj.user/` nincs verziókezelve (2026-11-06-tól a Git sem követi őket; ne kerüljenek vissza commitba).

## Karbantartási szabályok

- Képeket webre optimalizált méretben tegyünk fel (fotó: JPG, kb. 1500 px szélesség, néhány száz kB).
- Ne használjunk `date: today` mezőt olyan oldalon, ahol a dátumnak tartalmi jelentése van.
- Hírek beillesztése: YAML fejléc (`title`, `author: "OpenAI - ChatGpt"`, `date`), a forrásszöveg saját főcíme elhagyva; fájlnév `mi_hirek_ÉÉÉÉHHNN.qmd`. A honlap saját oldalaira mutató linkek relatívak legyenek.
- Új menüpontnál a menüfelirat és az oldal `title` mezője legyen összhangban.
- Akadálymentesség: minden képnek legyen képleírása (Markdown `![leírás](…)`, ábránál `fig-alt`, eseménynél a fejlécben `image-alt` a lista bélyegképéhez); oldalanként egy H1 (a lapcím) – a hírek, az események, a Kutatócsoportról és az MI eszközök oldalon a `#` fejezetcímek a `shift-heading-level-by: 1` beállítással (mappánként `_metadata.yml`) egy szinttel lejjebb kerülnek; kattintható elemek legalább 24×24 px.

## Változásnapló

- 2026-11-05: `about.qmd` sablonoldal eltávolítása; Tempus-eseménykép PNG → JPG (2,3 MB → 0,24 MB); a Linkek oldal címe egységesítve a menüvel, a `date: today` eltávolítva; ez a jegyzet létrehozva, és kizárva a renderelésből.
- 2026-11-05: napi MI-hírek pótolva (2026-10-28 – 2026-11-05), heti MI–pszichológia hír (2026-11-02) hozzáadva; új esemény: Abari Kálmán „A mesterséges intelligencia ma” online workshopja (2026-10-28, `lp_szakmai_esemenyek/honlap_20261028.qmd`, kép a diasor címlapjáról).
- 2026-11-05: workshop-esemény kiegészítve (12:00–13:00, beágyazott diasor, `resources:` a diasor HTML-jére); új esemény: IPCRF 2026, Hongkong (`lp_szakmai_esemenyek/ipcrf_20260728.qmd`), kép nélkül.
- 2026-11-06: a `.gitignore` által kizárt `_site/`, `.quarto/` és `.Rproj.user/` kivéve a Git követéséből (`git rm -r --cached`).
- 2026-11-06: a bal oldali menü helyett felső navigációs sáv (logó, Kezdőlap, Kutatócsoportról, Tudásmegosztás lenyíló menü, Események, keresés, színmód-váltó); új `theme-light.scss`; az oldalsáv stílusai törölve. Az üres „Munkacsoportok” és „Kutatás” menüpontok kikerültek.
- 2026-11-06: új arculat („A” irány, UI UX Pro Max „Research Lab” ajánlás alapján): sötétkék–arany paletta világos és sötét módra, Crimson Pro + Atkinson Hyperlegible betűk, fehér navigációs sáv arany aláhúzással, sötétkék lábléc; új kezdőlap bemutató sávval, kutatási területekkel, automatikus hír- és eseménylistával (`_templates/*.ejs`) és a vezetők kártyáival; logó színe frissítve.
- 2026-11-06: Impeccable-szerű átvizsgálás (12/20) után javítva: 20 MI-eszköz-kártya és az eseményképek képleírása; az MI-eszköz képek PNG → WebP (11,5 MB → 0,5 MB); hivatkozásjegyzék URL-tördelése mobilon; egyetlen H1 oldalanként (`shift-heading-level-by`); a kezdőlap „Hírek” / „Események” felirata valódi címsor; nagyobb színmód-váltó és rendezőfejlécek; a workshop-eseményről a duplikált borítókép kikerült.
- 2026-11-06: tervezési csiszolás: a címek egyszínűek (gradiens szöveg nélkül); oldalsó színes csíkok helyett felső arany vonal (eseménykártya) vagy vékony keret (kapcsolat, idézet); a dekoratív árnyékok és a navigációs sáv elmosása kikerült; a kutatási területek kártyái számozás nélkül; a betűk `@import` helyett `include-in-header` linkkel, `preconnect`-tel töltődnek; görgetősáv és kurzor a palettához igazítva, táblázatban táblázatos számjegyek. A kezdőlap felülcímkéje („Debreceni Egyetem · Pszichológiai Intézet”) tudatosan marad.
