import numpy as np
from pprint import pprint
import copy
#reading from terminal

def get_board():
    '''
    Function gets the board from the terminal
    '''
    board = [[]]
    for i in range(5):
        line = input("")
        for char in line:
            if char == '0':
                board[i].append(0)
            else:
                board[i].append(char)
        if i != 4:
            board.append([])
    return board

def get_board_file(filename):
    '''
    Function that gets the board from a file
    '''
    board = [[]]
    with open(filename, 'r') as f:
        i = 0
        while i < 5:
            line = f.readline().strip()
            for char in line:
                if char == '0':
                    board[i].append(0)
                else:
                    board[i].append(char)
            if i != 4:
                board.append([])
            i += 1

    return board 

def get_moves(array: list, colour: str):

    '''
    Gets a list of moves in a tuple (startx, starty, endx, endy).
    Colour must be 'B' or 'W'
    '''
    moves = []
    for y in range(len(array)):
        for x in range(len(array[y])):

            if array[y][x] == 0:
                continue

            if array[y][x].islower() and not colour:
                continue

            if array[y][x].isupper() and colour:
                continue

            if array[y][x].lower() == 'n':
                get_moves_knight(x, y, array, moves, colour)
            if array[y][x].lower() == 'q':
                get_moves_queen(x, y, array, moves, colour)
            if array[y][x].lower() == 'p':
                get_moves_pawn(x, y, array, moves, colour)
            if array[y][x].lower() == 'b':
                get_moves_bishop(x, y, array, moves, colour)
            if array[y][x].lower() == 'k':
                get_moves_king(x, y, array, moves, colour)
            if array[y][x].lower() == 'r':
                get_moves_rook(x, y, array, moves, colour)

    return moves

def get_moves_bishop(x: int, y: int, board: list, moves: list, colour):
    xlst = [x + 1, x + 1, x - 1, x - 1]
    ylst = [y + 1, y - 1, y + 1, y - 1]

    #loop through possible directions
    while len(xlst) > 0:
        nextx = xlst[len(xlst) - 1]
        nexty = ylst[len(ylst) - 1]
        xlst.pop()
        ylst.pop()

        #square out of bounds
        if nextx < 0 or nextx > 4 or nexty < 0 or nexty > 4:
            continue

        valid = test_valid_square(nextx, nexty, board, colour)
        if valid:
            moves.append((x, y, nextx, nexty))
            if board[nexty][nextx] != 0:
                continue
            if nextx > x:
                xlst.append(nextx + 1)
            else:
                xlst.append(nextx - 1)
            if nexty > y:
                ylst.append(nexty + 1)
            else:
                ylst.append(nexty - 1)
    return 
        
def test_valid_square(nextx, nexty, board, colour):
    valid = False
    #if its a valid square
    if board[nexty][nextx] == 0:
        valid = True
    elif colour and board[nexty][nextx].isupper():
        valid = True
    elif not colour and board[nexty][nextx].islower():
        valid = True
    return valid

def get_moves_rook(x: int, y: int, board: list, moves: list, colour):
    xlst = [x + 1, x - 1]
    ylst = [y + 1, y - 1]

    #loop through possible directions
    while len(xlst) > 0:
        nextx = xlst[len(xlst) - 1]
        nexty = y
        xlst.pop()

        #square out of bounds
        if nextx < 0 or nextx > 4 or nexty < 0 or nexty > 4:
            continue

        valid = test_valid_square(nextx, nexty, board, colour)

        if valid:
            moves.append((x, y, nextx, nexty))
            target = board[nexty][nextx]
            if target != 0:
                continue
            if nextx > x:
                xlst.append(nextx + 1)
            else:
                xlst.append(nextx - 1)
    
    #loop through possible directions
    while len(ylst) > 0:
        nextx = x
        nexty = ylst[len(ylst) - 1]
        ylst.pop()

        #square out of bounds
        if nextx < 0 or nextx > 4 or nexty < 0 or nexty > 4:
            continue

        valid = test_valid_square(nextx, nexty, board, colour)

        if valid:
            moves.append((x, y, nextx, nexty))
            target = board[nexty][nextx]
            if target != 0:
                continue
            if nexty > y:
                ylst.append(nexty + 1)
            else:
                ylst.append(nexty - 1)
    
    return 
    
