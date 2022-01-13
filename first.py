from classes import *
import pygame
import os
import sys

money = 0
exp = 0
lvl_step = 1
mob_lvl = {1: (('goblin', 100, 10),),
           2: (('goblin', 100, 10), ('goblin', 100, 10))}


def slot_load(name, place):
    slot = pygame.sprite.Sprite()
    slot.image = pygame.transform.scale(load_image(name, 0), (69, 69))
    slot.rect = slot.image.get_rect()
    slot.rect.x, slot.rect.y = place
    return slot


def load_game():
    screen.fill((0, 0, 0))
    screen.blit(load_image('./textures/scenes/menu_scene.png', 0), (0, 0))
    d = pygame.transform.scale(load_image('./textures/scenes/button_play.png'), (100, 100))
    screen.blit(d, (435, 425))
    xx, yy = d.get_size()
    for x in range(xx):
        for y in range(yy):
            r, g, b, i = d.get_at((x, y))
            d.set_at((x, y), (r * 0.2, g * 0.2, b * 0.2))
    pygame.display.flip()


def good_load(name, name_2):
    scene = load_image(name)
    button_play = pygame.transform.scale(load_image(name_2), (150, 150))
    for i in range(127):
        screen.fill((0, 0, 0))
        scene.set_alpha(i * 2)
        button_play.set_alpha(i * 2)
        screen.blit(scene, (0, 0))
        screen.blit(button_play, (410, 400))
        pygame.display.flip()


def slot_color_change(slot, color=None):
    xx, yy = slot.image.get_size()
    a = slot.image.get_at((0, 0))
    for x in range(xx):
        for y in range(yy):
            if a == slot.image.get_at((x, y)):
                if color:
                    change_color = color
                else:
                    change_color = (106, 106, 106)
                slot.image.set_at((x, y), change_color)


def common_load(group):
    screen.fill((0, 0, 0))
    group.draw(screen)


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


class StaminaBar(pygame.sprite.Sprite):
    def __init__(self, player_class, *group):
        super().__init__(*group)
        self.player = player_class
        self.max_stamina = player['max_stamina']
        self.image = load_image('./textures/player/info/stamina_bar_line.png', 0)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 46, 97

    def update(self):
        if player['stamina'] > 0:
            self.image = pygame.transform.scale(self.image, (409 / self.max_stamina * player['stamina'], 7))
        else:
            self.image = pygame.transform.scale(self.image, (1, 7))


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, player_class, *group):
        super().__init__(*group)
        self.player = player_class
        self.max_health = player['max_health']
        self.image = load_image('./textures/player/info/health_bar_line.png', 0)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 60, 24

    def update(self):
        if player['health'] > 0:
            if 3 >= self.max_health / player['health'] >= 2:
                if self.image.get_at((0, 0)) != (255, 255, 0, 255):
                    i, k = self.image.get_size()
                    for x in range(i):
                        for y in range(k):
                            self.image.set_at((x, y), (255, 255, 0))
            elif self.max_health / player['health'] >= 3:
                if self.image.get_at((0, 0)) != (255, 127, 0, 255):
                    i, k = self.image.get_size()
                    for x in range(i):
                        for y in range(k):
                            self.image.set_at((x, y), (255, 127, 0))
            else:
                if self.image.get_at((0, 0)) != (255, 0, 0, 255):
                    i, k = self.image.get_size()
                    for x in range(i):
                        for y in range(k):
                            self.image.set_at((x, y), (255, 0, 0))
            self.image = pygame.transform.scale(self.image, (405 / self.max_health * player['health'], 52))
        else:
            self.image = pygame.transform.scale(self.image, (0, 52))


