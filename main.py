import pygame
import sys

# Ініціалізація Pygame
pygame.init()

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Розміри та параметри клітини
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Створення вікна
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

# Шрифт для відображення тексту
font = pygame.font.Font(None, 36)

# Основний клас гри
class Game:
    def __init__(self):
        self.board = [
            [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'],
            ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '],
            [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
            [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'],
            ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' ']
        ]
        self.selected_piece = None
        self.turn = 'W'  # 'W' це білий, 'B' це чорний 
        self.game_over = False  # Додайте змінну для перевірки кінця гри

    def draw_board(self):
        win.fill(WHITE)
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(win, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(win, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 'W':
                    pygame.draw.circle(win, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
                elif self.board[row][col] == 'B':
                    pygame.draw.circle(win, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)

    def get_clicked_position(self, pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col

    def is_valid_move(self, start, end):
        # Перевірте, чи рух знаходиться в межах
        if not (0 <= end[0] < ROWS and 0 <= end[1] < COLS):
            return False

        # Перевірте, чи місце призначення порожнє
        if self.board[end[0]][end[1]] != ' ':
            return False

        # Визначити напрямок руху
        direction = 1 if self.turn == 'W' else -1

        # по діагоналі вперед
        if end[0] == start[0] + direction and abs(end[1] - start[1]) == 1:
            return True

        # стрибок через фігуру суперника
        if end[0] == start[0] + 2 * direction and abs(end[1] - start[1]) == 2:
            jumped_piece_row = (start[0] + end[0]) // 2
            jumped_piece_col = (start[1] + end[1]) // 2
            if self.board[jumped_piece_row][jumped_piece_col] != ' ' and self.board[jumped_piece_row][jumped_piece_col] != self.turn:
                return True

        return False

    def make_move(self, start, end):
        self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = ' '

        # Перевірте, чи це хід захоплення
        if abs(end[1] - start[1]) == 2:
            jumped_piece_row = (start[0] + end[0]) // 2
            jumped_piece_col = (start[1] + end[1]) // 2
            self.board[jumped_piece_row][jumped_piece_col] = ' jump'

    def switch_turn(self):
        self.turn = 'B' if self.turn == 'W' else 'W'

    def is_winner(self):
        # Перевірка, чи немає в одного гравця фігур
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != ' ' and self.board[row][col].startswith(self.turn):
                    return False
        print(f"Player {self.turn} wins!")
        return True if self.turn == 'B' else False


    # обробляти клацання миші
    def handle_mouse_click(self, event): 
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = self.get_clicked_position(pos)
            if 0 <= row < ROWS and 0 <= col < COLS:
                if self.selected_piece is None:
                    if self.board[row][col] != ' ' and self.board[row][col].startswith(self.turn):
                        self.selected_piece = (row, col)
                else:
                    if (row, col) == self.selected_piece:
                        self.selected_piece = None
                    elif self.is_valid_move(self.selected_piece, (row, col)):
                        self.make_move(self.selected_piece, (row, col))
                        self.switch_turn()
                        self.selected_piece = None

    def draw_winner_message(self, winner):
        text = font.render(f"Player {winner} wins!", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        win.blit(text, text_rect)

    def play(self):
        run = True
        while run:  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

                self.handle_mouse_click(event)  

            self.draw_board()
            self.draw_pieces()
            pygame.display.update()

            if self.is_winner():
                self.game_over = True  # Змініть статус гри на завершено
                break

        # Виведення повідомлення про переможця після завершення гри
        self.draw_board()
        self.draw_pieces()
        self.draw_winner_message(self.turn)  # Виведення переможця
        pygame.display.update()
        pygame.time.wait(3000)  # Затримка для перегляду повідомлення


# Запуск гри
if __name__ == "__main__":
    game = Game()
    game.play()
