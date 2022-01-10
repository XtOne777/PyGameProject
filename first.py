from classes import *
import pygame


def battle(player, mob, mode='do'):
    if mode == 'say':
        print(f'Битва между "{player["name"]}" и "{mob["name"]}"')
        print(f'{player["name"]}: {player["health"]}')
        print(f'{mob["name"]}: {mob["health"]}')
        while player.is_died() and mob.is_died():
            argument = input()
            if argument:
                player_dmg = player.heavy_attack()
            else:
                player_dmg = player.low_attack()
            mob_dmg = mob.low_attack()
            player.got_damage(mob_dmg)
            mob.got_damage(player_dmg)
            print(f'{player["name"]}: {player["health"]} (-{mob_dmg})')
            print(f'{mob["name"]}: {mob["health"]} (-{player_dmg})')
    else:
        while player.is_died() and mob.is_died():
            argument = bool(input())
            if argument:
                player_dmg = player.heavy_attack()
            else:
                player_dmg = player.low_attack()
            mob_dmg = mob.low_attack()
            player.got_damage(mob_dmg)
            mob.got_damage(player_dmg)
    if not player.is_died():
        return False
    return True


class Human:
    def __init__(self, name, classes=Standart()):
        if name[0:11] != 'load_data: ':
            self.name = name
            self.max_stamina = 10
            self.max_health = 100
            self.health = 0 + self.max_health
            self.stamina = 0 + self.max_stamina
            self.lvl = 1
            self.exp = 0
            self.classes = classes
        else:
            pass  # тут будет загрузка сохранёных данных

    def __getitem__(self, item):
        if item == 'name':
            return self.name
        if item == 'health':
            return self.health

    def low_attack(self, type_attack=None):
        if type_attack:
            return self.classes.low_attack(type_attack)
        return self.classes.low_attack()

    def heavy_attack(self, type_attack=None, miss_buff=None):
        if self.stamina - 5 >= 0:
            self.stamina -= 5
            if type_attack:
                if miss_buff:
                    return self.classes.heavy_attack(type_attack, miss_buff)
                return self.classes.heavy_attack(type_attack)
            else:
                if miss_buff:
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


class Mob:
    def __init__(self, name, health, dmg):
        self.name = name
        self.health = health
        self.dmg = dmg

    def __getitem__(self, item):
        if item == 'name':
            return self.name
        if item == 'health':
            return self.health

    def low_attack(self, chance=5):
        return self.dmg * 2 if randint(0, 100) < chance else self.dmg

    def got_damage(self, dmg):
        self.health -= dmg

    def is_died(self):
        return self.health > 0


if __name__ == "__main__":
    a = Human('Игрок 1', classes=Magic())
    b = Mob('Гоблин', health=100, dmg=10)
    c = list()
    c.append(battle(a, b, 'say'))
    money = 0
    if c[-1]:
        money += 1
    else:
        pass
    print(money)
