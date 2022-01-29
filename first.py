from classes import *
import pygame
import os
import sys
import csv
import webbrowser

player_name = 'Player 1'
money = 0
exp = 0
lvl_step = 1
mob_lvl = {1: (('goblin', 100, 10),),
           2: (('goblin', 100, 10), ('goblin', 100, 10)),
           3: (('goblin', 100, 10), ('goblin', 100, 10), ('goblin', 100, 10))}
particles = True
auto_save = True
true_inventory = [('', '') for _ in range(15)] + [('heavy_attack', 'Fire'), ('low_attack', 'Normal'), ('heal', 'Holy')]
attacks = {('low_attack', 'Normal'): './textures/player/attacks/low_attack.png',
           ('heavy_attack', 'Fire'): './textures/player/attacks/heavy_attack_fire.png',
           ('heal', 'Holy'): './textures/player/attacks/heal_magic.png'}


class Animation(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, x_transform=1, *group):
        super().__init__(*group)
        self.sprites = []
        self.sprites.append(load_image('./textures/scenes/frog_1.png', 0))
        self.sprites.append(load_image('./textures/scenes/frog_2.png', 0))
        self.sprites.append(load_image('./textures/scenes/frog_3.png', 0))
        self.sprites.append(load_image('./textures/scenes/frog_4.png', 0))
        self.sprites.append(load_image('./textures/scenes/frog_5.png', 0))
        self.sprites.append(load_image('./textures/scenes/frog_6.png', 0))
        self.sprites.append(load_image('./textures/scenes/frog_7.png', 0))
        self.sprites.append(load_image('./textures/scenes/frog_8.png', 0))
        self.sprites.append(load_image('./textures/scenes/frog_9.png', 0))
        self.sprites.append(load_image('./textures/scenes/frog_10.png', 0))
        self.current_sprite = 0
        self.x_transform = x_transform
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (128 * x_transform, 64 * x_transform))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (128 * self.x_transform,
                                                                                64 * self.x_transform))


def save_game():
    file_player = open(f'./{player["name"]}.csv', 'w')
    writer = csv.writer(file_player)
    data_got = player['all']
    writer.writerow(list(data_got[:-1]))
    writer.writerows(data_got[-1])
    file_player.close()


def leadboard_add():
    file_ap = open('./tire_list.csv', 'a')
    writer_csv = csv.writer(file_ap)
    writer_csv.writerow((player_name, lvl_step))
    file_ap.close()


