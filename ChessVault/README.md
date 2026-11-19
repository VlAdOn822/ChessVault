# Chess Vault: learn chess with Chess.com, Obsidian and Claude

An Obsidian vault (a folder of markdown notes) for improving at chess:

- **Chess.com** is where you play and get the engine's Game Review.
- **Obsidian** stores your games, mistakes, openings and plan, and shows games on an interactive board (Caissa plugin).
- **Claude Code** runs in the vault folder, imports your games, reads your notes, explains your mistakes and finds patterns.

The workflow was built for a beginner (about 600 rating), but it works at any level.

## What is in the vault

| Path | Purpose |
|------|---------|
| `import_chess.py` | Downloads your recent Chess.com games and creates one note per game in `Games/` |
| `Games/` | One note per game, with an interactive board and a review section |
| `Tactics/Pre-Move-Checklist.md` | Five questions to ask before every move |
| `Tactics/Mistake-Types.md` | Running list of your recurring mistakes |
| `Openings/Repertoire.md` | A simple opening repertoire and your problem lines |
| `Plan.md` | Training goals and weekly routine |
| `Claude-Prompts.md` | Ready-made prompts for Claude |
| `CLAUDE.md` | Context file that tells Claude Code how this project works |
| `config.json` | Created on first import, stores your Chess.com username (not committed to git) |

## Requirements

- A **Chess.com** account (free) and your username
- **Python 3** (free)
- **Obsidian** (free)
- A **Claude** subscription: Pro, Max, Team or Enterprise, or a Console (API) account. The free claude.ai plan does not include Claude Code.
- Windows 10 (version 1809 or newer), macOS or Linux, with an internet connection

The detailed steps below are written for Windows. macOS and Linux differences are noted.

---

## Step-by-step setup

### Step 1. Get the project

Option A (no git): on GitHub click **Code → Download ZIP**, then extract it. You get a folder called `ChessVault` (or the repository name).

Option B (git):
```
git clone https://github.com/YOUR-USER/YOUR-REPO.git ChessVault
```

Remember where the folder is. In this guide it is called "the vault folder".

> If you extracted a ZIP and see folders with garbled names, re-extract with 7-Zip or Windows Explorer into a new empty folder.

### Step 2. Install Python

1. Download Python 3 from <https://www.python.org/downloads/>.
2. Run the installer. **Tick "Add Python to PATH"** on the first screen, then click Install.
3. Open a new terminal and check:
   ```
   python --version
   ```
   You should see something like `Python 3.12.x`. On macOS/Linux use `python3 --version`.

The import script uses only Python's standard library, so there is nothing else to install.

### Step 3. Install Obsidian and open the vault

1. Download Obsidian from <https://obsidian.md> and install it.
2. Start Obsidian, choose **Open folder as vault**, and select the vault folder from Step 1.
3. If Obsidian asks whether you trust the author, you can choose to trust in order to enable community plugins.

### Step 4. Install the Obsidian plugins

1. Open **Settings → Community plugins**.
2. If you see "Restricted mode", click **Turn on community plugins**.
3. Click **Browse** and install and **Enable** these plugins:
   - **Caissa**: shows chess games on an interactive board inside notes (required for the board).
   - **Terminal**: lets you open a terminal inside Obsidian (needed to run Claude Code in the same window).
   - **Dataview** (optional): lets you build summary tables, for example results per opening.

### Step 5. Install Claude Code

Claude Code is Anthropic's command-line coding assistant. Here it works as your chess coach that can read and edit the notes.

Open **PowerShell** (Start menu, type `PowerShell`; no administrator rights needed) and run:

```
irm https://claude.ai/install.ps1 | iex
```

Important details:

- `irm` works **only in PowerShell**. A PowerShell prompt starts with `PS C:\...>`. In classic CMD (prompt `C:\...>`) you will get "irm is not recognized". In CMD use the CMD installer from the official page instead.
- macOS/Linux: see the official instructions at <https://code.claude.com/docs/en/setup>. Commands may change, so always check that page.
- When it finishes, the installer prints the install location (on Windows, `C:\Users\<you>\.local\bin\claude.exe`).

### Step 6. Fix PATH if `claude` is not found

If the installer warns that the folder is not in your PATH, or `claude` says "not recognized":

1. Run this in PowerShell (replace the path with the one the installer printed):
   ```
   [Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path","User") + ";C:\Users\<you>\.local\bin", "User")
   ```
   Or use the interface: Start menu → "Edit environment variables for your account" → select `Path` → Edit → New → paste the folder path → OK.
