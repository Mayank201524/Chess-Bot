# group1.py
import random
from copy import deepcopy
import time
import math

from components.GuiHandler import GREY, PURPLE  # Ensure PURPLE is imported as well

def group1(self, board):
    """
    Implements the AI's move selection using the minimax algorithm with the advanced evaluation function
    and quiescence search for tactical positions.
    """
    start_time = time.time()
    depth = 3  # Adjust based on performance requirements
    best_score = float('-inf')
    best_move = None
    best_choice = None
    possible_moves = self.getPossibleMoves(board)
    
    if not possible_moves:
        self.game.end_turn()
        return
    
    # Order moves to prioritize captures and promotions with advanced weighting
    ordered_moves = order_moves(possible_moves, board, self.color)
    
    for move in ordered_moves:
        for choice in move[2]:
            new_board = deepcopy(board)
            # Simulate the move
            self.moveOnBoard(new_board, (move[0], move[1]), choice)
            # Call minimax with alpha-beta pruning and quiescence search
            score = minimax(self, new_board, depth - 1, False, float('-inf'), float('inf'), self.opponent_color, start_time)
            if score > best_score:
                best_score = score
                best_move = move
                best_choice = choice
            # Time check to ensure responsiveness
            if time.time() - start_time > 19:
                print("Time limit reached during move selection.")
                break
        if time.time() - start_time > 19:
            break
    return best_move, best_choice

def minimax(self, board, depth, maximizingPlayer, alpha, beta, current_color, start_time):
    """
    Minimax algorithm with alpha-beta pruning and quiescence search.
    """
    # Time constraint check
    if time.time() - start_time > 19:
        print("Time limit reached in minimax.")
        return advanced_evaluate(self, board)
    
    if depth == 0:
        return quiescence_search(self, board, alpha, beta, maximizingPlayer, start_time)

    if isGameOver(self, board, current_color):
        return advanced_evaluate(self, board)
    
    if maximizingPlayer:
        maxEval = float('-inf')
        possible_moves = getPossibleMovesForColor(self, board, current_color)
        # Order moves within minimax as well
        ordered_moves = order_moves(possible_moves, board, current_color)
        for move in ordered_moves:
            for choice in move[2]:
                new_board = deepcopy(board)
                self.moveOnBoard(new_board, (move[0], move[1]), choice)
                eval = minimax(self, new_board, depth - 1, False, alpha, beta, self.opponent_color, start_time)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    print(f"Beta cut-off at move {move} with choice {choice}.")
                    break  # Beta cut-off
            # Time check within loop
            if time.time() - start_time > 19:
                print("Time limit reached during maximizingPlayer loop.")
                break
        return maxEval
    else:
        minEval = float('inf')
        possible_moves = getPossibleMovesForColor(self, board, current_color)
        # Order moves within minimax as well
        ordered_moves = order_moves(possible_moves, board, current_color)
        for move in ordered_moves:
            for choice in move[2]:
                new_board = deepcopy(board)
                self.moveOnBoard(new_board, (move[0], move[1]), choice)
                eval = minimax(self, new_board, depth - 1, True, alpha, beta, self.color, start_time)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    print(f"Alpha cut-off at move {move} with choice {choice}.")
                    break  # Alpha cut-off
            # Time check within loop
            if time.time() - start_time > 19:
                print("Time limit reached during minimizingPlayer loop.")
                break
        return minEval

def quiescence_search(self, board, alpha, beta, maximizingPlayer, start_time):
    """
    Quiescence search to extend the search in "noisy" positions where captures are available.
    This prevents horizon effects by continuing to search tactical sequences.
    """
    stand_pat = advanced_evaluate(self, board)
    
    # If we can't beat alpha, return immediately (pruning).
    if maximizingPlayer:
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)
    else:
        if stand_pat <= alpha:
            return alpha
        beta = min(beta, stand_pat)

    # Get possible capture moves only (or moves that significantly change material balance).
    capture_moves = get_capture_moves(self, board, self.color if maximizingPlayer else self.opponent_color)

    for move in capture_moves:
        for choice in move[2]:
            new_board = deepcopy(board)
            self.moveOnBoard(new_board, (move[0], move[1]), choice)
            score = quiescence_search(self, new_board, alpha, beta, not maximizingPlayer, start_time)
            if maximizingPlayer:
                alpha = max(alpha, score)
                if alpha >= beta:
                    return beta  # Beta cut-off
            else:
                beta = min(beta, score)
                if beta <= alpha:
                    return alpha  # Alpha cut-off

    return alpha if maximizingPlayer else beta

