import copy

import pygame
import sys
import math
import time


def euclidean_distance(point0, point1):
    (x0, y0) = point0
    (x1, y1) = point1
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


class Graph:
    nodes = [
        (3, 0),
        (4, 0),
        (5, 0),
        (3, 1),
        (4, 1),
        (5, 1),
        (1, 2),
        (2, 2),
        (3, 2),
        (4, 2),
        (5, 2),
        (6, 2),
        (7, 2),
        (1, 3),
        (2, 3),
        (3, 3),
        (4, 3),
        (5, 3),
        (6, 3),
        (7, 3),
        (1, 4),
        (2, 4),
        (3, 4),
        (4, 4),
        (5, 4),
        (6, 4),
        (7, 4),
        (3, 5),
        (4, 5),
        (5, 5),
        (3, 6),
        (4, 6),
        (5, 6)
    ]
    edges = [(0, 1), (0, 2), (0, 3), (0, 4),
             (1, 2), (1, 4),
             (2, 4), (2, 5),
             (3, 4), (3, 8),
             (4, 8), (4, 9), (4, 10), (4, 5),
             (5, 10),
             (6, 7), (6, 13), (6, 14),
             (7, 8), (7, 14),
             (8, 14), (8, 15), (8, 16), (8, 9),
             (9, 10), (9, 16),
             (10, 16), (10, 17), (10, 18), (10, 11),
             (11, 12), (11, 18),
             (12, 19), (12, 18),
             (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19),
             (20, 21), (21, 22), (22, 23), (23, 24), (24, 25), (25, 26),
             (27, 28), (28, 29),
             (30, 31), (31, 32),
             (13, 20), (14, 21), (15, 22), (16, 23), (17, 24), (18, 25), (19, 26),
             (22, 27), (23, 28), (24, 29),
             (27, 30), (28, 31), (29, 32),
             (20, 14), (14, 22),
             (22, 16), (16, 24),
             (24, 18), (18, 26),
             (22, 28), (24, 28),
             (30, 28), (28, 32)]
    nodes_neighbors = {
        0: [1, 2, 3, 4],
        1: [0, 2, 4],
        2: [0, 1, 4, 5],
        3: [0, 4, 8],
        4: [0, 1, 2, 3, 8, 9, 10, 5],
        5: [2, 4, 10],
        6: [7, 13, 14],
        7: [6, 8, 14],
        8: [3, 4, 7, 14, 15, 16, 9],
        9: [4, 8, 10, 16],
        10: [4, 5, 9, 16, 17, 18, 11],
        11: [10, 12, 18],
        12: [11, 19, 18],
        13: [6, 14, 20],
        14: [6, 7, 8, 13, 15, 21, 20, 22],
        15: [8, 14, 16, 22],
        16: [8, 9, 10, 15, 17, 23, 22, 24],
        17: [10, 16, 18, 24],
        18: [10, 11, 12, 17, 19, 25, 24, 26],
        19: [12, 18, 26],
        20: [21, 13, 14],
        21: [20, 22, 14],
        22: [21, 23, 15, 27, 14, 16, 28],
        23: [22, 24, 16, 28],
        24: [23, 25, 17, 29, 16, 18, 28],
        25: [24, 26, 18],
        26: [25, 19, 18],
        27: [28, 22, 30],
        28: [27, 29, 23, 31, 22, 24, 30, 32],
        29: [28, 24, 32],
        30: [31, 27, 28],
        31: [30, 32, 28],
        32: [31, 29, 28]
    }

    middle_positions = [4, 9, 14, 15, 16, 17, 18, 23, 28]

    scale = 100
    translation = 100
    point_radius = 20
    piece_radius = 30


def get_pixels(node):
    position = [Graph.translation + Graph.scale * x for x in Graph.nodes[node]]
    return position


def get_node_from_pixels(pixels):
    [x, y] = pixels
    x = (x - Graph.translation) / Graph.scale
    y = (y - Graph.translation) / Graph.scale
    t = (x, y)
    count = 0
    for elem in Graph.nodes:
        if elem == t:
            return count
        count += 1

    return -1


