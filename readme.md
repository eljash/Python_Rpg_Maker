## Rpg Maker
### Creator: Eljas Hirvelä
### Python version 3.11

# About project

The idea of this project is to make a role-playing game "maker". 
Intention is to have a simple game framework with QUI and Editor QUI 
which enables easy character class and in game item adding/editing.

So far class adding and editing features have been implemented to the editor.
For now items can only be added, but not modified.

The game itself has not been implemented. Game can be launched and 
starting new game will display all the classes that have been made with 
the editor and selecting a class will display all its details.

# Game launching

- Run Game.py from the root directory

# Editor launching

- Run Editor.py from the root directory

# Items

### Item data is stored inside data folder in "items.json" file.

- Item types (ItemType(Enum))
  - VALUABLE = 1
  - USABLE = 2
  - CLOTHING = 3
  - WEAPON = 4
  - PROJECTILE = 5 (ammo, arrows etc.)

- Usable types (UsableType(Enum))
  - DRINK = 1
  - EAT = 2
  - USE = 3

- Usable feature types (UsableFeatureType(Enum))
  - HEAL = 1
  - TAKE_DAMAGE = 2

- Clothing types (ClothingType(Enum))
  - HEAD = 1
  - BODY = 2
  - PANTS = 3
  - BOOTS = 4
  - GLOVES = 5
  - ACCESSORIES = 6

- Clothing feature types (ClothingFeatureType(Enum))
  - SNEAK = 1
  - STRENGTH = 2
  - AGILITY = 3

- Weapon types (WeaponType(Enum))
  - MELEE = 1
  - RANGED = 2

# Character classes

### Class data is stored inside data folder in "classes.json" file.

- Attributes
  - class_id : integer
  - class_name : string
  - starting_money : float
  - health_multiplier : float
  - strength_multiplier : float
  - agility_multiplier : float
  - iq_multiplier : float
  - charisma_multiplier : float
  - reputation_multiplier : float