class Attack(pygame.sprite.Sprite):
    def __init__(self, name, slot=0, *group):
        super().__init__(*group)
        if name == 'heavy_attack':
            self.attack = pygame.sprite.Sprite()
            self.image = self.image = pygame.transform.scale(load_image('./textures/player/attacks/heavy_attack.png'),
                                                             (45, 45))
        elif name == 'low_attack':
            self.attack = pygame.sprite.Sprite()
            self.image = self.image = pygame.transform.scale(load_image('./textures/player/attacks/low_attack.png'),
                                                             (45, 45))
        self.rect = self.image.get_rect()
        self.slot = slot
        if slot == 0:
            self.rect.x, self.rect.y = (-75, -75)
        elif slot == 1:
            self.rect.x, self.rect.y = (313, 500)
        elif slot == 2:
            self.rect.x, self.rect.y = (463, 500)
        elif slot == 3:
            self.rect.x, self.rect.y = (613, 500)

    def change_slot(self, slot):
        self.slot = slot
        if slot == 0:
            self.rect.x, self.rect.y = (-75, -75)
        elif slot == 1:
            self.rect.x, self.rect.y = (313, 500)
        elif slot == 2:
            self.rect.x, self.rect.y = (463, 500)
        elif slot == 3:
            self.rect.x, self.rect.y = (613, 500)


class Human(pygame.sprite.Sprite):
    def __init__(self, name, classes=Standart(), *group):
        super().__init__(*group)
        if name[0:11] != 'load_data: ':
            self.name = name
            self.max_stamina = 15
            self.max_health = 100
            self.health = 0 + self.max_health
            self.stamina = 0 + self.max_stamina
            self.lvl = 1
            self.exp = 0
            self.classes = classes
            image = './textures/player/standart.png'
            if isinstance(classes, Magic):
                image = './textures/player/magic(standart).png'
            elif isinstance(classes, Fighting):
                image = './textures/player/fighter.png'
            self.player = pygame.sprite.Sprite()
            self.image = pygame.transform.scale(load_image(image), (105, 127.5))
            self.rect = self.image.get_rect()
            self.rect.x = 150
            self.rect.y = 300

            self.animate = False
            self.step = 0
        else:
            pass  # тут будет загрузка сохранёных данных

    def attack(self, attack, type_attack='Normal'):
        if attack:
            if not type_attack:
                type_attack = 'Normal'
            if attack == 'low_attack':
                return self.low_attack(type_attack)
            if attack == 'heavy_attack':
                return self.heavy_attack(type_attack)
            return 0.0

    def update(self):
        if self.animate:
            if self.step <= 25:
                self.rect.x += 3 + (25 - self.step) / 75
                self.step += 1
            elif self.step <= 50:
                self.rect.x -= 3 + (self.step - 46) / 75
                self.step += 1
            else:
                self.step = 0
                self.animate = False

    def attack_animate(self):
        self.animate = True

    def __getitem__(self, item):
        if item == 'max_health':
            return self.max_health
        elif item == 'name':
            return self.name
        elif item == 'health':
            return self.health
        elif item == 'player':
            return self.player
        elif item == 'player.image':
            return self.image
        elif item == 'is_attacking':
            return self.animate
        elif item == 'stamina':
            return self.stamina
        elif item == 'max_stamina':
            return self.max_stamina

    def low_attack(self, type_attack=None):
        if self.stamina + 3 > self.max_stamina:
            self.stamina = 0 + self.max_stamina
        else:
            self.stamina += 3
        if type_attack:
            return self.classes.low_attack(type_attack)
        return self.classes.low_attack()

    def heavy_attack(self, type_attack=None, miss_buff=None):
        if self.stamina - 5 >= 0:
            self.stamina -= 5
            if type_attack:
                if miss_buff or miss_buff == 0:
                    return self.classes.heavy_attack(type_attack, miss_buff)
                return self.classes.heavy_attack(type_attack)
            else:
                if miss_buff or miss_buff == 0:
                    return self.classes.heavy_attack(miss_buff=miss_buff)
                return self.classes.heavy_attack()
        else:
            return 0.0

    def change(self, health):
        self.max_health = health

    def got_damage(self, dmg):
        self.health -= dmg

    def is_died(self):
        return self.health > 0

    def revive(self):
        self.health = 0 + self.max_health
        self.stamina = 0 + self.max_stamina