class Board:

    def __init__(self, display, background_color=(88, 199, 89), lines_color=(0, 0, 0)):
        self.background_color = background_color
        self.lines_color = lines_color
        self.display = display

    def load_icons(self):
        diameter = 2 * Graph.piece_radius
        geese = pygame.image.load('icons/geese.png')
        geese = pygame.transform.scale(geese, (diameter, diameter))

        fox = pygame.image.load('icons/fox.png')
        fox = pygame.transform.scale(fox, (diameter, diameter))

        selected_geese = pygame.image.load('icons/selected.png')
        selected_geese = pygame.transform.scale(selected_geese, (diameter, diameter))

        return geese, fox, selected_geese

    def draw_game_board(self, geese, fox, player, selected=False, selected_position=None):
        nodes_coordinates = [[Graph.translation + Graph.scale * x for x in nod] for nod in Graph.nodes]
        geese_icon, fox_icon, selected_geese_icon = self.load_icons()
        self.display.fill(self.background_color)

        turn_font = pygame.font.SysFont('Lobster', 40)

        if player:
            fox_turn_text = turn_font.render('Fox Turn', True, (0, 0, 0))
            fox_turn_rect = fox_turn_text.get_rect()
            fox_turn_rect.center = (100, 100)
            self.display.blit(fox_turn_text, fox_turn_rect)
        else:
            geese_turn_text = turn_font.render('Geese Turn', True, (0, 0, 0))
            geese_turn_rect = geese_turn_text.get_rect()
            geese_turn_rect.center = (100, 100)
            self.display.blit(geese_turn_text, geese_turn_rect)

        for nod in nodes_coordinates:
            pygame.draw.circle(surface=self.display, color=self.lines_color, center=nod, radius=Graph.point_radius, width=0)

        for edge in Graph.edges:
            p0 = nodes_coordinates[edge[0]]
            p1 = nodes_coordinates[edge[1]]
            pygame.draw.line(surface=self.display, color=self.lines_color, start_pos=p0, end_pos=p1, width=5)
        for nod in geese:
            self.display.blit(geese_icon,
                         (nodes_coordinates[nod][0] - Graph.piece_radius,
                          nodes_coordinates[nod][1] - Graph.piece_radius))

        if selected:
            self.display.blit(selected_geese_icon, (nodes_coordinates[selected_position][0] - Graph.piece_radius,
                                               nodes_coordinates[selected_position][1] - Graph.piece_radius))

        self.display.blit(fox_icon,
                     (nodes_coordinates[fox][0] - Graph.piece_radius, nodes_coordinates[fox][1] - Graph.piece_radius))

        pygame.display.update()


def get_next_point(fox, goose):
    [x_fox, y_fox] = fox
    [x_goose, y_goose] = goose
    x_new = 2 * x_goose - x_fox
    y_new = 2 * y_goose - y_fox
    return [x_new, y_new]


