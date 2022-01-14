from random import randint


def dupe(number):
    return float(str(number)[0:str(number).find('.') + 3])  # Округление


class Standart:
    def __init__(self, dam=10, chance=10, miss=5):
        self.damage = dam  # Урон
        self.critical_chance = chance  # Шанс на крит. урон
        self.miss_chance = miss  # Шанс на общий промах
        self.heavy_attack_buff = 2  # Усиление сильных атак
        self.buff = 1  # Обычное усиление атак

    def low_attack(self, type_attack='Normal'):
        total = 0.0
        if type_attack == 'Normal':
            # Стандарт
            bonus = self.damage if randint(0, 100) <= self.critical_chance else 0  # Бонусный урон(крит, тип атаки)
            total = randint(80, 120) * self.damage / 100 + bonus if randint(0, 100) > self.miss_chance else 0
            total = total * self.buff  # Стандартное усиление

        elif type_attack == 'Fire':
            # Крит урон +50%; Доп. урон(в районе от 0.5 до 5);
            # Бонусный урон(крит, тип атаки)
            bonus = self.damage * 1.5 + 0.5 * randint(1, 10) if randint(0, 100) <= self.critical_chance else 0

            total = randint(80, 120) * self.damage / 100 + bonus \
                if randint(0, 100) > self.miss_chance \
                else 0
            total = total * self.buff * self.heavy_attack_buff  # Стандартное усиление + усиление сильных атак

        elif type_attack == 'Water':
            # Крит урон +30%; Доп. урон(в районе от 0.2 до 10);
            # Бонусный урон(крит, тип атаки)
            bonus = self.damage * 1.3 + 0.2 * randint(1, 50) if randint(0, 100) <= self.critical_chance else 0

            total = randint(80, 120) * self.damage / 100 + bonus \
                if randint(0, 100) > self.miss_chance \
                else 0
            total = total * self.buff * self.heavy_attack_buff  # Стандартное усиление + усиление сильных атак

        elif type_attack == 'Wind':
            # Крит урон +50%; Доп. урон(в районе от 0.2 до 8); Доп крит. шанс +10%
            # Бонусный урон(крит, тип атаки)
            bonus = self.damage * 1.5 + 0.2 * randint(1, 40) if randint(0, 100) <= self.critical_chance + 10 else 0

            total = randint(80, 120) * self.damage / 100 + bonus \
                if randint(0, 100) > self.miss_chance \
                else 0
            total = total * self.buff * self.heavy_attack_buff  # Стандартное усиление + усиление сильных атак

        elif type_attack == 'Grass':
            # Крит урон +25%; Доп. урон(в районе от 0.2 до 10); Шанс крит. урона +10%
            # Бонусный урон(крит, тип атаки)
            bonus = self.damage * 1.25 + 0.2 * randint(1, 50) if randint(0, 100) <= self.critical_chance + 10 else 0

            total = randint(80, 120) * self.damage / 100 + bonus \
                if randint(0, 100) > self.miss_chance \
                else 0
            total = total * self.buff * self.heavy_attack_buff  # Стандартное усиление + усиление сильных атак
        return dupe(total)

    def heavy_attack(self, type_attack='Normal', miss_buff=2):
        total = 0.0
        if type_attack == 'Normal':
            # Стандарт
            bonus = self.damage if randint(0, 100) <= self.critical_chance else 0  # Бонусный урон(крит, тип атаки)
            total = randint(80, 120) * self.damage / 100 + bonus\
                if randint(0, 100) > self.miss_chance * miss_buff\
                else 0
            total = total * self.buff * self.heavy_attack_buff

        elif type_attack == 'Fire':
            # Крит урон +50%; Доп. урон(в районе от 0.5 до 25); Доп крит. шанс +15%
            # Бонусный урон(крит, тип атаки)
            bonus = self.damage * 1.5 + 0.5 * randint(1, 50) if randint(0, 100) <= self.critical_chance + 15 else 0
            total = randint(80, 120) * self.damage / 100 + bonus \
                if randint(0, 100) > self.miss_chance * miss_buff \
                else 0
            total = total * self.buff * self.heavy_attack_buff  # Стандартное усиление + усиление сильных атак

        elif type_attack == 'Water':
            # Крит урон +50%; Доп. урон(в районе от 0.2 до 20);
            # Бонусный урон(крит, тип атаки)
            bonus = self.damage * 1.5 + 0.2 * randint(1, 100) if randint(0, 100) <= self.critical_chance else 0

            total = randint(80, 120) * self.damage / 100 + bonus \
                if randint(0, 100) > self.miss_chance * miss_buff \
                else 0
            total = total * self.buff * self.heavy_attack_buff  # Стандартное усиление + усиление сильных атак

        elif type_attack == 'Wind':
            # Крит урон +70%; Доп. урон(в районе от 0.2 до 8); Доп крит. шанс +20%
            # Бонусный урон(крит, тип атаки)
            bonus = self.damage * 1.7 + 0.2 * randint(1, 40) if randint(0, 100) <= self.critical_chance + 20 else 0

            total = randint(80, 120) * self.damage / 100 + bonus \
                if randint(0, 100) > self.miss_chance * miss_buff \
                else 0
            total = total * self.buff * self.heavy_attack_buff  # Стандартное усиление + усиление сильных атак

        elif type_attack == 'Grass':
            # Крит урон +55%; Доп. урон(в районе от 0.2 до 10); Шанс крит. урона +40%
            # Бонусный урон(крит, тип атаки)
            bonus = self.damage * 1.55 + 0.2 * randint(1, 50) if randint(0, 100) <= self.critical_chance + 40 else 0

            total = randint(80, 120) * self.damage / 100 + bonus \
                if randint(0, 100) > self.miss_chance \
                else 0
            total = total * self.buff * self.heavy_attack_buff  # Стандартное усиление + усиление сильных атак
        return dupe(total)

    def change(self, dam):
        self.damage = dam    # Изменение урона


class Fighting(Standart):
    def __init__(self, dam=12, chance=20, miss=8):
        super().__init__(dam=dam, chance=chance, miss=miss)  # Урон, шанс на крит, шанс на промах
        # Усиленние на обычные(на 20%) и сильные(на 150%) атаки
        self.buff = 1.2
        self.heavy_attack_buff = 2.5

    def heavy_attack(self, type_attack='Normal', miss_buff=2.25):
        # Шанс промаха увеличен на 0.5
        return super().heavy_attack(miss_buff=miss_buff, type_attack=type_attack)


class Magic(Standart):
    def __init__(self, dam=14, chance=10, miss=5):
        super().__init__(dam=dam, chance=chance, miss=miss)
        # Усиленние на обычные(на 40%) и сильные(на 300%) атаки
        self.buff = 1.4
        self.heavy_attack_buff = 3  # Нуждается в изменение(Возможно)

    def heavy_attack(self, type_attack='Normal', miss_buff=2.25):
        # Шанс промаха увеличен на 1.0
        return super().heavy_attack(type_attack=type_attack, miss_buff=miss_buff)
