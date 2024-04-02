import pygame,sys
import random
from button import Button

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
BG = (255, 255, 255) 
TEXT_COLOR = (0,0,0)
SCREEN.fill(BG)
pygame.display.flip()
counter = 0
def sudoku(difficulty):
    board=[[0 for _ in range(9)] for _ in range(9)]
    fill_board(board)
    attempts = 2
    if difficulty == 'Easy':
        attempts +=1
    elif difficulty == 'Medium':
        attempts += 2
    elif difficulty == 'Hard':
        attempts += 3
    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        while board[row][col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

        backup = board[row][col]
        board[row][col] = 0

        copy_grid = board[:]

        solveGrid(copy_grid)
        if counter != 1:
            board[row][col] = backup
            attempts -= 1
def solveGrid(grid):
    global counter
    for i in range(0, 81):
        row = i // 9
        col = i % 9
        if grid[row][col] == 0:
            for value in range(1, 10):
                if value not in grid[row]:
                    if value not in (row[col] for row in grid):
                        square = []
                        box_row = row - row % 3
                        box_col = col - col % 3
                        for i in range(3):
                            for j in range(3):
                                square.append(grid[box_row + i][box_col + j])
                        if value not in square:
                            grid[row][col] = value
                            if checkGrid(grid):
                                counter += 1
                                break
                            else:
                                if solveGrid(grid):
                                    return True
            break
    grid[row][col] = 0

def checkGrid(grid):
    for row in range(0, 9):
        for col in range(0, 9):
            if grid[row][col] == 0:
                return False
    return True

def fill_board(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if (
                        num not in board[i] and
                        num not in (row[j] for row in board) and
                        is_valid_box(board, i, j, num)
                    ):
                        board[i][j] = num
                        if fill_board(board):
                            return True
                        board[i][j] = 0
                return False
    return True

def is_valid_box(board, row, col, num):
    box_row = row - row % 3
    box_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False
    return True
def play():
    SCREEN.fill(BG)
    pygame.display.flip()
    
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        DIF_TEXT = pygame.font.Font(None, 100).render("SELECT DIFICULTY", True, 'Black')
        DIF_RECT = DIF_TEXT.get_rect(center=(640, 100))
        EASY_BUTTON = Button(image=None, pos=(640, 250), text_input="EASY", font=pygame.font.Font(None, 75), base_color='#bed4eb', hovering_color='#d8e5f2')
        MEDIUM_BUTTON = Button(image=None, pos=(640, 400), text_input="MEDIUM", font=pygame.font.Font(None, 75), base_color='#bed4eb', hovering_color='#d8e5f2')
        HARD_BUTTON = Button(image=None, pos=(640, 550), text_input="HARD", font=pygame.font.Font(None, 75), base_color='#bed4eb', hovering_color='#d8e5f2')
        SCREEN.blit(DIF_TEXT, DIF_RECT)
        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON]:
            button.changecolor(PLAY_MOUSE_POS)
            button.update(SCREEN)
        PLAY_BACK = Button(image=None, pos=(640, 700), text_input="BACK", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="Green")

        PLAY_BACK.changecolor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkforinput(PLAY_MOUSE_POS):
                    main_menu()
                if EASY_BUTTON.checkforinput(PLAY_MOUSE_POS):
                    sudoku('easy')
                if EASY_BUTTON.checkforinput(PLAY_MOUSE_POS):
                    sudoku('medium')
                if EASY_BUTTON.checkforinput(PLAY_MOUSE_POS):
                    sudoku('hard')
        pygame.display.update()

def options():
    SCREEN.fill(BG)
    pygame.display.flip()
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_TEXT = pygame.font.Font(None,45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), text_input="BACK", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changecolor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkforinput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    pygame.display.set_caption("Menu")
    SCREEN.fill('black')
    SCREEN.fill(BG)
    pygame.display.flip()

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = pygame.font.Font(None, 100).render("SUDOKU", True, 'Black')
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        PLAY_BUTTON = Button(image=None, pos=(640, 250), text_input="PLAY", font=pygame.font.Font(None, 75), base_color='#bed4eb', hovering_color='#d8e5f2')
        OPTIONS_BUTTON = Button(image=None, pos=(640, 400), text_input="OPTIONS", font=pygame.font.Font(None, 75), base_color='#bed4eb', hovering_color='#d8e5f2')
        QUIT_BUTTON = Button(image=None, pos=(640, 550), text_input="QUIT", font=pygame.font.Font(None, 75), base_color='#bed4eb', hovering_color='#d8e5f2')
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changecolor(MENU_MOUSE_POS)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkforinput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkforinput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkforinput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

main_menu()