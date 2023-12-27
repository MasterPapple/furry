from random import randint
import copy

class Weapon:
    def __init__(self, name, attack_power, defense_power, durability):
        self.name = name
        self.attack_power = attack_power
        self.defense_power = defense_power
        self.durability = durability

    def decrease_durability(self, hero, amount=1):
        self.durability -= amount
        if self.durability <= 0:
            hero.weapon = None


weapons = [
    Weapon('Silver Knife', 2, 0, 1),
    Weapon('Sword', 3, 0, 2),
    Weapon('Big Axe', 4, 0, 1),
    Weapon('Long Spear', 3, 0, 1)
]

def get_random_weapon():
    n = randint(1, len(weapons)) - 1
    return copy.deepcopy(weapons[n])


"""class Warrior:
    def __init__(self, name, strength, agility, intelligence):
        self.name = name
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.left_hand_weapon = None
        self.right_hand_weapon = None

    def arm(self, weapon):
        if weapon.is_double_handed:
            self.arm_double_handed(weapon)
        else:
            if self.left_hand_weapon is None:
                self.arm_left_hand(weapon)
            elif self.right_hand_weapon is None:
                self.arm_left_hand(weapon)

    def arm_left_hand(self, weapon):
        if not weapon.is_double_handed:
            self.left_hand_weapon = weapon

    def arm_right_hand(self, weapon):
        if not weapon.is_double_handed:
            self.right_hand_weapon = weapon

    def arm_double_handed(self, weapon):
        if weapon.is_double_handed:
            self.left_hand_weapon = weapon
            self.right_hand_weapon = weapon

    def get_attack_power(self):
        power = self.strength
        if self.left_hand_weapon is not None and not self.left_hand_weapon.is_double_handed:
            power += self.left_hand_weapon.attack_power
        if self.right_hand_weapon is not None and not self.right_hand_weapon.is_double_handed:
            power += self.right_hand_weapon.attack_power
        if self.left_hand_weapon is not None and self.left_hand_weapon.is_double_handed:
            power += self.left_hand_weapon.attack_power
        return power

    def __str__(self):
        return self.name + ' (' + str(self.left_hand_weapon) + '/' + str(self.right_hand_weapon) + ')"""