def advanced_evaluate(self, board):
    """
    Advanced evaluation function considering multiple factors:
    - Piece Count
    - King Pieces
    - Piece Positioning
    - Mobility
    - Threats and Safe Zones
    - Endgame Considerations
    """
    try:
        score = 0
        player_pieces, opponent_pieces = self.allPiecesLocation(board)
        
        # Piece Count
        player_piece_count = len(player_pieces)
        opponent_piece_count = len(opponent_pieces)
        score += (player_piece_count - opponent_piece_count) * 1.0
        
        # King Pieces
        player_kings = sum(1 for piece in player_pieces if get_piece_king_status(board, piece))
        opponent_kings = sum(1 for piece in opponent_pieces if get_piece_king_status(board, piece))
        score += (player_kings - opponent_kings) * 2.0  # Kings are worth 2 points each
        
        # Piece Positioning and Advancement
        for piece in player_pieces:
            x, y = piece
            if self.color == GREY:
                score += y * 0.15  # Encourage advancing forward for GREY
            else:
                score += (7 - y) * 0.15  # Encourage advancing forward for PURPLE
            if 2 <= x <= 5:
                score += 0.5  # Bonus for controlling the center squares
        
        for piece in opponent_pieces:
            x, y = piece
            if self.opponent_color == GREY:
                score -= y * 0.15
            else:
                score -= (7 - y) * 0.15
            if 2 <= x <= 5:
                score -= 0.5
        
        # Mobility (number of possible moves)
        player_mobility = len(self.getPossibleMoves(board))
        opponent_mobility = 0
        for move in getPossibleMovesForColor(self, board, self.opponent_color):
            opponent_mobility += len(move[2])
        score += (player_mobility - opponent_mobility) * 0.1  # Weight for mobility
        
        # Threats (pieces that can be captured)
        for piece in player_pieces:
            if is_piece_threatened(self, board, piece, self.color):
                score -= 1.0  # Penalize for threatened pieces
        for piece in opponent_pieces:
            if is_piece_threatened(self, board, piece, self.opponent_color):
                score += 1.0  # Reward for threatening opponent pieces
        
        # Safe Zones (edges or protected positions)
        for piece in player_pieces:
            if is_piece_in_safe_zone(piece):
                score += 0.5  # Bonus for safe positions
        for piece in opponent_pieces:
            if is_piece_in_safe_zone(piece):
                score -= 0.5
        
        # Endgame Considerations
        total_pieces = player_piece_count + opponent_piece_count
        if total_pieces <= 6:  # Few pieces left on board
            score += (player_kings - opponent_kings) * 3.0  # Kings become even more valuable
            score += (player_mobility - opponent_mobility) * 0.2  # Mobility is critical in the endgame
        
        return score
    except Exception as e:
        print(f"Error in advanced_evaluate: {e}")
        return 0  # Neutral evaluation on error

def get_piece_king_status(board, piece):
    """
    Helper function to safely get the king status of a piece.
    """
    try:
        square = board.getSquare(piece[0], piece[1])
        if square and square.squarePiece:
            return square.squarePiece.king
        else:
            return False
    except Exception as e:
        print(f"Error in get_piece_king_status: {e}")
        return False

