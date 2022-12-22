from gui.Classes import Class
from gui.Items import Item, Usable


class Unit:
    """Base class for all 'units' in game. """

    def __init__(self, name: str, health: int, strength: int):
        self.name = name
        self.max_health = health
        self.current_health = health
        self.strength = strength
        self.isDead = False

    # METHODS

    def use_item(self, item: Usable):
        """Function takes a usable item as a parameter"""
        print("{0} uses {1}".format(self.name, item.get_name()))
        item.use(self)

    def heal(self, amount: int) -> float:
        """Heals unit x-amount and return current health after healing"""
        print("{0} heals for {1}".format(self.name, amount))
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        return self.current_health

    def take_damage(self, amount: int) -> float:
        """Unit takes x-amount of damage. If health goes 0 or below, unit dies"""
        print("{0} takes {1} damage to health".format(self.name, amount))
        self.current_health -= amount
        if self.current_health <= 0:
            self.isDead = True
        return self.current_health

    # GETTERS

    def get_max_health(self) -> int:
        return self.max_health

    def get_health(self) -> int:
        return self.current_health

    def get_strength(self) -> int:
        return self.strength


class Character(Unit):

    # CHARACTER DEFAULT VARIABLES
    DEFAULT_HEALTH: int = 100
    DEFAULT_STRENGTH: int = 10
    DEFAULT_AGILITY: int = 10
    DEFAULT_IQ: int = 50
    DEFAULT_CHARISMA: int = 20
    DEFAULT_REPUTATION: int = 5
    DEFAULT_MONEY: float = 25.50
    DEFAULT_INVENTORY: [] = []
    DEFAULT_CARS: [] = []
    DEFAULT_HOUSES: [] = []
    DEFAULT_INCOME: [] = []

    def __init__(self, player_class: Class, player_id: int = -1, player_name: str = "Nimetön",
                 health: int = DEFAULT_HEALTH, strength: int = DEFAULT_STRENGTH,
                 agility: int = DEFAULT_AGILITY, iq: int = DEFAULT_IQ,
                 charisma: int = DEFAULT_CHARISMA, reputation: int = DEFAULT_CHARISMA,
                 money: float = DEFAULT_MONEY, inventory: [] = DEFAULT_INVENTORY,
                 cars: [] = DEFAULT_CARS, houses: [] = DEFAULT_HOUSES,
                 income: [] = DEFAULT_INVENTORY):

        super().__init__(player_name, health, strength)

        self.player_class = player_class

        self.id = player_id
        self.name = player_name

        self.agility = agility
        self.iq = iq
        self.charisma = charisma
        self.reputation = reputation
        self.money = money
        self.inventory = inventory
        self.cars = cars
        self.houses = houses
        self.income = income

    # METHODS
    def add_money(self, money: float) -> bool:
        # Only add positive values to character money variable
        if money > 0:
            self.money += money
            return True
        return False

    # SETTERS


    # GETTERS
    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_health(self) -> int:
        return self.player_class.calculate_health(self.max_health)

    def get_strength(self) -> int:
        return self.player_class.calculate_strength(self.strength)

    def get_agility(self) -> int:
        return self.player_class.calculate_agility(self.agility)

    def get_iq(self) -> int:
        return self.player_class.calculate_iq(self.iq)

    def get_charisma(self) -> int:
        return self.player_class.calculate_charisma(self.charisma)

    def get_reputation(self) -> int:
        return self.player_class.calculate_reputation(self.reputation)

    def get_details(self) -> []:
        """Return list of string containing all character details"""
        return ["Health: {}".format(self.get_health()), "Strength: {}".format(self.get_strength()),
                       "Agility: {}".format(self.get_agility()), "Iq: {}".format(self.get_iq()),
                       "Charisma: {}".format(self.get_charisma()), "Reputation: {}".format(self.get_reputation())]
