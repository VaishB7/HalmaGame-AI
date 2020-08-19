import sys
import time
import math


class Halma():

    def __init__(self, turn, size, max_time, board):

        self.max_time = max_time
        self.size = size

        self.board = board
        self.converted_board = [[[i, j] for j in range(16)] for i in range(16)]
        self.white_list = []
        self.black_list = []
        self.none = []
        self.white_list, self.black_list, self.none = self.interpret_input()
        self.white_goals = []
        self.black_goals = []
        # White, red
        self.black_camp = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, 0],
                           [2, 1], [2, 2], [2, 3], [3, 0], [3, 1], [3, 2], [4, 0], [4, 1]]

        # Black, green
        self.white_camp = [[11, 14], [11, 15], [12, 13], [12, 14], [12, 15], [13, 12], [13, 13], [13, 14], [13, 15],
                           [14, 11], [14, 12], [14, 13], [14, 14], [14, 15], [15, 11], [15, 12], [15, 13], [15, 14],
                           [15, 15]]
        self.white_goals = [row for row in self.black_camp if not (row in self.black_list or row in self.white_list)]
        if not self.white_goals and sorted(self.black_camp) == sorted(self.black_list):
            self.white_goals = self.black_camp

        self.black_goals = [row for row in self.white_camp if not (row in self.black_list or row in self.white_list)]
        if self.black_goals == [] and sorted(self.white_camp) == sorted(self.white_list):
            self.black_goals = self.white_camp

        self.turn = turn
        if (self.turn == 'BLACK'):
            self.current = 'B'

        if (self.turn == 'WHITE'):
            self.current = 'W'

        self.max_player_depth = 2

        self.valid_moves = []

        self.halma_move()

    def interpret_input(self):
        # Tested Correct
        for i in range(16):
            for j in range(16):
                if self.board[i][j] == 'W':
                    self.white_list.append([i, j])
                elif self.board[i][j] == 'B':
                    self.black_list.append([i, j])
                else:
                    self.none.append([i, j])

        return self.white_list, self.black_list, self.none

    def get_next_moves(self, player):
        newmoves = []
        someinW = []
        moves = []  # All possible moves
        in_outMoves = []
        in_outMovesPresent = False
        for row in range(self.size):
            for col in range(self.size):

                curr_tile = self.board[row][col]

                # Skip board elements that are not the current player
                if curr_tile != player:
                    continue

                move = {
                    "from": [row, col],
                    "to": self.future_moves([row, col], player)  # changed
                }

                if player == 'W':
                    temp3 = []
                    if move["from"] in self.black_camp:
                        for i in move["to"]:
                            if i not in self.black_camp:
                                temp3.append(i)


                if player == 'B':
                    temp3 = []
                    if move["from"] in self.white_camp:
                        for i in move["to"]:
                            if i not in self.white_camp:
                                temp3.append(i)

                if temp3:
                    for z in temp3:
                        # print("z", z)
                        move["to"].remove(z)


                if player == 'W':
                    out_intemp = []
                    if move["from"] not in self.white_camp:
                        for i in move["to"]:
                            if i in self.white_camp:
                                out_intemp.append(i)

                if player == 'B':
                    out_intemp = []
                    if move["from"] not in self.black_camp:
                        for i in move["to"]:
                            if i in self.black_camp:
                                out_intemp.append(i)

                if out_intemp:
                    for z in out_intemp:
                        # print("z", z)
                        move["to"].remove(z)

                moves.append(move)

                if player == 'W':
                    someinW = [value for value in self.white_list if value in self.white_camp]
                    # print("SOME in W",someinW)
                    if move["from"] in someinW:
                        # print("MOVE FROM", move["from"])
                        newmoves.append(move)


                if player == 'B':
                    someinB = [value for value in self.black_list if value in self.black_camp]
                    if move["from"] in someinB:
                        newmoves.append(move)


