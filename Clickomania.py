# import pygame
import random
import numpy as np

# pygame.init()
# gameDisplay = pygame.display.set_mode((800, 600))
# pygame.display.set_caption('Clickomania')
# clock = pygame.time.Clock()

row = 12
column = 8

colors = ["Blu", "Red", "Grn", "Yel", "Pur"]


def create_board():
    board = np.zeros([12, 8], dtype=str)
    for rows in range(12):
        for columns in range(8):
            board[rows][columns] = random.choice(colors)
    return board


def valid_piece(board, row, column):
    for x in range(row - 1, row + 2, 2):
        if board[row][column] == board[x][column]:
            return True
    for x in range(column - 1, column + 2, 2):
        if board[row][column] == board[row][x]:
            return True
    return


def move(board, row, column, piece, graph):
    memo = []
    for keys in graph:
        if (row, column) == keys and graph[keys] != '0':
            return
    if row + 1 <= 11:
        if board[row + 1][column] == piece:
            memo.append([row + 1, column])
    if row - 1 >= 0:
        if board[row - 1][column] == piece:
            memo.append([row - 1, column])
    if column + 1 <= 7:
        if board[row][column + 1] == piece:
            memo.append([row, column + 1])
    if column - 1 >= 0:
        if board[row][column - 1] == piece:
            memo.append([row, column - 1])
    graph[(row, column)] = memo
    for location in memo:
        location = tuple(location)
        if location not in graph:
            graph[location] = '0'
    for keys in list(graph):
        keys = list(keys)
        move(board, keys[0], keys[1], piece, graph)
    for locations in list(graph):
        location = list(locations)
        board[locations[0]][location[1]] = '0'
    return graph


def reset_board(board, graph):
    g = list(graph)
    g.sort()
    for locations in g:
        locations = list(locations)
        for x in range(locations[0], -1, -1):
            if x - 1 >= 0:
                board[x][locations[1]] = board[x - 1][locations[1]]
                board[x - 1][locations[1]] = '0'
    for columns in range(0, len(board[11])):
        if board[11, columns] == '0':
            for locations in range(0, 12):
                np.delete(board, [locations][columns], )
    return board


board = create_board()
print(board)
game_over = False
while not game_over:
    row = int(input("Choose row to pick from (0-11): "))
    column = int(input("Choose column from row (0-7): "))
    if valid_piece(board, row, column):
        piece = board[row][column]
        graph = {}
        player = move(board, row, column, piece, graph)
        reset_board(board, player)
        print(board)
    else:
        print("No move available at this location.")
