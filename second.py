import pygame
import os
import sys
import webbrowser



pygame.init()
screenA = pygame.display.set_mode((1000, 600))

pygame.display.set_caption("для настроек")
background_image = pygame.image.load('data/textures/scenes/menu_scene.png')

setting_img = pygame.image.load("data/textures/scenes/setting_button.jpg")
discord_img = pygame.image.load("data/textures/scenes/dis_btn.jpg")
github_img = pygame.image.load("data/textures/scenes/git_btn.jpg")
credits_img = pygame.image.load("data/textures/scenes/cred_btn.jpg")
effect_img = pygame.image.load("data/textures/scenes/ef_btn.jpg")
menu_img = pygame.image.load("data/textures/scenes/menu_btn.jpg")
save_img = pygame.image.load("data/textures/scenes/save_btn.jpg")



class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screenA.blit(self.image, (self.rect.x, self.rect.y))

setting_btn = Button(750, 470, setting_img)
discord_btn = Button(400, 470, discord_img)
github_btn = Button(540, 460, github_img)
credits_btn = Button(260, 460, credits_img)
effect_btn = Button(350, 150, effect_img)
menu_btn = Button(350, 250, menu_img)
save_btn = Button(350, 350, save_img)
btn_click = False

while True:

    screenA.blit(background_image, (0, 0))
    setting_btn.draw()
    x, y = pygame.mouse.get_pos()
    if (x >= 750 or x <= 950) and (y >= 470 or y <= 570) and pygame.mouse.get_pressed()[0]:
        btn_click = False

    if (x >= 750 or x <= 950) and (y >= 470 or y <= 570) and pygame.mouse.get_pressed()[0]:
        btn_click = True

    if btn_click:
        a = pygame.image.load('data/textures/scenes/set_win2.jpg')
        screenA.blit(a, (240, 50))
        discord_btn.draw()
        github_btn.draw()
        credits_btn.draw()
        effect_btn.draw()
        menu_btn.draw()
        save_btn.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()