#BOTH FOR LOOP ENDS

        # print("ALL MOVES", newmoves)
        # print("Moves", moves)
        print("New Moves", newmoves)
        if newmoves:
            # in-out
            if player == 'W':

                for i in newmoves:
                    x = i["from"][0]
                    y = i["from"][1]
                    # print("from",i["from"])

                    movinginW = [value for value in i["to"] if value in self.white_camp]
                    movinginW2 = [value for value in i["to"] if value not in self.white_camp]
                    #print("MOVING Outside", movinginW2)
                    if movinginW2:
                        for j in movinginW:
                            i["to"].remove(j)
                        in_outMoves.append(i)
                        print("in_outMovesPresent",in_outMoves)
                        in_outMovesPresent = True
                    else:
                        in_outMovesPresent = False
                        temp2 = []
                        temp = i["to"]
                        # print("to",temp)
                        length = len(temp)
                        if length >= 1:
                            k = 0
                            while k < length:

                                # print("val",temp[k])
                                xnew = temp[k][0]
                                ynew = temp[k][1]

                                if (xnew < x and ynew == y) or (xnew == x and ynew < y) or (xnew < x and ynew < y):
                                    k += 1
                                    continue
                                else:
                                    temp2.append(temp[k])
                                    k += 1

                            # print("temp2",temp2)

                            for z in temp2:
                                # print("z",z)
                                i["to"].remove(z)
                if (in_outMovesPresent):
                    return in_outMoves
                else:
                    return newmoves

            if player == 'B':

                for i in newmoves:
                    x = i["from"][0]
                    y = i["from"][1]
                    # print("from", i["from"])

                    movinginW = [value for value in i["to"] if value in self.black_camp]
                    movinginW2 = [value for value in i["to"] if value not in self.black_camp]
                    print("MOVING Outside", movinginW2)
                    if movinginW2:
                        for j in movinginW:
                            i["to"].remove(j)
                        in_outMoves.append(i)
                        #print("in_outMovesPresent",in_outMovesPresent)
                        in_outMovesPresent = True

                    else:
                        in_outMovesPresent = False
                        temp2 = []
                        temp = i["to"]
                        # print("to", temp)
                        length = len(temp)
                        if length >= 1:
                            k = 0
                            while k < length:

                                # print("val",temp[k])
                                xnew = temp[k][0]
                                ynew = temp[k][1]

                                if (xnew > x and ynew == y) or (xnew == x and ynew > y) or (xnew > x and ynew > y):
                                    k += 1
                                    continue
                                else:
                                    temp2.append(temp[k])
                                    k += 1

                            # print("temp2", temp2)

                            for z in temp2:
                                # print("z", z)
                                i["to"].remove(z)

                if(in_outMovesPresent):
                    print("in_put",in_outMoves)
                    return in_outMoves
                else:
                    return newmoves

        else:
            return moves





    def winner(self):

        if all(elements in self.white_list for elements in self.white_goals):
            return "yes"
        elif all(elements in self.black_list for elements in self.black_goals):
            return "yes"
        else:
            return None

    def future_moves(self, tile, player, moves=None, adj=True):

        if moves is None:
            moves = []

        row = tile[0]
        col = tile[1]

        # List of valid tile types to move to
        valid_tiles = self.none + self.white_list + self.black_list

        """if player == 'W':
            lst3 = [value for value in self.white_list if value in self.T_W]
            print(lst3)"""

        # Find and save immediately adjacent moves
        for col_delta in range(-1, 2):
            for row_delta in range(-1, 2):

                # Check adjacent tiles

                new_row = row + row_delta
                new_col = col + col_delta

                # Skip checking degenerate values
                if ((new_row == row and new_col == col) or
                        new_row < 0 or new_col < 0 or
                        new_row >= self.size or new_col >= self.size):
                    continue
                # print(new_row, new_col)
                # print(valid_tiles)
                # Handle moves out of/in to goals
                new_tile = self.converted_board[new_row][new_col]
                if new_tile not in valid_tiles:
                    continue

                if new_tile in self.none:
                    if adj:
                        # Don't consider adjacent on subsequent calls
                        moves.append(new_tile)
                    continue

                # Check jump tiles
                new_row = new_row + row_delta
                new_col = new_col + col_delta

                # Skip checking degenerate values
                if (new_row < 0 or new_col < 0 or
                        new_row >= self.size or new_col >= self.size):
                    continue

                # Handle returning moves and moves out of/in to goals
                new_tile = self.converted_board[new_row][new_col]
                if new_tile in moves or (new_tile not in valid_tiles):
                    continue

                if new_tile in self.none:
                    moves.insert(0, new_tile)  # Prioritize jumps
                    self.future_moves(new_tile, player, moves, False)
        return moves

    """def move_piece(self, from_tile, to_tile):

        # Handle trying to move a non-existant piece and moving into a piece


        # Move piece
        self.board[to_tile[1]][to_tile[0]] = self.board[from_tile[1]][from_tile[0]]
        self.board[from_tile[1]][from_tile[0]] = '.'

        print("FROM TILE : ", from_tile)
        print("to TILE : ", to_tile)
        print("NEW BOARD", self.board)
        return self.board"""

    def halma_move(self):
        # print("halma_move TURN", self.current)

        max_time = time.time() + self.max_time

        # Execute min_max search
        start = time.time()
        _, move, prunes, boards = self.min_max(self.max_player_depth,
                                               self.current, max_time)  # ALERT NO MINIMAX move is a 2D Array
        end = time.time()

        print("complete")
        print("Time to compute:", round(end - start, 4))
        print("Total boards generated:", boards)
        print("Total prune events:", prunes)

        print("MOVE FINAL GENErated: ", move)
        move_from = self.converted_board[move[0][0]][move[0][1]]  # DONT KNOW WHAT BOARD OR MOVE IS
        move_to = self.converted_board[move[1][0]][move[1][1]]
        # self.move_piece(move_from, move_to)
        print("FINAL MOVE", move_from, move_to)
        temp = ""
        if abs(int(move_from[0]) - int(move_to[0])) <= 1 and abs(int(move_from[1]) - int(move_to[1])) <= 1:
            temp = 'E'
        else:
            temp = 'J'
        file = open("output.txt", "w+")
        file.write(temp)
        file.write(' ')
        file.write(str(move_from[1]) + ',' + str(move_from[0]))
        file.write(' ')
        file.write(str(move_to[1]) + ',' + str(move_to[0]))

    def min_max(self, depth, player_to_max, max_time, a=float("-inf"),
                b=float("inf"), maxing=True, prunes=0, boards=0):

        # print(self.winner())
        # print(time.time() > max_time)
        if depth == 0 or self.winner() or time.time() > max_time:
            return self.utility(player_to_max), None, prunes, boards  # NO UTILITY

        best_move = None
        if maxing:
            best_val = float("-inf")
            moves = self.get_next_moves(player_to_max)
        else:
            best_val = float("inf")
            moves = self.get_next_moves(('B'
                                         if player_to_max == 'W' else 'W'))

        # print("MOVES", moves)
        # print("best_val", best_val)

        for move in moves:
            for to in move["to"]:
                # print("TO", to)
                # Bail out when we're out of time
                if time.time() > max_time:
                    return best_val, best_move, prunes, boards

                # Move piece to the move outlined
                piece = move["from"]
                # print("FROM", piece)
                self.board[piece[0]][piece[1]] = '.'
                self.board[to[0]][to[1]] = player_to_max
                boards += 1

                # print("BOARD", self.board)
                self.white_list, self.black_list, self.none = self.interpret_input()

                self.white_goals = [row for row in self.black_camp if
                                    not (row in self.black_list or row in self.white_list)]
                if not self.white_goals and sorted(self.black_camp) == sorted(self.black_list):
                    self.white_goals = self.black_camp

                self.black_goals = [row for row in self.white_camp if
                                    not (row in self.black_list or row in self.white_list)]
                if self.black_goals == [] and sorted(self.white_camp) == sorted(self.white_list):
                    self.black_goals = self.white_camp

                val, temp, new_prunes, new_boards = self.min_max(depth - 1,
                                                                 player_to_max, max_time, a, b, not maxing, prunes,
                                                                 boards)
                prunes = new_prunes
                boards = new_boards
                # print("VALUE**", val)

                self.board[to[0]][to[1]] = '.'
                self.board[piece[0]][piece[1]] = player_to_max

                self.white_list, self.black_list, self.none = self.interpret_input()

                self.white_goals = [row for row in self.black_camp if
                                    not (row in self.black_list or row in self.white_list)]
                if not self.white_goals and sorted(self.black_camp) == sorted(self.black_list):
                    self.white_goals = self.black_camp

                self.black_goals = [row for row in self.white_camp if
                                    not (row in self.black_list or row in self.white_list)]
                if self.black_goals == [] and sorted(self.white_camp) == sorted(self.white_list):
                    self.black_goals = self.white_camp

                if maxing and val > best_val:
                    best_val = val
                    best_move = (move["from"], to)
                    a = max(a, val)

                if not maxing and val < best_val:
                    best_val = val
                    best_move = (move["from"], to)
                    b = min(b, val)

                if b <= a:
                    return best_val, best_move, prunes + 1, boards

        # print("HERE", best_val, best_move, prunes, boards)

        return best_val, best_move, prunes, boards

    def utility(self, current):
        def p_distance(p0, p1):

            return math.sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)

        value = 0

        for row in range(self.size):
            for col in range(self.size):

                tile = self.converted_board[row][col]

                if tile in self.black_list:
                    distances = [p_distance(tile, g) for g in
                                 self.black_goals if g not in self.black_list]
                    value -= max(distances) if len(distances) else -50



                elif tile in self.white_list:
                    distances = [p_distance(tile, g) for g in
                                 self.white_goals if g not in self.white_list]
                    value += max(distances) if len(distances) else -50

        if current == 'W':
            value *= -1

        return value




if __name__ == "__main__":

    f = open("input.txt", "r")
    lines = f.readlines()

    type = lines[0].rstrip('\n')
    if "SINGLE" in type:
        type = "SINGLE"
    else:
        type = "GAME"

    print("type", type)

    meType = lines[1].rstrip('\n')
    print(meType)

    Mtime = lines[2].rstrip('\n')
    Mtime = float(Mtime)
    print("time", Mtime)

    initial_board = []
    for i in range(16):
        initial_board.append(list((lines[3 + i].rstrip('\n')).strip()))

    print("board", initial_board)

    halma = Halma(meType, 16, Mtime, initial_board)


