import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("Djistras Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def __hash__(self):
        return hash((self.row, self.col))

    def get_pos(self):
        return self.row, self.col

    def is_already_visited(self):
        return self.color == RED

    def is_not_visited(self):
        return self.color == GREEN

    def is_blocked(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE
        return

    def set_closed(self):
        self.color = RED

    def set_open(self):
        self.color = GREEN

    def set_block(self):
        self.color = BLACK

    def set_end(self):
        self.color = TURQUOISE

    def set_start(self):
        self.color = ORANGE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        return

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_blocked():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_blocked():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_blocked():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_blocked():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False




def reconstruct_path(path, cur, draw, start):
    for cur in path:
        if cur != start:
            cur.make_path()
        draw()


def algorithm(draw, grid, start, end):
    pq = PriorityQueue()
    pq.put((0, start, []))
    distances = {node: float('inf') for row in grid for node in row}
    distances[start] = 0

    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pair = pq.get()
        cur_dis = pair[0]
        cur_node = pair[1]
        path = pair[2]

        if cur_node == end:
            # make path
            end.set_end()
            reconstruct_path(path, end, draw, start)
            return True
        path = path+[cur_node]
        for neighbor in cur_node.neighbors:
            dis = cur_dis +1
            if dis < distances[neighbor]:
                distances[neighbor] = dis
                pq.put((dis,neighbor,path))
                neighbor.set_open()


        draw()

        if cur_node != start:
            cur_node.set_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(mouse_pos, rows, width):
    gap = width // rows
    x, y = mouse_pos

    row = x // gap
    col = y // gap
    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True

    while (run):
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                # left mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.set_start()

                elif not end and node != start:
                    end = node
                    end.set_end()

                elif node != start and node != end:
                    node.set_block()



            elif pygame.mouse.get_pressed()[2]:
                # right mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WINDOW, WIDTH)