def shop_and_inventory():
    global true_inventory
    sprite_shop = pygame.sprite.Group()
    sprite_inventory = pygame.sprite.Group()
    main_buttons = pygame.sprite.Group()
    inventory_open = False

    button_inventory = pygame.sprite.Sprite()
    button_inventory.image = load_image('./textures/scenes/inventory_button.png', 0)
    button_inventory.rect = button_inventory.image.get_rect()
    button_inventory.rect.x, button_inventory.rect.y = 870, 500
    main_buttons.add(button_inventory)

    scene_shop = pygame.sprite.Sprite()
    scene_shop.image = load_image('./textures/scenes/shop.png', 0)
    scene_shop.rect = scene_shop.image.get_rect()
    scene_shop.rect.x, scene_shop.rect.y = 0, 0
    sprite_shop.add(scene_shop)

    player_sprite = pygame.sprite.Sprite()
    player_sprite.image = pygame.transform.scale(load_image('./textures/player/standart.png'), (140, 170))
    player_sprite.rect = player_sprite.image.get_rect()
    player_sprite.rect.x, player_sprite.rect.y = 100, 300
    sprite_shop.add(player_sprite)

    inventory = pygame.sprite.Sprite()
    inventory.image = load_image('./textures/scenes/inventory.png', 0)
    inventory.rect = inventory.image.get_rect()
    inventory.rect.x, inventory.rect.y = 0, 0

    button_skip = pygame.sprite.Sprite()
    button_skip.image = load_image('./textures/scenes/level_button.png', 0)
    button_skip.rect = button_skip.image.get_rect()
    button_skip.rect.x, button_skip.rect.y = 760, 500
    sprite_shop.add(button_skip)

    font_inventory = pygame.font.Font(None, 30)

    mouse_place = pygame.sprite.Sprite()
    mouse_place.image = pygame.surface.Surface((1, 1))
    mouse_place.rect = mouse_place.image.get_rect()
    mouse_place.rect.x, mouse_place.rect.y = pygame.mouse.get_pos()
    sprite_shop.add(mouse_place)

    global money, exp

    money_inv = pygame.sprite.Sprite()
    money_inv.image = font_inventory.render(f'Деньги: {money}', True, (255, 255, 0))
    money_inv.rect = money_inv.image.get_rect()
    money_inv.rect.x, money_inv.rect.y = 900 - len(str(money)) * 10, 10

    sprite_shop.add(money_inv)

    exp_inv = pygame.sprite.Sprite()
    exp_inv.image = font_inventory.render(f'Опыт: {exp}', True, (100, 100, 255))
    exp_inv.rect = exp_inv.image.get_rect()
    exp_inv.rect.x, exp_inv.rect.y = 910 - len(str(exp)) * 10, 40

    soda = pygame.sprite.Sprite()
    soda.image = load_image('./textures/scenes/soda.png')
    soda.rect = soda.image.get_rect()
    soda.rect.x, soda.rect.y = 790, 240
    sprite_shop.add(soda)

    soda_sound = pygame.mixer.Sound('./data/sounds/mew.mp3')

    sprite_shop.add(exp_inv)

    class Attacks(pygame.sprite.Sprite):
        def __init__(self, pos, name, *group):
            super().__init__(*group)
            if name[0]:
                self.image = pygame.transform.scale(load_image(attacks[name]), (90, 90))
            else:
                self.image = pygame.surface.Surface((0, 0))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos

        def change_pos(self, pos):
            self.rect.x, self.rect.y = pos

    class Slot(pygame.sprite.Sprite):
        def __init__(self, pos, *group):
            super().__init__(*group)
            self.image = pygame.transform.scale(load_image('./textures/scenes/inventory_slot.png', 0), (100, 100))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
            pp = self.image.get_at((0, 0))
            self.colors = pp
            self.click = False

        def return_pos(self):
            return self.rect.x, self.rect.y

        def change_color(self, color):
            color_pos = self.image.get_at((0, 0))
            for x_pos in range(self.image.get_size()[0]):
                for y_pos in range(self.image.get_size()[1]):
                    if self.image.get_at((x_pos, y_pos)) == color_pos:
                        self.image.set_at((x_pos, y_pos), color)

        def clicked(self):
            if self.colors == self.image.get_at((0, 0)):
                self.change_color((255, 0, 0))
                self.click = not self.click
            else:
                self.change_color(self.colors)
                self.click = not self.click

        def reload(self):
            if self.colors != self.image.get_at((0, 0)):
                self.change_color((0, 0, 0))

    slots = list()
    sprite_inventory.add(inventory)
    clicked_slots = []
    true_slots = true_inventory
    for xs in range(5):
        for ys in range(3):
            a = (25 + xs * 100 + 110 * xs, 30 + ys * 100 + 30 * ys)
            slots.append(Slot(a, sprite_inventory))
    for xy in range(3):
        a = (180 + 250 * xy, 455)
        slots.append(Slot(a, sprite_inventory))
    attack_slots = list()
    for i in range(18):
        pose = slots[i].return_pos()
        attack_slots.append(Attacks((pose[0] + 5, pose[1] + 5), true_slots[i], sprite_inventory))

    inventory_shop = True
    while inventory_shop:
        screen.fill((0, 0, 0))

        mouse_place.rect.x, mouse_place.rect.y = pygame.mouse.get_pos()

        if inventory_open:
            sprite_inventory.update()
            sprite_inventory.draw(screen)
        else:
            sprite_shop.update()
            sprite_shop.draw(screen)
        for events in pygame.event.get():
            if events.type == pygame.MOUSEBUTTONUP:
                if pygame.sprite.collide_mask(soda, mouse_place):
                    soda_sound.play()
                    if randint(0, 100) == 100:
                        money += 1
                    money_inv.image = font_inventory.render(f'Деньги: {money}', True, (255, 255, 0))
                    money_inv.rect.x, money_inv.rect.y = 900 - len(str(money)) * 10, 10
                    exp_inv.image = font_inventory.render(f'Опыт: {exp}', True, (100, 100, 255))
                xx, yy = pygame.mouse.get_pos()
                if inventory_open:
                    for number, i in enumerate(slots):
                        xx2, yy2 = i.return_pos()
                        if xx2 <= xx <= xx2 + 100 and yy2 <= yy <= yy2 + 100:
                            i.clicked()
                            clicked_slots.append(number)
                if 870 <= xx <= 960 and 500 <= yy <= 590:
                    inventory_open = not inventory_open
                if 760 <= xx <= 850 and 500 <= yy <= 590 and not inventory_open:
                    inventory_shop = False
            if events.type == pygame.QUIT:
                sys.exit()
        if len(clicked_slots) == 2:
            true_slots[clicked_slots[0]], true_slots[clicked_slots[1]] =\
                true_slots[clicked_slots[1]], true_slots[clicked_slots[0]]
            slots[clicked_slots[0]].reload()
            slots[clicked_slots[1]].reload()
            xd = slots[clicked_slots[1]].return_pos()
            attack_slots[clicked_slots[0]].change_pos((xd[0] + 5, xd[1] + 5))
            xd = slots[clicked_slots[0]].return_pos()
            attack_slots[clicked_slots[1]].change_pos((xd[0] + 5, xd[1] + 5))
            attack_slots[clicked_slots[1]], attack_slots[clicked_slots[0]] =\
                attack_slots[clicked_slots[0]], attack_slots[clicked_slots[1]]
            clicked_slots = []
        main_buttons.update()
        main_buttons.draw(screen)
        pygame.display.flip()
    true_inventory = true_slots


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, *group):
        super().__init__(*group)
        self.velocity = [randint(-15, 15), randint(-5, 5)]
        random = randint(1, 10)
        self.image = pygame.transform.scale(load_image('textures/particles/blood.png', 0), (random, random))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.ticks = 0
        if not particles:
            self.kill()

    def update(self):
        if self.ticks == 10:
            self.kill()
        self.ticks += 1
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.velocity[0] > 0:
            self.velocity[0] -= 2
        elif self.velocity[0] < 0:
            self.velocity[0] += 2
        if self.velocity[1] < 5:
            self.velocity[1] += 1


