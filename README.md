# purpleknight-setup

A reproducible macOS desktop environment built around tiling window management, a modern terminal, a dedicated Neovim/LazyVim IDE workspace, and Android Studio.

## Overview

| Component | Purpose | Version |
|-----------|---------|---------|
| [AeroSpace](https://github.com/nikitabobko/AeroSpace) | Tiling window manager | 0.20.3-Beta |
| [JankyBorders](https://github.com/FelixKratz/JankyBorders) | Focused window border highlight (purple `#c099ff`) | 1.8.4 |
| [Ghostty](https://ghostty.org) | Primary terminal (workspace **T**) | — |
| [Kitty](https://sw.kovidgoyal.net/kitty/) | Dedicated LazyVim host (workspace **V**) | — |
| [Neovim](https://neovim.io) / [LazyVim](https://www.lazyvim.org) | Editor running inside Kitty | — |
| [Android Studio](https://developer.android.com/studio) | Android IDE (workspace **A**) — installed via JetBrains Toolbox | — |
| `cheatsheet.py` | Python `rich` TUI showing all shortcuts — launched via `ct` alias | — |

## Prerequisites

- macOS 13 (Ventura) or later
- [Homebrew](https://brew.sh)
- Python 3 (ships with macOS Command Line Tools)

## Installation

### Automated

```bash
git clone <repo-url> ~/purpleknight-setup
cd ~/purpleknight-setup
./install.sh
```

The script is idempotent — re-run it safely after edits.

### Manual

1. **Install dependencies:**

    ```bash
    brew install --cask nikitabobko/tap/aerospace
    brew install FelixKratz/formulae/borders
    brew install --cask ghostty
    brew install --cask kitty
    python3 -m pip install --user rich
    ```

2. **Deploy configs:**

    ```bash
    cp aerospace/aerospace.toml ~/.aerospace.toml

    mkdir -p ~/.config/ghostty ~/.config/kitty ~/.config/nvim/lua/plugins
    cp ghostty/config   ~/.config/ghostty/config
    cp kitty/kitty.conf ~/.config/kitty/kitty.conf

    cp    nvim/init.lua      ~/.config/nvim/init.lua
    cp    nvim/.neoconf.json ~/.config/nvim/.neoconf.json
    cp    nvim/stylua.toml   ~/.config/nvim/stylua.toml
    cp -R nvim/lua/          ~/.config/nvim/lua/
    # Fresh install only:
    cp nvim/lazy-lock.json ~/.config/nvim/lazy-lock.json
    cp nvim/lazyvim.json   ~/.config/nvim/lazyvim.json
    ```

3. **Add the cheatsheet alias** to `~/.zshrc`:

    ```bash
    echo "alias ct='python3 ~/purpleknight-setup/cheatsheet.py'" >> ~/.zshrc
    ```

4. **Launch AeroSpace** from `/Applications/AeroSpace.app` and grant Accessibility permission when prompted.

5. **Configure macOS:**
    - System Settings → Desktop & Dock → Mission Control → disable **"Displays have separate Spaces"** (requires logout).

6. **Install Android Studio** — install [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/), then use it to install Android Studio. AeroSpace routes it to workspace **A** automatically via app-id `com.google.android.studio`.

## Workspace Layout

| WS | Purpose | Auto-routed apps |
|----|---------|------------------|
| 1 | Browser | Chrome |
| 2 | Chat | Discord |
| 3 | Git UI | Sourcetree |
| 4 | Secrets | Bitwarden |
| 5 | AI | Claude desktop |
| 6 | Media | Spotify, WhatsApp |
| 7–9 | General-purpose | — |
| **T** | Terminal (Ghostty) | Ghostty |
| **V** | Editor (Kitty/LazyVim) | Kitty |
| **A** | Android Studio | Android Studio |

Workspaces **T**, **V**, and **A** are protected: any non-owning app that lands on them is forced to floating layout, so Ghostty / Kitty / Android Studio never tile against unrelated windows.

## Keybindings

### AeroSpace (⌥ Option)

| Shortcut | Action |
|----------|--------|
| `⌥ H J K L` | Focus window left / down / up / right |
| `⌥ ⇧ H J K L` | Move window left / down / up / right |
| `⌥ 1–9` | Switch to workspace 1–9 |
| `⌥ ⇧ 1–9` | Move focused window to workspace 1–9 |
| `⌥ T` / `⌥ V` / `⌥ A` | Switch to Ghostty / Kitty / Android Studio workspace (launches the app if it's not running) |
| `⌥ ⇧ T` / `⌥ ⇧ V` / `⌥ ⇧ A` | Move window to T / V / A |
| `⌥ Tab` / `⌥ ⇧ Tab` | Next / previous workspace (wraps) |
| `⌥ F` | Toggle fullscreen |
| `⌥ ⇧ F` | Toggle floating ⇄ tiling |
| `⌥ /` | Toggle tiles ⇄ accordion |
| `⌥ ,` | Toggle horizontal ⇄ vertical split |
| `⌥ ⇧ R` | Reset workspace (flatten + balance) |
| `⌥ -` / `⌥ =` | Shrink / grow focused window |
| `⌥ Q` | Close window |
| `⌥ M` | Focus other monitor |
| `⌥ ⇧ M` | Move focused window to other monitor |
| `⌥ ⌃ M` | Move entire workspace to other monitor |

### Ghostty (⌘ Cmd)

Run `ct` in any terminal for the full cheatsheet — Ghostty shortcuts, LazyVim navigation, and LazyVim debug/test/tools are all there, laid out as a responsive 4-column TUI.

### Keybinding allocation

- **⌥ (Option)** is reserved for AeroSpace window/workspace management.
- **⌘ (Cmd)** is reserved for Ghostty terminal shortcuts.
- Do not assign conflicting keys across these groups.

## Cheatsheet

```bash
ct
```

A Python `rich` TUI that adapts to the terminal width:

- 4-column grid at ≥ 160 cols
- 2×2 grid at ≥ 80 cols
- Stacked on narrower terminals

Covers AeroSpace, Ghostty, LazyVim Navigate & Code, and LazyVim Debug/Test/Tools. To change a shortcut: update BOTH the relevant config file AND `cheatsheet.py`.

## Architecture

- **AeroSpace** tiles every window by default; `on-window-detected` rules pin specific apps to their workspaces.
- **JankyBorders** paints a 5px purple border (`#c099ff`, from TokyoNight Moon) around the focused window; inactive windows have no border.
- **Ghostty** and **Kitty** are both TokyoNight Moon with brighter foreground (`#dce4ff`) for consistency.
- **Kitty** is configured with `shell nvim` — it boots straight into LazyVim, behaving like a native editor window.
- **Android Studio** is launched from the Toolbox-managed location at `~/Applications/Android Studio.app`.

## Uninstall

```bash
./uninstall.sh
```

Removes AeroSpace, Ghostty, Kitty configs and the `ct` alias. Optionally also uninstalls the brew packages. Neovim config/state is preserved by default (see the script's output for the manual purge command). Android Studio and JetBrains Toolbox are **not** touched.

## Known Limitations

- AeroSpace is in public beta (v0.20.3). `resize smart` can occasionally cause layout glitches — run `aerospace flatten-workspace-tree` (or `⌥ ⇧ R`) to reset.
- Apps enforce their own minimum window size; tiles cannot be resized below those constraints.

## License

Personal configuration. Not licensed for redistribution.
