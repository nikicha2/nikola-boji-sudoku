import pygame,sys
import random
from button import Button

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
BG = (255, 255, 255) 
TEXT_COLOR = '#000000'
SCREEN.fill(BG)
pygame.display.flip()
counter=0

def sudoku(difficulty):
    pygame.display.set_caption(difficulty + ' Sudoku')
    board = final_board(difficulty)
    SCREEN.fill(BG)
    pygame.display.flip()
    grid_width = 450
    grid_height = 450
    pygame.draw.rect(SCREEN, TEXT_COLOR, pygame.Rect(410, 100, grid_width, grid_height), 8)
    for i in range(1, 9):
        if i % 3 == 0:
            pygame.draw.line(SCREEN, TEXT_COLOR, pygame.Vector2((i * 50 + 410), 100), pygame.Vector2((i * 50 + 410), 545), 7)
            pygame.draw.line(SCREEN, TEXT_COLOR, pygame.Vector2((410, (i * 50 + 100))), pygame.Vector2(855, (i * 50 + 100)), 7)
        else:
            pygame.draw.line(SCREEN, TEXT_COLOR, pygame.Vector2((i * 50 + 410), 100), pygame.Vector2((i * 50 + 410), 545), 3)
            pygame.draw.line(SCREEN, TEXT_COLOR, pygame.Vector2((410, (i * 50 + 100))), pygame.Vector2(855, (i * 50 + 100)), 3)
    pygame.display.flip()
    BOARD_NUMS=[[0 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                button =Button(image=None,pos=(410 + i * 50 + 25,100 + j * 50 + 25), text_input=str(board[i][j]),font=pygame.font.Font(None, 35),base_color=TEXT_COLOR,hovering_color='red')
                BOARD_NUMS[i][j]=button
                BOARD_NUMS[i][j].update(SCREEN)
            else:
                button =Button(image=None,pos=(410 + i * 50 + 25,100 + j * 50 + 25), text_input=str(board[i][j]),font=pygame.font.Font(None, 35),base_color=BG,hovering_color='red')
                BOARD_NUMS[i][j]=button
                BOARD_NUMS[i][j].update(SCREEN)
    pygame.display.flip()
    NUM_BUTTONS = []
    for i in range(9):
        button = Button(image=None, pos=(410 + i * 50 + 25, 650), text_input=str(i + 1), font=pygame.font.Font(None, 30), base_color=TEXT_COLOR,hovering_color='red')
        button.update(SCREEN)
        NUM_BUTTONS.append(button)
    pygame.display.flip()
    input_num(BOARD_NUMS,NUM_BUTTONS)
    

def input_num(board, num_buttons):
    while True: 
        select_num_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(9):
                    if num_buttons[i].checkforinput(select_num_pos):
                        for button in num_buttons:
                            button.unhighlight()
                            button.update(SCREEN)
                        for row in range(9):
                            for col in range(9):
                                if board[row][col].text_input != '':
                                    board[row][col].unhighlight()
                                    board[row][col].update(SCREEN)
                        
                        num_buttons[i].highlight()
                        num_buttons[i].update(SCREEN)
                        
                        clicked_num = num_buttons[i].text_input
                        for row in range(9):
                            for col in range(9):
                                if board[row][col].text_input == clicked_num:
                                    board[row][col].highlight()
                                    board[row][col].update(SCREEN)
                    else:
                        for row in range(9):
                            for col in range(9):
                                if board[row][col].checkforinput(select_num_pos):
                                    if board[row][col].text_input=='0':
                                        board[row][col] = Button(image= None, pos=(410 + row * 50 + 25, 100 + col * 50 + 25), text_input=str(clicked_num), font=pygame.font.Font(None, 35), base_color=TEXT_COLOR, hovering_color='red')
                                        board[row][col].highlight()
                                        board[row][col].update(SCREEN)
                                        pygame.display.flip()
        pygame.display.update()


def final_board(difficulty):
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_board(board)
    attempts = 6
    if difficulty == 'Easy':
        attempts += 1
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
        copy_grid =board[:]
        global counter
        counter = 0
        solveGrid(copy_grid)
        if counter != 1:
            board[row][col] = backup
            attempts -= 1
    return board
def solveGrid(grid):
    global counter
    counter=0
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
                    sudoku('Easy')
                if MEDIUM_BUTTON.checkforinput(PLAY_MOUSE_POS):
                    sudoku('Medium')
                if HARD_BUTTON.checkforinput(PLAY_MOUSE_POS):
                    sudoku('Hard')
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