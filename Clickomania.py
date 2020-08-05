# import pygame
import random
import numpy as np

# pygame.init()
# gameDisplay = pygame.display.set_mode((800, 600))
# pygame.display.set_caption('Clickomania')
# clock = pygame.time.Clock()

colors = ["B", "R", "G", "Y", "P"]  # List of available pieces for board placement.


def create_board():
    """Function creates 12x8 game board and fills board with available pieces."""
    board = np.zeros([12, 8], dtype=str)  # Establishes empty 12x8 game board.
    for rows in range(12):  # Loops through each row.
        for columns in range(8):  # Loops through each column.
            board[rows][columns] = random.choice(colors)  # Places piece at current position of game board.
    return board  # Returns game board.


def valid_piece(board, row, column):
    """Function checks if current position chosen can produce a valid move or elimination of pieces."""
    if board[row][column] == '0':  # Checks if chosen position contains a piece.
        return
    for x in range(row - 1, row + 2, 2):  # Loops through row above and below current position.
        if x > 11 or x < 0:  # Checks if current position to be observed is within bounds.
            continue
        elif board[row][column] == board[x][column]:  # Checks if position to be observed contains same chosen piece.
            return True
    N = len(board[11])  # Variable represents current number of columns present in game play.
    for x in range(column - 1, column + 2, 2):  # Loops through columns left and right current position.
        if x > (N - 1) or x < 0:  # Checks if current position to be observed is within bounds.
            continue
        elif board[row][column] == board[row][x]:  # Checks if position to be observed contains same chosen piece.
            return True
    return


def move(board, row, column, piece, graph):
    """Function performs move/elimination of valid piece in current game play."""
    memo = []  # Empty list to hold piece locations of valid moves of current position.
    for keys in graph:  # Loops through keys in current graph.
        if (row, column) == keys and graph[keys] != '0':
            # Checks if current position is already present in graph without valid moves.
            return
    if row + 1 <= 11:  # Checks to ensure row to be observed is within bounds.
        if board[row + 1][column] == piece:  # Checks if row below contains same piece.
            memo.append([row + 1, column])  # Adds observed position to graph for current position.
    if row - 1 >= 0:  # Checks to ensure row to be observed is within bounds.
        if board[row - 1][column] == piece:  # Checks if row above contains same piece.
            memo.append([row - 1, column])  # Adds observed position to graph for current position.
    N = len(board[11])  # Variable represent current available columns in game play.
    if column + 1 <= (N - 1):  # Checks to ensure column to be observed is within bounds.
        if board[row][column + 1] == piece:  # Checks if column to right contains same piece.
            memo.append([row, column + 1])  # Adds observed position to graph for current position.
    if column - 1 >= 0:  # Checks to ensure column to be observed is within bounds.
        if board[row][column - 1] == piece:  # Checks if column to left contains same piece.
            memo.append([row, column - 1])  # Adds observed position to graph for current position.
    graph[(row, column)] = memo  # Updates graph to contain current position with all pieces available for valid move.
    for location in memo:  # Loops through locations present in current memo.
        location = tuple(location)  # Converts location to tuple data type.
        if location not in graph:  # Checks if location is present in graph.
            graph[location] = '0'  # Creates an empty placeholder for valid moves.
    for keys in list(graph):  # Loops through a list of keys from graph.
        keys = list(keys)  # Converts current key to a list data type.
        move(board, keys[0], keys[1], piece, graph)
        # Recursively iterates through move function for current key/location.
    return graph  # Returns graph containing all valid moves.


def reset_board(board, graph):
    g = list(graph)  # Variable represents list of keys within graph.
    g.sort()  # Sorts location into ascending order.
    for locations in g:  # Loops through a list of keys from graph.
        locations = list(locations)  # Converts current location to a list data type.
        for x in range(locations[0], -1, -1):  # Loops through rows beginning with row closest to last row.
            if x - 1 >= 0:  # Checks to ensure row to be observed is not out of bounds.
                board[x][locations[1]] = board[x - 1][locations[1]]
                # Moves position located above current position down to current position.
                board[x - 1][locations[1]] = '0'  # Places empty placeholder into position of piece just moved down.
    return board  # Returns updated game board.


board = create_board()  # Board variable to represent newly created board.
print(board)
game_over = "In Progress"  # Initializes game_over status to in progress.
while game_over == "In Progress":  # Loops through game play until game is either won or lost.
    game_count = 0  # Counter variable used to check if player has lost.
    win_count = 0  # Counter variable used to check if player has won.
    for x in range(12):  # Loops through each row on game board.
        for n in range(len(board[11])):  # Loops through each column available in current game play.
            if win_count > 0:  # Checks if win-count counter has been increased.
                break
            if board[x][n] != '0':  # Checks if current location contains a game piece.
                win_count += 1  # Increases counter variable.
    if win_count == 0:  # Checks if counter remained zero during iteration of game board.
        game_over = "You Won!"  # Sets game_over to you won.
    for x in range(12):  # Loops through each row on game board.
        for n in range(len(board[11])):  # Loops through each column available in current game play.
            if game_count > 0:  # Checks if game_count counter has increased.
                break
            if valid_piece(board, x, n):  # Checks if current position contains a valid move.
                game_count += 1  # Increases counter.
    if game_count == 0:  # Checks if game_count counter remained zero during iteration of board.
        game_over = "You Lost!"  # Sets game_over to you lost.
        continue
    row = int(input("Choose row to pick from (0-11): "))  # User asked to input row choice.
    while row > 11 or row < 0:  # Loops if player inputs an invalid row number.
        print("Invalid Row")
        row = int(input("Choose row to pick from (0-11): "))
    C = len(board[11])  # Variable represents number of columns present on current game board.
    column = int(input("Choose column from row (0-" + str(C - 1) + "): "))  # User asked to input column choice.
    while column >= C or column < 0:  # Loops if player inputs an invalid column number.
        print("Invalid Column")
        column = int(input("Choose column from row (0-" + str(C - 1) + "): "))
    if valid_piece(board, row, column):  # Checks if position chosen contains a valid move.
        piece = board[row][column]  # Variable represents piece at current position.
        graph = {}  # Empty graph to be used for move function.
        player = move(board, row, column, piece, graph)  # Variable represents graph constructed from move function.
        reset_board(board, player)  # Calls reset_board function to reset board following move.
        for n in range(len(board[11])):  # Loops for number of current columns present on game board.
            N = 0
            while N < len(board[11]):  # Loops through until last column has been reached on game board.
                if board[11][N] == '0':  # Checks if current position in loop contains an empty placeholder.
                    board = np.delete(board, N, axis=1)  # Deletes column in current location of game board.
                N += 1
        print(board)
    else:
        print("No move available at this location.")  # Prints if no valid move available for current position.
print(game_over)
