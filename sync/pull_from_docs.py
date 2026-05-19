"""
pull_from_docs.py — ongoing sync: Google Docs tabs → local .md files.

Run this after the team makes edits in Google Docs to bring the changes
into the git repository.

Usage:
    python pull_from_docs.py              # sync all mapped tabs
    python pull_from_docs.py --list-tabs  # print all tab titles and IDs (useful for setup)
"""

import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ── config ────────────────────────────────────────────────────────────────────

DOCUMENT_ID = "1yWOzzF4uSnGYGq62yCdOEbBpA4h0bwGdlrA0S_9E2p0"
SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]

ROOT = Path(__file__).parent.parent
CREDS_FILE = ROOT / "credentials.json"
TOKEN_FILE = Path(__file__).parent / "token_read.json"

# Google Docs tab title → local markdown file.
# Run with --list-tabs first to see the exact tab names in your document.
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

# ── Docs → markdown ───────────────────────────────────────────────────────────

def extract_text(paragraph: dict) -> str:
    """Concatenate all text runs in a paragraph element."""
    text = ""
    for elem in paragraph.get("elements", []):
        text += elem.get("textRun", {}).get("content", "")
    return text.rstrip("\n")


def tab_to_markdown(tab: dict) -> str:
    """
    Convert a Google Docs tab body to markdown.

    Mapping:
      HEADING_1  → # …
      HEADING_2  → ## …
      HEADING_3  → ### …
      bullet     → - …
      (blank)    → empty line
      other      → plain text
    """
    content = (
        tab.get("documentTab", {})
           .get("body", {})
           .get("content", [])
    )
    lines = []

    for elem in content:
        para = elem.get("paragraph")
        if not para:
            continue

        text = extract_text(para)
        style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
        bullet = para.get("bullet")

        if not text.strip():
            lines.append("")
            continue

        if style == "HEADING_1":
            lines.append(f"# {text}")
        elif style == "HEADING_2":
            lines.append(f"## {text}")
        elif style == "HEADING_3":
            lines.append(f"### {text}")
        elif bullet:
            nesting = bullet.get("nestingLevel", 0)
            lines.append("  " * nesting + f"- {text}")
        else:
            lines.append(text)

    # Collapse consecutive blank lines into one
    result = []
    prev_blank = False
    for line in lines:
        is_blank = not line.strip()
        if is_blank and prev_blank:
            continue
        result.append(line)
        prev_blank = is_blank

    return "\n".join(result).strip() + "\n"

# ── main ──────────────────────────────────────────────────────────────────────

def list_tabs(service):
    doc = service.documents().get(
        documentId=DOCUMENT_ID,
        includeTabsContent=True,
    ).execute()
    print(f"Document: {doc.get('title')}\n")
    tabs = doc.get("tabs", [])
    if not tabs:
        print("No tabs found (document may pre-date the Tabs feature).")
        return
    print(f"{'Index':<8} {'Title':<20} Tab ID")
    print("-" * 60)
    for tab in tabs:
        p = tab.get("tabProperties", {})
        print(f"{p.get('index', '?'):<8} {p.get('title', '(untitled)'):<20} {p.get('tabId', '')}")


def pull():
    creds = get_creds()
    service = build("docs", "v1", credentials=creds)

    print(f"Fetching document {DOCUMENT_ID} ...")
    doc = service.documents().get(
        documentId=DOCUMENT_ID,
        includeTabsContent=True,
    ).execute()

    tabs = doc.get("tabs", [])
    if not tabs:
        print("No tabs found. Verify the document ID and that tabs exist.")
        return

    matched = 0
    for tab in tabs:
        title = tab.get("tabProperties", {}).get("title", "")
        if title not in TAB_MAP:
            print(f"  skip  '{title}' (no mapping in TAB_MAP)")
            continue

        md_path = TAB_MAP[title]
        md_content = tab_to_markdown(tab)
        md_path.write_text(md_content, encoding="utf-8")
        print(f"  OK  '{title}' -> {md_path.relative_to(ROOT)}")
        matched += 1

    if matched == 0:
        print("\nNo tabs matched TAB_MAP. Run with --list-tabs to see actual tab names.")
    else:
        print(f"\nDone: {matched} file(s) updated.")


if __name__ == "__main__":
    if "--list-tabs" in sys.argv:
        creds = get_creds()
        service = build("docs", "v1", credentials=creds)
        list_tabs(service)
    else:
        pull()
