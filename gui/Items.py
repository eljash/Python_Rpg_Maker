from enum import Enum


class ItemType(Enum):
    VALUABLE = 1
    USABLE = 2
    CLOTHING = 3
    WEAPON = 4
    PROJECTILE = 5


class UsableType(Enum):
    DRINK = 1
    EAT = 2
    USE = 3


class UsableFeatureType(Enum):
    HEAL = 1
    TAKE_DAMAGE = 2


class ClothingType(Enum):
    HEAD = 1
    BODY = 2
    PANTS = 3
    BOOTS = 4
    GLOVES = 5
    ACCESSORIES = 6


class WeaponType(Enum):
    MELEE = 1
    RANGED = 2


class ClothingFeatureType(Enum):
    SNEAK = 1
    STRENGTH = 2
    AGILITY = 3


class Item:
    # INTERFACE FOR DIFFERENT TYPES ITEMS

    def __init__(self, item_id, item_type: ItemType, name: str, value: float, icon_name: str):
        self.id = item_id
        self.type = item_type
        self.name = name
        self.value = value
        self.icon = icon_name

    # METHODS

    def increase_value(self, amount: float) -> bool:
        self.value += amount
        return True

    # SETTERS

    def set_name(self, name: str) -> bool:
        self.name = name
        return True

    def set_value(self, value: float) -> bool:
        self.value = value
        return True

    def set_icon(self, icon_name: str) -> bool:
        self.icon = icon_name
        return True

    # GETTERS

    def get_id(self):
        return self.id

    def get_icon_name(self):
        return self.icon

    def get_value(self) -> float:
        return self.value

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> ItemType:
        return self.type


class Valuable(Item):
    # Valuable item, cannot be utilized in any other way, but value vice

    def __init__(self, item_id: int, name: str, value: float, icon_name: str = ""):
        super().__init__(item_id, ItemType.VALUABLE, name, value, icon_name)


class UsableEffect:
    # Defines what features a usable item has (healing etc.)

    def __init__(self, name: str, feature_type: UsableFeatureType, feature_value: int):
        self.feature_name = name
        self.feature_type = feature_type
        self.feature_value = feature_value

    # METHODS

    def use(self):
        pass

    # GETTERS

    def get_feature_name(self):
        return self.feature_name

    def get_feature_value(self):
        return self.feature_value

    def get_feature_type(self) -> UsableFeatureType:
        return self.feature_type


class Usable(Item):
    # Usable item

    def __init__(self, item_id: int, name: str, value: float, usable_type: UsableType,
                 effects: [] = [], icon_name: str = ""):
        super().__init__(item_id, ItemType.USABLE, name, value, icon_name)
        self.usable_type = usable_type
        self.effects = effects

    # METHODS

    def get_usable_type(self) -> UsableType:
        return self.usable_type

    def get_effects(self) -> []:
        return self.effects

    def add_effect(self, effect: UsableEffect) -> bool:
        self.effects.append(effect)
        return True

    def use(self):
        # Define use case by UsableTypes-enum given to item
        match self.usable_type:
            case UsableType.DRINK:
                pass
            case UsableType.EAT:
                pass
            case UsableType.USE:
                pass
        for e in self.effects:
            if type(e) == UsableEffect:
                e.use()


class ClothingFeature:
    # Class to represent features for clothes.

    def __init__(self, name: str, feature_type: ClothingFeatureType, feature_value: int):
        self.name = name
        self.feature = feature_type
        self.feature_value = feature_value

    def get_name(self) -> str:
        return self.name

    def get_feature(self) -> ClothingFeatureType:
        return self.feature

    def get_value(self) -> float:
        return self.feature_value


class Clothing(Item):
    # Clothes can have multiple features (ClothingFeatures)

    def __init__(self, item_id: int, name: str, value: float, clothing_type: ClothingType,
                 features: [] = [], icon_name: str = ""):
        super().__init__(item_id, ItemType.CLOTHING, name, value, icon_name)
        self.clothing_type = clothing_type
        self.features = features

    # METHODS

    def add_feature(self, feature: ClothingFeature) -> bool:
        self.features.append(feature)
        return True

    # GETTERS

    def get_clothing_type(self) -> ClothingType:
        return self.clothing_type

    def get_features(self) -> [ClothingFeature]:
        return self.features


class Projectile(Item):
    # Class to define different projectile types (ammo, arrows..)

    def __init__(self, item_id: int, name: str, value: float, dmg: int, icon_name: str = ""):
        super().__init__(item_id, ItemType.PROJECTILE, name, value, icon_name)
        self.damage = dmg

    # GETTERS

    def get_damage(self):
        return self.damage


class Weapon(Item):
    # Weapon, used for fighting

    def __init__(self, item_id: int, name: str, value: float, weapon_type: WeaponType,
                 dmg: int, projectile: Projectile | str = None, icon_name: str = ""):
        super().__init__(item_id, ItemType.WEAPON, name, value, icon_name)
        self.weapon_type = weapon_type
        self.weapon_damage = dmg
        self.projectile = projectile

    # GETTERS

    def get_weapon_type(self) -> WeaponType:
        return self.weapon_type

    def get_damage(self) -> int:
        return self.weapon_damage

    def get_projectile(self) -> Projectile | None:
        return self.projectile
