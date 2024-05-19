import pygame,sys
import random,math
from button import Button

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
BG = (255, 255, 255) 
TEXT_COLOR = '#000000'
SCREEN.fill(BG)
pygame.display.flip()
counter=0
class Sudoku:
    def __init__(self, N, K):
        self.N = N
        self.K = K
        SRNd = math.sqrt(N)
        self.SRN = int(SRNd)
        self.mat = [[0 for _ in range(N)] for _ in range(N)]
     
    def fillValues(self):
        self.fillDiagonal()
        self.fillRemaining(0, self.SRN)
        self.removeKDigits()
     
    def fillDiagonal(self):
        for i in range(0, self.N, self.SRN):
            self.fillBox(i, i)
     
    def unUsedInBox(self, rowStart, colStart, num):
        for i in range(self.SRN):
            for j in range(self.SRN):
                if self.mat[rowStart + i][colStart + j] == num:
                    return False
        return True
     
    def fillBox(self, row, col):
        num = 0
        for i in range(self.SRN):
            for j in range(self.SRN):
                while True:
                    num = self.randomGenerator(self.N)
                    if self.unUsedInBox(row, col, num):
                        break
                self.mat[row + i][col + j] = num
     
    def randomGenerator(self, num):
        return math.floor(random.random() * num + 1)
     
    def checkIfSafe(self, i, j, num):
        return (self.unUsedInRow(i, num) and self.unUsedInCol(j, num) and self.unUsedInBox(i - i % self.SRN, j - j % self.SRN, num))
     
    def unUsedInRow(self, i, num):
        for j in range(self.N):
            if self.mat[i][j] == num:
                return False
        return True
     
    def unUsedInCol(self, j, num):
        for i in range(self.N):
            if self.mat[i][j] == num:
                return False
        return True
    
    def fillRemaining(self, i, j):
        if i == self.N - 1 and j == self.N:
            return True
        if j == self.N:
            i += 1
            j = 0
        if self.mat[i][j] != 0:
            return self.fillRemaining(i, j + 1)
        
        for num in range(1, self.N + 1):
            if self.checkIfSafe(i, j, num):
                self.mat[i][j] = num
                if self.fillRemaining(i, j + 1):
                    return True
                self.mat[i][j] = 0
        return False
 
    def removeKDigits(self):
        count = self.K
 
        while (count != 0):
            i = self.randomGenerator(self.N) - 1
            j = self.randomGenerator(self.N) - 1
            if (self.mat[i][j] != 0):
                count -= 1
                self.mat[i][j] = 0
     
        return
def sudoku(difficulty):
    pygame.display.set_caption(difficulty + ' Sudoku')
    if difficulty == 'Easy':
        K=40
    elif difficulty == 'Medium':
        K=45
    elif difficulty == 'Hard':
        K=55
    board = Sudoku(9,K)
    board.fillValues()
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
            if board.mat[i][j] != 0:
                button =Button(image=None,pos=(410 + i * 50 + 25,100 + j * 50 + 25), text_input=str(board.mat[i][j]),font=pygame.font.Font(None, 35),base_color=TEXT_COLOR,hovering_color='red')
                BOARD_NUMS[i][j]=button
                BOARD_NUMS[i][j].update(SCREEN)
            else:
                button =Button(image=None,pos=(410 + i * 50 + 25,100 + j * 50 + 25), text_input=str(board.mat[i][j]),font=pygame.font.Font(None, 35),base_color=BG,hovering_color='red')
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
                                if board[row][col].text_input != '0':
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
        el = []
        for i in range(9):
            for j in range(9):
                el.append(int(board[i][j].text_input))
        if 0 not in el:
            TEXT=pygame.font.Font(None, 120).render("CONGRATULATIONS!", True, 'Black')
            TEXT_RECT=TEXT.get_rect(center=(640, 200))
            SCREEN.fill(BG)
            pygame.display.flip()
            SCREEN.blit(TEXT,TEXT_RECT)
            pygame.display.flip()
            while True:
                WIN_MOUSE_POS=pygame.mouse.get_pos()  
                PLAY_BACK = Button(image=None, pos=(640, 600), text_input="BACK", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="Green")
                PLAY_BACK.changecolor(WIN_MOUSE_POS)
                PLAY_BACK.update(SCREEN)
                pygame.display.flip()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if PLAY_BACK.checkforinput(WIN_MOUSE_POS):
                            main_menu()  
        el.clear()              
        pygame.display.update()
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