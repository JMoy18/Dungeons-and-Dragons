class Creature:
    def __init__(self, name, initiative, health, armorClass, quantity = 1, is_player=False, id = None):
        self.id = id
        self.name = name
        self.initiative = initiative
        self.is_player = is_player
        self.health = health
        self.quantity = quantity
        self.armorClass = armorClass
