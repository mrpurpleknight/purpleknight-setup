-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua

local map = vim.keymap.set

-- Remove default Alt+j/k move-line maps (conflict with AeroSpace window focus)
vim.keymap.del({ "n", "i", "v" }, "<A-j>")
vim.keymap.del({ "n", "i", "v" }, "<A-k>")

-- Remap move line to Ctrl+Shift+j/k (Ctrl+j/k is taken by window navigation)
map("n", "<C-S-j>", "<cmd>execute 'move .+' . v:count1<cr>==", { desc = "Move Line Down" })
map("n", "<C-S-k>", "<cmd>execute 'move .-' . (1 + v:count1)<cr>==", { desc = "Move Line Up" })
map("i", "<C-S-j>", "<esc><cmd>m .+1<cr>==gi", { desc = "Move Line Down" })
map("i", "<C-S-k>", "<esc><cmd>m .-2<cr>==gi", { desc = "Move Line Up" })
map("v", "<C-S-j>", ":<C-u>execute \"'<,'>move '>+\" . v:count1<cr>gv=gv", { desc = "Move Line Down" })
map("v", "<C-S-k>", ":<C-u>execute \"'<,'>move '<-\" . (1 + v:count1)<cr>gv=gv", { desc = "Move Line Up" })
