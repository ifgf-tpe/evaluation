# IFGF Taipei — Service Evaluation Repository

Weekly Sunday-service evaluation points for the PAW, Sound, and Multimedia teams, extracted from LINE group chat backups and kept in sync with the team's Google Docs working document.

---

## Repository Structure

```text
evaluation/
├── evaluations/
│   ├── paw.md          # Praise & Worship evaluations
│   ├── sound.md        # Sound system evaluations
│   └── multimedia.md   # Multimedia evaluations
├── sync/
│   ├── push_to_docs.py # md → Google Docs (one-time seed)
│   ├── pull_from_docs.py # Google Docs → md (ongoing sync)
│   └── requirements.txt
├── credentials.json    # ← YOU create this (gitignored, see setup below)
├── CLAUDE.md           # LLM knowledge snapshot
└── .gitignore
```

> LINE chat `.txt` exports are gitignored. Obtain them separately from the LINE backup.

---

## Google Docs Working Document

The canonical editable document lives here:
**[Google Docs — IFGF Taipei Evaluasi](https://docs.google.com/document/d/1yWOzzF4uSnGYGq62yCdOEbBpA4h0bwGdlrA0S_9E2p0/edit)**

It has three tabs — **PAW**, **Sound**, **Multimedia** — one per team. The team edits evaluations directly in this document; the sync scripts keep the `.md` files in this repo in step.

---

## Quick-start Sync Workflow

```text
Google Docs (team edits here)
        │
        │  python sync/pull_from_docs.py
        ▼
  evaluations/*.md  (source for SOP updates, git history)
        │
        │  git commit + push
        ▼
     GitHub
```

---

## One-Time Setup

### 1 — Python environment

```bash
# From the repo root
pip install -r sync/requirements.txt
```

Requires **Python 3.8+**.

---

### 2 — Google Cloud project & credentials

> You only need to do this once. After that, the OAuth token is cached locally.

#### 2a — Create a Google Cloud project

1. Open [console.cloud.google.com](https://console.cloud.google.com)
2. Click the project selector (top bar) → **New Project**
3. Name it something like `IFGF Eval Sync` → **Create**

#### 2b — Enable the Google Docs API

1. With your new project selected, go to **APIs & Services → Library**
2. Search **Google Docs API** → click it → **Enable**

#### 2c — Configure the OAuth consent screen

1. Go to **APIs & Services → OAuth consent screen**
2. Choose **External** → **Create**
3. Fill in:
   - App name: `IFGF Eval Sync` (or anything)
   - User support email: your Gmail
   - Developer contact email: your Gmail
4. Click **Save and Continue** through all steps (no scopes needed here)
5. On the **Test users** screen, click **Add users** → add your Gmail address → **Save**

#### 2d — Create OAuth credentials

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth client ID**
3. Application type: **Desktop app**
4. Name: `eval-sync-desktop` (or anything)
5. Click **Create**
6. In the dialog, click **Download JSON**
7. Rename the downloaded file to `credentials.json`
8. Place it in the **repo root** (same folder as this README)

> `credentials.json` is gitignored — it will never be committed.

---

### 3 — Verify tab names

Run the discovery command. The first run opens a browser window asking you to sign in with the Google account that has access to the Docs file.

```bash
python sync/pull_from_docs.py --list-tabs
```

Expected output:

```text
Document: IFGF Taipei Evaluasi

Index    Title                Tab ID
------------------------------------------------------------
0        PAW                  t.abc123...
1        Sound                t.def456...
2        Multimedia           t.ghi789...
```

If any tab title differs from `PAW`, `Sound`, or `Multimedia`, open `sync/pull_from_docs.py` **and** `sync/push_to_docs.py` and update the `TAB_MAP` dictionary at the top of each file to match the exact title shown.

---

### 4 — Seed Google Docs from the current .md files (first time only)

```bash
python sync/push_to_docs.py
```

This clears each matched tab and writes the markdown content into Google Docs with proper heading and bullet formatting. **Only run this once** (or when you deliberately want to overwrite the Docs content with the .md state).

After this step, open the Google Docs link and confirm the content looks correct.

---

## Ongoing Sync Workflow

### After the team edits in Google Docs → update the repo

```bash
# 1. Pull latest changes from Docs into .md files
python sync/pull_from_docs.py

# 2. Review the diff
git diff evaluations/

# 3. Commit and push
git add evaluations/
git commit -m "Sync evaluations from Google Docs YYYY-MM-DD"
git push
```

---

## Evaluation Format

Each `.md` file follows this structure:

```markdown
# Evaluasi <Team>

## YYYY-MM-DD
- Evaluation point in Indonesian
- Location-specific point (Zhongli)
- Location-specific point (Taipei)
```

Rules:

- **Header date** = the Sunday service date
- **Order** = newest week at the top
- **Language** = Indonesian throughout
- **No personal names** — use role labels (WL, singer, gitaris, soundman, mulmed)
- Points must be constructive and actionable

---

## Troubleshooting

| Problem | Fix |
| ------- | --- |
| `FileNotFoundError: credentials.json` | Complete step 2d — download and place the file in the repo root |
| Browser doesn't open for OAuth | Run from a machine with a browser; or set up a redirect URI manually |
| `No tabs found` | The document may be older than the Google Docs Tabs feature; check that tabs exist in the Docs UI |
| Tab titles don't match | Run `--list-tabs` and update `TAB_MAP` in both sync scripts |
| `403 The caller does not have permission` | Make sure your Google account is added as a **Test user** (step 2c) and has edit access to the Google Doc |
| Token expired after 7 days | Delete `sync/token_read.json` or `sync/token_write.json` and re-run; browser will ask to sign in again |
