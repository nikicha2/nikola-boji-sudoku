import pygame
import sys
from button import Button

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
BG = (255, 255, 255)
SCREEN.fill(BG)
pygame.display.flip()

def play():
    SCREEN.fill(BG)
    pygame.display.flip()
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        
        PLAY_TEXT = pygame.font.Font(None, 45).render("This is the PLAY screen.", True, "Black")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), text_input="BACK", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="Green")

        PLAY_BACK.changecolor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkforinput(PLAY_MOUSE_POS):
                    main_menu()

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