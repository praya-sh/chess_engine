# ChessAI
**Lightweight Python Chess Engine with Negabeta Pruning**

ChessAI is a local chess engine built in Python using Pygame for the user interface.  
It features a custom evaluation function and an optimized negabeta pruning search algorithm for faster move generation and decision-making.

---

## Features
- **Custom Chess Engine** – Implements all standard chess rules.
- **Negabeta Pruning** – Optimized alpha-beta pruning for efficient decision-making.
- **Heuristic Evaluation Function** – Balances piece values, mobility, and positional advantage.
- **Pygame UI** – Clean, interactive board with real-time move highlighting.
- **Local Play** – Play against the AI without an internet connection.

---

## 🛠Tech Stack
- **Languages:** Python  
- **Libraries:** Pygame  
- **Algorithms:** Negabeta pruning, heuristic evaluation  
- **Platform:** Cross-platform (Windows/Linux/Mac)  

---

## How It Works
1. **Board Setup** – Standard chessboard is initialized.  
2. **Move Generation** – AI generates all possible legal moves.  
3. **Evaluation** – Each move is scored using the heuristic function.  
4. **Search Optimization** – Negabeta pruning eliminates suboptimal branches.  
5. **Move Execution** – AI selects the best move and updates the board.

---

## 🖥️ Installation & Setup
```bash
# Clone the repository

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
