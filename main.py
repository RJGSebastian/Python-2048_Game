import inspect
import pygame
import random

from termcolor import cprint

pygame.init()

DEBUG = False
CONSOLE = False
COLOURS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0)
}
screen_height = 400
screen_width = 400
border = 20
tiles = 0
tile_size = 80

score_val = 0

large_font = pygame.font.Font('freesansbold.ttf', 115)
normal_font = pygame.font.Font('freesansbold.ttf', 20)


def debug_method(msg):
    trace = True
    i = 0
    cprint(f'<debug_msg>   {msg}', 'yellow')
    while trace:
        try:
            cprint(f' <debug_trace> {inspect.stack()[i][1]} | {inspect.stack()[i][2]} | {inspect.stack()[i][3]}',
                   'yellow')
        except IndexError:
            trace = False
        i += 1
    print('')


def is_num(value):
    if DEBUG: debug_method(f'testing if {value} is an number')
    if DEBUG: debug_method(f'{value} is of type {type(value)}')
    try:
        value = int(value)
        if type(value) == int:
            return True
    except ValueError:
        if DEBUG: debug_method(f'{value} is not a number')
        return False


def menu_loop():
    global tiles
    if DEBUG: debug_method(f'starting <menu> loop')

    menu_height = 400
    menu_width = 400

    menu_screen = pygame.display.set_mode((menu_width, menu_height))
    pygame.display.set_caption('2048 - Menu')
    if DEBUG: debug_method(f'created new display (menu_screen): {menu_screen}')

    clock = pygame.time.Clock()

    input_box = pygame.Rect(10, 200, 100, 32)

    ib_colour_inactive = COLOURS['black']
    ib_colour_active = COLOURS['red']
    color = ib_colour_inactive
    active = False
    text = 'PLEASE ENTER GAME SIZE'

    menu = True
    start_game = False

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if DEBUG: debug_method(f'quitting menu')
                menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                    text = ''
                else:
                    active = False
                    if text == '' or text == 'PLEASE ENTER GAME SIZE':
                        text = 'PLEASE ENTER GAME SIZE'
                    else:
                        if not is_num(text):
                            text = 'PLEASE ENTER A NUMBER'
                        else:
                            value = int(text)
                            if value < 3:
                                text = 'PLEASE ENTER A HIGHER NUMBER'
                            elif value > 8:
                                text = 'PLEASE ENTER A SMALLER NUMBER'
                color = ib_colour_active if active else ib_colour_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and is_num(text):
                        value = int(text)
                        if value < 3:
                            text = 'PLEASE ENTER A HIGHER NUMBER'
                        elif value > 8:
                            text = 'PLEASE ENTER A SMALLER NUMBER'
                        else:
                            tiles = value
                            start_game = True
                            menu = False
                        active = False
                        color = ib_colour_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        menu_screen.fill(COLOURS['white'])

        menu_text = large_font.render('MENU', True, COLOURS['black'])
        menu_screen.blit(menu_text, (10, 10))

        txt_surface = normal_font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        menu_screen.blit(txt_surface, (input_box.x+5, input_box.y+5))

        pygame.display.update()

        clock.tick(30)

    if start_game:
        if DEBUG: debug_method(f'selected tiles: {tiles}x{tiles}')
        game_loop()


def game_loop():
    if DEBUG: debug_method(f'starting <game> loop')

    board = init_board()
    if CONSOLE: print_board_in_console(board)

    game_height = border + tile_size + border + tile_size * tiles + border
    game_width = border + tile_size * tiles + border

    game_screen = pygame.display.set_mode((game_width, game_height))
    pygame.display.set_caption(f'2048 - Game {tiles}x{tiles}')
    field = pygame.Rect((border - 2), (border * 2 + tile_size - 2), (tiles * tile_size + 4), (tiles * tile_size + 4))

    if DEBUG: debug_method(f'created new display (game_screen): {game_screen}')

    tile_list = init_draw_board()

    game = True
    open_menu = False
    game_over = [False, False, False, False, False]

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if DEBUG: debug_method(f'quitting game')
                game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    game = False
                    open_menu = True
                if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_KP8:
                    if not game_over[1]:
                        if DEBUG: debug_method(f'moving tiles up')

                        move_tile(board, 'up')
                        if not game_over[0]: new_tile(board)

                        game_over = game_over_check(board)
                        if DEBUG: debug_method(f'game over: {game_over}')

                        if CONSOLE: print_board_in_console(board)

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_KP6:
                    if not game_over[2]:
                        if DEBUG: debug_method(f'moving tiles right')

                        move_tile(board, 'right')
                        if not game_over[0]: new_tile(board)

                        game_over = game_over_check(board)
                        if DEBUG: debug_method(f'game over: {game_over}')

                        if CONSOLE: print_board_in_console(board)

                if event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_KP2:
                    if not game_over[3]:
                        if DEBUG: debug_method(f'moving tiles down')

                        move_tile(board, 'down')
                        if not game_over[0]: new_tile(board)

                        game_over = game_over_check(board)
                        if DEBUG: debug_method(f'game over: {game_over}')

                        if CONSOLE: print_board_in_console(board)

                if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_KP4:
                    if not game_over[4]:
                        if DEBUG: debug_method(f'moving tiles left')

                        move_tile(board, 'left')
                        if not game_over[0]: new_tile(board)

                        game_over = game_over_check(board)
                        if DEBUG: debug_method(f'game over: {game_over}')

                        if CONSOLE: print_board_in_console(board)

        if game_over[0] and game_over[1] and game_over[2] and game_over[3] and game_over[4]:
            game = False

        game_screen.fill(COLOURS['black'])
        pygame.draw.rect(game_screen, COLOURS['white'], field)
        score_text = normal_font.render(str(score_val), True, COLOURS['white'])
        game_screen.blit(score_text, (border, int(tile_size / 2 + border)))
        draw_board(tile_list, board, game_screen)

        pygame.display.update()

    if not game and open_menu:
        menu_loop()


def init_board():
    if DEBUG: debug_method(f'initialising board with {tiles} rows and {tiles} columns')
    temp_board = []

    for row in range(tiles):

        temp_board.append([])
        for column in range(tiles):
            temp_board[row].append(0)  # the value of the tile is 2 ** board[row][column]
        if DEBUG: debug_method(f'row {row}: {temp_board[row]}')

    return temp_board


def print_board_in_console(board):
    if DEBUG: debug_method(f'printing board with {tiles} rows and {tiles} columns')

    for row in board:
        temp_str = f'{row}:  '
        for value in row:
            if value != 0:
                temp_str = temp_str + f'{2 ** value} '
            else:
                temp_str = temp_str + f'  '
        print(temp_str)


def init_draw_board():
    y = border + tile_size + border

    temp_tile_list = []

    for row in range(tiles):
        x = border

        temp_tile_list.append([])
        for column in range(tiles):
            temp_tile_list[row].append(pygame.Rect(x + 2, y + 2, tile_size - 4, tile_size - 4))
            x += tile_size
        y += tile_size

    return temp_tile_list


def draw_board(tile_list, board, surface):
    y = border + tile_size + border
    for row in range(tiles):
        x = border

        for column in range(tiles):
            pygame.draw.rect(surface, colour(board[row][column]), tile_list[row][column])
            if board[row][column] != 0:
                value = normal_font.render(f'{2 ** board[row][column]}', True, COLOURS['black'])
                surface.blit(value, (
                    int(x + (tile_size - value.get_rect().width) / 2),
                    int(y + (tile_size - value.get_rect().height) / 2)))
            x += tile_size
        y += tile_size


def colour(value):
    if value != 0:
        colour_val = ((value - 1) // 5) + 1
        colour_val_r = (value - 1) % 5
    else:
        colour_val = 0
        colour_val_r = 0

    if colour_val == 0:
        r_val = 255
        g_val = 255
        b_val = 255

    elif colour_val == 1:
        r_val = 255
        g_val = 255
        b_val = 215 - 40 * colour_val_r

    elif colour_val == 2:
        r_val = 255
        g_val = 215 - 40 * colour_val_r
        b_val = 0

    elif colour_val == 3:
        r_val = 255
        g_val = 0
        b_val = 55 + 40 * colour_val_r

    elif colour_val == 4:
        r_val = 215 - 40 * colour_val_r
        g_val = 0
        b_val = 255

    elif colour_val == 5:
        r_val = 0
        g_val = 55 + 40 * colour_val_r
        b_val = 255

    elif colour_val == 6:
        r_val = 0
        g_val = 255
        b_val = 215 - 40 * colour_val_r

    elif colour_val == 7:
        r_val = 0
        g_val = 215 - 40 * colour_val_r
        b_val = 0

        if g_val < 55: g_val = 0
    else:
        r_val = 0
        g_val = 0
        b_val = 0

    rgb = (r_val, g_val, b_val)

    return rgb


def move_tile(board, direction):
    global score_val
    if DEBUG: debug_method(f'moving tiles in direction {direction}')

    if direction == 'up':
        j = 0
        while j < tiles:
            i = 0
            while i < tiles:
                if DEBUG: debug_method(f'tile ({j} | {i}) is: {board[j][i]}')
                if board[j][i] == 0:
                    f = False
                    for c in range(j + 1, tiles, +1):
                        if not f and board[c][i] != 0:
                            board[j][i] = board[c][i]
                            board[c][i] = 0
                            f = True
                            i -= 1
                else:
                    f = False
                    for c in range(j + 1, tiles, +1):
                        if not f and board[j][i] == board[c][i]:
                            board[j][i] += 1
                            board[c][i] = 0
                            f = True

                            score_val += 2 ** board[j][i]
                            if DEBUG: debug_method(f'new score: {score_val} ({2 ** board[j][i]})')
                if DEBUG: print_board_in_console(board)

                i += 1
            j += 1
    elif direction == 'right':
        j = tiles - 1
        while j > -1:
            i = 0
            while i < tiles:
                if DEBUG: debug_method(f'tile ({i} | {j}) is: {board[i][j]}')
                if board[i][j] == 0:
                    f = False
                    for c in range(j - 1, -1, -1):
                        if not f and board[i][c] != 0:
                            board[i][j] = board[i][c]
                            board[i][c] = 0
                            f = True
                            i -= 1
                else:
                    f = False
                    for c in range(j - 1, -1, -1):
                        if not f and board[i][j] == board[i][c]:
                            board[i][j] += 1
                            board[i][c] = 0
                            f = True

                            score_val += 2 ** board[i][j]
                            if DEBUG: debug_method(f'new score: {score_val} ({2 ** board[i][j]})')
                if DEBUG: print_board_in_console(board)

                i += 1
            j -= 1
    elif direction == 'down':
        j = tiles - 1
        while j > -1:
            i = 0
            while i < tiles:
                if DEBUG: debug_method(f'tile ({j} | {i}) is: {board[j][i]}')
                if board[j][i] == 0:
                    f = False
                    for c in range(j - 1, -1, -1):
                        if not f and board[c][i] != 0:
                            board[j][i] = board[c][i]
                            board[c][i] = 0
                            f = True
                            i -= 1
                else:
                    f = False
                    for c in range(j - 1, -1, -1):
                        if not f and board[j][i] == board[c][i]:
                            board[j][i] += 1
                            board[c][i] = 0
                            f = True

                            score_val += 2 ** board[j][i]
                            if DEBUG: debug_method(f'new score: {score_val} ({2 ** board[j][i]})')
                if DEBUG: print_board_in_console(board)

                i += 1
            j -= 1
    elif direction == 'left':
        j = 0
        while j < tiles:
            i = tiles - 1
            while i > -1:
                if DEBUG: debug_method(f'tile ({i} | {j}) is: {board[i][j]}')
                if board[i][j] == 0:
                    f = False
                    for c in range(j + 1, tiles, +1):
                        if not f and board[i][c] != 0:
                            board[i][j] = board[i][c]
                            board[i][c] = 0
                            f = True
                            i += 1
                else:
                    f = False
                    for c in range(j + 1, tiles, +1):
                        if not f and board[i][j] == board[i][c]:
                            board[i][j] += 1
                            board[i][c] = 0
                            f = True

                            score_val += 2 ** board[i][j]
                            if DEBUG: debug_method(f'new score: {score_val} ({2 ** board[i][j]})')
                if DEBUG: print_board_in_console(board)

                i -= 1
            j += 1


def game_over_check(board):
    if DEBUG: debug_method(f'checking for game over')
    not_free = [True, True, True, True, True]
    for row in range(0, tiles, +1):
        for column in range(0, tiles, +1):
            try:
                if board[row][column] == 0:
                    not_free[0] = False
            except IndexError:
                pass
            try:
                if (board[row][column] == board[row - 1][column] or board[row - 1][column] == 0) and \
                        board[row][column] != 0:
                    not_free[1] = False
            except IndexError:
                pass
            try:
                if (board[row][column] == board[row][column + 1] or board[row][column + 1] == 0) and \
                        board[row][column] != 0:
                    not_free[2] = False
            except IndexError:
                pass
            try:
                if (board[row][column] == board[row + 1][column] or board[row + 1][column] == 0) and \
                        board[row][column] != 0:
                    not_free[3] = False
            except IndexError:
                pass
            try:
                if (board[row][column] == board[row][column - 1] or board[row][column - 1] == 0) and \
                        board[row][column] != 0:
                    not_free[4] = False
            except IndexError:
                pass

    if CONSOLE: print(not_free)

    return not_free


def new_tile(board):
    if DEBUG: debug_method(f'placing new tile')
    found = False
    while not found:
        x = random.randint(0, tiles - 1)
        y = random.randint(0, tiles - 1)

        if DEBUG: debug_method(f'checking tile at ( x: {x} | y: {y} )')

        if board[y][x] == 0:
            if DEBUG: debug_method(f'placing new tile at ( x: {x} | y: {y} )')
            board[y][x] = 1
            found = True


if DEBUG: debug_method(f'Debug activated')
elif not DEBUG: debug_method(f'Debug deactivated')

if CONSOLE: print('Console activated')
elif not CONSOLE: print('Console deactivated')

menu_loop()  # the game starts in the menu window

