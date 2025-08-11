### **Chess Bot – AI-Powered Competitive Chess Engine**  

#### **Project Overview**  
This project is a **competitive chess bot** implemented in Python using **Pygame**. It supports key chess mechanics and integrates **AI-based decision-making** using the **Minimax algorithm with Alpha-Beta Pruning and Quiescence Search** to play strategically at different difficulty levels.  

---

### **Features**  
✅ **Complete Chess Mechanics** – Implements legal move generation, check, checkmate, stalemate detection, castling, pawn promotion, and move undoing.  
✅ **AI-Powered Opponent** – Uses **Minimax with Alpha-Beta Pruning** for efficient decision-making.  
✅ **Move Evaluation & Ordering** – Prioritizes captures and strong positional moves using an **advanced evaluation function**.  
✅ **Quiescence Search** – Extends search depth for tactical positions to prevent the **horizon effect**.  
✅ **Interactive GUI** – Built with **Pygame**, allowing users to play against the AI in a visually engaging chessboard interface.  
✅ **Multiple AI Difficulty Levels** – Depth-based AI difficulty selection for challenging gameplay.  

---

### **Tech Stack**  
- **Python** – Core programming language  
- **Pygame** – GUI and chessboard visualization  
- **Minimax Algorithm** – AI decision-making  
- **Alpha-Beta Pruning** – Optimized search performance  
- **Quiescence Search** – Tactical move extension  

---

### **How It Works**  
1. **Move Generation** – The bot generates all legal moves for the current board state.  
2. **AI Decision-Making** – The **Minimax algorithm** evaluates future moves, applying **Alpha-Beta pruning** to speed up search.  
3. **Evaluation Function** – Considers piece value, mobility, threats, and positional advantages.  
4. **Move Execution** – The best move is selected, and the game updates accordingly.  

---

### **Installation & Setup**  
#### **Prerequisites**  
Ensure Python is installed. Install required dependencies using:  
```bash
pip install pygame
```

#### **Run the Chess Bot**  
Clone the repository and execute the main script:  
```bash
git clone https://github.com/your-username/chess-bot.git
cd chess-bot
python main.py
```

---

### **Future Improvements**  
🔹 **Deep Learning Integration** – Train a neural network for move prediction.  
🔹 **Enhanced Heuristic Evaluation** – Incorporate **piece-square tables** and **positional advantages** for stronger play.  
🔹 **Multiplayer Mode** – Enable online play against other users.  

---

### **Contributors**  
- **Mayank Kumar Rajput** – AI Implementation, Game Logic, GUI Development  

---

### **License**  
This project is open-source under the **MIT License**.  

---

🚀
