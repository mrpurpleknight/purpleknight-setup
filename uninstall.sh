#!/bin/bash
set -e

echo "=== purpleknight-setup uninstall ==="
echo ""

read -p "Remove AeroSpace, JankyBorders, Ghostty, Kitty configs and the 'ct' alias? (y/N) " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Aborted."
    exit 0
fi

# --- 1. Stop services ---
echo "[1/4] Stopping services..."
pkill borders   2>/dev/null || true
pkill AeroSpace 2>/dev/null || true

# --- 2. Remove configs ---
echo "[2/4] Removing configs..."
rm -f ~/.aerospace.toml
rm -f ~/.config/ghostty/config
rm -f ~/.config/kitty/kitty.conf
rmdir ~/.config/ghostty ~/.config/kitty 2>/dev/null || true

echo ""
echo "  Neovim (LazyVim) config and state are NOT removed automatically —"
echo "  they hold user plugin state and caches. To purge manually:"
echo "    rm -rf ~/.config/nvim ~/.local/share/nvim ~/.local/state/nvim ~/.cache/nvim"
echo ""

# --- 3. Remove ct alias ---
echo "[3/4] Removing 'ct' alias from ~/.zshrc..."
if [ -f "$HOME/.zshrc" ] && grep -Fq "alias ct=" "$HOME/.zshrc"; then
    # Also strip the preceding "# purpleknight-setup cheatsheet" marker line
    sed -i '' -e "/# purpleknight-setup cheatsheet/d" -e "/^alias ct='python3 ~\/purpleknight-setup\/cheatsheet\.py'$/d" "$HOME/.zshrc"
    echo "  Removed."
else
    echo "  Alias not found, skipping."
fi

# --- 4. Uninstall brew packages (optional) ---
echo "[4/4] Uninstall brew packages?"
read -p "Also uninstall AeroSpace, JankyBorders, Ghostty, Kitty via brew? (y/N) " brewconfirm
if [[ "$brewconfirm" == "y" || "$brewconfirm" == "Y" ]]; then
    brew uninstall --cask nikitabobko/tap/aerospace 2>/dev/null || true
    brew uninstall FelixKratz/formulae/borders      2>/dev/null || true
    brew uninstall --cask ghostty                   2>/dev/null || true
    brew uninstall --cask kitty                     2>/dev/null || true
else
    echo "  Skipped — brew packages remain installed."
fi

echo ""
echo "=== Uninstall complete ==="
echo ""
echo "Manual steps:"
echo "  1. Remove AeroSpace from System Settings > Privacy & Security > Accessibility."
echo "  2. Android Studio and JetBrains Toolbox were NOT touched (managed externally)."
echo "  3. Reload your shell (source ~/.zshrc) or open a new terminal to drop the 'ct' alias."
echo ""
