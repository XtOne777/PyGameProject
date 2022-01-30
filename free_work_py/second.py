import pygame
import os
import sys

pygame.init()
screenA = pygame.display.set_mode((1000, 600))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey != 0:
        if not colorkey:
            image = image.convert()
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    if colorkey:
        image.set_colorkey(colorkey)
    return image


background_image = load_image('textures/scenes/menu_scene.png')
setting_img = load_image("textures/scenes/setting_button.png")
discord_img = load_image("textures/scenes/dis_btn.jpg")
github_img = load_image("textures/scenes/git_btn.jpg")
# credits_img = load_image("textures/scenes/cred_btn.jpg")
effect_img = load_image("textures/scenes/ef_btn.jpg")
menu_img = load_image("textures/scenes/menu_btn.jpg")
save_img = load_image("textures/scenes/save_btn.jpg")


class Button(pygame.sprite.Sprite):
    def __init__(self, x1, y2, image, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x1, y2)

    def draw(self):
        screenA.blit(self.image, (self.rect.x, self.rect.y))


settings_group = pygame.sprite.Group()
window_set = pygame.sprite.Sprite()
window_set.image = load_image('textures/scenes/set_win2.jpg')
window_set.rect = window_set.image.get_rect()
window_set.rect.x, window_set.y = 0, 0
settings_group.add(window_set)
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
setting_btn = Button(750, 470, setting_img, sprites)
discord_btn = Button(400, 470, discord_img, settings_group)
github_btn = Button(540, 460, github_img, settings_group)
# credits_btn = Button(260, 460, credits_img, settings_group)
effect_btn = Button(350, 150, effect_img, settings_group)
menu_btn = Button(350, 250, menu_img, settings_group)
save_btn = Button(350, 350, save_img, settings_group)
btn_click = False

while True:
    screen.fill((0, 0, 0))
    x, y = pygame.mouse.get_pos()
    if (x >= 750 or x <= 950) and (y >= 470 or y <= 570) and pygame.mouse.get_pressed()[0]:
        btn_click = False
    if (x >= 750 or x <= 950) and (y >= 470 or y <= 570) and pygame.mouse.get_pressed()[0]:
        btn_click = True
    if btn_click:
        settings_group.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