class Game:
    P_MIN = None
    P_MAX = None

    def __init__(self, board, geese=None, fox=None):
        self.board = board
        if geese is None:
            self.geese = [6, 13, 20, 21, 22, 23, 24, 25, 26, 19, 12, 27, 28, 29, 30, 31, 32]  # default config for geese
            # self.geese = sorted(self.geese)
        else:
            self.geese = geese

        if fox is None:
            self.fox = 9
        else:
            self.fox = fox

    def check_valid_geese(self, current, destination):
        if current in self.geese:
            if destination not in self.geese and destination != self.fox:
                if destination in Graph.nodes_neighbors[current]:
                    return True
        return False

    def check_valid_fox(self, current, destination):
        if current == self.fox:
            if destination not in self.geese and destination != self.fox:
                if destination in Graph.nodes_neighbors[self.fox]:
                    return True, destination
            elif destination in self.geese and destination != self.fox and destination in Graph.nodes_neighbors[self.fox]:
                goose = destination
                goose_pixels = get_pixels(goose)
                fox_pixels = get_pixels(self.fox)
                coords = [[Graph.translation + Graph.scale * x for x in nod] for nod in Graph.nodes]
                new_point = get_next_point(fox_pixels, goose_pixels)
                if new_point in coords:
                    position = get_node_from_pixels(new_point)
                    if position not in self.geese and position != self.fox:
                        return True, position
        return False, None

    def check_endgame(self):
        if len(self.geese) <= 3:
            return True, "Fox"
        else:
            neighbors = Graph.nodes_neighbors[self.fox]
            count = 0
            for elem in neighbors:
                if elem in self.geese:
                    count += 1

            if count == len(neighbors):
                return True, "Geese"

        return False, ""

    def generate_moves_fox(self):
        neighbors = Graph.nodes_neighbors[self.fox]
        moves = [] # [ (destination, piece_taken)]
        for neighbor in neighbors:
            if neighbor in self.geese:
                value, position = self.check_valid_fox(self.fox, neighbor)
                if value:
                    if position != neighbor:
                        new_config = Game(self.board, copy.deepcopy(self.geese), self.fox)
                        new_config.geese.remove(neighbor)
                        new_config.fox = position
                        moves.append(new_config)
                    else:
                        new_config = Game(self.board, copy.deepcopy(self.geese), self.fox)
                        new_config.fox = position
                        moves.append(new_config)

        return moves

    def generate_moves_geese(self):
        moves = []
        for goose in self.geese:
            neighbors = Graph.nodes_neighbors[goose]
            for neighbor in neighbors:
                if neighbor not in self.geese:
                    value = self.check_valid_geese(goose, neighbor)
                    if value:
                        new_config = Game(self.board, copy.deepcopy(self.geese), self.fox)
                        # new_config = copy.deepcopy(self)
                        new_config.geese.remove(goose)
                        new_config.geese.append(neighbor)
                       # new_config.geese = sorted(new_config.geese)
                        if new_config not in moves:
                            moves.append(new_config)
        return moves

    def compute_score1(self):
        neighbors = Graph.nodes_neighbors[self.fox]
        count = 0
        for elem in neighbors:
            if elem in self.geese:
                count += 1

        if count == len(neighbors):
            return -1000000

        if len(self.geese) <= 3:
            return 1000000

        geese_taken = 17 - len(self.geese)

        fox_score = 20 * geese_taken

        geese_score = (-20) * count

        return fox_score + geese_score

    def compute_score2(self):
        score = self.compute_score1()
        count = 0
        neighbors = Graph.nodes_neighbors[self.fox]
        removable = 0
        for elem in neighbors:
            if elem in self.geese:
                value, destination = self.check_valid_fox(self.fox, elem)
                if value:
                    if destination != elem:
                        removable += 1
                count += 1

        score += 50 * removable
        score += (-50) * count
        return score

    def estimate_score(self, h):
        inf = 1000000000
        value, winner = self.check_endgame()
        if winner == self.__class__.P_MAX:
            return inf + h
        elif winner == self.__class__.P_MIN:
            return - inf - h
        else:
            return self.compute_score1()


class State:
    def __init__(self, game, current_player, depth, parent=None, score=0):
        # board is an instance of game class
        self.game = game
        self.current_player = current_player
        self.depth = depth
        self.parent = parent
        self.score = score
        self.next_moves = []
        self.next_state = None

    def possible_moves(self):
        if self.current_player == "fox":
            l_moves = self.game.generate_moves_fox()
            l_states = [State(move, "geese", self.depth - 1, parent=self) for move in l_moves]

            return l_states
        else:
            l_moves = self.game.generate_moves_geese()
            if self.game.geese in l_moves:
                l_moves.remove(self.game.geese)
            l_states = [State(move, "fox", self.depth - 1, parent=self) for move in l_moves]
            return l_states

    def __str__(self):
        sir = str(self.game)
        return sir

    def __repr__(self):
        sir = str(self)
        return sir


def min_max(state):
    value, winner = state.game.check_endgame()
    if state.depth == 0 or value:
        state.score = state.game.estimate_score(state.depth)
        return state

    state.next_moves = state.possible_moves()
    if len(state.next_moves) == 0:
        # print(state)
        return state
    print(state.next_moves)

    moves_with_scores = [min_max(move) for move in state.next_moves]

    if len(moves_with_scores) == 0:
        return state

    if state.current_player == Game.P_MAX:
        state.next_state = max(moves_with_scores, key=lambda x: x.score)
    else:
        state.next_state = min(moves_with_scores, key=lambda x: x.score)
    state.score = state.next_state.score
    print("aici")
    return state


