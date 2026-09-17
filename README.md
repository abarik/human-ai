# Ember--MI Kapcsolatok Kutatócsoport

Ez a projekt az Ember–MI Kapcsolatok Kutatócsoport honlapját tartalmazza.


# Működés

A honlap Quarto segítségével van generálva, és a tartalom Markdown (`.qmd`) fájlokban található. A `render` workflow automatikusan generálja a statikus HTML fájlokat a `main` ágra történő push esetén. 

A teljes frissítési folyamat (CI/CD pipeline) két fő részből áll: a GitHubon futó generálásból és a szerveren futó szinkronizálásból.

## 1. Weboldal generálása (GitHub Actions)

Amikor új tartalom kerül a `main` ágra, a `.github/workflows/render.yml` fájlban definiált folyamat az alábbi lépéseket hajtja végre:
1. **Környezet felállítása:** Telepíti a Quarto-t, az R környezetet, valamint a rendszerfüggőségeket (C++ könyvtárakat), amelyek az `rmarkdown` és `knitr` csomagok futásához szükségesek.
2. **Renderelés:** A `quarto render` parancs lefuttatásával a forrásfájlokból elkészíti a statikus weboldalt a `_site/` mappába.
3. **Artifact mentése:** A kész weboldalt becsomagolja, és `human-ai-site` néven elmenti a GitHub szerverére (Artifact).
4. **Webhook trigger:** Egy biztonságos POST kérést küld a szerverünknek, amely tartalmazza a folyamat azonosítóját (`run_id`) és egy titkos kulcsot (Deploy Token).

## 2. Publikálás a szerveren (`deploy.php`)

A GitHub értesítését a szerveren található `deploy.php` script fogadja, amely a következőket végzi el a háttérben:
1. **Hitelesítés:** Ellenőrzi, hogy a bejövő kérés a megadott titkos kulccsal érkezett-e (így védve a rendszert az illetéktelen hívásoktól).
2. **Letöltés:** A megkapott `run_id` és egy GitHub Personal Access Token (PAT) segítségével a script lekérdezi a GitHub API-t, és letölti a frissen generált `human-ai-site` ZIP fájlt.
3. **Kicsomagolás:** A fájlokat egy átmeneti (`tmp`) mappába bontja ki.
4. **Szinkronizálás (`rsync`):** Az `rsync -a --delete` parancs segítségével a kicsomagolt fájlokat átmásolja a weboldal éles gyökérkönyvtárába (`human-ai`). 
   *Megjegyzés: A `--delete` kapcsoló gondoskodik arról, hogy a forráskódból időközben törölt fájlok (pl. régi képek, átnevezett mappák) a szerverről is automatikusan törlődjenek.*

## 3. Rendszergazdai tudnivalók és Hibaelhárítás

Mivel a fájlok mozgatását és törlését a `deploy.php`-n keresztül maga a webszerver végzi, **kritikus fontosságú a megfelelő Linux fájljogosultságok fenntartása**. 

