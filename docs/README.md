# Interactive Atlas (static GitHub Pages)

The dependency-free, responsive HTML directory lives at [docs/index.html](index.html) and consumes the generated [docs/catalog.js](catalog.js). The JavaScript dataset is generated from the canonical `data/projects.json`.

## Preview locally

Open `docs/index.html` in a browser. There is no build step, framework, backend, tracking, or network requirement for the filters. Upstream GitHub links naturally require an internet connection.

## Update the dataset

After editing `data/projects.json`, run:

```bash
python scripts/build_atlas.py
python scripts/validate.py
```

Commit both `data/projects.json` and `docs/catalog.js`. CI rejects stale copies.

## Deploy via GitHub Pages

In repository **Settings → Pages**, choose **Deploy from a branch**, select `main` and `/docs`, then Save. When GitHub finishes deployment, the URL is generally `https://notsointresting.github.io/awesome-low-memory-llm/`. The page is only live once GitHub Pages has actually been enabled and deployed.

## Integrity and interpretation

The RAM selector shows only projects with a **published minimum** or **a documented test system no larger than the selected RAM**. It is not a compatibility guarantee. Unknown measurements are deliberately excluded from RAM-filtered search results rather than mislabeled incompatible.

Every numeric result in the explorer is labeled author-reported. Rates from different model/hardware/context configurations must not be ranked as an apples-to-apples performance comparison.