2. **Close the terminal completely and open a new one.** PATH changes apply only to new windows.
3. Verify:
   ```
   claude --version
   ```
   It should print a version number. `claude doctor` runs a more detailed health check.

You can always run Claude by its full path, for example `C:\Users\<you>\.local\bin\claude.exe`.

### Step 7. Open a terminal inside Obsidian

1. In Obsidian press `Ctrl+P` (Command palette) and type `Terminal`.
2. Choose the command that opens a terminal (the exact name depends on the plugin version). A terminal opens in the vault folder.
3. If it opens CMD and you prefer PowerShell, change the shell in **Settings → Terminal**.
4. Type `claude --version` to confirm it is found.

**If `claude` is not found inside Obsidian** even though it works elsewhere: Obsidian reads PATH only when it starts. **Quit Obsidian completely** (also close it from the system tray near the clock) and start it again. Or run Claude by its full path.

Alternative without the plugin: in File Explorer open the vault folder, click the address bar, type `powershell` and press Enter. A terminal opens in that folder.

### Step 8. Log in to Claude Code

1. In the terminal (inside the vault folder) run:
   ```
   claude
   ```
2. A browser window opens. Sign in with your Claude account (Pro, Max, Team, Enterprise or Console).
3. Back in the terminal, accept the prompts. If asked whether to trust the folder, choose yes.

Claude Code asks permission before editing files or running commands. Approve actions one at a time until you are comfortable.

### Step 9. Import your Chess.com games

In the terminal, in the vault folder, run (use your own Chess.com username):

```
python import_chess.py --username YourChessComName --months 3
```

- The username is saved in `config.json`, so next time just run `python import_chess.py`.
- `--months 3` fetches the last 3 months. The default is 2.
- New notes appear in the `Games/` folder. Games that are already imported are skipped.
- macOS/Linux: use `python3`.

### Step 10. View a game on the board

Open any note in `Games/`. Thanks to the Caissa plugin, the `chess` code block is shown as an interactive board you can step through with the arrow buttons.

Useful Caissa blocks you can add to your own notes:

````
```chess
fen: r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3
arrows: f3e5
highlights: e5 f7-red
```
````

- `fen:` shows any position, `arrows:` and `highlights:` mark threats and ideas.
- `opening: Italian Game` shows an opening from Caissa's library.
- `play: white` with `level: 3` lets you play against Stockfish.
- Command palette (`Ctrl+P`) has "Insert chess game from PGN" and others.

### Step 11. Use Claude as your coach

In the terminal inside the vault folder, run `claude` and give it a task. Example:

```
Run python import_chess.py, then read the new notes in Games/ with reviewed: false
and do the weekly review. Update Tactics/Mistake-Types.md.
```

Claude reads `CLAUDE.md` automatically, so it knows the structure and rules of this vault. More prompts are in [Claude-Prompts.md](Claude-Prompts.md).

**Important:** let Chess.com Game Review (or Stockfish) provide the evaluations and best moves. Claude is great at explaining why a mistake happened and finding patterns across games, but it can be wrong when calculating variations itself.

---

## Suggested weekly routine

1. Play 5-10 games (10+0 or 15+10 is a good time control to start).
2. Import: `python import_chess.py`
3. Run Chess.com **Game Review** on your losses and note the key mistakes.
4. In Claude Code run the weekly review prompt.
5. Read the updated [Mistake Types](Tactics/Mistake-Types.md) and pick next week's puzzle themes.
6. Do 15-20 puzzles daily on the weakest theme.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `irm is not recognized` | You are in CMD. Open PowerShell (prompt starts with `PS`). |
| `claude is not recognized` | Fix PATH (Step 6), then open a **new** terminal. In Obsidian, fully restart the app. Or use the full path to `claude.exe`. |
| `python is not recognized` | Reinstall Python with "Add Python to PATH" ticked, or on macOS/Linux use `python3`. |
| `No username saved yet` | Run `python import_chess.py --username YourChessComName` once. |
| `Could not fetch the archive list` | Check the username spelling and your internet connection. Corporate networks or VPNs may block `api.chess.com`. |
| The board does not show | Make sure the Caissa plugin is installed **and enabled**, and that the block starts with three backticks followed by `chess`. |
| Garbled folder names after unzipping | Extract with 7-Zip into a new empty folder. |
| Claude Code asks for login every time | Run `claude` from a normal terminal, finish the browser login, and make sure you have a paid plan or a Console account. |

## Publishing your own copy to GitHub

The included `.gitignore` keeps personal data out of the repository (`config.json`, imported game notes, `.obsidian/` and `.claude/`).

```
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USER/YOUR-REPO.git
git push -u origin main
```

## License

MIT, see [LICENSE](LICENSE).