def alpha_beta(alpha, beta, state):
    value, winner = state.game.check_endgame()
    if state.depth == 0 or value:
        state.score = state.game.estimate_score(state.depth)
        return state

    if alpha > beta:
        return state

    state.next_moves = state.possible_moves()

    if state.current_player == Game.P_MAX:
        current_score = float('-inf')

        for move in state.next_moves:
            new_state = alpha_beta(alpha, beta, move)
            if current_score < new_state.score:
                state.next_state = new_state
                current_score = new_state.score
            if alpha < new_state.score:
                alpha = new_state.score
                if alpha >= beta:
                    break

    elif state.current_player == Game.P_MIN:
        current_score = float('inf')

        for move in state.next_moves:
            new_state = alpha_beta(alpha, beta, move)
            if current_score > new_state.score:
                state.next_state = new_state
                current_score = new_state.score

            if beta > new_state.score:
                beta = new_state.score
                if alpha >= beta:
                    break
    state.score = state.next_state.score

    return state


class Button:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, background_color=(0, 0, 0),
                 selection_color=(227, 91, 18), text="", font="arial", font_size=20, text_color=(255, 255, 255),
                 value=""):
        self.display = display
        self.background_color = background_color
        self.selection_color = selection_color
        self.text = text
        self.font = font
        self.left = left
        self.top = top
        self.w = w
        self.h = h
        self.selected = False
        self.font_size = font_size
        self.text_color = text_color

        pygame.font.init()
        font_obj = pygame.font.SysFont('Lobster', font_size)
        self.rendered_text = font_obj.render(self.text, True, self.text_color)
        self.rectangle = pygame.Rect(left, top, w, h)

        self.text_box = self.rendered_text.get_rect(center=self.rectangle.center)
        self.value = value

    def select(self, selection):
        self.selected = selection
        self.draw()

    def select_from_coord(self, coord):
        if self.rectangle.collidepoint(coord):
            self.select(True)
            return True
        return False

    def update_rectangle(self):
        self.rectangle.left = self.left
        self.rectangle.top = self.top
        self.text_box = self.rendered_text.get_rect(center=self.rectangle.center)

    def draw(self):
        color = self.selection_color if self.selected else self.background_color
        pygame.draw.rect(self.display, color, self.rectangle)
        self.display.blit(self.rendered_text, self.text_box)


class ButtonsGroup:
    def __init__(self, buttons_list=None, selected_index=0, space=10, left=0, top=0):
        if buttons_list is None:
            buttons_list = []
        self.buttons_list = buttons_list
        self.selected_index = selected_index
        self.buttons_list[self.selected_index].selected = True
        self.top = top
        self.left = left
        current_pos = self.left
        for button in self.buttons_list:
            button.top = self.top
            button.left = current_pos
            button.update_rectangle()
            current_pos += (space + button.w)

    def select_from_coord(self, coord):
        for idx, button in enumerate(self.buttons_list):
            if button.select_from_coord(coord):
                if idx != self.selected_index:
                    self.buttons_list[self.selected_index].select(False)
                self.selected_index = idx
                return True
        return False

    def draw(self):
        for button in self.buttons_list:
            button.draw()

    def get_value(self):
        return self.buttons_list[self.selected_index].value


def draw_text(display, text, y, x, font_size=32):
    font = pygame.font.SysFont('Lobster', font_size)
    text = font.render(text, True, (0, 0, 0))
    text_box = text.get_rect()
    text_box.top = y
    text_box.left = x
    display.blit(text, text_box)


