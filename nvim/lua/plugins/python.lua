return {
  -- Python venv selector — pick the right interpreter per project
  {
    "linux-cultist/venv-selector.nvim",
    branch = "regexp",
    dependencies = { "neovim/nvim-lspconfig" },
    ft = "python",
    opts = {
      settings = {
        search = {
          -- Only search the current project directory
          project_venvs = {
            command = "fd -H -t d -a --max-depth 1 '(^\\.venv$|^venv$)' $CWD",
          },
          -- Disable all other default search locations
          hatch = false,
          pipenv = false,
          poetry = false,
          pyenv = false,
          anaconda_base = false,
          anaconda_envs = false,
          anaconda = false,
          venvs = false,
          workspace = false,
        },
      },
    },
    keys = {
      { "<leader>cv", "<cmd>VenvSelect<cr>", desc = "Select Python Venv", ft = "python" },
    },
  },

  -- Ensure pyright checks common venv folder names
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        pyright = {
          settings = {
            python = {
              venvPath = ".",
              venv = ".venv",
            },
          },
        },
      },
    },
  },
}
