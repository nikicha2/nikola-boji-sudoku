import pygame,sys,os
import random,math,time,json
from button import Button

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
if os.path.exists("color_scheme.json"):
    with open("color_scheme.json","r") as file:
        colors = json.load(file)
        bgcolor=colors['bgc']
        tupletextcolor=colors['ttc']
        textcolor=colors["tc"]

SCREEN.fill(bgcolor)
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

    def draw(self,key):
        # Draw Grid Lines
        gap = self.width / 9
        offset = 360  
        for i in range(self.rows+1):
            if i % 3 == 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (offset, i*gap), (self.width+offset, i*gap), thick)
            pygame.draw.line(self.win, (0,0,0), (i * gap+offset, 0), (i * gap+offset, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win,key)

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

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()

        return False
    def removeAdjNotes(self,key,i,j):
        bigCube_x=(i // 3) * 3
        bigCube_y=(j // 3) * 3
        for row in range(3):
            for col in range(3):
                if key in self.cubes[bigCube_x+row][bigCube_y+col].notes:
                    self.cubes[bigCube_x+row][bigCube_y+col].notes.remove(key) 
        [self.cubes[i][yCoord].notes.remove(key) for yCoord in range(9) if key in self.cubes[i][yCoord].notes]
        [self.cubes[xCoord][j].notes.remove(key) for xCoord in range(9) if key in self.cubes[xCoord][j].notes]
    def checkForKey(self,key):
        self.update_model()
        sumOfKey=0
        for i in range(9):
            for j in range(9):
                if self.model[i][j]==key:
                    sumOfKey+=1
        if sumOfKey<9:
            return True
        else:
            return False
    def unselect_all(self, key):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cubes[row][col].value == key:
                    self.cubes[row][col].selected = False



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

    def draw(self, win,key):
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
                if note ==key:
                    text = small_fnt.render(str(note), 1, (255, 0, 0))
                else:
                    text = small_fnt.render(str(note), 1, (128, 128, 128))
                win.blit(text, (note_x + 3, note_y-2))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, tupletextcolor)
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        
        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        offset = 360 
        x = self.col * gap + offset
        y = self.row * gap

        pygame.draw.rect(win, bgcolor, (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, tupletextcolor)
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


def redraw_window(win, board, time, strikes,notes,key):
    win.fill(bgcolor)
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, tupletextcolor)
    win.blit(text, (700, 560))
    if notes:
        text=fnt.render("ON",1,tupletextcolor)
        win.blit(text,(620,560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (380, 560))
    # Draw grid and board
    board.draw(key)


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

def is_valid(board, row, col, num):
    """Check if num can be placed at board[row][col]."""
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board, solutions):
    """Solve the Sudoku board and count the number of solutions."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        solve_sudoku(board, solutions)
                        board[row][col] = 0
                return
    solutions[0] += 1

def has_unique_solution(board):
    """Check if the Sudoku board has exactly one solution."""
    solutions = [0]
    solve_sudoku(board, solutions)
    return solutions[0] == 1

def sudoku(difficulty,initialBoard=None, initialNotes=None):
    win = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption(difficulty + " Sudoku")
    if initialBoard:
        board = Grid(9, 9, 540, 540, win,initialBoard)
        for i in range(9):
            for j in range(9):
                board.cubes[i][j].notes=initialNotes[9 * i + j]
        with open("last_board.json" ,"w") as file:
            pass
    else:
        if difficulty == 'Easy':
            K=35
        elif difficulty == 'Medium':
            K=40
        elif difficulty == 'Hard':
            K=47
        while True:
            boardObj = Sudoku(9,K)
            boardObj.fillValues()
            if has_unique_solution(boardObj.mat[:]):
                break
        board = Grid(9, 9, 540, 540, win,boardObj.mat[:])
    key = None
    start = time.time()
    strikes = 0
    notes=False
    while True:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dumpDict={}
                dumpDict["values"]=board.model
                notesList=[]
                for x in range(9):
                    for y in range(9):
                        notesList.append(board.cubes[x][y].notes)
                dumpDict['notes']=notesList
                dumpDict['difficulty']=difficulty
                colors={}
                colors["bgc"]=bgcolor
                colors["tc"]=textcolor
                colors["ttc"]=tupletextcolor
                with open("last_board.json", "w") as file:   
                    json.dump(dumpDict,file)
                with open("color_scheme.json","w") as cfile:
                    json.dump(colors,cfile)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if board.checkForKey(1):
                        key = 1
                if event.key == pygame.K_2:
                    if board.checkForKey(2):
                        key = 2
                if event.key == pygame.K_3:
                    if board.checkForKey(3):
                        key = 3
                if event.key == pygame.K_4:
                    if board.checkForKey(4):
                        key = 4
                if event.key == pygame.K_5:
                    if board.checkForKey(5):
                        key = 5
                if event.key == pygame.K_6:
                    if board.checkForKey(6):
                        key = 6
                if event.key == pygame.K_7:
                    if board.checkForKey(7):
                        key = 7
                if event.key == pygame.K_8:
                    if board.checkForKey(8):
                        key = 8
                if event.key == pygame.K_9:
                    if board.checkForKey(9):
                        key = 9
                if event.key == pygame.K_KP1:
                    if board.checkForKey(1):
                        key = 1
                if event.key == pygame.K_KP2:
                    if board.checkForKey(2):
                        key = 2
                if event.key == pygame.K_KP3:
                    if board.checkForKey(3):
                        key = 3
                if event.key == pygame.K_KP4:
                    if board.checkForKey(4):
                        key = 4
                if event.key == pygame.K_KP5:
                    if board.checkForKey(5):
                        key = 5
                if event.key == pygame.K_KP6:
                    if board.checkForKey(6):
                        key = 6
                if event.key == pygame.K_KP7:
                    if board.checkForKey(7):
                        key = 7
                if event.key == pygame.K_KP8:
                    if board.checkForKey(8):
                        key = 8
                if event.key == pygame.K_KP9:
                    if board.checkForKey(9):
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
                            board.removeAdjNotes(key,i,j)
                            if not board.checkForKey(key):
                                board.unselect_all(key)
                                for uns_x in range(9):
                                    for uns_y in range(9):
                                        if key in board.cubes[uns_x][uns_y].notes:
                                            board.cubes[uns_x][uns_y].notes.remove(key)
                                key = None
                        else:
                            print("Wrong")
                            strikes += 1
                    else:
                        board.cubes[i][j].set_notes(key)
            if key:
                board.select(key)
        if board.is_finished():
            with open("last_board.json" ,"w") as file:
                pass
            win.fill(bgcolor)
            congrats = pygame.font.SysFont("comicsans", 80).render("CONGRATULATIONS!", 1, (128,128,128))
            win.blit(congrats, congrats.get_rect(center=(640, 100)))
            pygame.display.update()
            while True:
                pos = pygame.mouse.get_pos()
                PLAY_BACK = Button(image=None, pos=(640, 550), text_input="BACK", font=pygame.font.SysFont("comicsans", 85), base_color=textcolor, hovering_color="Green")
                PLAY_BACK.changecolor(pos)
                PLAY_BACK.update(SCREEN)
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        dumpDict={}
                        colors={}
                        colors["bgc"]=bgcolor
                        colors["tc"]=textcolor
                        colors["ttc"]=tupletextcolor
                        with open("last_board.json","w") as file:
                            json.dump(dumpDict,file)
                        with open("color_scheme.json","w") as cfile:
                            json.dump(colors,cfile)
                        pygame.quit()
                        sys.exit()
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        if PLAY_BACK.checkforinput(pos):
                            main_menu()
                pygame.display.update()
        redraw_window(win, board, play_time, strikes,notes,key)
        pygame.display.update()
def play():
    SCREEN.fill(bgcolor)
    pygame.display.flip()
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        DIF_TEXT = pygame.font.SysFont("comicsans", 90).render("SELECT DIFICULTY", True, textcolor)
        DIF_RECT = DIF_TEXT.get_rect(center=(640, 100))
        EASY_BUTTON = Button(image=None, pos=(640, 250), text_input="EASY", font=pygame.font.SysFont("comicsans", 75), base_color=textcolor, hovering_color=textcolor)
        MEDIUM_BUTTON = Button(image=None, pos=(640, 400), text_input="MEDIUM", font=pygame.font.SysFont("comicsans", 75), base_color=textcolor, hovering_color=textcolor)
        HARD_BUTTON = Button(image=None, pos=(640, 550), text_input="HARD", font=pygame.font.SysFont("comicsans", 75), base_color=textcolor, hovering_color=textcolor)
        SCREEN.blit(DIF_TEXT, DIF_RECT)
        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON]:
            button.changecolor(PLAY_MOUSE_POS)
            button.update(SCREEN)
        PLAY_BACK = Button(image=None, pos=(640, 680), text_input="BACK", font=pygame.font.SysFont("comicsans", 75), base_color=textcolor, hovering_color="Green")
        PLAY_BACK.changecolor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dumpDict={}
                colors={}
                colors["bgc"]=bgcolor
                colors["tc"]=textcolor
                colors["ttc"]=tupletextcolor
                with open("last_board.json","w") as file:
                    json.dump(dumpDict,file)
                with open("color_scheme.json","w") as cfile:
                    json.dump(colors,cfile)
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
    global bgcolor
    global textcolor
    global tupletextcolor
    SCREEN.fill(bgcolor)
    pygame.display.flip()
    tempbg=bgcolor
    tempttc=tupletextcolor
    temptc=textcolor
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        
        lightmode=Button(image=None, pos=(640, 200), text_input='Light mode', font=pygame.font.SysFont("comicsans", 75), base_color=temptc, hovering_color=temptc)
        darkmode=Button(image=None, pos=(640, 300), text_input='Dark mode', font=pygame.font.SysFont("comicsans", 75), base_color=temptc, hovering_color=temptc)#444444 #E2E2E2
        beigemode=Button(image=None, pos=(640, 400), text_input='Beige mode', font=pygame.font.SysFont("comicsans", 75), base_color=temptc, hovering_color=temptc)#FFCF9F #7B5E41
        
        if lightmode.checkforinput(OPTIONS_MOUSE_POS):
            tempbg=(255,255,255)
            tempttc=(0,0,0)
            temptc='#000000'
            SCREEN.fill(tempbg)
        if darkmode.checkforinput(OPTIONS_MOUSE_POS):
            tempbg=(44,44,44)
            tempttc=(226,226,226)
            temptc='#E2E2E2'
            SCREEN.fill(tempbg)
        if beigemode.checkforinput(OPTIONS_MOUSE_POS):
            tempbg=(255,207,159)
            tempttc=(33,20,9)
            temptc='#211409'
            SCREEN.fill(tempbg)
        if not (lightmode.checkforinput(OPTIONS_MOUSE_POS) or darkmode.checkforinput(OPTIONS_MOUSE_POS) or beigemode.checkforinput(OPTIONS_MOUSE_POS)):
            tempbg=bgcolor
            tempttc=tupletextcolor
            temptc=textcolor
            SCREEN.fill(tempbg)
        options_text = pygame.font.SysFont("comicsans", 85).render("CHOOSE COLOR SCHEME", True,tempttc)
        SCREEN.blit(options_text, ((1280-options_text.get_width())/2,40))
        for option in [lightmode,darkmode,beigemode]:
            option.changecolor(OPTIONS_MOUSE_POS)
            option.update(SCREEN)

        OPTIONS_BACK = Button(image=None, pos=(640, 540), text_input="BACK", font=pygame.font.SysFont("comicsans", 75), base_color=temptc, hovering_color="Green")

        OPTIONS_BACK.changecolor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dumpDict={}
                colors={}
                colors["bgc"]=bgcolor
                colors["tc"]=textcolor
                colors["ttc"]=tupletextcolor
                with open("last_board.json","w") as file:
                    json.dump(dumpDict,file)
                with open("color_scheme.json","w") as cfile:
                    json.dump(colors,cfile)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkforinput(OPTIONS_MOUSE_POS):
                    main_menu()
                if lightmode.checkforinput(OPTIONS_MOUSE_POS):
                    bgcolor=(255,255,255)
                    tupletextcolor=(0,0,0)
                    textcolor='#000000'
                    SCREEN.fill(bgcolor)
                if darkmode.checkforinput(OPTIONS_MOUSE_POS):
                    bgcolor=(44,44,44)
                    tupletextcolor=(226,226,226)
                    textcolor='#E2E2E2'
                    SCREEN.fill(bgcolor)
                if beigemode.checkforinput(OPTIONS_MOUSE_POS):
                    bgcolor=(255,207,159)
                    tupletextcolor=(33,20,9)
                    textcolor='#211409'
                    SCREEN.fill(bgcolor)
                pygame.display.flip()

        pygame.display.update()
def main_menu():
    global textcolor
    global bgcolor
    global tupletextcolor
    pygame.display.set_caption("Menu")
    SCREEN.fill(bgcolor)
    pygame.display.flip()
    continue_button = None
    if os.path.exists("last_board.json") and os.path.getsize("last_board.json") > 2:
        continue_button = Button(image=None, pos=(640, 150), text_input="CONTINUE", font=pygame.font.SysFont("comicsans", 65), base_color='#bed4eb', hovering_color=textcolor)
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = pygame.font.SysFont("comicsans", 100).render("SUDOKU", True,textcolor)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 50))
        PLAY_BUTTON = Button(image=None, pos=(640, 250), text_input="PLAY", font=pygame.font.SysFont("comicsans", 75), base_color=textcolor, hovering_color=textcolor)
        OPTIONS_BUTTON = Button(image=None, pos=(640, 400), text_input="OPTIONS", font=pygame.font.SysFont("comicsans", 75), base_color=textcolor, hovering_color=textcolor)
        QUIT_BUTTON = Button(image=None, pos=(640, 550), text_input="QUIT", font=pygame.font.SysFont("comicsans", 75), base_color=textcolor, hovering_color=textcolor)
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        if continue_button:
            continue_button.changecolor(MENU_MOUSE_POS)
            continue_button.update(SCREEN)
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changecolor(MENU_MOUSE_POS)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dumpDict={}
                colors={}
                colors["bgc"]=bgcolor
                colors["tc"]=textcolor
                colors["ttc"]=tupletextcolor
                with open("last_board.json","w") as file:
                    json.dump(dumpDict,file)
                with open("color_scheme.json","w") as cfile:
                    json.dump(colors,cfile)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button and continue_button.checkforinput(MENU_MOUSE_POS):
                    with open("last_board.json", "r") as file:
                        saved_game = json.load(file)
                        board_values = saved_game["values"]
                        notes = saved_game["notes"]
                        difficulty=saved_game['difficulty']
                        sudoku(difficulty,board_values,notes)
                if PLAY_BUTTON.checkforinput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkforinput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkforinput(MENU_MOUSE_POS):
                    dumpDict={}
                    colors={}
                    colors["bgc"]=bgcolor
                    colors["tc"]=textcolor
                    colors["ttc"]=tupletextcolor
                    with open("last_board.json","w") as file:
                        json.dump(dumpDict,file)
                    with open("color_scheme.json","w") as cfile:
                        json.dump(colors,cfile)
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
main_menu()