def create_blood(pos, k=20, *group):
    for _ in range(k):
        Particle(pos, *group)


def slot_color_reload(pos):
    if not player['is_attacking']:
        if 300 <= pos[0] <= 300 + 69 and 488 <= pos[1] <= 488 + 69:
            slot_color_change(slot_1, (255, 255, 0))
            slot_color_change(slot_2)
            slot_color_change(slot_3)
        elif 450 <= pos[0] <= 450 + 69 and 488 <= pos[1] <= 488 + 69:
            slot_color_change(slot_2, (255, 255, 0))
            slot_color_change(slot_1)
            slot_color_change(slot_3)
        elif 600 <= pos[0] <= 600 + 69 and 488 <= pos[1] <= 488 + 69:
            slot_color_change(slot_3, (255, 255, 0))
            slot_color_change(slot_1)
            slot_color_change(slot_2)
        else:
            slot_color_change(slot_1)
            slot_color_change(slot_2)
            slot_color_change(slot_3)


class FontLoad(pygame.sprite.Sprite):
    def __init__(self, place, value, size_value, color, *group):
        super().__init__(*group)
        font = pygame.font.Font(None, size_value)
        self.group = group
        self.text = font.render(str(value), True, color)
        self.image = self.text
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = place
        self.step = 0

    def update(self):
        if self.step <= 25:
            self.rect.y -= 2.5
        else:
            sprites.remove(self)
            self.kill()
        self.step += 1


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


