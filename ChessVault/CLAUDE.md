# Project context for Claude Code

This folder is an Obsidian vault for learning chess, using Chess.com games.

## Structure
- `Games/`: one note per imported game (created by `import_chess.py`). Frontmatter fields: date, color, result, opening, ratings, opponent, time_control, url, `reviewed`.
- `Tactics/Mistake-Types.md`: running list of recurring mistakes, grouped by category, with links to game notes.
- `Tactics/Pre-Move-Checklist.md`: the five-question habit checklist.
- `Openings/Repertoire.md`: the player's opening repertoire and problem lines.
- `Plan.md`: training goals and routine.
- `Claude-Prompts.md`: ready-made prompts.
- `config.json`: saved Chess.com username (created by the import script).

## How to work here
- To import games run `python import_chess.py` (use `python3` on macOS/Linux).
- The player is a beginner. Explain in simple language, focus on one or two habits per game, avoid long variations and heavy theory.
- Do not calculate concrete variations from memory and present them as fact. Evaluations and best moves should come from Chess.com Game Review output or an engine. Your job is to explain the ideas and find patterns across games.
- When reviewing a game note: fill in the "Review" section, add a link to the game under the right category in `Tactics/Mistake-Types.md`, and set `reviewed: true`.
- Never edit the PGN inside the `chess` code block.
- Use standard relative markdown links (not wikilinks) so notes render on GitHub as well as in Obsidian.
