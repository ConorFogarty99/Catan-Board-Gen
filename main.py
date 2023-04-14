import random


# Resources:
#       4 - Forest
#       4 - Plains
#       4 - Wheat
#       3 - Brick
#       3 - Mountain
#       1 - Desert

#  Rules:
#      1: No 2 brick or stone tiles next to e/o
#      2: No 3 Wheat, Sheep or Wood tiles next to e/o
#      3: No two of the same number next to e/o
#      4: No 6s or 8s next to e/o
#      5: No two of the same resource of the same number
#      6: No 6s or 8s on the same resource

def translate_board(board):
    text_list = ['desert', 'wheat', 'wood', 'sheep', 'brick', 'ore']
    for i in range(len(board)):
        for j in range(len(board[i])):
            resource_num = board[i][j][0]
            if resource_num != 0:
                resource_text = text_list[resource_num]
                board[i][j][0] = resource_text
    return board


def check_board(board):
    # Loop over each row
    for row in range(len(board)):
        # Loop over each tile in the row
        for col in range(len(board[row])):
            # Get the current tile
            current_tile = board[row][col]

            # Get the adjacent tiles
            if row % 2 == 0:
                # Even row
                top_left = (row - 1, col)
                top_right = (row - 1, col + 1)
                left = (row, col - 1)
                right = (row, col + 1)
                bottom_left = (row + 1, col)
                bottom_right = (row + 1, col + 1)
            else:
                # Odd row
                top_left = (row - 1, col - 1)
                top_right = (row - 1, col)
                left = (row, col - 1)
                right = (row, col + 1)
                bottom_left = (row + 1, col - 1)
                bottom_right = (row + 1, col)

            adjacent_tiles = [top_left, top_right, left, right, bottom_left, bottom_right]
            adjacent_resources = [board[row][col] for row, col in adjacent_tiles if
                                  0 <= row < len(board) and 0 <= col < len(board[row])]

            # print(current_tile, adjacent_resources)

            # Rule 1: No 2 brick or stone tiles next to e/o
            if current_tile[0] == 'brick' or current_tile[0] == 'ore':
                same_resource_adjacent = False
                for adj_tile in adjacent_resources:
                    if adj_tile[0] == current_tile[0]:
                        same_resource_adjacent = True
                        break
                if same_resource_adjacent:
                    print("Rule 1: No 2 brick or stone tiles next to e/o violation at", (row, col))
                    print("Regenerating the board...")
                    board_layout()
                    return

    return True


def board_layout():
    resource_list = [0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5]
    numbers_list = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    board = [[], [], [], [], []]
    row_len = [3, 4, 5, 4, 3]

    for i, row_len in enumerate(row_len):
        while len(board[i]) < row_len:
            resource = random.choice(resource_list)
            board[i].append([resource])
            resource_list.remove(resource)

    # Looping through the board and the rows
    # If the tile is != desert continue
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            if tile[0] != 0 and numbers_list:
                number = random.choice(numbers_list)
                board[i][j].append(number)
                numbers_list.remove(number)

    board_texted = translate_board(board)
    check_board(board_texted)


if __name__ == '__main__':
    board_generated = False
    while not board_generated:
        board = board_layout()
        if board is not None:
            board_generated = True
    # board_texted = translate_board(board)
    print(board)
