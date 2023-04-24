import random
import pygame
import math

# Resources:
#       4 - Forest
#       4 - Plains
#       4 - Wheat
#       3 - Brick
#       3 - Mountain
#       1 - Desert

#  Rules:
#  1: No 2 brick or stone tiles next to each other
#  2: No 3 Wheat, Sheep or Wood tiles next to each other
#  3: No two of the same number next to each other
#  4: No 6s next to 8s or other 6s and no 8s next to 6s or other 8s
#  5: No two of the same resource of the same number
#  6: No 6s or 8s on the same resource

# Initialize pygame
pygame.init()

# Set up display
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catan Board")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = {
    'brick': (191, 87, 0),
    'wood': (0, 153, 0),
    'ore': (128, 128, 128),
    'sheep': (153, 255, 153),
    'wheat': (255, 255, 102)
}


def translate_board(board):
    text_list = ['desert', 'wheat', 'wood', 'sheep', 'brick', 'ore']
    for i in range(len(board)):
        for j in range(len(board[i])):
            resource_num = board[i][j][0]
            if resource_num != 0:
                resource_text = text_list[resource_num]
                board[i][j][0] = resource_text
    return board


def get_adjacent_positions(row, col):
    #  Really bad implementation of adjacency but the pointed top hexagonal adjaceny proved to be tricky
    adjacent_tiles = {
        (0, 0): [(0, 1), (1, 0), (1, 1)],  # A
        (0, 1): [(0, 0), (1, 1), (1, 2), (0, 3)],  # B
        (0, 2): [(0, 1), (1, 2), (1, 3)],  # C
        (1, 0): [(0, 0), (1, 1), (2, 0), (2, 1)],  # D
        (1, 1): [(0, 0), (0, 1), (1, 2), (2, 2), (2, 1), (1, 0)],  # E
        (1, 2): [(0, 1), (0, 2), (1, 3), (2, 3), (2, 2), (1, 1)],  # F
        (1, 3): [(0, 2), (1, 2), (2, 3), (2, 4)],  # G
        (2, 0): [(1, 0), (2, 1), (3, 0)],  # H
        (2, 1): [(1, 0), (1, 1), (2, 2), (3, 1), (3, 0), (2, 0)],  # I
        (2, 2): [(1, 1), (1, 2), (2, 3), (3, 2), (3, 1), (2, 1)],  # J
        (2, 3): [(1, 2), (1, 3), (2, 4), (3, 3), (3, 2), (2, 2)],  # K
        (2, 4): [(1, 3), (2, 3), (3, 3)],  # L
        (3, 0): [(2, 0), (2, 1), (3, 1), (4, 0)],  # M
        (3, 1): [(2, 1), (2, 2), (3, 2), (4, 1), (4, 0), (3, 0)],  # N
        (3, 2): [(2, 2), (2, 3), (3, 3), (4, 2), (4, 1), (3, 1)],  # O
        (3, 3): [(2, 3), (2, 4), (3, 2), (4, 2)],  # P
        (4, 0): [(3, 0), (3, 1), (4, 1)],  # Q
        (4, 1): [(4, 0), (3, 1), (3, 2), (4, 2)],  # R
        (4, 2): [(4, 1), (3, 2), (3, 3)]  # S
    }

    return adjacent_tiles.get((row, col))


def get_adjacent_tiles(board, row, col):
    adjacent_positions = get_adjacent_positions(row, col)
    adjacent_tiles = [
        (board[r][c], r, c) for r, c in adjacent_positions
        if 0 <= r < len(board) and 0 <= c < len(board[r])
    ]
    return adjacent_tiles


def count_adjacent_tiles(board, row, col, resource_type):
    count = 0
    adjacent_resources = get_adjacent_tiles(board, row, col)

    for adj_tile in adjacent_resources:
        if len(adj_tile[0]) > 1 and adj_tile[0][0] == resource_type:
            count += 1

            if count == 3:
                break

            adj_adj_resources = get_adjacent_tiles(board, adj_tile[1], adj_tile[2])

            for adj_adj_tile in adj_adj_resources:
                if len(adj_adj_tile[0]) > 1 and adj_adj_tile[0][0] == resource_type:
                    count += 1

                    if count == 3:
                        break

        if count == 3:
            break

    return count


