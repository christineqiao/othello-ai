# Name: Christine Qiao
# Date: 1/10
 
import random
 
class RandomBot:
    def __init__(self):
        self.white = "O"
        self.black = "@"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None
 
    def best_strategy(self, board, color):
        self.x_max = len(board)
        self.y_max = len(board[0])
 
        if color == "#000000":
            color = self.black
        else:
            color = self.white
 
        possible_moves = self.find_moves(board, color)
 
        if not possible_moves:
            return None, 0
 
        move = random.choice(list(possible_moves.keys()))
        return [move // self.y_max, move % self.y_max], 0
 
    def find_moves(self, board, color):
        moves_found = {}
        for x in range(self.x_max):
            for y in range(self.y_max):
                flipped_stones = self.find_flipped(board, x, y, color)
                if flipped_stones:
                    moves_found[(x * self.y_max) + y] = flipped_stones
        return moves_found
 
    def find_flipped(self, board, x, y, color):
        if board[x][y] != ".":
            return []
 
        flipped_stones = []
        for direction in self.directions:
            temp_flipped = []
            x_pos, y_pos = x + direction[0], y + direction[1]
 
            while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                if board[x_pos][y_pos] == ".":
                    break
                if board[x_pos][y_pos] == color:
                    flipped_stones.extend(temp_flipped)
                    break
                temp_flipped.append((x_pos, y_pos))
                x_pos += direction[0]
                y_pos += direction[1]
 
        return flipped_stones
 
class Best_AI_bot:
    def __init__(self):
        self.white = "O"
        self.black = "@"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None
        
        self.weight_matrix = [
            [120, -20, 20,  5,  5, 20, -20, 120],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [ 20,  -5, 15,  3,  3, 15,  -5,  20],
            [  5,  -5,  3,  3,  3,  3,  -5,   5],
            [  5,  -5,  3,  3,  3,  3,  -5,   5],
            [ 20,  -5, 15,  3,  3, 15,  -5,  20],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [120, -20, 20,  5,  5, 20, -20, 120]
        ]

    def best_strategy(self, board, color):
        self.x_max = len(board)
        self.y_max = len(board[0])
        
        color = self.black if color == "#000000" else self.white
        
        possible_moves = self.find_moves(board, color)
        if not possible_moves:
            return None, 0
            
        total_pieces = sum(row.count(self.black) + row.count(self.white) for row in board)
        if total_pieces >= 50:  
            depth = 6
        elif total_pieces >= 40:  
            depth = 5
        elif len(possible_moves) > 8: 
            depth = 4
        else: 
            depth = 5
            
        best_move, eval_score = self.negamax(board, color, depth=depth, alpha=-float('inf'), beta=float('inf'))
        if best_move is None:
            return None, 0
            
        return [best_move[0], best_move[1]], eval_score

    def negamax(self, board, color, depth, alpha, beta):
        possible_moves = self.find_moves(board, color)
        if depth == 0 or not possible_moves:
            return None, self.evaluate(board, color)
            
        best_value = -float('inf')
        best_move = None
        
        moves_with_eval = []
        for move, flipped in possible_moves.items():
            x, y = move // self.y_max, move % self.y_max
            quick_eval = self.weight_matrix[x][y] + len(flipped) * 2
            moves_with_eval.append((move, flipped, quick_eval))
            
        sorted_moves = sorted(moves_with_eval, key=lambda x: x[2], reverse=True)
        
        for move, flipped, _ in sorted_moves:
            new_board = self.make_move(board, color, move, flipped)
            _, val = self.negamax(new_board, self.opposite_color[color], depth - 1, -beta, -alpha)
            val = -val
            
            if val > best_value:
                best_value = val
                best_move = (move // self.y_max, move % self.y_max)
                
            alpha = max(alpha, val)
            if alpha >= beta:
                break
                
        return best_move, best_value

    def make_move(self, board, color, move, flipped):
        new_board = [row[:] for row in board]
        x, y = move // self.y_max, move % self.y_max
        new_board[x][y] = color
        for fx, fy in flipped:
            new_board[fx][fy] = color
        return new_board

    def evaluate(self, board, color):
        opponent = self.opposite_color[color]
        
        my_weighted_count = 0
        opp_weighted_count = 0
        my_count = 0
        opp_count = 0
        
        for x in range(self.x_max):
            for y in range(self.y_max):
                if board[x][y] == color:
                    my_weighted_count += self.weight_matrix[x][y]
                    my_count += 1
                elif board[x][y] == opponent:
                    opp_weighted_count += self.weight_matrix[x][y]
                    opp_count += 1
        
        my_mobility = len(self.find_moves(board, color))
        opp_mobility = len(self.find_moves(board, opponent))
        mobility_score = 0
        if my_mobility + opp_mobility != 0:
            mobility_score = 100 * (my_mobility - opp_mobility) / (my_mobility + opp_mobility)
        
        corners = [(0, 0), (0, self.y_max-1), (self.x_max-1, 0), (self.x_max-1, self.y_max-1)]
        my_corners = sum(1 for x, y in corners if board[x][y] == color)
        opp_corners = sum(1 for x, y in corners if board[x][y] == opponent)
        corner_score = 25 * (my_corners - opp_corners)
        
        my_stable = self.count_stable_pieces(board, color)
        opp_stable = self.count_stable_pieces(board, opponent)
        stability_score = 30 * (my_stable - opp_stable)
        
        piece_ratio = 0
        if my_count + opp_count != 0:
            piece_ratio = 100 * (my_count - opp_count) / (my_count + opp_count)
        
        total_pieces = my_count + opp_count
        if total_pieces >= 50:  
            return piece_ratio * 2 + stability_score * 2 + corner_score * 3
        else:  
            return (my_weighted_count - opp_weighted_count) + \
                   mobility_score * 2 + \
                   corner_score * 3 + \
                   stability_score * 2

    def count_stable_pieces(self, board, color):
        stable = set()
        
        corners = [(0, 0), (0, self.y_max-1), (self.x_max-1, 0), (self.x_max-1, self.y_max-1)]
        for corner in corners:
            if board[corner[0]][corner[1]] == color:
                self.expand_stable(board, corner[0], corner[1], color, stable)
                
        return len(stable)
        
    def expand_stable(self, board, x, y, color, stable):
        if (x, y) in stable or board[x][y] != color:
            return
            
        stable.add((x, y))
        
        for dx, dy in self.directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.x_max and 0 <= new_y < self.y_max:
                self.expand_stable(board, new_x, new_y, color, stable)

    def find_moves(self, board, color):
        moves_found = {}
        for x in range(self.x_max):
            for y in range(self.y_max):
                flipped_stones = self.find_flipped(board, x, y, color)
                if flipped_stones:
                    moves_found[(x * self.y_max) + y] = flipped_stones
        return moves_found

    def find_flipped(self, board, x, y, color):
        if board[x][y] != ".":
            return []
            
        flipped_stones = []
        for direction in self.directions:
            temp_flipped = []
            x_pos, y_pos = x + direction[0], y + direction[1]
            
            while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                if board[x_pos][y_pos] == ".":
                    break
                if board[x_pos][y_pos] == color:
                    flipped_stones.extend(temp_flipped)
                    break
                temp_flipped.append((x_pos, y_pos))
                x_pos += direction[0]
                y_pos += direction[1]
                
        return flipped_stones