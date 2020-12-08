import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 20

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        color = pygame.Color(255, 255, 255)
        for j in range(self.height):
            for i in range(self.width):
                if self.board[j][i] == 1:
                    pygame.draw.rect(screen, pygame.Color('green'), (
                        self.left + j * self.cell_size + 1, self.top + i * self.cell_size + 1,
                        self.cell_size - 1,
                        self.cell_size - 1))
                pygame.draw.rect(screen, color, (
                    self.left + i * self.cell_size, self.top + j * self.cell_size, self.cell_size,
                    self.cell_size), 1)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if (0 <= cell_x < self.width) and (0 <= cell_y < self.height):
            return (cell_x, cell_y)

    def on_click(self, cell_coords):
        x, y = cell_coords
        self.board[x][y] = (self.board[x][y] + 1) % 2

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


class Life(Board):
    def __init__(self, width, height, left=10, top=1, cell_size=20):
        super().__init__(width, height)
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def count_near_life(self, x, y):
        count = 0
        deltas = [(delta_x, delta_y) for delta_x in [-1, 0, 1] for delta_y in [-1, 0, 1] if
                  delta_x != 0 or delta_y != 0]
        for delta_x, delta_y in deltas:
            new_x, new_y = x + delta_x, y + delta_y
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                if self.board[x + delta_x][y + delta_y] == 1:
                    count += 1
        return count

    def next_move(self):
        new_board = [[0] * self.width for _ in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] == 0 and self.count_near_life(x, y) == 3:
                    new_board[x][y] = 1
                if self.board[x][y] == 1:
                    if 2 <= self.count_near_life(x, y) <= 3:
                        new_board[x][y] = 1
                    else:
                        new_board[x][y] = 0
        self.board = new_board


if __name__ == '__main__':
    pygame.init()
    size = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инициализация игры')
    board = Life(25, 25)
    running = True
    lifing = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    lifing = not lifing
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        if lifing:
            board.next_move()
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
    pygame.quit()