def check_board(board):
    resources_6_8 = set()

    for row in range(len(board)):
        for col in range(len(board[row])):
            current_tile = board[row][col]

            # Skip desert tile
            if len(current_tile) <= 1 and current_tile[0] == 0:
                continue

            adjacent_resources = get_adjacent_tiles(board, row, col)

            # Check 6s & 8s are not on the same resource and no 6s or 8s adjacent
            if current_tile[1] in (6, 8):
                resource_type = current_tile[0]
                # Found a duplicate 6 or 8 tile with the same resource type
                if resource_type in resources_6_8:
                    return
                resources_6_8.add(resource_type)

                for adj_tile in adjacent_resources:
                    if len(adj_tile[0]) > 1 and adj_tile[0][1] in (6, 8):
                        return

            # No 2 Brick adjacent
            if current_tile[0] in 'brick':
                for adj_tile in adjacent_resources:
                    if len(adj_tile[0]) > 1 and adj_tile[0][0] in 'brick':
                        return

            # No 2 Ore adjacent
            if current_tile[0] in 'ore':
                for adj_tile in adjacent_resources:
                    if len(adj_tile[0]) > 1 and adj_tile[0][0] in 'ore':
                        return

            # No 3 sheep adjacent
            if current_tile[0] == 'sheep':
                sheep_count = count_adjacent_tiles(board, row, col, 'sheep')

                if sheep_count >= 3:
                    return

            # No 3 wood adjacent
            if current_tile[0] == 'wood':
                wood_count = count_adjacent_tiles(board, row, col, 'wood')

                if wood_count >= 3:
                    return

            # No 3 wheat adjacent
            if current_tile[0] == 'wheat':
                wheat_count = count_adjacent_tiles(board, row, col, 'wheat')

                if wheat_count >= 3:
                    return

            # Check neighbouring numbers are not equal
            for adj_tile in adjacent_resources:
                if len(adj_tile[0]) > 1 and current_tile[1] == adj_tile[0][1]:
                    return

    return board


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
    # print(board_texted)
    checked_board = check_board(board_texted)
    return checked_board


def draw_hexagon(surface, x, y, size, color):
    points = []
    for angle in range(30, 390, 60):
        px = x + size * math.cos(math.radians(angle))
        py = y + size * math.sin(math.radians(angle))
        points.append((px, py))
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, BLACK, points, 1)


def draw_text(surface, text, x, y, size, color=BLACK):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)


def draw_catan_board(surface, board):
    size = 60
    h_offset = size * math.sqrt(3)
    v_offset = size * 1.5

    starting_positions = [
        (width / 2 - size - 100, height / 2 - v_offset * 2),
        (width / 2 - h_offset - size / 6 - 100, height / 2 - v_offset),
        (width / 2 - h_offset * 1.6 - 100, height / 2),
        (width / 2 - h_offset - size / 6 - 100, height / 2 + v_offset),
        (width / 2 - size - 100, height / 2 + v_offset * 2)
    ]

    for row_data, start in zip(board, starting_positions):
        x, y = start
        for tile_data in row_data:
            if len(tile_data) == 2:
                resource, number = tile_data
                color = COLORS[resource]
                draw_hexagon(surface, x, y, size, color)
                text_color = (255, 0, 0) if number in [6, 8] else BLACK
                draw_text(surface, str(number), x, y, 24, text_color)
            else:
                draw_hexagon(surface, x, y, size, WHITE)
            x += h_offset
        y += v_offset


def draw_legend(surface):
    legend_x = 850
    legend_y_start = 100
    legend_y_offset = 60
    legend_size = 30
    text_offset = legend_size * 2

    for idx, (resource, color) in enumerate(COLORS.items()):
        draw_hexagon(surface, legend_x, legend_y_start + idx * legend_y_offset, legend_size, color)
        draw_text(surface, resource.capitalize(), legend_x + text_offset, legend_y_start + idx * legend_y_offset, 24)


if __name__ == '__main__':
    # Generate the board
    board_generated = False
    count = 0
    while not board_generated:
        board = board_layout()
        count = count + 1
        if board is not None:
            board_generated = True
    print()
    print(board)
    print('Attempts to generate board: ', count)
    # Draw the board
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_catan_board(screen, board)
        draw_legend(screen)
        pygame.display.flip()

    pygame.quit()
