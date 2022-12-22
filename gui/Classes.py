class Class:

    # float-arvoiset parametrit vaikuttavat käyttäjän eri ominaisuuksien kertoimiin
    def __init__(self, class_id: int, class_name: str, starting_money: float,
                 health_mlt: float, strength_mlt: float,
                 agility_mlt: float, iq_mlt: float,
                 charisma_mlt: float, reputation_mlt: float):
        self.class_id = class_id
        self.className = class_name
        self.starting_money = starting_money
        self.health_multiplier = health_mlt
        self.strength_multiplier = strength_mlt
        self.agility_multiplier = agility_mlt
        self.iq_multiplier = iq_mlt
        self.charisma_multiplier = charisma_mlt
        self.reputation_multiplier = reputation_mlt

    # GETTERS
    def get_class_id(self) -> int:
        return self.class_id

    def get_class_name(self) -> str:
        return self.className

    def get_starting_money(self) -> float:
        return self.starting_money

    def get_health_multiplier(self) -> float:
        return self.health_multiplier

    def get_strength_multiplier(self) -> float:
        return self.strength_multiplier

    def get_agility_multiplier(self) -> float:
        return self.agility_multiplier

    def get_iq_multiplier(self) -> float:
        return self.iq_multiplier

    def get_charisma_multiplier(self) -> float:
        return self.charisma_multiplier

    def get_reputation_multiplier(self) -> float:
        return self.reputation_multiplier

    # SETTERS

    def set_class_id(self, id: int):
        self.class_id = id

    def set_class_name(self, name: str):
        self.className = name

    def set_starting_money(self, starting_money: float):
        self.starting_money = round(starting_money, 2)

    def set_health_multiplier(self, health_multiplier: float):
        self.health_multiplier = round(health_multiplier, 4)

    def set_strength_multiplier(self, strength_multiplier: float):
        self.strength_multiplier = round(strength_multiplier, 4)

    def set_agility_multiplier(self, agility_multiplier: float):
        self.agility_multiplier = round(agility_multiplier, 4)

    def set_iq_multiplier(self, iq_multiplier: float):
        self.iq_multiplier = round(iq_multiplier, 4)

    def set_charisma_multiplier(self, charisma_multiplier: float):
        self.charisma_multiplier = round(charisma_multiplier, 4)

    def set_reputation_multiplier(self, reputation_multiplier: float):
        self.reputation_multiplier = round(reputation_multiplier, 4)

    # METHODS

    def calculate_health(self, health: int) -> int:
        return round(health * self.health_multiplier)

    def calculate_strength(self, strength: int) -> int:
        return round(strength * self.strength_multiplier)

    def calculate_agility(self, agility: int) -> int:
        return round(agility * self.agility_multiplier)

    def calculate_iq(self, iq: int) -> int:
        return round(iq * self.iq_multiplier)

    def calculate_charisma(self, charisma: int) -> int:
        return round(charisma * self.charisma_multiplier)

    def calculate_reputation(self, reputation: int) -> int:
        return round(reputation * self.reputation_multiplier)
