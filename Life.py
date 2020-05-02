import pygame, numpy as np


class Field:
    def __init__(self, screen, rows, cols, left=0, top=0, cell_size=30):
        self.screen = screen
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.left = left
        self.top = top
        self.field = [[0] * cols for _ in range(rows)]

    def render(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.field[x][y]:
                    pygame.draw.rect(self.screen, pygame.Color('red'),
                                     (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                      self.cell_size + self.left, self.cell_size + self.top), )
                pygame.draw.rect(self.screen, pygame.Color('white'),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size + self.left, self.cell_size + self.top), 1)

    def on_click(self, cell):
        y, x = cell
        self.field[x][y] = not self.field[x][y]

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= cell_x <= self.cols and 0 <= cell_y <= self.rows:
            return cell_y, cell_x

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


class Life(Field):
    def __init__(self, screen, rows, cols, left=0, top=0, cell_size=30):
        super().__init__(screen, rows, cols, left, top, cell_size)
        self.field = np.zeros((rows, cols), dtype='i1')

    def next_population(self):
        neighbors = sum([
            np.roll(np.roll(self.field, -1, 1), 1, 0),
            np.roll(np.roll(self.field, 1, 1), -1, 0),
            np.roll(np.roll(self.field, 1, 1), 1, 0),
            np.roll(np.roll(self.field, -1, 1), -1, 0),
            np.roll(self.field, 1, 1),
            np.roll(self.field, -1, 1),
            np.roll(self.field, 1, 0),
            np.roll(self.field, -1, 0)
        ])
        self.field = (neighbors == 3) | (self.field & (neighbors == 2))


if __name__ == '__main__':
    pygame.init()
    size = 650, 650
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    board = Life(screen, 30, 30)

    fps = 100
    font = pygame.font.Font(None, 10)
    text = font.render(str(fps), 1, (255, 0, 0))

    time_on = False
    running = True
    delay = 100
    ticks = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                time_on = not time_on
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                delay = min(100, delay + 1)
                text = font.render(str(delay), 1, (255, 0, 0))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                delay = max(1, delay - 1)
                text = font.render(str(delay), 1, (255, 0, 0))

        screen.fill((0, 0, 0))
        screen.blit(text, (size[0] - 30, 5))
        board.render()

        if ticks >= delay:
            if time_on:
                board.next_population()
            ticks = 0
        pygame.display.flip()
        clock.tick(fps)
        ticks += 1

    pygame.quit()