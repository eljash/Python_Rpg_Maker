import Details
import json
import io
import os
from gui.Root import GuiRoot
from gui.Classes import Class
import gui.Items as Items


class ItemLoader:
    # Handles item loading tasks

    def __init__(self):
        # Creates item-objects from json file items.json
        self.FILE = 'data/items.json'
        self.ITEMS_JSON_DEFAULT = {"Items": []}
        self.startup_check()
        self.file = open(self.FILE, 'r')
        self.data = json.load(self.file)
        self.file.close()

        self.items = [[], [], [], [], []]

        # DICTIONARY CONTAINING ALL DIFFERENT GAME ITEMS CATEGORIZED
        #self.items = {
        #    "valuables": [],
        #    "weapons": [],
        #    "usables": [],
        #    "clothing": [],
        #    "projectiles": []
        #}
        self.load_items_from_json()

    def startup_check(self):
        # CHECKS IF THE JSON FILE EXISTS, IF NOT, CREATES A NEW ONE
        try:
            with open(self.FILE, 'r') as fp:
                json.load(fp)
        except:
            with open(self.FILE, 'w') as fp:
                json.dump(self.ITEMS_JSON_DEFAULT, fp, indent=4)

    def load_items_from_json(self):
        try:
            file = open(self.FILE, 'r')
            data = json.load(file)
            #self.items = []
            self.items = [[], [], [], [], []]
            valuable_items = []
            weapon_items = []
            usable_items = []
            clothing_items = []
            projectile_items = []
            # LOOP THROUGH ALL JSON OBJECTS IN 'Items'
            if len(data['Items']) == 0:
                print("Ei esineitä tiedostossa.")
            else:
                print("{} esinettä löytyi!".format(len(data['Items'])))
                for i in data['Items']:
                    # CHECK IF ALL BASE ITEM KEYS ARE FOUND
                    if 'id' and 'type' and 'name' and 'value' and 'icon' in i:
                    #"if 'id' in i:
                        # CALLS ITEM OBJECT CREATION BASED ON ITEM TYPE MARKED IN JSON OBJECT
                        match i['type']:
                            case 'ItemType.VALUABLE':
                                item = self.create_valuable_item(i)
                                if item is not None:
                                    valuable_items.append(item)
                            case 'ItemType.WEAPON':
                                item = self.create_weapon_item(i)
                                if item is not None:
                                    weapon_items.append(item)
                            case 'ItemType.USABLE':
                                item = self.create_usable_item(i)
                                if item is not None:
                                    usable_items.append(item)
                            case 'ItemType.CLOTHING':
                                item = self.create_clothing_item(i)
                                if item is not None:
                                    clothing_items.append(item)
                            case 'ItemType.PROJECTILE':
                                item = self.create_projectile_item(i)
                                if item is not None:
                                    projectile_items.append(item)
                    else:
                        print("Corrupted item. Cannot load.")
                # ADD ITEMS TO ITEM DICTIONARY
                if len(valuable_items) > 0:
                    self.set_valuable_items(valuable_items)
                if len(weapon_items) > 0:
                    self.set_weapons_items(weapon_items)
                if len(usable_items) > 0:
                    self.set_usables_items(usable_items)
                if len(clothing_items) > 0:
                    self.set_clothing_items(clothing_items)
                if len(projectile_items) > 0:
                    self.set_projectile_items(projectile_items)

                loaded_item_count = 0

                for i in self.items:
                    for j in i:
                        loaded_item_count += 1

                print("{} item (s) was loaded from file!".format(loaded_item_count))

            file.close()
        except Exception as e:
            print(e)

    def add_item(self, item: Items.Item) -> bool:
        try:
            file = open(self.FILE, 'r')
            data = json.load(file)
            item_id = len(data['Items'])
            file.close()
            item_json = {
                    "id": int(item_id),
                    "type": str(item.get_type()),
                    "name": str(item.get_name()),
                    "value": float(item.get_value()),
                    "icon": str(item.get_icon_name()),
                    "specifics": []
                }
            if isinstance(item, Items.Valuable):
                print("Adding valuable item")
            elif isinstance(item, Items.Usable):
                usable_type = {"usable_type": str(item.get_usable_type())}
                effects_json = {"effects": []}
                effects = item.get_effects()
                for e in effects:
                    if isinstance(e, Items.UsableEffect):
                        effects_json["effects"].append({
                            "name": str(e.get_feature_name()),
                            "type": str(e.get_feature_type()),
                            "value": int(e.get_feature_value())
                        })
                item_json["specifics"].append(usable_type)
                item_json["specifics"].append(effects_json)
                print("Usable")
            elif isinstance(item, Items.Clothing):
                clothing_type = {"clothing_type": str(item.get_clothing_type())}
                features_json = {"features": []}
                features = item.get_features()
                for f in features:
                    if isinstance(f, Items.ClothingFeature):
                        features_json["features"].append({
                            "feature_name": str(f.get_name()),
                            "feature_type": str(f.get_feature()),
                            "feature_value": float(f.get_value())
                        })
                item_json["specifics"].append(clothing_type)
                item_json["specifics"].append(features_json)
                print("Clothing")
            elif isinstance(item, Items.Weapon):
                weapon_specifics = {
                    "weapon_type": str(item.get_weapon_type()),
                    "weapon_damage": int(item.get_damage()),
                    "weapon_projectile": str(item.get_projectile())
                }
                item_json["specifics"].append(weapon_specifics)
                print("Weapon")
            elif isinstance(item, Items.Projectile):
                projectile_specifics = {
                    "projectile_damage": int(item.get_damage())
                }
                item_json["specifics"].append(projectile_specifics)
                print("Projectile")

            print(json.dumps(item_json, indent=4))
            data["Items"].append(item_json)
            file = open(self.FILE, 'w', encoding='utf-8')
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            file.close()
            self.load_items_from_json()
            return True
        except Exception as e:
            print(e)
            return False

    # METHODS TO CREATE ITEM-OBJECTS FROM JSON

    def create_projectile_item(self, data) -> Items.Valuable or None:
        try:
            item_id = int(data.get('id'))
            item_name = str(data.get('name'))
            item_value = float(data.get('value'))
            item_icon = str(data.get('icon'))
            item_specifics = data['specifics']
            #projectile_damage = int(item_specifics.get('projectile_damage'))
            projectile_damage = 0
            for i in item_specifics:
                if 'projectile_damage' in i:
                    projectile_damage = int(i.get('projectile_damage'))
                    break
            return Items.Projectile(item_id, item_name, item_value, projectile_damage, item_icon)
        except Exception as e:
            print(e)
            print("Corrupted item. Cannot load.")
        return None

    def create_valuable_item(self, data) -> Items.Valuable or None:
        try:
            item_id = int(data.get('id'))
            item_name = str(data.get('name'))
            item_value = float(data.get('value'))
            item_icon = str(data.get('icon'))
            return Items.Valuable(item_id, item_name, item_value, item_icon)
        except Exception as e:
            print(e)
            print("Corrupted item. Cannot load.")
        return None

    def create_weapon_item(self, data) -> Items.Weapon or None:
        # CHECK THAT ALL ITEM TYPE SPECIFIC KEYS ARE FOUND
        try:
            item_id = int(data.get('id'))
            item_name = str(data.get('name'))
            item_value = float(data.get('value'))
            item_icon = str(data.get('icon'))
            item_specifics = data['specifics']
            weapon_type = None
            weapon_damage = 0
            weapon_projectile = None
            for i in item_specifics:
                if 'weapon_type' and 'weapon_damage' and 'weapon_projectile' in i:
                    weapon_type = i.get('weapon_type')
                    weapon_damage = i.get('weapon_damage')
                    weapon_projectile = str(i.get('weapon_projectile'))

            if str(weapon_projectile) == 'None':
                weapon_projectile = None
            return Items.Weapon(item_id, item_name, item_value, weapon_type,
                                weapon_damage, weapon_projectile, item_icon)
        except Exception as e:
            print(e)
            print("Corrupted item. Cannot load.")
        return None

    def create_usable_item(self, data) -> Items.Usable or None:
        # CHECK THAT ALL ITEM TYPE SPECIFIC KEYS ARE FOUND
        try:
            item_id = int(data.get('id'))
            item_name = str(data.get('name'))
            item_value = float(data.get('value'))
            item_icon = str(data.get('icon'))
            item_specifics = data['specifics']
            usable_type = []
            usable_effects_data = []
            for i in item_specifics:
                if 'usable_type' in i:
                    usable_type = i.get('usable_type')
                elif 'effects' in i:
                    usable_effects_data = i.get('effects')
            #usable_effects_data = item_specifics.get('effects')
            #usable_type = item_specifics.get('usable_type')
            usable_effects = []
            for effect in usable_effects_data:
                if 'name' and 'type' and 'value' in effect:
                    effect_name = str(effect.get('name'))
                    effect_type = effect.get('type')
                    effect_value = int(effect.get('value'))
                    usable_effects.append(Items.UsableEffect(effect_name, effect_type, effect_value))
            return Items.Usable(item_id, item_name, item_value, usable_type, usable_effects, item_icon)
        except Exception as e:
            print(e)
            print("Corrupted item. Cannot load.")
        return None

    def create_clothing_item(self, data) -> Items.Clothing or None:
        # CHECK THAT ALL ITEM TYPE SPECIFIC KEYS ARE FOUND
        try:
            item_id = int(data.get('id'))
            item_name = str(data.get('name'))
            item_value = float(data.get('value'))
            item_icon = str(data.get('icon'))
            item_specifics = data['specifics']
            clothing_type = None
            clothing_features_data = []
            for i in item_specifics:
                if 'clothing_type' in i:
                    clothing_type = i.get('clothing_type')
                elif 'features' in i:
                    clothing_features_data = i.get('features')

            #clothing_type = item_specifics.get('clothing_type')
            #clothing_features_data = item_specifics.get('features')
            clothing_features = []
            for feature in clothing_features_data:
                if 'feature_name' and 'feature_type' and 'feature_value' in feature:
                    feature_name = str(feature.get('feature_name'))
                    feature_type = feature.get('feature_type')
                    feature_value = int(feature.get('feature_value'))
                    clothing_features.append(Items.ClothingFeature(feature_name, feature_type, feature_value))
            return Items.Clothing(item_id, item_name, item_value, clothing_type, clothing_features, item_icon)
        except Exception as e:
            print(e)
            print("Corrupted item. Cannot load.")
        return None

    # GETTERS

    def get_items(self) -> {}:
        return self.items

    # SETTERS

    def set_valuable_items(self, items: []):
        if len(items) > 0:
            self.items[0] = items
            #self.items['valuable'] = items

    def set_weapons_items(self, items: []):
        if len(items) > 0:
            self.items[1] = items
            #self.items['weapons'] = items

    def set_usables_items(self, items: []):
        if len(items) > 0:
            self.items[2] = items
            #self.items['usables'] = items

    def set_clothing_items(self, items: []):
        if len(items) > 0:
            self.items[3] = items
            #self.items['clothing'] = items

    def set_projectile_items(self, items: []):
        if len(items) > 0:
            self.items[4] = items
            #self.items['projectiles'] = items

    def set_items(self, valuables: [], weapons: [], usable: [], clothing: [], projectiles: []):
        self.items[0] = valuables
        self.items[1] = weapons
        self.items[2] = usable
        self.items[3] = clothing
        self.items[4] = projectiles
        #self.items["valuables"] = valuables
        #self.items["weapons"] = weapons
        #self.items["usables"] = usable
        #self.items["clothing"] = clothing


