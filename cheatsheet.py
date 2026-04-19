#!/usr/bin/env python3
"""Keyboard cheatsheet — TUI replica using Rich.

Renders a 4-column keyboard shortcut reference for AeroSpace, Ghostty,
and Neovim.  Designed to run inside a Ghostty split or dedicated tab.

Usage:
    python3 cheatsheet.py
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text

# ── Palette (TokyoNight Moon) ──────────────────────────────────────────────
PURPLE     = "#c099ff"
DIM        = "#666666"
KEY_FG     = "#f7f7f7"
KEY_BG     = "grey19"
VIM_FG     = "#82aaff"
VIM_BG     = "grey11"
ACCENT_FG  = PURPLE
ACCENT_BG  = "grey15"
ACTION_FG  = "#c3c8c2"
HINT_STYLE = f"italic {DIM}"


# ── Helpers ────────────────────────────────────────────────────────────────

def k(label, style="key"):
    """Single key-cap."""
    if style == "vim":
        return Text(f" {label} ", style=f"{VIM_FG} on {VIM_BG}")
    if style == "accent":
        return Text(f" {label} ", style=f"bold {ACCENT_FG} on {ACCENT_BG}")
    # default "key"
    return Text(f" {label} ", style=f"{KEY_FG} on {KEY_BG}")


def sp(label=" "):
    """Thin separator between key-caps."""
    return Text(f" {label} ", style=DIM)


def join(*parts):
    """Concatenate key-caps and separators into one Text object."""
    t = Text()
    for p in parts:
        t.append_text(p)
    return t


def _build_panel(title, groups):
    """Return a Panel wrapping a table of shortcut rows.

    *groups* is a list of (group_label, rows) tuples.
    Each row is (action_str, keys_Text[, highlight_bool]).
    A row whose action starts with "hint:" is rendered as a dim hint line.
    """
    tbl = Table(
        show_header=False, box=None, padding=(0, 1),
        expand=True, show_edge=False,
    )
    tbl.add_column("action", ratio=5, no_wrap=False)
    tbl.add_column("keys",   ratio=4, no_wrap=True, justify="right")

    first = True
    for label, rows in groups:
        if not first:
            tbl.add_row("", "")          # blank spacer between groups
        first = False
        tbl.add_row(Text(label.upper(), style=f"bold {DIM}"), Text(""))

        for row in rows:
            act, keys_text = row[0], row[1]
            hl = row[2] if len(row) > 2 else False

            if act.startswith("hint:"):
                tbl.add_row(Text(act[5:], style=HINT_STYLE), Text(""))
                continue

            action = Text(act, style=f"bold {ACCENT_FG}" if hl else ACTION_FG)
            tbl.add_row(action, keys_text)

    return Panel(
        tbl, title=f"[bold {PURPLE}]{title}[/]", title_align="left",
        border_style="grey30", padding=(0, 1), expand=True,
    )


def _build_recipes(wide=False):
    """Return a wide recipes panel — situational quick-reference."""

    def section(title, rows):
        tbl = Table(show_header=False, box=None, padding=(0, 1), expand=True, show_edge=False)
        tbl.add_column("action", ratio=5, no_wrap=False)
        tbl.add_column("keys",   ratio=4, no_wrap=True, justify="right")
        tbl.add_row(Text(title, style=f"bold {DIM}"), Text(""))
        for act, keys_text, *rest in rows:
            hl = bool(rest)
            tbl.add_row(Text(act, style=f"bold {ACCENT_FG}" if hl else ACTION_FG), keys_text)
        return tbl

    nvim_nav = section("NEOVIM — FIND & NAVIGATE", [
        ("Don't know filename",
         join(k("Space", "vim"), k("/", "vim")), True),
        ("Know part of filename",
         join(k("Space", "vim"), k("Space", "vim"))),
        ("Browse file tree",
         join(k("Space", "vim"), k("e", "vim"))),
        ("Recently edited",
         join(k("Space", "vim"), k("f r", "vim"))),
        ("Switch open buffer",
         join(k("Space", "vim"), k(",", "vim"))),
        ("Jump anywhere in file",
         join(k("s", "accent")), True),
        ("Jump to definition",
         join(k("g d", "vim"))),
        ("Jump back",
         join(k("⌃o", "accent")), True),
        ("Find symbol / fn",
         join(k("Space", "vim"), k("s s", "vim"))),
        ("Projects list",
         join(k("Space", "vim"), k("f p", "vim"))),
    ])

    nvim_edit = section("NEOVIM — EDIT & FIX", [
        ("Rename symbol",
         join(k("Space", "vim"), k("c r", "vim")), True),
        ("Code action / fix",
         join(k("Space", "vim"), k("c a", "vim")), True),
        ("See line errors",
         join(k("Space", "vim"), k("c d", "vim"))),
        ("All errors (Trouble)",
         join(k("Space", "vim"), k("x x", "vim"))),
        ("Format file",
         join(k("Space", "vim"), k("c f", "vim"))),
        ("Extract function",
         join(k("Space", "vim"), k("r e", "vim"))),
        ("Stage hunk (git)",
         join(k("Space", "vim"), k("g h s", "vim"))),
        ("Open LazyGit",
         join(k("Space", "vim"), k("g g", "vim"))),
        ("Undo / Redo",
         join(k("u", "vim"), sp("/"), k("⌃r", "vim"))),
    ])

    other = section("AEROSPACE & GHOSTTY", [
        ("Layout broken",
         join(k("⌥", "accent"), k("⇧", "accent"), k("R", "accent")), True),
        ("App in wrong workspace",
         join(k("⌥", "accent"), k("⇧", "accent"), k("1", "accent"), sp("…"), k("9", "accent"))),
        ("New terminal pane",
         join(k("⌘"), k("D")), True),
        ("Zoom pane",
         join(k("⌘"), k("⇧"), k("⏎"))),
        ("Search terminal output",
         join(k("⌘"), k("F"))),
        ("Jump to prev prompt",
         join(k("⌘"), k("↑"))),
        ("Switch workspace",
         join(k("⌥"), k("T"), sp("/"), k("⌥"), k("V"), sp("/"), k("⌥"), k("A"))),
    ])

    if wide:
        grid = Table.grid(expand=True, padding=(0, 1))
        grid.add_column(ratio=1)
        grid.add_column(ratio=1)
        grid.add_column(ratio=1)
        grid.add_row(nvim_nav, nvim_edit, other)
    else:
        right = Table.grid(expand=True)
        right.add_column(ratio=1)
        right.add_row(nvim_edit)
        right.add_row(other)
        grid = Table.grid(expand=True, padding=(0, 1))
        grid.add_column(ratio=1)
        grid.add_column(ratio=1)
        grid.add_row(nvim_nav, right)

    return Panel(
        grid,
        title=f"[bold {PURPLE}]✦  Recipes — reach for this when…[/]",
        title_align="center",
        border_style=PURPLE,
        padding=(0, 1),
        expand=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Column 1 — AeroSpace
# ═══════════════════════════════════════════════════════════════════════════

col1 = _build_panel("◧ AeroSpace", [
    ("Focus Window", [
        ("Left / Down / Up / Right",
         join(k("⌥"), k("H"), sp(), k("J"), sp(), k("K"), sp(), k("L"))),
    ]),
    ("Move Window", [
        ("Left / Down / Up / Right",
         join(k("⌥"), k("⇧"), k("H"), sp(), k("J"), sp(), k("K"), sp(), k("L"))),
    ]),
    ("Workspaces", [
        ("Next / Prev",
         join(k("⌥"), k("Tab"), sp(), k("⇧"), k("Tab"))),
        ("Send to workspace",
         join(k("⌥"), k("⇧"), k("1"), sp("…"), k("9"))),
        ("hint:1 Chrome · 2 Discord · 3 Sourcetree", Text("")),
        ("hint:4 Bitwarden · 5 Claude · 6 Spotify+WA", Text("")),
        ("Terminal",
         join(k("⌥", "accent"), k("T", "accent"), sp("send"), k("⇧"), k("T")),
         True),
        ("Neovim (Kitty)",
         join(k("⌥", "accent"), k("V", "accent"), sp("send"), k("⇧"), k("V")),
         True),
        ("Android Studio",
         join(k("⌥", "accent"), k("A", "accent"), sp("send"), k("⇧"), k("A")),
         True),
    ]),
    ("Layout", [
        ("Fullscreen",
         join(k("⌥"), k("F"))),
        ("Float / Tile",
         join(k("⌥"), k("⇧"), k("F"))),
        ("Tiles / Accordion",
         join(k("⌥"), k("/"))),
        ("H / V split",
         join(k("⌥"), k(","))),
        ("Shrink / Grow",
         join(k("⌥"), k("-"), sp(), k("="))),
        ("Reset workspace",
         join(k("⌥", "accent"), k("⇧", "accent"), k("R", "accent")),
         True),
        ("Close window",
         join(k("⌥"), k("Q"))),
    ]),
    ("Monitors", [
        ("Focus other monitor",
         join(k("⌥"), k("M"))),
        ("Send window to monitor",
         join(k("⌥"), k("⇧"), k("M"))),
        ("Move workspace to monitor",
         join(k("⌥"), k("⌃"), k("M"))),
    ]),
])


# ═══════════════════════════════════════════════════════════════════════════
# Column 2 — Ghostty  (ordered: common → advanced)
# ═══════════════════════════════════════════════════════════════════════════

col2 = _build_panel("▸ Ghostty", [
    ("Windows & Tiles", [
        ("New tile / Close",
         join(k("⌘"), k("T"), sp(), k("⌘"), k("W"))),
        ("New window",
         join(k("⌘"), k("N"))),
        ("Fullscreen",
         join(k("⌘"), k("⏎"))),
        ("Close window",
         join(k("⌘"), k("⇧"), k("W"))),
    ]),
    ("Navigation", [
        ("Search",
         join(k("⌘"), k("F"))),
        ("Next / Prev match",
         join(k("⌘"), k("G"), sp(), k("⇧"), k("G"))),
        ("Jump to prompt ↑ / ↓",
         join(k("⌘"), k("↑"), sp(), k("↓"))),
        ("Clear screen",
         join(k("⌘"), k("K"))),
        ("Select all",
         join(k("⌘"), k("A"))),
        ("Scroll top / bottom",
         join(k("⌘"), k("Home"), sp(), k("End"))),
    ]),
    ("Splits", [
        ("Split right / down",
         join(k("⌘"), k("D"), sp(), k("⇧"), k("D"))),
        ("Focus split",
         join(k("⌘"), k("⌥"), k("↑"), sp(), k("↓"), sp(), k("←"), sp(), k("→"))),
        ("Prev / Next split",
         join(k("⌘"), k("["), sp(), k("]"))),
        ("Zoom split",
         join(k("⌘", "accent"), k("⇧", "accent"), k("⏎", "accent")),
         True),
        ("Resize split",
         join(k("⌘"), k("⌃"), k("↑"), sp(), k("↓"), sp(), k("←"), sp(), k("→"))),
        ("Equalize splits",
         join(k("⌘"), k("⌃"), k("="))),
    ]),
    ("Config & Tools", [
        ("Command palette",
         join(k("⌘", "accent"), k("⇧", "accent"), k("P", "accent")),
         True),
        ("Open / Reload config",
         join(k("⌘"), k(","), sp(), k("⇧"), k(","))),
        ("Zoom in / out",
         join(k("⌘"), k("+"), sp(), k("-"))),
        ("Reset zoom",
         join(k("⌘"), k("0"))),
    ]),
])


# ═══════════════════════════════════════════════════════════════════════════
# Column 3 — Neovim: Navigate & Code
# ═══════════════════════════════════════════════════════════════════════════

col3 = _build_panel("⚡ Neovim — Navigate & Code", [
    ("Files & Search", [
        ("hint:Leader = Space · press Space then wait for hints", Text("")),
        ("Find files",
         join(k("Space", "vim"), k("Space", "vim"))),
        ("Grep project",
         join(k("Space", "vim"), k("/", "vim"))),
        ("File explorer",
         join(k("Space", "vim"), k("e", "vim"))),
        ("Recent files",
         join(k("Space", "vim"), k("f r", "vim"))),
        ("Buffer switcher",
         join(k("Space", "vim"), k(",", "vim"))),
        ("Search & replace",
         join(k("Space", "vim"), k("s r", "vim"))),
        ("Symbols (buffer)",
         join(k("Space", "vim"), k("s s", "vim"))),
        ("Symbols (workspace)",
         join(k("Space", "vim"), k("s S", "vim"))),
    ]),
    ("Movement", [
        ("End / Start of line",
         join(k("$", "vim"), sp("/"), k("0", "vim"))),
        ("Top / Bottom of file",
         join(k("g g", "vim"), sp("/"), k("G", "vim"))),
        ("Half page down / up",
         join(k("⌃d", "vim"), sp("/"), k("⌃u", "vim"))),
        ("Word forward / back",
         join(k("w", "vim"), sp("/"), k("b", "vim"))),
        ("Jump back / forward",
         join(k("⌃o", "accent"), sp("/"), k("⌃i", "vim")),
         True),
    ]),
    ("Jump & Select", [
        ("Flash jump (anywhere)",
         join(k("s", "accent")),
         True),
        ("Treesitter select",
         join(k("S", "accent")),
         True),
        ("Word under cursor",
         join(k("*", "vim"), sp("/"), k("#", "vim"))),
    ]),
    ("LSP / Code", [
        ("Go to definition",
         join(k("g d", "vim"))),
        ("Go to references",
         join(k("g r", "vim"))),
        ("Go to implementation",
         join(k("g I", "vim"))),
        ("Go to type definition",
         join(k("g y", "vim"))),
        ("Hover docs",
         join(k("K", "vim"))),
        ("Code actions",
         join(k("Space", "vim"), k("c a", "vim"))),
        ("Rename (inline)",
         join(k("Space", "vim"), k("c r", "vim"))),
        ("Format",
         join(k("Space", "vim"), k("c f", "vim"))),
        ("Line diagnostics",
         join(k("Space", "vim"), k("c d", "vim"))),
        ("Next / Prev error",
         join(k("] d", "vim"), sp(), k("[ d", "vim"))),
        ("Symbol outline",
         join(k("Space", "vim"), k("c s", "vim"))),
    ]),
    ("Refactoring (visual select first)", [
        ("Extract function",
         join(k("Space", "vim"), k("r e", "vim"))),
        ("Extract variable",
         join(k("Space", "vim"), k("r v", "vim"))),
        ("Inline variable",
         join(k("Space", "vim"), k("r i", "vim"))),
    ]),
    ("Editing", [
        ("Comment line / selection",
         join(k("g c c", "vim"), sp("/"), k("g c", "vim"))),
        ("Move line down / up",
         join(k("⌃", "accent"), k("⇧", "accent"), k("J", "accent"), sp(), k("K", "accent")),
         True),
        ("Duplicate line",
         join(k("y y p", "vim"))),
        ("Delete line",
         join(k("d d", "vim"))),
        ("Undo / Redo",
         join(k("u", "vim"), sp("/"), k("⌃"), k("r", "vim"))),
        ("Save",
         join(k("⌃"), k("s", "vim"))),
        ("Indent / Dedent",
         join(k(">", "vim"), sp("/"), k("<", "vim"))),
    ]),
])


# ═══════════════════════════════════════════════════════════════════════════
# Column 4 — Neovim: Debug, Test & Tools
# ═══════════════════════════════════════════════════════════════════════════

col4 = _build_panel("⚡ Neovim — Debug, Test & Tools", [
    ("Debug (DAP)", [
        ("Toggle breakpoint",
         join(k("Space", "vim"), k("d b", "vim"))),
        ("Conditional breakpoint",
         join(k("Space", "vim"), k("d B", "vim"))),
        ("Continue / Start",
         join(k("Space", "vim"), k("d c", "vim"))),
        ("Step over",
         join(k("Space", "vim"), k("d o", "vim"))),
        ("Step into",
         join(k("Space", "vim"), k("d i", "vim"))),
        ("Step out",
         join(k("Space", "vim"), k("d O", "vim"))),
        ("Debug UI",
         join(k("Space", "vim"), k("d u", "vim"))),
        ("Eval expression",
         join(k("Space", "vim"), k("d e", "vim"))),
        ("Terminate",
         join(k("Space", "vim"), k("d t", "vim"))),
    ]),
    ("Testing", [
        ("Run nearest test",
         join(k("Space", "vim"), k("t r", "vim"))),
        ("Run file tests",
         join(k("Space", "vim"), k("t t", "vim"))),
        ("Run all tests",
         join(k("Space", "vim"), k("t T", "vim"))),
        ("Debug nearest test",
         join(k("Space", "vim"), k("t d", "vim"))),
        ("Test output",
         join(k("Space", "vim"), k("t o", "vim"))),
        ("Test summary",
         join(k("Space", "vim"), k("t s", "vim"))),
        ("Stop tests",
         join(k("Space", "vim"), k("t S", "vim"))),
    ]),
    ("Git", [
        ("LazyGit",
         join(k("Space", "vim"), k("g g", "vim"))),
        ("Blame line",
         join(k("Space", "vim"), k("g b", "vim"))),
        ("Next / Prev hunk",
         join(k("] h", "vim"), sp(), k("[ h", "vim"))),
        ("Stage / Reset hunk",
         join(k("Space", "vim"), k("g h s", "vim"), sp(), k("r", "vim"))),
    ]),
    ("Diagnostics (Trouble)", [
        ("Toggle trouble",
         join(k("Space", "vim"), k("x x", "vim"))),
        ("Workspace diagnostics",
         join(k("Space", "vim"), k("x X", "vim"))),
        ("Todo list",
         join(k("Space", "vim"), k("x t", "vim"))),
        ("Quickfix list",
         join(k("Space", "vim"), k("x q", "vim"))),
    ]),
    ("Buffers & Windows", [
        ("Prev / Next buffer",
         join(k("S-h", "vim"), sp(), k("S-l", "vim"))),
        ("Close buffer",
         join(k("Space", "vim"), k("b d", "vim"))),
        ("Close other buffers",
         join(k("Space", "vim"), k("b o", "vim"))),
        ("Split H / V",
         join(k("Space", "vim"), k("-", "vim"), sp(), k("|", "vim"))),
        ("Navigate windows",
         join(k("⌃"), k("h", "vim"), sp(), k("j", "vim"), sp(), k("k", "vim"), sp(), k("l", "vim"))),
        ("Terminal",
         join(k("⌃"), k("/", "vim"))),
    ]),
    ("Tools", [
        ("Which-key (show all keys)",
         join(k("Space", "accent"), sp("wait")),
         True),
        ("Mason (LSP tools)",
         join(k("Space", "vim"), k("c m", "vim"))),
        ("Lazy (plugins)",
         join(k("Space", "vim"), k("l", "vim"))),
    ]),
])


# ═══════════════════════════════════════════════════════════════════════════
# Render
# ═══════════════════════════════════════════════════════════════════════════

def main():
    console = Console()
    console.print()
    console.print(
        Text("Keyboard Cheatsheet", style=f"bold {PURPLE}"),
        justify="center",
    )
    console.print()

    w = console.width
    if w >= 160:
        console.print(Columns([col1, col2, col3, col4], equal=True, expand=True))
    elif w >= 80:
        grid = Table.grid(expand=True)
        grid.add_column(ratio=1)
        grid.add_column(ratio=1)
        grid.add_row(col1, col2)
        grid.add_row(col3, col4)
        console.print(grid)
    else:
        for panel in (col1, col2, col3, col4):
            console.print(panel)
            console.print()

    console.print()
    console.print(_build_recipes(wide=(w >= 120)))


if __name__ == "__main__":
    main()
