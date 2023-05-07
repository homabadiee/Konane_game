from Tile import Tile

class KonaneGame2:
    def __init__(self):
        NotImplemented

        
    def initialize_board(self, board_size):
        board = []
        tile = Tile(2, 0, 0, 0)
        for i in range(board_size):
            row_gui = []
            for j in range(board_size):
                row_gui.append(tile)
                tile = Tile(3-tile.piece, tile.outline, i, j+1)
            board.append(row_gui)
            if board_size%2 == 0:
                tile = Tile(3-tile.piece, tile.outline, i+1, 0)

        return board


    def generate_all_possible_moves(self, board, player):
        """
        Generates and returns all legal moves for the given player using the
        current board configuration.
        """
        if board.is_opening_move():
            if player == Tile.P_Black:
                return self.generate_first_moves(board)
            else:
                return self.generate_second_moves(board)
        else:
            moves = []
            rd = [-1, 0, 1, 0]
            cd = [0, 1, 0, -1]
            for r in range(board.size):
                for c in range(board.size):
                    if board.game_board[r][c].piece == player:
                        for i in range(len(rd)):
                            moves += self.check(board, r,c,rd[i],cd[i],1,
                                                self.opponent(player))
            return moves
        

    def generate_first_moves(self, board):
        """
        Returns the special cases for the first move of the game.
        """
        moves = []
        moves.append([0]*4)
        moves.append([board.size-1]*4)
        moves.append([board.size//2]*4)
        moves.append([(board.size//2)-1]*4)
        return moves


    def generate_second_moves(self, board):
        """
        Returns the special cases for the second move of the game, based
        on where the first move occurred.
        """
        moves = []
        if board.game_board[0][0].piece == Tile.P_NONE:
            moves.append([0,1]*2)
            moves.append([1,0]*2)
            return moves
        elif board.game_board[board.size-1][board.size-1].piece == Tile.P_NONE:
            moves.append([board.size-1,board.size-2]*2)
            moves.append([board.size-2,board.size-1]*2)
            return moves
        elif board.game_board[board.size//2-1][board.size//2-1].piece == Tile.P_NONE:
            pos = board.size//2 -1
        else:
            pos = board.size//2
        moves.append([pos,pos-1]*2)
        moves.append([pos+1,pos]*2)
        moves.append([pos,pos+1]*2)
        moves.append([pos-1,pos]*2)
        return moves


    def check(self, board, r, c, rd, cd, factor, opponent):
        """
        Checks whether a jump is possible starting at (r,c) and going in the
        direction determined by the row delta (rd), and the column delta (cd).
        The factor is used to recursively check for multiple jumps in the same
        direction.  Returns all possible jumps in the given direction.
        """
        if board.contains(r+factor*rd,c+factor*cd,opponent) and \
           board.contains(r+(factor+1)*rd,c+(factor+1)*cd, Tile.P_NONE):
            return [[r,c,r+(factor+1)*rd,c+(factor+1)*cd]] + \
                   self.check(board, r,c,rd,cd,factor+2,opponent)
        else:
            return []


    def get_moves_at_tile(self, board, tile, player):
        moves =  self.generate_all_possible_moves(board, player)
        valid_moves_at_tile = []
        print(moves)
        for move in moves:
            if move[0] == tile.row and move[1] == tile.col:
                valid_tile = board.game_board[move[2]][move[3]]
                valid_moves_at_tile.append(valid_tile)
        return valid_moves_at_tile
    

    def find_winner(self, board, color):
        valid_moves = self.generate_all_possible_moves(board, color)

        if valid_moves == []:
            winner = (Tile.P_Black if color == Tile.P_White else Tile.P_White)
            return winner

    
    def check_terminal(self, board, color): 

        valid_moves = self.generate_all_possible_moves(board, color)
        return True if valid_moves == [] else False


    def opponent(self, tile):
        """
        Given a player symbol, returns the opponent's symbol, 'B' for black,
        or 'W' for white.  (3 - color)
        """
        return Tile.P_Black if tile == Tile.P_White else Tile.P_White

    def count_position_score(self, board, color):
        center_piece = 0
        edge_piece = 0
        corner_piece = 0

        for i in range(6):
            for j in range(6):
                # center
                if (i == 2 or i == 3) and (j == 2 or j == 3):
                    if board.contains(i, j, color):
                        center_piece += 1

                # corner
                elif (i == 0 or i == 5) and (j == 0 or j == 5):
                    if board.contains(i, j, color):
                        corner_piece += 1

                # edge
                elif i == 0 or i == 5 or j == 0 or j == 5:
                    if board.contains(i, j, color):
                        edge_piece += 1

        return center_piece, edge_piece, corner_piece

    def connectivity(self, board, color):
        for i in range(6):
            for j in range(6):
                i = 2


    def evaluate(self, board, color, terminal_value = 0):

        possible_moves_weight = 8
        score_weight = 2
        corner_weight = 4
        center_weight = 2
        edge_weight = 2

        value = 0
        valid_moves_color = self.generate_all_possible_moves(board, color)
        valid_moves_opponent = self.generate_all_possible_moves(board, self.opponent(color))

        value += (possible_moves_weight * len(valid_moves_color))
        value -= (possible_moves_weight * len(valid_moves_opponent))

        piece_count = score_weight * (board.count_symbol(1) - board.count_symbol(2))


        center_piece, edge_piece, corner_piece = self.count_position_score(board, color)
        center_piece_op, edge_piece_op, corner_piece_op = self.count_position_score(board, self.opponent(color))

        tmp = ((center_piece - center_piece_op) * center_weight) + ((edge_piece - edge_piece_op) * edge_weight) \
              + ((corner_piece - corner_piece_op)* corner_weight)

        value += tmp + piece_count


        value += terminal_value

        return value