class ClassLoader:
    # Handles character class loading tasks

    def __init__(self):
        # Creates Class-objects from json file classes.json
        self.FILE = 'data/classes.json'
        self.CLASS_JSON_DEFAULT = {"Classes": []}
        self.startup_check()
        self.file = open(self.FILE, 'r')
        self.data = json.load(self.file)
        self.file.close()
        self.classes = []
        self.load_classes_from_json()

    def startup_check(self):
        # CHECKS IF THE JSON FILE EXISTS, IF NOT, CREATES A NEW ONE
        try:
            with open(self.FILE, 'r') as fp:
                json.load(fp)
        except:
            with open(self.FILE, 'w') as fp:
                json.dump(self.CLASS_JSON_DEFAULT, fp, indent=4)

    def load_classes_from_json(self):
        try:
            file = open(self.FILE, 'r')
            data = json.load(file)
            self.classes = []
            for i in data['Classes']:
                self.classes.append(Class(
                    int(i["class_id"]), str(i["class_name"]), float(i["starting_money"]),
                    float(i["health_multiplier"]), float(i["strength_multiplier"]),
                    float(i["agility_multiplier"]), float(i["iq_multiplier"]),
                    float(i["charisma_multiplier"]), float(i["reputation_multiplier"])
                ))
            file.close()
        except Exception as e:
            print(e)

    def get_classes(self) -> []:
        return self.classes

    def get_json(self):
        return self.data

    def save(self) -> bool:
        try:
            file = open(self.FILE, 'w', encoding='utf-8')
            file.seek(0)
            json.dump(self.data, file, indent=4)
            file.truncate()
            file.close()
            self.load_classes_from_json()
            return True
        except Exception as e:
            print(e)
            return False


class GameBody:
    # Holds all relevant data like character class types, tkinter root holder...

    def __init__(self):
        self.DETAILS = Details
        self.guiRoot = GuiRoot(self.DETAILS)
        self.classes = ClassLoader().get_classes()

    def get_gui_root(self):
        return self.guiRoot.getRoot()

    def get_classes(self) -> []:
        return self.classes

    def run_mainloop(self):
        self.guiRoot.loop()