class Mob(pygame.sprite.Sprite):
    def __init__(self, name, health, dmg, place, *group):
        super().__init__(*group)
        self.group = group
        self.name = name
        self.max_health = health
        self.health = 0 + self.max_health
        self.dmg = dmg
        self.sprite = pygame.sprite.Sprite()
        if name == 'goblin':
            self.image = pygame.transform.scale(load_image('./textures/mobs/lvl 0/goblin.png'), (105, 127.5))
        self.rect = self.image.get_rect()
        self.rect.x = place[0]
        self.rect.y = place[1]

    def update(self):
        pygame.draw.polygon(screen, (0, 0, 0), [(self.rect.x, self.rect.y - 10), (self.rect.x + 105, self.rect.y - 10),
                                                (self.rect.x + 105, self.rect.y), (self.rect.x, self.rect.y)])
        if self.health > 0:
            pygame.draw.polygon(screen, (255, 50, 50), [(self.rect.x, self.rect.y - 10),
                                                        (self.rect.x + 105 / self.max_health * self.health,
                                                         self.rect.y - 10),
                                                        (self.rect.x + 105 / self.max_health * self.health,
                                                         self.rect.y),
                                                        (self.rect.x, self.rect.y)])

    def __getitem__(self, item):
        if item == 'name':
            return self.name
        if item == 'health':
            return self.health
        if item == 'max_health':
            return self.max_health

    def low_attack(self, chance=5):
        return self.dmg * 2 if randint(0, 100) < chance else self.dmg

    def got_damage(self, dmg):
        self.health -= dmg

    def is_died(self):
        if self.health <= 0:
            self.image = pygame.transform.scale(load_image('./textures/mobs/RIP.png'), (105, 127.5))
        return self.health > 0


