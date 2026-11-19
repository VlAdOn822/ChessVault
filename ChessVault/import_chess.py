#!/usr/bin/env python3
"""Import your Chess.com games into this Obsidian vault as markdown notes.

Usage (run from the vault folder):
    python import_chess.py --username YourChessComName     # first run, saves the name
    python import_chess.py                                 # later runs, uses saved name
    python import_chess.py --months 6                      # last 6 months instead of 2

Uses the public Chess.com API (no API key needed). Games that were already
imported are skipped, so it is safe to run repeatedly.
On macOS/Linux use `python3` instead of `python`.
"""
import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

VAULT = Path(__file__).resolve().parent
GAMES_DIR = VAULT / "Games"
CONFIG = VAULT / "config.json"

# Chess.com result codes that count as a draw.
DRAW = {"agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"}


def get_json(url, username):
    # Chess.com asks API users to identify themselves in the User-Agent.
    headers = {"User-Agent": f"obsidian-chess-vault (username: {username})"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def pgn_header(pgn, tag):
    m = re.search(rf'\[{tag} "([^"]*)"\]', pgn)
    return m.group(1) if m else ""


def opening_name(pgn):
    url = pgn_header(pgn, "ECOUrl")
    if not url:
        return "Unknown opening"
    slug = url.rstrip("/").split("/")[-1]
    # Drop trailing move sequences such as "-3.Nf3-Nc6".
    slug = re.split(r"-\d+\.", slug)[0]
    return slug.replace("-", " ")


def result_of(game, username):
    me_white = game["white"]["username"].lower() == username.lower()
    mine = game["white" if me_white else "black"]["result"]
    if mine == "win":
        return "win", me_white
    if mine in DRAW:
        return "draw", me_white
    return "loss", me_white


def game_id(game):
    return game["url"].rstrip("/").split("/")[-1]


def already_imported(gid):
    return any(p.name.endswith(f"_{gid}.md") for p in GAMES_DIR.glob("*.md"))


def make_note(game, username):
    res, me_white = result_of(game, username)
    me = game["white" if me_white else "black"]
    opp = game["black" if me_white else "white"]
    pgn = game.get("pgn", "")
    date = datetime.fromtimestamp(game["end_time"], tz=timezone.utc).strftime("%Y-%m-%d")
    gid = game_id(game)
    opening = opening_name(pgn)
    fname = f"{date}_{res}_{opp['username']}_{gid}.md"
    body = f"""---
type: game
date: {date}
color: {"white" if me_white else "black"}
result: {res}
opening: "{opening}"
my_rating: {me.get("rating", "")}
opp_rating: {opp.get("rating", "")}
opponent: {opp["username"]}
time_control: {game.get("time_control", "")}
url: {game["url"]}
reviewed: false
---

# {date}: {opening} ({res})

[Open on Chess.com]({game["url"]})

## Game
```chess
{pgn.strip()}
```

## Review (fill in after Chess.com Game Review)
- **Key moment (move number):**
- **What I played / what was better:**
- **Mistake type:** [Mistake Types](../Tactics/Mistake-Types.md)
- **One-sentence lesson:**

## Questions for Claude
"""
    return fname, body


def resolve_username(arg):
    """Use --username if given (and remember it), else the saved one."""
    if arg:
        CONFIG.write_text(json.dumps({"username": arg}), encoding="utf-8")
        return arg
    if CONFIG.exists():
        name = json.loads(CONFIG.read_text(encoding="utf-8")).get("username")
        if name:
            return name
    sys.exit("No username saved yet. Run: python import_chess.py --username YourChessComName")


def main():
    ap = argparse.ArgumentParser(description="Import Chess.com games into this vault.")
    ap.add_argument("--username", help="your Chess.com username (saved to config.json)")
    ap.add_argument("--months", type=int, default=2, help="how many recent months to fetch (default 2)")
    args = ap.parse_args()

    username = resolve_username(args.username)
    GAMES_DIR.mkdir(exist_ok=True)

    try:
        archives = get_json(
            f"https://api.chess.com/pub/player/{username.lower()}/games/archives", username
        )["archives"]
    except Exception as e:
        sys.exit(f"Could not fetch the archive list for '{username}': {e}")

    new = 0
    for url in archives[-args.months:]:
        try:
            games = get_json(url, username)["games"]
        except Exception as e:
            print(f"Skipping {url}: {e}")
            continue
        for g in games:
            if g.get("rules") != "chess" or "pgn" not in g:
                continue  # skip variants (chess960, etc.) and games without PGN
            if already_imported(game_id(g)):
                continue
            fname, body = make_note(g, username)
            (GAMES_DIR / fname).write_text(body, encoding="utf-8")
            new += 1
    print(f"Done. New games imported: {new}")


if __name__ == "__main__":
    main()