def is_piece_threatened(self, board, piece, color):
    """
    Determines if a piece is threatened (can be captured by the opponent).
    """
    try:
        x, y = piece
        opponent_color = GREY if color == PURPLE else PURPLE
        opponent_moves = getPossibleMovesForColor(self, board, opponent_color)
        for move in opponent_moves:
            from_x, from_y, to_positions = move
            for to_pos in to_positions:
                to_x, to_y = to_pos
                # Check if the move is a capture that lands on the piece's position
                if abs(to_x - from_x) > 1 or abs(to_y - from_y) > 1:
                    # Calculate the landing position after capture
                    landing_x = to_x + (to_x - from_x)
                    landing_y = to_y + (to_y - from_y)
                    if landing_x == x and landing_y == y:
                        return True
        return False
    except Exception as e:
        print(f"Error in is_piece_threatened: {e}")
        return False

def is_piece_in_safe_zone(piece):
    """
    Checks if a piece is in a safe zone (e.g., edges of the board).
    """
    try:
        x, y = piece
        return x == 0 or x == 7 or y == 0 or y == 7  # Edges are safer
    except Exception as e:
        print(f"Error in is_piece_in_safe_zone: {e}")
        return False

def getPossibleMovesForColor(self, board, color):
    """
    Retrieves all possible moves for a given color.
    """
    possible_moves = []
    for i in range(8):
        for j in range(8):
            square = board.getSquare(i, j)
            if square.squarePiece and square.squarePiece.color == color:
                legal_moves = board.get_valid_legal_moves(i, j, self.game.continue_playing)
                if legal_moves:
                    possible_moves.append((i, j, legal_moves))
    return possible_moves

def get_capture_moves(self, board, color):
    """
    Returns only the capture moves for the given color. 
    These are moves where a piece can capture an opponent's piece.
    """
    capture_moves = []
    possible_moves = getPossibleMovesForColor(self, board, color)
    for move in possible_moves:
        from_x, from_y, to_positions = move
        for to_x, to_y in to_positions:
            if abs(to_x - from_x) > 1 or abs(to_y - from_y) > 1:  # Capture condition
                capture_moves.append((from_x, from_y, [(to_x, to_y)]))
    return capture_moves

def isGameOver(self, board, color):
    """
    Checks if the game is over for a given color.
    """
    try:
        for x in range(8):
            for y in range(8):
                square = board.getSquare(x, y)
                if square.squarePiece and square.squarePiece.color == color:
                    if board.get_valid_legal_moves(x, y, False):
                        return False
        return True
    except Exception as e:
        print(f"Error in isGameOver: {e}")
        return False  # Assume game is not over on error

def order_moves(moves, board, color):
    """
    Orders moves to prioritize captures, king promotions, and higher-weighted captures.
    """
    def move_priority(move):
        from_x, from_y, to_positions = move
        priority = 0
        piece = board.getSquare(from_x, from_y).squarePiece
        piece_weight = get_piece_weight(piece)
        
        for to_pos in to_positions:
            to_x, to_y = to_pos
            # Check if the move is a capture
            if abs(to_x - from_x) > 1 or abs(to_y - from_y) > 1:
                # Calculate the captured piece's position
                captured_x = (from_x + to_x) // 2
                captured_y = (from_y + to_y) // 2
                captured_piece = board.getSquare(captured_x, captured_y).squarePiece
                captured_weight = get_piece_weight(captured_piece) if captured_piece else 0
                priority += 10 + captured_weight  # Base priority for capture plus captured piece weight
            # Check for king promotion
            if piece:
                if piece.color == GREY and to_y == 0:
                    priority += 5
                elif piece.color == PURPLE and to_y == 7:
                    priority += 5
            # Encourage central control
            if 2 <= to_x <= 5:
                priority += 1
        # Additionally, prioritize moves made by higher-weighted pieces
        priority += piece_weight * 0.5
        return priority
    
    # Sort moves based on priority in descending order
    try:
        sorted_moves = sorted(moves, key=lambda move: move_priority(move), reverse=True)
    except Exception as e:
        print(f"Error in order_moves: {e}")
        sorted_moves = moves  # Fallback to unsorted moves on error
    return sorted_moves

def get_piece_weight(piece):
    """
    Assigns weight values to pieces based on their type.
    Regular pieces have a weight of 1, kings have a weight of 2.
    """
    if piece is None:
        return 0
    return 2 if piece.king else 1