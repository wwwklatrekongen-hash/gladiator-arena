# Gladiator Arena

Single-file browser game: **thirteen rounds**, shop upgrades, loot satchel, boss gauntlet, and a **daily seeded** mode with streak tracking.

## Your live URL (GitHub Pages)

After you deploy (see **What to do now** below), the game is usually at:

| Site type | Example URL (replace parts in `ALL_CAPS`) |
|-----------|---------------------------------------------|
| **Project site** (repo `gladiator-arena` under your user) | `https://YOUR_GITHUB_USERNAME.github.io/gladiator-arena/` → [`index.html`](./index.html) redirects into the game |
| **Direct game file** | `https://YOUR_GITHUB_USERNAME.github.io/gladiator-arena/gladiator_arena.html` |

If the repo name is not `gladiator-arena`, swap that segment for your actual repository name.

---

## What to do now (checklist)

1. **Put these files in one folder** (your Desktop copy is fine), then into a Git repository:
   - `gladiator_arena.html` — the game  
   - `index.html` — optional shortcut URL  
   - `manifest.json`, `icon.svg` — PWA / install  
   - `sw.js` — offline cache (optional but recommended)  
   - `README.md` — this file  

2. **Create a new repository** on GitHub (empty, no README if you are uploading this README yourself).

3. **Push the folder** (GitHub Desktop, or in a terminal):
   ```bash
   git init
   git add .
   git commit -m "Add Gladiator Arena for GitHub Pages"
   git branch -M main
   git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

4. **Turn on GitHub Pages**  
   - Repo → **Settings** → **Pages**  
   - **Build and deployment** → Source: **Deploy from a branch**  
   - Branch: **main** / folder: **/ (root)**  
   - Save. After a minute, open the green **Visit site** URL (or the table above).

5. **Open the game once online** so the service worker can install and cache `gladiator_arena.html` (then offline reload works for that origin).

6. **When you change the game**, bump the cache name in `sw.js` (`CACHE_NAME = '...'`) and push again so returning players get the new HTML without stale cache issues.

---

## Play (local)

- Open [`gladiator_arena.html`](./gladiator_arena.html) in a browser from disk or a static server.
- Optional clean URL: [`index.html`](./index.html) redirects to the game file.

## Controls

- **Mouse / touch:** action buttons in the fight panel; shop and satchel are tappable.
- **Keyboard:** `1` Slash · `2` Thrust · `3` Defend · `4` Taunt · `5` Reckless · `6` War Cry (when it is your turn and the fight panel is visible).
- **Audio:** on mobile, tap once if prompted so Web Audio can resume.

## Features (high level)

- Classic random run vs **Daily** (same seed worldwide for the day).
- **Difficulty** (Story / Normal / Hard), **text size**, **reduced motion**, **combat log filter**, optional **continue run** (autosave at the merchant).
- **PWA-style** [`manifest.json`](./manifest.json) + [`icon.svg`](./icon.svg) for add-to-home-screen where supported.
- **Offline:** [`sw.js`](./sw.js) precaches the listed files and serves them when the network fails (same folder on Pages as the HTML).

## Boss order (spoilers)

Rounds escalate through human gladiators into demonic and cosmic bosses; the final encounter is the **Concept Dragon**. Exact names and mechanics are best discovered in-game.

## License

All rights reserved unless you specify otherwise in your repository.
