# Prompts for Claude

> Important: take evaluations and best moves from Chess.com Game Review or Stockfish. Claude is good at explaining ideas and spotting patterns, but it can make mistakes when calculating concrete variations.

## Review a single game
```
I play at around [YOUR RATING] on Chess.com. Here is the PGN of my game and the
Game Review results (mistakes and blunders with move numbers): [paste].
Explain in simple language why each mistake was a mistake, which thinking habit
it shows, and give me one rule I can apply in my next game.
Do not suggest complex theory.
```

## Weekly review (after importing games)
```
Read the notes in Games/ with reviewed: false. Find:
1. The most frequent types of mistakes (use Tactics/Mistake-Types.md)
2. Openings where I lose most often
3. Time trouble, if visible from the time control
Then write a plan for the week: 3 puzzle themes, 1 opening line, 1 endgame topic.
Mark the notes you reviewed with reviewed: true and update Tactics/Mistake-Types.md.
```

## Learn an opening
```
Explain the ideas of the London System as White at my level: where to put the
pieces, typical plans and common opponent mistakes. No long variations, only
ideas and 3-5 main moves.
```

## One-step workflow with Claude Code
```
Run python import_chess.py, then read the new notes in Games/ with reviewed: false
and do the weekly review. Update Tactics/Mistake-Types.md.
```
