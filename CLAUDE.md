# purpleknight-setup

macOS desktop environment configuration: AeroSpace tiling window manager, JankyBorders, Ghostty terminal, and Kitty (LazyVim host).

## Project Structure

```
purpleknight-setup/
├── CLAUDE.md              # This file — project conventions and context
├── README.md              # Setup and usage documentation
├── install.sh             # Automated install script
├── uninstall.sh           # Automated uninstall script
├── cheatsheet.py          # Keyboard cheatsheet (TUI, runs in any terminal via `rich`)
├── aerospace/
│   └── aerospace.toml     # AeroSpace tiling WM config → deployed to ~/.aerospace.toml
├── ghostty/
│   └── config             # Ghostty terminal config → deployed to ~/.config/ghostty/config
├── kitty/
│   └── kitty.conf         # Kitty config (LazyVim host) → deployed to ~/.config/kitty/kitty.conf
└── nvim/                  # Neovim / LazyVim config → deployed to ~/.config/nvim/
```

## Key Decisions

### AeroSpace (v0.20.3-Beta)
- **Config version 2** — latest config format
- **Tiles layout by default** — not accordion
- **Workspace T** is reserved for Ghostty — non-Ghostty windows that open on T are forced to floating layout
- **Workspace V** is reserved for Kitty running LazyVim
- **Workspace A** is reserved for Android Studio (Toolbox-managed install at `~/Applications/Android Studio.app`)
- **JankyBorders** purple active border (`#c099ff` from TokyoNight Moon)
- **Normalizations enabled** — flatten containers and opposite orientation for nested containers
- **8px gaps** on all sides
- **Keybindings use `alt` (Option/⌥)** — no conflicts with Ghostty (⌘) or VimR

### Ghostty
- Theme: `TokyoNight Moon` (bundled) with brighter foreground override (`#dce4ff`)
- Font: JetBrains Mono, size 14
- Shell integration: zsh (auto-injected)
- Config at `~/.config/ghostty/config`

### Kitty (LazyVim host)
- Dedicated Kitty instance that launches nvim directly (`shell nvim` in config)
- TokyoNight Moon theme matching Ghostty, brighter foreground (`#dce4ff`)
- Separate app ID (`net.kovidgoyal.kitty`) for clean AeroSpace workspace routing
- Tab bar hidden, titlebar-only decorations removed — behaves as a pure nvim window
- Config at `~/.config/kitty/kitty.conf`

### Cheatsheet
- TUI cheatsheet rendered via Python `rich` library — run with `ct` alias or `python3 cheatsheet.py`
- 4 columns: AeroSpace, Ghostty, LazyVim Navigate & Code, LazyVim Debug/Test/Tools
- Adapts layout to terminal width (4-col at 160+, 2×2 at 80+, stacked on narrow)
- Shell alias `ct` defined in `~/.zshrc` (`alias ct='python3 ~/purpleknight-setup/cheatsheet.py'`)

### macOS Requirements
- "Displays have separate Spaces" must be **disabled** (System Settings → Desktop & Dock → Mission Control)
- AeroSpace requires **Accessibility** permission

## Conventions

### Config Changes
Configs live under version control in this repo and are **copied** into `~/` (not symlinked). After editing a source file, redeploy the specific one or re-run `./install.sh` (idempotent).

- **AeroSpace config**: Edit `aerospace/aerospace.toml`, copy to `~/.aerospace.toml`, run `aerospace reload-config`.
- **Ghostty config**: Edit `ghostty/config`, copy to `~/.config/ghostty/config`. Ghostty hot-reloads on save.
- **Kitty config**: Edit `kitty/kitty.conf`, copy to `~/.config/kitty/kitty.conf`. Kitty picks up changes on next launch.
- **Neovim (LazyVim)**: Edit files under `nvim/`, copy (or `cp -R`) into `~/.config/nvim/`. LazyVim picks up plugin changes on restart. `nvim/lazy-lock.json` and `nvim/lazyvim.json` are version-pinning manifests — commit them whenever plugin versions or LazyVim extras change.
- **Cheatsheet**: When adding/changing shortcuts, update BOTH the relevant config file AND `cheatsheet.py`.

### Keybinding Allocation
- **⌥ (Option)** — reserved for AeroSpace window/workspace management
- **⌘ (Cmd)** — reserved for Ghostty terminal shortcuts
- Do not assign conflicting keys across these groups

### Known Limitations
- AeroSpace is in beta — `resize smart` can occasionally cause layout glitches. Use `aerospace flatten-workspace-tree` to reset.
- Apps enforce their own minimum window size — tiles cannot be resized below app constraints.