if __name__ == "__main__":
    # инициализация Pygame:
    pygame.init()
    # размеры окна:
    size = width, height = 1000, 600
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.flip()
    running = True
    start_menu = True
    start_game = False
    clock.tick(45)
    good_load('./textures/scenes/menu_scene.png', './textures/scenes/button_play.png')
    while running:
        while start_menu:
            screen.fill((0, 0, 0))
            screen.blit(load_image('./textures/scenes/menu_scene.png', 0), (0, 0))
            screen.blit(pygame.transform.scale(load_image('./textures/scenes/button_play.png'), (150, 150)), (410, 400))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if 410 <= event.pos[0] <= 410 + 150 and 400 <= event.pos[1] <= 550:
                        start_menu = False
                        start_game = True
                        load_game()
            if not running:
                break
            pygame.display.flip()
        while running:
            sprites = pygame.sprite.Group()

            # Главная сцена
            main_scene = pygame.sprite.Sprite()
            main_scene.image = load_image('./textures/scenes/scene(lvl 1).png', 0)
            main_scene.rect = main_scene.image.get_rect()
            main_scene.rect.x, main_scene.rect.y = 0, 0
            sprites.add(main_scene)

            # Игрок
            player = Human('Player 1', Magic(), sprites)

            # Полоска жизней
            health_bar_line = HealthBar(player, sprites)

            health_bar = pygame.sprite.Sprite()
            health_bar.image = load_image('./textures/player/info/health_bar.png')
            health_bar.rect = health_bar.image.get_rect()
            health_bar.rect.x, health_bar.rect.y = 0, 0
            sprites.add(health_bar)

            # Полоска стамины
            stamina_bar_line = StaminaBar(player, sprites)

            stamina_bar = pygame.sprite.Sprite()
            stamina_bar.image = load_image('./textures/player/info/stamina_bar.png', (255, 255, 255))
            stamina_bar.rect = stamina_bar.image.get_rect()
            stamina_bar.rect.x, stamina_bar.rect.y = 45, 95
            sprites.add(stamina_bar)

            # Слоты атак
            slot_1 = slot_load('./textures/player/attacks/slot_1.png', (300, 488))
            slot_2 = slot_load('./textures/player/attacks/slot_2.png', (450, 488))
            slot_3 = slot_load('./textures/player/attacks/slot_3.png', (600, 488))
            sprites.add(slot_1)
            sprites.add(slot_2)
            sprites.add(slot_3)

            # Атаки
            slot_1_attack = ('heavy_attack', 'Normal')
            Attack(slot_1_attack[0], 1, sprites)
            slot_2_attack = ('low_attack', 'Normal')
            Attack(slot_2_attack[0], 2, sprites)
            slot_3_attack = (None, )

            # Мобы
            mobs = list()
            mobs_list = mob_lvl[lvl_step]
            check_list = list()
            for mob_data in mobs_list:
                check_list.append(mob_data)
            for steps in range(len(mobs_list)):
                mobs.append(Mob(check_list[steps][0], check_list[steps][1], check_list[steps][2],
                                (600 + (steps % 2) * 100, 150 + 200 / len(mobs_list) * (steps + 1)), sprites))
            # Старт игры
            while start_game:
                screen.fill((0, 0, 0))
                sprites.draw(screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEMOTION:
                        if not player['is_attacking']:
                            if 300 <= event.pos[0] <= 300 + 69 and 488 <= event.pos[1] <= 488 + 69:
                                slot_color_change(slot_1, (255, 255, 0))
                                slot_color_change(slot_2)
                                slot_color_change(slot_3)
                            elif 450 <= event.pos[0] <= 450 + 69 and 488 <= event.pos[1] <= 488 + 69:
                                slot_color_change(slot_2, (255, 255, 0))
                                slot_color_change(slot_1)
                                slot_color_change(slot_3)
                            elif 600 <= event.pos[0] <= 600 + 69 and 488 <= event.pos[1] <= 488 + 69:
                                slot_color_change(slot_3, (255, 255, 0))
                                slot_color_change(slot_1)
                                slot_color_change(slot_2)
                            else:
                                slot_color_change(slot_1)
                                slot_color_change(slot_2)
                                slot_color_change(slot_3)
                    if event.type == pygame.MOUSEBUTTONUP:
                        if not player['is_attacking']:
                            flag = False
                            if 300 <= event.pos[0] <= 300 + 69 and 488 <= event.pos[1] <= 488 + 69:
                                player.attack_animate()
                                num = int(input())
                                slot_color_change(slot_1, (255, 0, 0))
                                if mobs[num]:
                                    damage = player.attack(slot_1_attack[0], slot_1_attack[1])
                                    mobs[num].got_damage(damage)
                                flag = True
                            elif 450 <= event.pos[0] <= 450 + 69 and 488 <= event.pos[1] <= 488 + 69:
                                player.attack_animate()
                                num = int(input())
                                slot_color_change(slot_2, (255, 0, 0))
                                if mobs[num]:
                                    damage = player.attack(slot_2_attack[0], slot_2_attack[1])
                                    mobs[num].got_damage(damage)
                                flag = True
                            elif 600 <= event.pos[0] <= 600 + 69 and 488 <= event.pos[1] <= 488 + 69:
                                player.attack_animate()
                                num = int(input())
                                slot_color_change(slot_3, (255, 0, 0))
                                if mobs[num]:
                                    damage = player.attack(slot_3_attack[0], slot_3_attack[1])
                                    mobs[num].got_damage(damage)
                                flag = True
                            else:
                                damage = None
                            if flag:
                                sprites.update()
                                pygame.display.flip()
                                flag = False
                                if mobs:
                                    for step in range(len(mobs)):
                                        if mobs[step].is_died():
                                            pass
                sprites.update()
                pygame.display.flip()
            money += 10
            exp += 10
            lvl_step += 1
    pygame.quit()  # завершение работы:
