'''
Renders raw AI summary text as styled HTML for the summary display.

The summarizer marks every span it generated itself with ``<...>`` pairs
(everything outside the pairs is quoted verbatim from the sources).  This
module strips those markers and highlights the AI-generated spans in the
theme blue, while turning the markdown-ish structure (``###`` headings,
``**bold**`` and ``*`` bullet lists) into proper rich text so the output
reads like a chat reply instead of a raw document.
'''

import html

# Theme colors, kept in sync with PySide/styles.py
THEME_BLUE = "#8ab4f8"
THEME_TEXT = "#dfe1e5"
THEME_HEADING = "#f5f5f6"

_AI_OPEN = "<"
_AI_CLOSE = ">"
_BOLD_MARK = "**"

# A span of text with its AI-generated and bold flags
Span = tuple[str, bool, bool]


def render_summary(text: str) -> str:
    '''
    Convert raw summary text into an HTML document for QTextEdit.
    Returns an empty string when there is nothing to display.
    '''
    if not text or not text.strip():
        return ""

    blocks: list[str] = []
    ai_open = False
    in_list = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            blocks.append("</ul>")
            in_list = False

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            close_list()
            continue

        spans, ai_open = _line_spans(line, ai_open)
        # Block detection runs on the marker-stripped text, so a heading
        # like "<### Title>" is still recognized as a heading
        plain = "".join(text for text, _, _ in spans)

        if plain.startswith("###"):
            close_list()
            content = _render_spans(_strip_prefix(spans, "###"))
            blocks.append(
                f'<h3 style="color:{THEME_HEADING}; font-size:15px; '
                f"font-weight:600; margin-top:14px; margin-bottom:6px;\">"
                f"{content}</h3>"
            )
        elif plain[:2] in ("* ", "- "):
            if not in_list:
                blocks.append(
                    '<ul style="margin-top:4px; margin-bottom:6px; '
                    "margin-left:10px;\">"
                )
                in_list = True
            content = _render_spans(_strip_prefix(spans, plain[:2]))
            blocks.append(f'<li style="margin-bottom:4px;">{content}</li>')
        else:
            close_list()
            blocks.append(
                f'<p style="margin-top:8px; margin-bottom:8px;">'
                f"{_render_spans(spans)}</p>"
            )

    close_list()

    return (
        f'<html><body style="color:{THEME_TEXT}; font-size:13px; '
        f'font-family:Inter,"Segoe UI",sans-serif;">'
        + "\n".join(blocks)
        + "</body></html>"
    )


def _line_spans(line: str, ai_open: bool) -> tuple[list[Span], bool]:
    '''
    Split a line into ``(text, is_ai, is_bold)`` spans.

    ``<`` opens an AI-generated span and ``>`` closes one; the state
    carries across lines.  ``**`` toggles bold.  Marker characters are
    dropped.  Returns the merged spans and the updated AI state.
    '''
    spans: list[Span] = []
    bold = False
    buf = ""
    buf_ai = ai_open
    buf_bold = False

    def flush() -> None:
        nonlocal buf
        if buf:
            spans.append((buf, buf_ai, buf_bold))
        buf = ""

    i = 0
    while i < len(line):
        ch = line[i]
        if ch == _AI_OPEN and not ai_open:
            flush()
            ai_open = True
            i += 1
        elif ch == _AI_CLOSE and ai_open:
            flush()
            ai_open = False
            i += 1
        elif line.startswith(_BOLD_MARK, i):
            flush()
            bold = not bold
            i += 2
        else:
            buf_ai = ai_open
            buf_bold = bold
            buf += ch
            i += 1

    flush()

    # Merge adjacent spans that share the same flags
    merged: list[Span] = []
    for span in spans:
        if merged and merged[-1][1] == span[1] and merged[-1][2] == span[2]:
            merged[-1][0] += span[0]
        else:
            merged.append(span)

    return merged, ai_open


def _strip_prefix(spans: list[Span], prefix: str) -> list[Span]:
    '''
    Drop a literal prefix (e.g. ``###`` or ``* ``) from the span list.
    '''
    remaining = prefix
    out = []
    for text, ai, bold in spans:
        if remaining:
            take = min(len(text), len(remaining))
            text = text[take:]
            remaining = remaining[take:]
            if not text:
                continue
        if not out:
            text = text.lstrip()
            if not text:
                continue
        out.append((text, ai, bold))
    return out


def _render_spans(spans: list[Span]) -> str:
    '''
    Turn spans into HTML: escaped text, bold where flagged, and the
    theme blue for AI-generated segments.
    '''
    parts: list[str] = []
    for text, is_ai, is_bold in spans:
        if not text:
            continue
        chunk = html.escape(text)
        if is_bold:
            chunk = f"<b>{chunk}</b>"
        if is_ai:
            chunk = f'<span style="color:{THEME_BLUE}">{chunk}</span>'
        parts.append(chunk)
    return "".join(parts)
