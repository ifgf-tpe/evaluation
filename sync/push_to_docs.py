"""
push_to_docs.py — one-time seed: push local .md files → Google Docs tabs.

Run this once to populate the Docs with the current markdown state.
After this, Google Docs is the source of truth; use pull_from_docs.py
to sync future edits back to the .md files.

WARNING: Clears each matched tab before writing. Any content already
in those tabs will be overwritten.

Usage:
    python push_to_docs.py
"""

import re
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ── config ────────────────────────────────────────────────────────────────────

DOCUMENT_ID = "1yWOzzF4uSnGYGq62yCdOEbBpA4h0bwGdlrA0S_9E2p0"
SCOPES = ["https://www.googleapis.com/auth/documents"]

ROOT = Path(__file__).parent.parent
CREDS_FILE = ROOT / "credentials.json"
TOKEN_FILE = Path(__file__).parent / "token_write.json"

# Google Docs tab title → local markdown file.
# Update the keys to match the exact tab names shown in your Google Doc.
TAB_MAP = {
    "PAW": ROOT / "evaluations" / "paw.md",
    "Sound System": ROOT / "evaluations" / "sound.md",
    "Multimedia": ROOT / "evaluations" / "multimedia.md",
}

# ── auth ──────────────────────────────────────────────────────────────────────

def get_creds() -> Credentials:
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return creds

# ── markdown → Docs requests ──────────────────────────────────────────────────

def build_requests(md_text: str, tab_id: str) -> list:
    """
    Convert markdown text into a list of Google Docs batchUpdate requests.

    Strategy:
    1. Insert all text as a single block at index 1.
    2. Walk through lines again, applying HEADING_1/HEADING_2/bullet styles
       at the correct character offsets.

    Character index arithmetic uses len() which is correct for our content
    (Indonesian + ASCII; no surrogate-pair characters).
    """
    lines = [line.rstrip() for line in md_text.strip().splitlines()]
    full_text = "\n".join(lines) + "\n"

    requests = [
        {
            "insertText": {
                "location": {"index": 1, "tabId": tab_id},
                "text": full_text,
            }
        }
    ]

    cursor = 1
    for line in lines:
        line_len = len(line) + 1  # +1 for the \n separator
        line_end = cursor + line_len

        if line.startswith("# "):
            requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": cursor, "endIndex": line_end, "tabId": tab_id},
                    "paragraphStyle": {"namedStyleType": "HEADING_1"},
                    "fields": "namedStyleType",
                }
            })
        elif line.startswith("## "):
            requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": cursor, "endIndex": line_end, "tabId": tab_id},
                    "paragraphStyle": {"namedStyleType": "HEADING_2"},
                    "fields": "namedStyleType",
                }
            })
        elif line.startswith("### "):
            requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": cursor, "endIndex": line_end, "tabId": tab_id},
                    "paragraphStyle": {"namedStyleType": "HEADING_3"},
                    "fields": "namedStyleType",
                }
            })
        elif re.match(r"^- ", line):
            requests.append({
                "createParagraphBullets": {
                    "range": {"startIndex": cursor, "endIndex": line_end, "tabId": tab_id},
                    "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                }
            })

        cursor = line_end

    return requests


def get_body_end_index(tab: dict) -> int:
    """Return the last deletable index in a tab body (sentinel \n excluded)."""
    content = tab.get("documentTab", {}).get("body", {}).get("content", [])
    if not content:
        return 1
    return content[-1].get("endIndex", 2) - 1  # leave the sentinel newline

# ── main ──────────────────────────────────────────────────────────────────────

def push():
    creds = get_creds()
    service = build("docs", "v1", credentials=creds)

    print(f"Fetching document {DOCUMENT_ID} ...")
    doc = service.documents().get(
        documentId=DOCUMENT_ID,
        includeTabsContent=True,
    ).execute()

    tabs = doc.get("tabs", [])
    if not tabs:
        print("No tabs found. Verify the document ID and that Tabs API is supported.")
        return

    for tab in tabs:
        props = tab.get("tabProperties", {})
        title = props.get("title", "")
        tab_id = props.get("tabId", "")

        if title not in TAB_MAP:
            print(f"  skip  '{title}' (no mapping in TAB_MAP)")
            continue

        md_path = TAB_MAP[title]
        if not md_path.exists():
            print(f"  skip  '{title}' — {md_path} not found")
            continue

        md_text = md_path.read_text(encoding="utf-8")

        # 1. Clear existing tab content
        end_idx = get_body_end_index(tab)
        requests = []
        if end_idx > 1:
            requests.append({
                "deleteContentRange": {
                    "range": {
                        "startIndex": 1,
                        "endIndex": end_idx,
                        "tabId": tab_id,
                    }
                }
            })

        # 2. Write markdown content
        requests += build_requests(md_text, tab_id)

        service.documents().batchUpdate(
            documentId=DOCUMENT_ID,
            body={"requests": requests},
        ).execute()

        print(f"  OK  '{title}' <- {md_path.relative_to(ROOT)}")

    print("\nDone. Google Docs is now populated from the markdown files.")


if __name__ == "__main__":
    push()
