return {
  {
    "folke/snacks.nvim",
    opts = {
      lazygit = { enabled = true },
      explorer = {
        replace_netrw = true,
      },
      picker = {
        sources = {
          explorer = {
            hidden = true,
            ignored = true,
          },
          projects = {
            -- Where to look for project directories
            dev = { "~/sartiq", "~/projects", "~/dev" },
            -- How to recognize a project root
            patterns = { ".git", "pyproject.toml", "package.json", "Makefile" },
            confirm = function(picker, item)
              picker:close()
              if item then
                -- Close all buffers
                vim.cmd("%bdelete!")
                -- Switch to project directory
                vim.cmd("tcd " .. vim.fn.fnameescape(item.file))
                -- Open explorer
                Snacks.explorer.open()
              end
            end,
          },
        },
      },
    },
    keys = {
      { "<leader>fp", function() Snacks.picker.projects() end, desc = "Projects" },
    },
  },
}
