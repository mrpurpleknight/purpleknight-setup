#!/bin/bash
set -e

echo "=== purpleknight-setup ==="
echo ""

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

# --- 1. Dependencies ---
echo "[1/5] Installing dependencies via Homebrew..."

if ! command -v brew &>/dev/null; then
    echo "Error: Homebrew is required. Install from https://brew.sh"
    exit 1
fi

brew install --cask nikitabobko/tap/aerospace 2>/dev/null || echo "  AeroSpace already installed"
brew install FelixKratz/formulae/borders     2>/dev/null || echo "  JankyBorders already installed"
brew install --cask ghostty                  2>/dev/null || echo "  Ghostty already installed"
brew install --cask kitty                    2>/dev/null || echo "  Kitty already installed"

# Python `rich` powers the TUI cheatsheet
if ! python3 -c "import rich" 2>/dev/null; then
    echo "  Installing Python rich..."
    python3 -m pip install --user --break-system-packages rich
else
    echo "  Python rich already installed"
fi

echo ""
echo "  NOTE: Android Studio is NOT auto-installed."
echo "        Install JetBrains Toolbox, then install Android Studio through it."
echo "        AeroSpace routes it to workspace A via app-id 'com.google.android.studio'."
echo ""

# --- 2. AeroSpace ---
echo "[2/5] Deploying AeroSpace config..."
cp aerospace/aerospace.toml ~/.aerospace.toml

# --- 3. Terminals ---
echo "[3/5] Deploying Ghostty and Kitty configs..."
mkdir -p ~/.config/ghostty ~/.config/kitty
cp ghostty/config   ~/.config/ghostty/config
cp kitty/kitty.conf ~/.config/kitty/kitty.conf

# --- 4. Neovim / LazyVim ---
echo "[4/5] Deploying Neovim (LazyVim) config..."
mkdir -p ~/.config/nvim/lua/plugins
cp    nvim/init.lua       ~/.config/nvim/init.lua
cp    nvim/.neoconf.json  ~/.config/nvim/.neoconf.json
cp    nvim/stylua.toml    ~/.config/nvim/stylua.toml
cp -R nvim/lua/           ~/.config/nvim/lua/

# Seed version pins only on a fresh install — never stomp an existing lockfile,
# since LazyVim manages it at runtime.
[ -f ~/.config/nvim/lazy-lock.json ] || cp nvim/lazy-lock.json ~/.config/nvim/lazy-lock.json
[ -f ~/.config/nvim/lazyvim.json   ] || cp nvim/lazyvim.json   ~/.config/nvim/lazyvim.json

# --- 5. Shell alias + post-install ---
echo "[5/5] Shell alias + post-install..."

ZSHRC="$HOME/.zshrc"
touch "$ZSHRC"
if ! grep -Fq "alias ct=" "$ZSHRC"; then
    printf "\n# purpleknight-setup cheatsheet\nalias ct='python3 ~/purpleknight-setup/cheatsheet.py'\n" >> "$ZSHRC"
    echo "  Added 'ct' alias to ~/.zshrc"
else
    echo "  'ct' alias already present in ~/.zshrc"
fi

if pgrep -q AeroSpace; then
    aerospace reload-config
    echo "  AeroSpace config reloaded"
else
    echo "  Start AeroSpace from /Applications/AeroSpace.app"
fi

echo ""
echo "=== Setup complete ==="
echo ""
echo "Manual steps:"
echo "  1. Grant AeroSpace Accessibility permission (System Settings > Privacy & Security > Accessibility)."
echo "  2. Disable 'Displays have separate Spaces' (System Settings > Desktop & Dock > Mission Control)."
echo "     Requires logout to take effect."
echo "  3. Install JetBrains Toolbox and Android Studio (needed for workspace A)."
echo "  4. Reload your shell:  source ~/.zshrc   (or open a new terminal)"
echo "  5. Run 'ct' to see the keyboard cheatsheet."
echo ""
