import openai
import chess 
import chess.engine

openai.api_key = "API KEY"

STOCKFISH_PATH = r"C:\Users\Sahil Sahu\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
fen = "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"

your_move = "Nf3"
board = chess.Board(fen)
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

result = engine.analyse(board, chess.engine.Limit(time=1.0))
best_move = result["pv"][0].uci()
engine.quit()

prompt = f"""
You are a chess coach.

The current board position is represented by this FEN: {fen}

The player is considering the move: {your_move}
Stockfish recommends the move: {best_move}

Please compare the two moves and explain:
- What each move aims to achieve
- Which is stronger and why
- Any tactical or positional implications
- Short and long-term consequences of each move
"""

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)
print("\n GPT's Analysis:\n")
print(response["choices"][0]["message"]["content"])