class AttackingZoneClass(pygame.sprite.Sprite):
    def __init__(self, mob_list, *group):
        super().__init__(*group)
        self.image = load_image('./textures/mobs/scale_model.png')
        self.rect = self.image.get_rect()
        self.mob_list = mob_list
        self.rect.x, self.rect.y = mob_list[0]['place']
        self.mob_attack = 0
        self.is_show = False
        self.scaled = False
        self.step = 0

    def update(self):
        if self.is_show:
            self.image.set_alpha(255)
            if self.step == 0:
                if self.scaled:
                    self.image = load_image('./textures/mobs/scale_model.png')
                else:
                    self.image = load_image('./textures/mobs/scale_model_1.png')
            self.step += 1
            if self.step == 30:
                self.step = 0
                self.scaled = not self.scaled
        else:
            self.image.set_alpha(0)

    def mouse_place(self, place):
        x, y = place
        for i in range(len(self.mob_list)):
            xx, yx = self.mob_list[i]['place']
            if xx <= x <= xx + 105 and yx <= y <= yx + 127.5:
                self.rect.x, self.rect.y = xx, yx
                self.mob_attack = i
                break

    def attack(self):
        return self.mob_attack

    def change_picture(self, change):
        self.is_show = change


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
        if name[0]:
            self.attack = pygame.sprite.Sprite()
            self.image = pygame.transform.scale(load_image(attacks[name]), (45, 45))
        else:
            self.attack = pygame.sprite.Sprite()
            self.image = pygame.surface.Surface((0, 0))
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
            self.classes = classes
        else:
            with open(f'./{name[11:]}') as csvfile:
                data = list(csv.reader(csvfile))
                data_get = data[0]
                self.name = data_get[0]
                self.max_health = int(data_get[1])
                self.max_stamina = int(data_get[2])
                if data_get[3] == 'magic':
                    self.classes = Magic()
                elif data_get[3] == 'fighter':
                    self.classes = Fighting()
                else:
                    self.classes = Standart()
                global lvl_step, exp, money, true_inventory
                lvl_step = int(data_get[4])
                exp = int(data_get[5])
                money = int(data_get[6])
                true_inventory = list()
                for i in data[1:]:
                    if len(i) != 0:
                        true_inventory.append(tuple(i))
        image = './textures/player/standart.png'
        self.class_name = 'standart'
        if isinstance(self.classes, Magic):
            image = './textures/player/magic(standart).png'
            self.class_name = 'magic'
        elif isinstance(self.classes, Fighting):
            image = './textures/player/fighter.png'
            self.class_name = 'fighter'
        self.health = 0 + self.max_health
        self.stamina = 0 + self.max_stamina
        self.player = pygame.sprite.Sprite()
        self.image = pygame.transform.scale(load_image(image), (105, 127.5))
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 300

        self.animate = False
        self.step = 0

    def attack(self, attack, type_attack='Normal'):
        if attack:
            if not type_attack:
                type_attack = 'Normal'
            if attack == 'low_attack':
                return self.low_attack(type_attack), 'attack'
            if attack == 'heavy_attack':
                return self.heavy_attack(type_attack), 'attack'
            if attack == 'heal':
                if not isinstance(self.classes, Fighting):
                    heal = randint(20, 50)
                    if isinstance(self.classes, Magic):
                        heal += 20
                    return heal, 'heal'
        if self.stamina + 2 < self.max_stamina:
            self.stamina += 2
        else:
            self.stamina = self.max_stamina + 0
        return 0.0, 'attack'

    def update(self):
        if self.animate:
            if self.step <= 25:
                self.step += 1
            else:
                self.step = 0
                self.animate = False

    def attack_animate(self):
        self.animate = True

    def __getitem__(self, item):
        if item == 'all':
            return self.name, self.max_health, self.max_stamina, self.class_name, lvl_step, exp, money, true_inventory
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
        elif item == 'place':
            return self.rect.x, self.rect.y

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

    def revive(self, health=None, stamina=False):
        if stamina:
            self.stamina = 0 + self.max_stamina
        if self.stamina >= self.max_stamina / 2:
            if not health:
                self.health = 0 + self.max_health
            else:
                self.health += health
            if self.health > self.max_health:
                self.health = 0 + self.max_health
            self.stamina -= self.max_stamina / 2
        else:
            return False
        return True


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
        if item == 'place':
            return self.rect.x, self.rect.y

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

    background_image = load_image('textures/scenes/menu_scene.png', 0)
    setting_img = load_image("textures/scenes/setting_button.png", 0)
    discord_img = pygame.transform.scale(load_image("textures/scenes/Discord_Logo.png"), (90, 90))
    github_img = pygame.transform.scale(load_image("textures/scenes/git_btn.png"), (90, 90))
    # credits_img = load_image("textures/scenes/cred_btn.jpg")
    effect_img = load_image("textures/scenes/ef_btn.png", 0)
    save_img = load_image("textures/scenes/save_btn.png", 0)


    class Button(pygame.sprite.Sprite):
        def __init__(self, xx, yy, image, *groups):
            super().__init__(*groups)
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = (xx, yy)


    sprites = pygame.sprite.Group()
    settings_group = pygame.sprite.Group()
    window_set = pygame.sprite.Sprite()
    window_set.image = load_image('textures/scenes/set_win2.jpg', 0)
    window_set.rect = window_set.image.get_rect()
    window_set.rect.x, window_set.rect.y = 250, 50
    settings_group.add(window_set)
    setting_btn = Button(850, 470, pygame.transform.scale(setting_img, (100, 100)), sprites)
    discord_btn = Button(420, 430, discord_img, settings_group)
    github_btn = Button(570, 430, github_img, settings_group)
    # credits_btn = Button(260, 460, credits_img, settings_group)
    effect_btn = Button(370, 130, effect_img, settings_group)
    save_btn = Button(370, 330, save_img, settings_group)
    btn_click = False
    clock = pygame.time.Clock()
    pygame.display.flip()
    running = True
    start_menu = True
    start_game = False
    clock.tick(60)
    good_load('./textures/scenes/menu_scene.png', './textures/scenes/button_play.png')
    try:
        while running:
            while start_menu:
                screen.fill((0, 0, 0))
                screen.blit(load_image('./textures/scenes/menu_scene.png', 0), (0, 0))
                screen.blit(pygame.transform.scale(load_image('./textures/scenes/button_play.png'), (150, 150)),
                            (410, 400))
                sprites.draw(screen)
                sprites.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        # slot_color_change(effect_btn, (255, 0, 0)) - так надо менять цвета на красный
                        # slot_color_change(effect_btn, (0, 255, 0)) - а так на зеленый
                        x1, y1 = pygame.mouse.get_pos()
                        if 750 <= x1 <= 950 and 470 <= y1 <= 570:
                            btn_click = not btn_click
                        if not btn_click:
                            if 410 <= event.pos[0] <= 410 + 150 and 400 <= event.pos[1] <= 550:
                                start_menu = False
                                start_game = True
                                load_game()
                        else:
                            if 370 <= event.pos[0] <= 370 + 200 and 130 <= event.pos[1] <= 130 + 67:
                                if particles:
                                    slot_color_change(effect_btn, (255, 0, 0))
                                    particles = False
                                else:
                                    slot_color_change(effect_btn, (0, 255, 0))
                                    particles = True
                            elif 370 <= event.pos[0] <= 370 + 200 and 330 <= event.pos[1] <= 330 + 67:
                                if auto_save:
                                    slot_color_change(save_btn, (255, 0, 0))
                                    auto_save = False
                                else:
                                    slot_color_change(save_btn, (0, 255, 0))
                                    auto_save = True
                            elif 420 <= event.pos[0] <= 420 + 90 and 430 <= event.pos[1] <= 430 + 90:
                                webbrowser.open('https://discord.com/invite/sRH3PQFCHY', new=2)
                            elif 570 <= event.pos[0] <= 570 + 90 and 430 <= event.pos[1] <= 430 + 90:
                                webbrowser.open('https://github.com/XtOne777/PyGameProject', new=2)
                if btn_click:
                    settings_group.draw(screen)
                    settings_group.update()
                if not running:
                    break
                pygame.display.flip()
            while running:
                sprites.empty()
                anim_group = pygame.sprite.Group()
                animation = Animation(180, 150, 5, anim_group)
                load_text = pygame.sprite.Sprite()
                load_text.image = load_image('./textures/scenes/load_image.png', 0)
                load_text.rect = load_text.image.get_rect()
                load_text.rect.x, load_text.rect.y = 350, 10
                anim_group.add(load_text)

                def animation_next():
                    screen.fill((0, 0, 0))
                    anim_group.update()
                    anim_group.draw(screen)
                    pygame.display.flip()
                    clock.tick(20)


                # Главная сцена
                main_scene = pygame.sprite.Sprite()
                main_scene.image = load_image('./textures/scenes/scene(lvl 1).png', 0)
                main_scene.rect = main_scene.image.get_rect()
                main_scene.rect.x, main_scene.rect.y = 0, 0
                sprites.add(main_scene)

                # Игрок
                list_files = os.listdir()
                player = None
                for file in list_files:
                    if file[-4:] == '.csv' and file != 'tire_list.csv':
                        player = Human(f'load_data: {file}', Magic(), sprites)
                        player_name = file[:-4]
                        break
                if not player:
                    name_inp = ''
                    stop_name = True
                    font1 = pygame.font.Font(None, 50)
                    tick = 0
                    while stop_name:
                        screen.fill((0, 0, 0))
                        add_symbol = False
                        text1_text = 'Введите имя персонажа:'
                        font1.set_underline(False)
                        text1 = font1.render(text1_text, True, (255, 255, 255))
                        font1.set_underline(True)
                        text2 = font1.render(name_inp, True, (255, 255, 255))
                        for event in pygame.event.get():
                            if event.type == pygame.KEYUP:
                                if len(pygame.key.name(event.key)) == 1:
                                    name_inp += pygame.key.name(event.key).upper()
                                elif pygame.key.name(event.key) == 'backspace':
                                    name_inp = name_inp[:-1]
                                if event.key == pygame.K_RETURN:
                                    stop_name = False
                        screen.blit(text1, (275, 200))
                        screen.blit(text2, (470 - len(name_inp) * 10, 300))
                        pygame.display.update()
                    player_name = name_inp
                    player = Human(name_inp, Magic(), sprites)
                animation_next()

                # Полоска жизней
                health_bar_line = HealthBar(player, sprites)

                health_bar = pygame.sprite.Sprite()
                health_bar.image = load_image('./textures/player/info/health_bar.png')
                health_bar.rect = health_bar.image.get_rect()
                health_bar.rect.x, health_bar.rect.y = 0, 0
                sprites.add(health_bar)
                animation_next()

                # Полоска стамины
                stamina_bar_line = StaminaBar(player, sprites)

                stamina_bar = pygame.sprite.Sprite()
                stamina_bar.image = load_image('./textures/player/info/stamina_bar.png', (255, 255, 255))
                stamina_bar.rect = stamina_bar.image.get_rect()
                stamina_bar.rect.x, stamina_bar.rect.y = 45, 95
                sprites.add(stamina_bar)
                animation_next()

                # Слоты атак
                slot_1 = slot_load('./textures/player/attacks/slot_1.png', (300, 488))
                animation_next()
                slot_2 = slot_load('./textures/player/attacks/slot_2.png', (450, 488))
                animation_next()
                slot_3 = slot_load('./textures/player/attacks/slot_3.png', (600, 488))
                animation_next()
                sprites.add(slot_1)
                sprites.add(slot_2)
                sprites.add(slot_3)
                animation_next()

                # Мобы
                mobs = list()
                mobs_list = mob_lvl[lvl_step]
                check_list = list()
                for mob_data in mobs_list:
                    check_list.append(mob_data)
                    animation_next()
                for steps in range(len(mobs_list)):
                    mobs.append(Mob(check_list[steps][0], check_list[steps][1], check_list[steps][2],
                                    (600 + (steps % 2) * 100, 150 + 200 / len(mobs_list) * (steps + 1)), sprites))
                animation_next()

                # Зоны атаки
                AttackingZone = AttackingZoneClass(mobs, sprites)
                for _ in range(15):
                    animation_next()

                # Старт игры
                shop_and_inventory()
                animation_next()

                # Атаки
                slot_1_attack = true_inventory[15]
                Attack(slot_1_attack, 1, sprites)
                animation_next()
                slot_2_attack = true_inventory[16]
                Attack(slot_2_attack, 2, sprites)
                animation_next()
                slot_3_attack = true_inventory[17]
                Attack(slot_3_attack, 3, sprites)
                animation_next()
                
                rage_quit = False

                while start_game:
                    screen.fill((0, 0, 0))
                    if not player.is_died():
                        if auto_save:
                            os.remove(f'./{player["name"]}.csv')
                            leadboard_add()
                        good_load('./textures/scenes/game_over.png',
                                  './textures/scenes/game_over_RIP.png')
                        fonts = pygame.font.Font(None, 30)
                        screen.blit(fonts.render(f'{player_name} дошёл до {lvl_step} уровня!', True, (255, 255, 255)),
                                    (350, 200))
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    sys.exit()
                            pygame.display.flip()
                    slot_color_reload(pygame.mouse.get_pos())  # Желтые или серые слоты
                    sprites.draw(screen)
                    slot_color_change(slot_1)
                    slot_color_change(slot_2)
                    slot_color_change(slot_3)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            start_game = False
                            rage_quit = True
                            running = False
                        if event.type == pygame.MOUSEMOTION:
                            pass
                        if event.type == pygame.MOUSEBUTTONUP:
                            if not player['is_attacking']:
                                flag = False
                                if 300 <= event.pos[0] <= 300 + 69 and 488 <= event.pos[1] <= 488 + 69:
                                    slot_color_change(slot_1, (255, 0, 0))
                                    damage, type_move = player.attack(slot_1_attack[0], slot_1_attack[1])
                                    flag = True
                                elif 450 <= event.pos[0] <= 450 + 69 and 488 <= event.pos[1] <= 488 + 69:
                                    slot_color_change(slot_2, (255, 0, 0))
                                    damage, type_move = player.attack(slot_2_attack[0], slot_2_attack[1])
                                    flag = True
                                elif 600 <= event.pos[0] <= 600 + 69 and 488 <= event.pos[1] <= 488 + 69:
                                    slot_color_change(slot_3, (255, 0, 0))
                                    damage, type_move = player.attack(slot_3_attack[0], slot_3_attack[1])
                                    flag = True
                                else:
                                    damage = None
                                    type_move = 'attack'
                                if flag:
                                    if type_move == 'attack':
                                        stop = False
                                        AttackingZone.change_picture(True)
                                        while not stop:
                                            screen.fill((0, 0, 0))
                                            sprites.draw(screen)
                                            for event_2 in pygame.event.get():
                                                if event_2 == pygame.QUIT:
                                                    stop = True
                                                    rage_quit = True
                                                    running = False
                                                if event_2.type == pygame.MOUSEBUTTONUP:
                                                    num = AttackingZone.attack()
                                                    mobs[num].got_damage(damage)
                                                    place_mob = list(mobs[num]['place'])
                                                    place_mob[0] -= 20
                                                    FontLoad(place_mob, f'-{damage}', 35, (255, 70, 70), sprites)
                                                    stop = True
                                                if event_2.type == pygame.MOUSEMOTION:
                                                    AttackingZone.mouse_place(event_2.pos)
                                            sprites.update()
                                            pygame.display.flip()
                                        AttackingZone.change_picture(False)
                                        player.attack_animate()
                                    elif type_move == 'heal':
                                        player_place = list(player['place'])
                                        player_place[0] += 100
                                        if player.revive(damage):
                                            FontLoad(player_place, f'+{damage}', 35, (0, 255, 0, 255), sprites)
                                        else:
                                            FontLoad((100, 250), 'Не хватает стамины!', 40, (255, 255, 255, 255),
                                                     sprites)
                                            continue
                                    flag = False
                                    if mobs:
                                        mob_died = 0
                                        player_place = list(player['place'])
                                        player_place[0] += 45
                                        player_place[1] += 55
                                        create_blood(player_place, 20, sprites)
                                        for step in range(len(mobs)):
                                            if mobs[step].is_died():
                                                damage_mob = mobs[step].low_attack()
                                                player.got_damage(damage_mob)
                                                player_place = list(player['place'])
                                                player_place[0] += 100
                                                player_place[1] += 20 + 20 * step
                                                FontLoad(player_place, f'-{damage_mob}', 35, (255, 70, 70), sprites)
                                            else:
                                                mob_died += 1
                                        if mob_died == len(mobs):
                                            start_game = False
                    sprites.update()
                    pygame.display.flip()
                for _ in range(30):
                    screen.fill((0, 0, 0))
                    sprites.update()
                    sprites.draw(screen)
                    pygame.display.flip()
                if not rage_quit:
                    money += 10
                    exp += 10
                    lvl_step += 1
                    start_game = True
                if auto_save:
                    save_game()
    except KeyError as e:
        print(e)
        print('YOU WIN')  # сюда надо заставку "Ты победил"
        if auto_save:
            leadboard_add()
            os.remove(f'./{player_name}.csv')
    pygame.quit()  # завершение работы