def draw_options():
    pygame.font.init()
    display = pygame.display.set_mode(size=(1000, 850))
    display.fill((88, 199, 89))
    draw_text(display, "Fox and Geese", 50, 250, 120)

    draw_text(display, "Player 1:", 150, 330, 80)
    gamemode_button = ButtonsGroup(
        top=225,
        left=330,
        buttons_list=[
            Button(display=display, w=120, h=30, text="Player", value=1),
            Button(display=display, w=120, h=30, text="Fox AI", value=2),
            Button(display=display, w=120, h=30, text="Geese AI", value=3)
        ],
        selected_index=0)

    draw_text(display, "Player 2:", 300, 330, 80)
    player_button = ButtonsGroup(
        top=375,
        left=330,
        buttons_list=[
            Button(display=display, w=120, h=30, text="Player", value=1),
            Button(display=display, w=120, h=30, text="Fox AI", value=2),
            Button(display=display, w=120, h=30, text="Geese AI", value=3)
        ],
        selected_index=0)

    draw_text(display, "Algorithm:", 450, 330, 80)
    alg_button = ButtonsGroup(
        top=525,
        left=330,
        buttons_list=[
            Button(display=display, w=120, h=35, text="minimax", value="minimax"),
            Button(display=display, w=120, h=35, text="alpha-beta", value="alpha-beta")
        ],
        selected_index=0)

    draw_text(display, "Difficulty:", 600, 330, 80)
    difficulty_button = ButtonsGroup(
        top=675,
        left=330,
        buttons_list=[
            Button(display=display, w=120, h=35, text="easy", value=2),
            Button(display=display, w=120, h=35, text="medium", value=3),
            Button(display=display, w=120, h=35, text="hard", value=4),
        ],
        selected_index=0)

    ok = Button(display=display, top=750, left=425, w=150, h=80, text="Ok", background_color=(227, 91, 18), font_size=100)
    gamemode_button.draw()
    player_button.draw()
    alg_button.draw()
    difficulty_button.draw()
    ok.draw()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not gamemode_button.select_from_coord(pos):
                    if not player_button.select_from_coord(pos):
                        if not alg_button.select_from_coord(pos):
                            if not difficulty_button.select_from_coord(pos):
                                if ok.select_from_coord(pos):
                                    display.fill((0, 0, 0))
                                    pygame.display.update()
                                    # must draw initial state
                                    return  gamemode_button.get_value(), player_button.get_value(), alg_button.get_value(), \
                                            difficulty_button.get_value()
        pygame.display.update()


def player_vs_ai(algorithm, difficulty):
    pygame.init()
    pygame.display.set_caption("Fox and Geese - Broscoteanu Daria Mihaela")
    display = pygame.display.set_mode(size=(1000, 850))

    background_color = (88, 199, 89)
    lines_color = (0, 0, 0)
    board = Board(display, background_color, lines_color)
    game = Game(board)
    game.P_MAX = "fox"
    game.P_MIN = "geese"
    current_state = State(game, 'fox', difficulty)

    current_state.game.board.draw_game_board(game.geese, game.fox, True)
    pygame.display.update()

    coords = [[Graph.translation + Graph.scale * x for x in nod] for nod in Graph.nodes]

    moved = True
    win = ""
    while moved:
        if current_state.current_player == "fox":
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for nod in coords:
                        if euclidean_distance(pos, nod) <= Graph.point_radius:
                            index = get_node_from_pixels(nod)
                            valid, dest = current_state.game.check_valid_fox(current_state.game.fox, index)
                            if valid:
                                if index in current_state.game.geese:
                                    current_state.game.geese.remove(index)
                                current_state.game.fox = dest
                                current_state.current_player = "geese"
                                current_state.game.board.draw_game_board(current_state.game.geese, current_state.game.fox, current_state.current_player)
                                value, winner = current_state.game.check_endgame()
                                if value:
                                    if winner == "Fox":
                                        win = "fox"
                                        turn_font = pygame.font.SysFont('Lobster', 100)
                                        geese_turn_text = turn_font.render('Fox Won!', True, (0, 0, 0))
                                        geese_turn_rect = geese_turn_text.get_rect()
                                        geese_turn_rect.center = (500, 425)
                                        display.blit(geese_turn_text, geese_turn_rect)
                                        current_state.game.board.draw_game_board(current_state.game.geese, current_state.game.fox, current_state.current_player)
                                        pygame.display.update()
                                        moved = False
                                        break
                                    else:
                                        win = "geese"
                                        turn_font = pygame.font.SysFont('Lobster', 100)
                                        geese_turn_text = turn_font.render('Goose Won!', True, (0, 0, 0))
                                        geese_turn_rect = geese_turn_text.get_rect()
                                        geese_turn_rect.center = (500, 425)
                                        display.blit(geese_turn_text, geese_turn_rect)
                                        current_state.game.board.draw_game_board(current_state.game.geese, current_state.game.fox, current_state.current_player)
                                        pygame.display.update()
                                        moved = False
                                        break
                                else:
                                    continue
                                # break
                            else:
                                current_state.current_player = "geese"
                                current_state.game.board.draw_game_board(current_state.game.geese, current_state.game.fox, current_state.current_player)
                                break
                        current_state.game.board.draw_game_board(current_state.game.geese, current_state.game.fox, current_state.current_player)
        else:
            print("here")
            start_t = (time.time() * 1000)
            if algorithm == 'minimax':
                new_state = min_max(current_state)
            else:
                new_state = alpha_beta(-500, 500, current_state)
            current_state.game = new_state.next_state.game
            current_state.current_player = "fox"
            final_t = int(round(time.time() * 1000))
            print("The pc \"thought\" about " + str(final_t - start_t) + " milliseconds.")

            current_state.game.board.draw_game_board(current_state.game.geese, current_state.game.fox, current_state.current_player)

        if not moved:
            if win == "fox":
                turn_font = pygame.font.SysFont('Lobster', 100)
                geese_turn_text = turn_font.render('Fox Won!', True, (255, 255, 255))
                geese_turn_rect = geese_turn_text.get_rect()
                geese_turn_rect.center = (500, 425)
                start_time = time.time()
                while time.time() - start_time < 8:
                    display.fill(background_color)
                    display.blit(geese_turn_text, geese_turn_rect)
                    pygame.display.update()
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                pygame.quit()
                sys.exit()
                # draw_game_board(display, background_color, lines_color, geese, fox, True)
            elif win == "geese":
                turn_font = pygame.font.SysFont('Lobster', 100)
                geese_turn_text = turn_font.render('Goose Won!', True, (255, 255, 255))
                geese_turn_rect = geese_turn_text.get_rect()
                geese_turn_rect.center = (500, 425)
                start_time = time.time()
                while time.time() - start_time < 8:
                    display.fill(background_color)
                    display.blit(geese_turn_text, geese_turn_rect)
                    pygame.display.update()
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                pygame.quit()
                sys.exit()


def player_vs_player():
    pygame.init()
    pygame.display.set_caption("Fox and Geese - Broscoteanu Daria Mihaela")
    display = pygame.display.set_mode(size=(1000, 850))

    background_color = (88, 199, 89)
    lines_color = (0, 0, 0)
    board = Board(display, background_color, lines_color)
    game = Game(board)
    # geese = [6, 13, 20, 21, 22, 23, 24, 25, 26, 19, 12, 27, 28, 29, 30, 31, 32]  # default config for geese
    # # geese = [6, 13, 20, 8]
    # fox = 9  # default position for fox
    # geese, fox, player, selected=False, selected_position=None
    game.board.draw_game_board(game.geese, game.fox, True)
    pygame.display.update()

    player = True

    coords = [[Graph.translation + Graph.scale * x for x in nod] for nod in Graph.nodes]

    selected = False
    index_goose = None

    moved = True
    win = ""
    while moved:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if player:
                    for nod in coords:
                        if euclidean_distance(pos, nod) <= Graph.point_radius:
                            index = get_node_from_pixels(nod)
                            valid, dest = game.check_valid_fox(game.fox, index)
                            if valid:
                                if index in game.geese:
                                    game.geese.remove(index)
                                game.fox = dest
                                player = False
                                game.board.draw_game_board(game.geese, game.fox, player)
                                value, winner = game.check_endgame()
                                if value:
                                    if winner == "Fox":
                                        win = "fox"
                                        turn_font = pygame.font.SysFont('Lobster', 100)
                                        geese_turn_text = turn_font.render('Fox Won!', True, (0, 0, 0))
                                        geese_turn_rect = geese_turn_text.get_rect()
                                        geese_turn_rect.center = (500, 425)
                                        display.blit(geese_turn_text, geese_turn_rect)
                                        game.board.draw_game_board(game.geese, game.fox, player)
                                        pygame.display.update()
                                        moved = False
                                        break
                                    else:
                                        win = "geese"
                                        turn_font = pygame.font.SysFont('Lobster', 100)
                                        geese_turn_text = turn_font.render('Goose Won!', True, (0, 0, 0))
                                        geese_turn_rect = geese_turn_text.get_rect()
                                        geese_turn_rect.center = (500, 425)
                                        display.blit(geese_turn_text, geese_turn_rect)
                                        game.board.draw_game_board(game.geese, game.fox, player)
                                        pygame.display.update()
                                        moved = False
                                        break
                                else:
                                    continue
                                # break
                            else:
                                player = False
                                game.board.draw_game_board(game.geese, game.fox, player)
                                break
                        game.board.draw_game_board(game.geese, game.fox, player)
                else: # goose turn
                    for nod in coords:
                        if euclidean_distance(pos, nod) <= Graph.point_radius:
                            index = get_node_from_pixels(nod)
                            if not selected:
                                if index in game.geese:
                                    selected = True
                                    index_goose = index
                                    game.board.draw_game_board(game.geese, game.fox, player, selected, index_goose)
                                    break
                            else:
                                if game.check_valid_geese(index_goose, index):
                                    game.geese.remove(index_goose)
                                    game.geese.append(index)
                                    selected = False
                                    index_goose = None
                                    player = True
                                    game.board.draw_game_board(game.geese, game.fox, player, selected, index_goose)
                                    value, winner = game.check_endgame()
                                    if value:
                                        if winner == "Fox":
                                            win = "fox"
                                            moved = False
                                            break
                                        else:
                                            win = "geese"
                                            moved = False
                                            break
                                    break
                                else:
                                    selected = False
                                    index_goose = None
                                    player = True
                                    game.board.draw_game_board(game.geese, game.fox, player, selected, index_goose)
                                    break

                        game.board.draw_game_board(game.geese, game.fox, player)

        if win == "fox":
            turn_font = pygame.font.SysFont('Lobster', 100)
            geese_turn_text = turn_font.render('Fox Won!', True, (255, 255, 255))
            geese_turn_rect = geese_turn_text.get_rect()
            geese_turn_rect.center = (500, 425)
            start_time = time.time()
            while time.time() - start_time < 8:
                display.fill(background_color)
                display.blit(geese_turn_text, geese_turn_rect)
                pygame.display.update()
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            pygame.quit()
            sys.exit()
            # draw_game_board(display, background_color, lines_color, geese, fox, True)
        elif win == "geese":
            turn_font = pygame.font.SysFont('Lobster', 100)
            geese_turn_text = turn_font.render('Goose Won!', True, (255, 255, 255))
            geese_turn_rect = geese_turn_text.get_rect()
            geese_turn_rect.center = (500, 425)
            start_time = time.time()
            while time.time() - start_time < 8:
                display.fill(background_color)
                display.blit(geese_turn_text, geese_turn_rect)
                pygame.display.update()
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            pygame.quit()
            sys.exit()


def run_game():
    player1, player2, algorithm, difficulty = draw_options()
    if player1 == 1 and player2 == 1:
        player_vs_player()
    elif player1 == 1 and player2 == 3:
        player_vs_ai(algorithm, difficulty)

run_game()
# player_vs_player()
# pygame.init()
# pygame.display.set_caption("Fox and Geese - Broscoteanu Daria Mihaela")
# display = pygame.display.set_mode(size=(1000, 850))
#
# background_color = (88, 199, 89)
# lines_color = (0, 0, 0)
# board = Board(display, background_color, lines_color)
# game = Game(board)
# game.P_MAX = "fox"
# game.P_MIN = "geese"
# board = Board(display, background_color, lines_color)
# game = Game(board, [6, 14, 22, 23, 24])
#
# current_state = State(game, 'fox', 1)
# print(game.geese)
# moves = game.generate_moves_geese()
# for move in moves:
#     print(move.geese)