def get_moves_pawn(x: int, y: int, board: list, moves: list, colour):
    
    #moving forward
    if colour:
        nexty = y - 1
        nextx = x
    else:
        nexty = y + 1
        nextx = x

    #if the pawn is still on the board
    if nexty >= 0 and nexty < 5:
        if board[nexty][nextx] == 0:
            moves.append((x, y, nextx, nexty))
    
    #moving diagonal
    if colour:
        nexty = y - 1
        nextx = x + 1
        if test_valid_square(nextx, nexty, board, colour) and board[nexty][nextx] != 0:
            moves.append((x, y, nextx, nexty))
        nexty = y - 1
        nextx = x - 1
        if test_valid_square(nextx, nexty, board, colour) and board[nexty][nextx] != 0:
            moves.append((x, y, nextx, nexty))
    else:
        nexty = y + 1
        nextx = x + 1
        if test_valid_square(nextx, nexty, board, colour) and board[nexty][nextx] != 0:
            moves.append((x, y, nextx, nexty))
        nexty = y + 1
        nextx = x - 1
        if test_valid_square(nextx, nexty, board, colour) and board[nexty][nextx] != 0:
            moves.append((x, y, nextx, nexty))

    return 
    
    

def get_moves_king(x: int, y: int, board: list, moves: list, colour):
    
    xlst = [x + 1, x + 1, x, x - 1, x - 1, x - 1, x, x + 1]
    ylst = [y, y + 1, y + 1, y + 1, y, y - 1, y - 1, y - 1]

        #loop through possible directions
    while len(xlst) > 0:
        nextx = xlst[len(xlst) - 1]
        nexty = ylst[len(ylst) - 1]
        xlst.pop()
        ylst.pop()

        #square out of bounds
        if nextx < 0 or nextx > 4 or nexty < 0 or nexty > 4:
            continue

        valid = test_valid_square(nextx, nexty, board, colour)
        if valid:
            moves.append((x, y, nextx, nexty))
            
    return 

def get_moves_queen(x: int, y: int, board: list, moves: list, colour):
    get_moves_bishop(x, y, board, moves, colour)
    get_moves_rook(x, y, board, moves, colour)
    return 

def get_moves_knight(x: int, y: int, board: list, moves: list, colour):
    xlst = [x + 1, x + 2, x - 1, x - 2, x + 1, x + 2, x - 1, x - 2]
    ylst = [y + 2, y + 1, y + 2, y + 1, y - 2, y - 1, y - 2, y - 1]

    while len(xlst) > 0:
        nextx = xlst[len(xlst) - 1]
        nexty = ylst[len(ylst) - 1]
        xlst.pop()
        ylst.pop()

        #square out of bounds
        if nextx < 0 or nextx > 4 or nexty < 0 or nexty > 4:
            continue

        valid = test_valid_square(nextx, nexty, board, colour)
        if valid:
            moves.append((x, y, nextx, nexty))


def check_position(board, colour):
    '''
    Function takes in a board.
    Return true if the board is in check
    '''
    moves = get_moves(board, colour)
    if len(moves) == 0:
        return False

    for x,y,newx,newy in moves:
        if board[newy][newx] == 0:
            continue
        if board[newy][newx].lower() == 'k':
            return True 
    return False
            

def rebuild_board(move, board):
    '''
    Function takes in a move and creates a new board
    after the move is executed
    '''
    x,y,newx,newy = move
    new_board = copy.deepcopy(board)
    new_board[newy][newx] = new_board[y][x] 
    new_board[y][x] = 0
    return new_board

def filter_possible_moves(moves, board, colour):
    ''' 
    Determines that the moves we make are legal
    '''
    final_moves = []
    for move in moves:
        #create a new board
        newboard = rebuild_board(move, board)

        #if the board is not in check add it to the final list
        if not check_position(newboard, not colour):
            final_moves.append(move)
        else:
            continue
    return final_moves

def main():
    #In this code True is White and False is Black

    #function to get the board from a file
    array = get_board_file('sample.txt')
    #function to get the baord from the terminal
    #array = get_board()
    possible_moves = get_moves(array, True)
    filtered_moves = filter_possible_moves(possible_moves, array, True)

    for move in filtered_moves:
        new_board = rebuild_board(move, array)
        if check_position(new_board, True):
            print(f"The '{array[move[0]][move[1]]}' has moved to ({move[2]},{move[3]}) and made a check")
            print(True)
            return True
    
    print("No check possible")
    print(False)
    return False

     
if __name__ == '__main__':
    main()