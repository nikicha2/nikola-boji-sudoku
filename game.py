import pygame,sys
import random,math,time
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
class Grid:
    def __init__(self, rows, cols, width, height, win,board):
        self.rows = rows
        self.cols = cols
        self.board=board
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.win = win
        

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val, row, col):
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and self.solve():
                self.cubes[row][col].set_notes(0)
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_notes(0)
                self.update_model()
                return False

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        offset = 360  
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (offset, i*gap), (self.width+offset, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap+offset, 0), (i * gap+offset, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, key):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value==key:
                    self.cubes[i][j].selected = True
                else:
                    self.cubes[i][j].selected = False

    def clear_notes(self,row,col):
        self.cubes[row][col].set_notes(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        x, y = pos
        gap = self.width / 9
        offset = 360 

        if offset <= x < self.width + offset and 0 <= y < self.height:
            x_adjusted = x - offset
            col = x_adjusted // gap
            row = y // gap
            return int(row), int(col)
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False



class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.notes = []
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)
        small_fnt = pygame.font.SysFont("comicsans", 18)

        gap = self.width / 9
        offset = 360
        x = self.col * gap + offset
        y = self.row * gap

        if len(self.notes) != 0 and self.value == 0:
            for note in self.notes:
                note_x = x + (note - 1) % 3 * gap / 3
                note_y = y + (note - 1) // 3 * gap / 3
                text = small_fnt.render(str(note), 1, (128, 128, 128))
                win.blit(text, (note_x + 3, note_y-2))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        
        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        offset = 360 
        x = self.col * gap + offset
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_notes(self, val):
        if val==0:
            self.notes.clear()
        else: 
            if val in self.notes:
                self.notes.remove(val)
            else: 
                self.notes.append(val)



def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True


def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (700, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (380, 560))
    # Draw grid and board
    board.draw()


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def sudoku(difficulty):
    win = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption(difficulty + " Sudoku")
    if difficulty == 'Easy':
        K=40
    elif difficulty == 'Medium':
        K=45
    elif difficulty == 'Hard':
        K=55
    boardObj = Sudoku(9,K)
    boardObj.fillValues()
    board = Grid(9, 9, 540, 540, win,boardObj.mat[:])
    key = None
    start = time.time()
    strikes = 0
    notes=False
    while True:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9

                if event.key ==pygame.K_f:
                    notes=not notes

                if event.key == pygame.K_SPACE:
                    board.solve_gui()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos=pygame.mouse.get_pos()
                clicked=board.click(clickPos)
                if clicked and key is not None: 
                    i, j=clicked
                    if board.cubes[i][j].value==0 and notes==False:
                        if board.place(key,i,j):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                    else:
                        board.cubes[i][j].set_notes(key)
            if key:
                board.select(key)
        if board.is_finished():
            win.fill((255,255,255))
            congrats = pygame.font.SysFont("comicsans", 40).render("CONGRATULATIONS!", 1, (128,128,128))
            win.blit(congrats, (410, 50))
            pygame.display.update()
            while True:
                pos = pygame.mouse.get_pos()
                PLAY_BACK = Button(image=None, pos=(640, 700), text_input="BACK", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="Green")
                PLAY_BACK.changecolor(pos)
                PLAY_BACK.update(SCREEN)
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        if PLAY_BACK.checkforinput(pos):
                            main_menu()
                pygame.display.update()
        redraw_window(win, board, play_time, strikes)
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