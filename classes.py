from random import randint


class Standart:
    def __init__(self, dam=10, chance=10, miss=5):
        self.damage = dam
        self.critical_chance = chance
        self.miss_chance = miss
        self.heavy_attack_buff = 2
        self.buff = 1

    def low_attack(self, type_attack='Normal'):
        total = 0.0
        if type_attack == 'Normal':
            bonus = self.damage if randint(0, 100) <= self.critical_chance else 0
            total = randint(80, 120) * self.damage / 100 + bonus if randint(0, 100) > self.miss_chance else 0
            total = total * self.buff
        if type_attack == 'Fire':
            bonus = self.damage * 1.5 + 0.5 * randint(1, 10) if randint(0, 100) <= self.critical_chance else 0
            total = randint(80, 120) * self.damage / 100 + bonus \
                if randint(0, 100) > self.miss_chance \
                else 0
            total = total * self.buff * self.heavy_attack_buff
        return total

    def heavy_attack(self, type_attack='Normal', miss_buff=2):
        total = 0.0
        if type_attack == 'Normal':
            bonus = self.damage if randint(0, 100) <= self.critical_chance else 0
            total = randint(80, 120) * self.damage / 100 + bonus\
                if randint(0, 100) > self.miss_chance * miss_buff\
                else 0
            total = total * self.buff * self.heavy_attack_buff
        if type_attack == 'Fire':
            bonus = self.damage * 1.5 + 0.5 * randint(1, 10) if randint(0, 100) <= self.critical_chance else 0
            total = randint(80, 120) * self.damage / 100 + bonus \
                if randint(0, 100) > self.miss_chance * miss_buff \
                else 0
            total = total * self.buff * self.heavy_attack_buff
        return total

    def change(self, dam):
        self.damage = dam


class Fighting(Standart):
    def __init__(self, dam=12, chance=20, miss=8):
        super().__init__(dam=dam, chance=chance, miss=miss)
        self.buff = 1.2
        self.heavy_attack_buff = 2.5

    def heavy_attack(self, type_attack='Normal', miss_buff=2.5):
        return super().heavy_attack(miss_buff=miss_buff)


class Magic(Standart):
    def __init__(self, dam=14, chance=10, miss=5):
        super().__init__(dam=dam, chance=chance, miss=miss)
        self.buff = 1.4
        self.heavy_attack_buff = 3

    def heavy_attack(self, type_attack='Normal', miss_buff=3):
        return super().heavy_attack(miss_buff=miss_buff)
