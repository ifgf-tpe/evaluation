# CLAUDE.md — IFGF Taipei Service Evaluation Repository

Static knowledge snapshot for LLMs. Do not log session activity or prompting history here.

---

## Project Purpose

This repository stores weekly Sunday-service evaluation points for IFGF Taipei (Gereja IFGF Taipei), extracted from LINE group chat backups. The goal is to build a structured, searchable record of past evaluation points that can be used to sharpen and update the team's Standard Operating Procedures (SOP).

---

## Repository Structure

```
evaluation/
├── CLAUDE.md                              # This file
├── README.md                              # Minimal project description
├── .gitignore                             # Ignores all *.txt files (LINE chat exports)
├── .claude/
│   └── settings.local.json               # Claude Code local permissions
├── [LINE] Chat in PaW _ Mulmed.txt        # GITIGNORED — PAW & Multimedia combined group chat export
├── [LINE] Chat in IFGF - Soundman.txt     # GITIGNORED — Sound team group chat export
├── [LINE] Chat in IFGF - Multimedia Sy.txt # GITIGNORED — Multimedia systems group chat export
└── evaluations/
    ├── paw.md        # Praise & Worship team evaluations (Oct 2021 – present)
    ├── sound.md      # Sound system team evaluations (Dec 2021 – present)
    └── multimedia.md # Multimedia team evaluations (Oct 2021 – present)
```

> The `.txt` source files are gitignored and must be obtained separately from the LINE chat export backups.

---

## Teams

### PAW — Praise and Worship
Covers everything related to music performance:
- Worship Leader (WL) — leads the congregation in worship, gives cues
- Singers / Backup singers
- Musicians: pianist/keyboardist, guitarist, bassist, drummer, tambourine

### Sound
Covers the sound system and audio engineering:
- Mixer operation (gain staging, EQ, fader levels)
- IEM (In-Ear Monitor) setup and mix for musicians and WL
- Check-sound / sound check process
- Hardware: microphones, cables, soundcard, speaker, DI box

> **Classification rule**: Gain-related feedback (mixer gain, audio input levels, recording levels) is categorised under **Sound**, not Multimedia — even when the symptom appears in an OBS recording.

### Multimedia
Covers visual and broadcast systems:
- ProPresenter / PPT — song lyrics display
- OBS — recording and live-streaming
- Cameras — video production
- Countdown timers and announcement videos

---

## Key Terminology

| Term | Meaning |
|------|---------|
| WL | Worship Leader |
| MD | Music Director — runs the click track and sequencer, cues musicians |
| Click | Click track (metronome feed for musicians via IEM) |
| Sequencer | Pre-recorded instrumental arrangement / backing track |
| IEM | In-Ear Monitor — personal mix earpiece for each musician/singer |
| AUX | Auxiliary send on the mixer (used to route to IEM or monitor speakers) |
| Gain | Input gain (preamp level) on the mixer |
| Fader | Channel volume on the mixer |
| PRE | Pre-fader send mode on AUX — level does not follow fader changes |
| Snake | Multi-channel audio cable (stage box) |
| OBS | Open Broadcaster Software — used for recording and streaming |
| PPT | ProPresenter or PowerPoint — lyrics display software |
| Dopeng | Internal shorthand for Sunday main service |
| Super Sunday | Special Sunday service (e.g., HUT RI, Easter, Christmas) |
| Zhongli | One of two IFGF Taipei service locations (Zhongli campus) |
| Taipei | One of two IFGF Taipei service locations (Taipei campus) |
| Overtune | Modulation / key change during worship |
| Free Worship | Improvised worship section led by WL, no fixed arrangement |
| Singkup | Harmony singing (harmonization) |
| Gladi | Rehearsal (Sabtu = Saturday rehearsal) |

---

## Evaluation File Conventions

### Format

```markdown
# Evaluasi <Team Name>

## YYYY-MM-DD
- <Evaluation point in Indonesian>
- <Evaluation point in Indonesian> (Zhongli)
- <Evaluation point in Indonesian> (Taipei)
```

### Rules
- **Header date** = Sunday service date (not the date the evaluation was posted)
- **Order** = newest date at the top, oldest at the bottom
- **Language** = Indonesian throughout; translate Chinese or English content
- **Location** = append `(Taipei)` or `(Zhongli)` at the end of a point if it is location-specific; no parentheses if it applies to both
- **No author names** — content only, no attribution
- **No redundancy** — if the same point appears multiple times for the same week, keep only one

### Grouping Rule
An evaluation posted on Sunday through the following Saturday belongs to that Sunday's section.

---

## Source Chat Files

| File | Group | Team(s) | Active Since |
|------|-------|---------|--------------|
| `[LINE] Chat in PaW _ Mulmed.txt` | PaW & Mulmed | PAW, Sound, Multimedia | Sep 2021 |
| `[LINE] Chat in IFGF - Soundman.txt` | IFGF Soundman | Sound | Apr 2025 |
| `[LINE] Chat in IFGF - Multimedia Sy.txt` | IFGF Multimedia Sy | Multimedia | Nov 2021 |

### Extraction Notes
- **PaW _ Mulmed**: Evaluations are typically prefixed with "Eval" or "Evaluasi". Each message may contain points for multiple teams — tag each point to its correct team.
- **Soundman**: Evaluations are not always explicitly tagged. Extract all discussions that contain feedback, problems encountered, improvement suggestions, SOP guidance, or lessons learned from a service.
- **Multimedia Sy**: Same as Soundman — extract all relevant improvement-oriented content, not only explicitly tagged evaluations.
