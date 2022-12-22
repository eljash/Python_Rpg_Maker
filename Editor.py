import tkinter
import re
import json
from tkinter import ttk, Frame, LabelFrame, Entry, Label, Button, END, messagebox
from Essentials import ClassLoader, Class, ItemLoader, Items


class Root:

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry("400x450")

    def get_root(self):
        return self.root

    def run_loop(self):
        self.root.mainloop()


class GameDataEditor:

    def __init__(self, master: Root):
        self.class_loader = ClassLoader()
        self.item_loader = ItemLoader()

        self.master = master.get_root()
        self.master.title("Pelin editori")
        self.classes = self.class_loader.get_classes()

        # data/classes.json tiedosto
        self.classes_data = self.class_loader.get_json()

    def get_values(self):
        self.classes = self.class_loader.get_classes()
        self.classes_data = self.class_loader.get_json()

    def clear_screen(self):
        # Clears all widgets from root
        for widget in self.master.winfo_children():
            widget.destroy()

    def clear_frame(self, frame: tkinter.ttk.Frame or tkinter.ttk.LabelFrame):
        # Clears all widgets from a frame
        for widget in frame.winfo_children():
            widget.destroy()

    def main_window(self):
        # EDITORS MAIN WINDOW
        self.clear_screen()
        self.get_values()
        frame = Frame(self.master)
        frame.grid()

        class_editor = LabelFrame(frame, text="Luokka editori")
        class_editor.pack(fill="both", expand="yes")

        item_editor = LabelFrame(frame, text="Tavara editori")
        item_editor.pack(fill="both", expand="yes")

        add_classes_button = Button(class_editor, text="Lisää luokkia", command=self.add_classes_window)
        add_classes_button.grid(row=0, column=0)
        edit_classes_button = Button(class_editor, text="Luokkien muokkaus", command=self.class_edit_window)
        edit_classes_button.grid(row=0, column=1)
        add_classes_button = Button(item_editor, text="Lisää tavaroita", command=self.add_items_window)
        add_classes_button.grid(row=1, column=0)

    def add_items_window(self):
        # EDITORS ITEM ADDING WINDOW
        self.clear_screen()
        frame = Frame(self.master)
        frame.grid()

        item_types = []

        for e in Items.ItemType:
            item_types.append(e)

        if len(item_types) > 0:
            combo_box = ttk.Combobox(
                frame,
                width=30,
                values=item_types,
                state='readonly'
            )
            combo_box.current(0)
            combo_box.pack(padx=5, pady=5)

            default_values = LabelFrame(self.master, text="Tavaran perus arvot")
            default_values.grid()

            item_specifics = LabelFrame(self.master, text="Tyyppi kohtaiset arvot")
            item_specifics.grid()

            button_frame = LabelFrame(self.master, text="Valinnat")
            button_frame.grid()

            combo_box.bind("<<ComboboxSelected>>",
                           lambda _: self.item_specific_fields(default_values, item_specifics, button_frame, item_types[combo_box.current()]))

            self.item_specific_fields(default_values, item_specifics, button_frame, item_types[combo_box.current()])

        # CREATES BOTTOM FRAME WITH BACK BUTTON ON WINDOW
        bottom_frame = Frame(self.master)
        bottom_frame.grid()
        back_button = Button(bottom_frame, text="Takaisin",
                             command=self.main_window)
        back_button.grid(row=1, column=0)

    def item_specific_fields(self, default_values: tkinter.ttk.LabelFrame, item_specifics_frame: tkinter.ttk.LabelFrame,
                             button_frame: tkinter.ttk.LabelFrame, item_type: Items.ItemType):
        # HOLDS ALL THE FIELDS FOR ITEM ADDING

        self.clear_frame(default_values)
        self.clear_frame(item_specifics_frame)

        # CREATES ITEM ADD BUTTON
        add_button = Button(button_frame, text="Lisää")

        # ITEM DEFAULT VALUES FRAME

        item_name_label = Label(default_values, text="Tavaran nimi")
        item_value_label = Label(default_values, text="Tavaran arvo")
        item_icon_label = Label(default_values, text="Tavaran kuvake")

        item_labels = [
            item_name_label, item_value_label, item_icon_label
        ]

        item_name_entry = Entry(default_values, width=20)
        item_value_entry = Entry(default_values, width=20)
        item_icon_entry = Entry(default_values, width=20)

        item_entries = [
            item_name_entry, item_value_entry, item_icon_entry
        ]

        # FOR FLOAT ENTRY ALLOW ONLY FLOAT TYPE VALUES
        item_value_entry['validate'] = "key"
        vcmd = (item_value_entry.register(self.on_validate_float_entry), "%P")
        item_value_entry['validatecommand'] = vcmd

        item_name_type_label = Label(default_values, text="string")
        item_value_type_label = Label(default_values, text="float")
        item_icon_type_label = Label(default_values, text="string")

        item_entry_type_labels = [
            item_name_type_label, item_value_type_label, item_icon_type_label
        ]

        for i in range(len(item_labels)):
            item_labels[i].grid(row=i, column=0)
        for i in range(len(item_entries)):
            item_entries[i].grid(row=i, column=1)
        for i in range(len(item_entry_type_labels)):
            item_entry_type_labels[i].grid(row=i, column=2)

        # ITEM TYPE SPECIFIC VALUES

        match item_type:
            case Items.ItemType.VALUABLE:
                add_button.configure(command=lambda: self.add_item_valuable(item_name_entry, item_value_entry,
                                                                            item_icon_entry))
            case Items.ItemType.WEAPON:
                # CREATE COMBOBOX FOR WEAPON TYPES
                weapon_types = []
                for e in Items.WeaponType:
                    weapon_types.append(e)
                if len(weapon_types) > 0:
                    combo_box = ttk.Combobox(
                        item_specifics_frame,
                        width=30,
                        values=weapon_types,
                        state='readonly'
                    )
                    combo_box.current(0)
                    combo_box.grid(row=0, column=0, padx=5, pady=5)

                damage_label = Label(item_specifics_frame, text="Vahinko")
                damage_label.grid(row=1, column=0)

                damage_entry = Entry(item_specifics_frame, width=20)
                # FOR INTEGER ENTRY ALLOW ONLY INTEGER TYPE VALUES
                damage_entry['validate'] = "key"
                vcmd = (damage_entry.register(self.on_validate_integer_entry), "%P")
                damage_entry['validatecommand'] = vcmd
                damage_entry.grid(row=1, column=1)

                damage_entry_type = Label(item_specifics_frame, text="integer")
                damage_entry_type.grid(row=1, column=2)

                # PROJECTILE SPECIFICATION
                projectile_label = Label(item_specifics_frame, text="Ammus (ranged)")
                projectile_label.grid(row=2, column=0)

                projectile_entry = Entry(item_specifics_frame, width=20)
                projectile_entry.grid(row=2, column=1)

                projectile_entry_type = Label(item_specifics_frame, text="string")
                projectile_entry_type.grid(row=2, column=2)

                add_button.configure(command=lambda: self.add_item_weapon(
                    item_name_entry, item_value_entry,
                    item_icon_entry, combo_box.current(), damage_entry, projectile_entry
                ))
            case Items.ItemType.USABLE:
                # CREATE COMBOBOX FOR USABLE ITEM TYPES
                usable_types = []
                usable_effects = []
                for e in Items.UsableType:
                    usable_types.append(e)
                if len(usable_types) > 0:
                    combo_box = ttk.Combobox(
                        item_specifics_frame,
                        width=30,
                        values=usable_types,
                        state='readonly'
                    )
                    combo_box.current(0)
                    combo_box.grid(row=0, column=0, padx=5, pady=5)

                # USABLE EFFECT ADDING
                effect_frame = LabelFrame(item_specifics_frame, text="Efektit")
                effect_frame.grid()

                effect_name_label = Label(effect_frame, text="Efektin nimi")
                effect_name_label.grid(row=0, column=0)
                effect_name_entry = Entry(effect_frame)
                effect_name_entry.grid(row=0, column=1)
                effect_name_entry_type = Label(effect_frame, text="string")
                effect_name_entry_type.grid(row=0, column=2)

                usable_feature_types = []
                for e in Items.UsableFeatureType:
                    usable_feature_types.append(e)

                if len(usable_feature_types) > 0:
                    effects_combobox = ttk.Combobox(
                        effect_frame,
                        width=30,
                        values=usable_feature_types,
                        state='readonly'
                    )
                    effects_combobox.current(0)
                    effects_combobox.grid(row=1, column=0)

                effect_value_label = Label(effect_frame, text="Efektin vahvuus")
                effect_value_label.grid(row=2, column=0)

                effect_value_entry = Entry(effect_frame)
                # ALLOW ONLY INTEGER INPUT
                effect_value_entry['validate'] = "key"
                vcmd = (effect_value_entry.register(self.on_validate_integer_entry), "%P")
                effect_value_entry['validatecommand'] = vcmd
                effect_value_entry.grid(row=2, column=1)

                effect_value_entry_type = Label(effect_frame, text="int")
                effect_value_entry_type.grid(row=2, column=2)

                add_effect_button = Button(effect_frame, text="Lisää efekti")
                add_effect_button.configure(command=lambda: self.add_usable_effect(
                    usable_effects, effect_frame, effect_name_entry, effects_combobox.current(), effect_value_entry
                ))
                add_effect_button.grid(row=3, column=0)

                add_button.configure(command=lambda: self.add_item_usable(
                    item_name_entry, item_value_entry,
                    item_icon_entry, effects_combobox.current(), usable_effects
                ))
            case Items.ItemType.CLOTHING:
                clothing_types = []
                for e in Items.ClothingType:
                    clothing_types.append(e)
                if len(clothing_types) > 0:
                    combo_box = ttk.Combobox(
                        item_specifics_frame,
                        width=30,
                        values=clothing_types,
                        state='readonly'
                    )
                    combo_box.current(0)
                    combo_box.grid(row=0, column=0, padx=5, pady=5)

                    # CLOTHING FEATURE ADDING
                    feature_frame = LabelFrame(item_specifics_frame, text="Lisää ominaisuus")
                    feature_frame.grid()

                    clothing_features = []

                    feature_name_label = Label(feature_frame, text="Ominaisuuden nimi")
                    feature_name_label.grid(row=0, column=0)
                    feature_name_entry = Entry(feature_frame)
                    feature_name_entry.grid(row=0, column=1)
                    feature_name_entry_type = Label(feature_frame, text="string")
                    feature_name_entry_type.grid(row=0, column=2)

                    clothing_feature_types = []
                    for e in Items.ClothingFeatureType:
                        clothing_feature_types.append(e)

                    if len(clothing_feature_types) > 0:
                        feature_combobox = ttk.Combobox(
                            feature_frame,
                            width=30,
                            values=clothing_feature_types,
                            state='readonly'
                        )
                        feature_combobox.current(0)
                        feature_combobox.grid(row=1, column=0)

                    feature_value_label = Label(feature_frame, text="Ominaisuuden vahvuus")
                    feature_value_label.grid(row=2, column=0)

                    feature_value_entry = Entry(feature_frame)
                    # ALLOW ONLY INTEGER INPUT
                    feature_value_entry['validate'] = "key"
                    vcmd = (feature_value_entry.register(self.on_validate_integer_entry), "%P")
                    feature_value_entry['validatecommand'] = vcmd
                    feature_value_entry.grid(row=2, column=1)

                    effect_value_entry_type = Label(feature_frame, text="int")
                    effect_value_entry_type.grid(row=2, column=2)

                    add_effect_button = Button(feature_frame, text="Lisää ominaisuus")
                    add_effect_button.configure(command=lambda: self.add_clothe_feature(
                        clothing_features, feature_frame, feature_name_entry,
                        feature_combobox.current(), feature_value_entry
                    ))
                    add_effect_button.grid(row=3, column=0)

                add_button.configure(command=lambda: self.add_item_clothing(
                    item_name_entry, item_value_entry,
                    item_icon_entry, combo_box.current(), clothing_features
                ))
            case Items.ItemType.PROJECTILE:
                # PROJECTILE DAMAGE
                damage_label = Label(item_specifics_frame, text="Vahinko")
                damage_label.grid(row=1, column=0)

                damage_entry = Entry(item_specifics_frame, width=20)
                # FOR INTEGER ENTRY ALLOW ONLY INTEGER TYPE VALUES
                damage_entry['validate'] = "key"
                vcmd = (damage_entry.register(self.on_validate_integer_entry), "%P")
                damage_entry['validatecommand'] = vcmd
                damage_entry.grid(row=1, column=1)

                damage_entry_type = Label(item_specifics_frame, text="integer")
                damage_entry_type.grid(row=1, column=2)

                add_button.configure(command=lambda: self.add_item_projectile(
                    item_name_entry, item_value_entry,
                    item_icon_entry, damage_entry
                    ))

        add_button.grid(row=0, column=0)

    # ITEM ADDING METHODS

    def add_clothe_feature(self, features: [], features_label: tkinter.ttk.LabelFrame, name: tkinter.ttk.Entry,
                           type: Items.ClothingFeatureType, value: tkinter.ttk.Entry):
        try:
            feature = Items.ClothingFeature(str(name.get()), type, int(value.get()))
            features.append(feature)
            features_label.configure(text="Lisää ominaisuus ({})".format(len(features)))
        except Exception as e:
            print(e)
            messagebox.showerror(title="Virhe tallennuksessa",
                                 message="Varmista, että jokaisella kentällä on oikean tyyppinen arvo!")

    def add_usable_effect(self, effects: [], effects_label: tkinter.ttk.LabelFrame, name: tkinter.ttk.Entry,
                          type: Items.UsableFeatureType, value: tkinter.ttk.Entry):
        try:
            effect = Items.UsableEffect(str(name.get()), type, int(value.get()))
            effects.append(effect)
            effects_label.configure(text="Lisää efekti ({})".format(len(effects)))
        except Exception as e:
            print(e)
            messagebox.showerror(title="Virhe tallennuksessa",
                                 message="Varmista, että jokaisella kentällä on oikean tyyppinen arvo!")

    def add_item_valuable(self, name: tkinter.ttk.Entry, value: tkinter.ttk.Entry, icon: tkinter.ttk.Entry):
        try:
            item = Items.Valuable(-1, str(name.get()), float(value.get()), str(icon.get()))
            self.item_loader.add_item(item)
            self.add_items_window()
        except Exception as e:
            print(e)
            messagebox.showerror(title="Virhe tallennuksessa",
                                 message="Varmista, että jokaisella kentällä on oikean tyyppinen arvo!")


    def add_item_usable(self, name: tkinter.ttk.Entry, value: tkinter.ttk.Entry, icon: tkinter.ttk.Entry,
                        usable_type: Items.UsableType, effects: []):
        try:
            item = Items.Usable(-1, str(name.get()), float(value.get()), usable_type, effects, str(icon.get()))
            self.item_loader.add_item(item)
            self.add_items_window()
        except Exception as e:
            print(e)
            messagebox.showerror(title="Virhe tallennuksessa",
                                 message="Varmista, että jokaisella kentällä on oikean tyyppinen arvo!")

    def add_item_clothing(self, name: tkinter.ttk.Entry, value: tkinter.ttk.Entry, icon: tkinter.ttk.Entry,
                          clothing_type: Items.ClothingType, features: []):
        try:
            item = Items.Clothing(-1, str(name.get()), float(value.get()), clothing_type, features, str(icon.get()))
            self.item_loader.add_item(item)
            self.add_items_window()
        except Exception as e:
            print(e)
            messagebox.showerror(title="Virhe tallennuksessa",
                                 message="Varmista, että jokaisella kentällä on oikean tyyppinen arvo!")

    def add_item_weapon(self, name: tkinter.ttk.Entry, value: tkinter.ttk.Entry, icon: tkinter.ttk.Entry,
                        weapon_type: Items.WeaponType, weapon_damage: tkinter.ttk.Entry,
                        weapon_projectile: tkinter.ttk.Entry):
        try:
            item = Items.Weapon(-1, str(name.get()), float(value.get()),
                                weapon_type, int(weapon_damage.get()), str(weapon_projectile.get()), str(icon.get()))
            self.item_loader.add_item(item)
            self.add_items_window()
        except Exception as e:
            print(e)
            messagebox.showerror(title="Virhe tallennuksessa",
                                 message="Varmista, että jokaisella kentällä on oikean tyyppinen arvo!")

    def add_item_projectile(self, name: tkinter.ttk.Entry, value: tkinter.ttk.Entry, icon: tkinter.ttk.Entry,
                            projectile_damage: tkinter.ttk.Entry):
        try:
            item = Items.Projectile(-1, str(name.get()), float(value.get()),
                                    int(projectile_damage.get()), str(icon.get()))
            self.item_loader.add_item(item)
            self.add_items_window()
        except Exception as e:
            print(e)
            messagebox.showerror(title="Virhe tallennuksessa",
                                 message="Varmista, että jokaisella kentällä on oikean tyyppinen arvo!")

    # -------------------- CLASSES METHODS --------------------

    def add_classes_window(self):
        # EDITORS CLASS ADDING WINDOW
        self.clear_screen()
        frame = Frame(self.master)
        frame.grid()

        # CREATE LABELS AND ENTRIES

        class_frame = Frame(self.master)
        class_frame.grid()

        class_name_label = Label(class_frame, text="Luokan nimi")
        starting_money_label = Label(class_frame, text="Aloitus raha")
        health_multiplier_label = Label(class_frame, text="Elämä kerroin")
        strength_multiplier_label = Label(class_frame, text="Voima kerroin")
        agility_multiplier_label = Label(class_frame, text="Ketteryys kerroin")
        iq_multiplier_label = Label(class_frame, text="Älykkyys kerroin")
        charisma_multiplier_label = Label(class_frame, text="Karsima kerroin")
        reputation_multiplier_label = Label(class_frame, text="Maine kerroin")

        class_name_entry = Entry(class_frame, width=40)
        starting_money_entry = Entry(class_frame, width=20)
        health_multiplier_entry = Entry(class_frame, width=20)
        strength_multiplier_entry = Entry(class_frame, width=20)
        agility_multiplier_entry = Entry(class_frame, width=20)
        iq_multiplier_entry = Entry(class_frame, width=20)
        charisma_multiplier_entry = Entry(class_frame, width=20)
        reputation_multiplier_entry = Entry(class_frame, width=20)

        class_name_type_label = Label(class_frame, text="string")
        starting_money_type_label = Label(class_frame, text="float")
        health_multiplier_type_label = Label(class_frame, text="float")
        strength_multiplier_type_label = Label(class_frame, text="float")
        agility_multiplier_type_label = Label(class_frame, text="float")
        iq_multiplier_type_label = Label(class_frame, text="float")
        charisma_multiplier_type_label = Label(class_frame, text="float")
        reputation_multiplier_type_label = Label(class_frame, text="float")

        stat_labels = [
            class_name_label,
            starting_money_label, health_multiplier_label, strength_multiplier_label,
            agility_multiplier_label, iq_multiplier_label, charisma_multiplier_label,
            reputation_multiplier_label
        ]

        stat_entrys = [
            class_name_entry,
            starting_money_entry, health_multiplier_entry, strength_multiplier_entry,
            agility_multiplier_entry, iq_multiplier_entry, charisma_multiplier_entry,
            reputation_multiplier_entry
        ]

        stat_types_labels = [
            class_name_type_label,
            starting_money_type_label, health_multiplier_type_label, strength_multiplier_type_label,
            agility_multiplier_type_label, iq_multiplier_type_label, charisma_multiplier_type_label,
            reputation_multiplier_type_label
        ]

        # PUTS LABELS AND ENTRYS IN THE FRAME GRID

        for i in range(len(stat_labels)):
            stat_labels[i].grid(row=i, column=0)

        for i in range(len(stat_entrys)):
            stat_entrys[i].grid(row=i, column=1)
            if i > 0:
                stat_entrys[i].insert(0, 1.0)
                stat_entrys[i]['validate'] = "key"
                vcmd = (stat_entrys[i].register(self.on_validate_float_entry), "%P")
                stat_entrys[i]['validatecommand'] = vcmd

        for i in range(len(stat_types_labels)):
            stat_types_labels[i].grid(row=i, column=2)

        # CREATE BUTTON FRAME (save etc.)

        button_frame = Frame(self.master)
        button_frame.grid()

        error_label = Label(button_frame, text="")
        error_label.grid(row=0, column=0)

        add_button = Button(button_frame, text="Lisää luokka",
                             command=lambda: self.add_class(
                                 class_name_entry,
                                 starting_money_entry,
                                 health_multiplier_entry,
                                 strength_multiplier_entry,
                                 agility_multiplier_entry,
                                 iq_multiplier_entry,
                                 charisma_multiplier_entry,
                                 reputation_multiplier_entry,
                                 error_label
                             ))
        add_button.grid(row=1, column=0)

        # CREATES BOTTOM FRAME WITH BACK BUTTON ON WINDOW

        bottom_frame = Frame(self.master)
        bottom_frame.grid()
        back_button = Button(bottom_frame, text="Takaisin",
                             command=self.main_window)
        back_button.grid(row=1, column=0)

    def add_class(self,
                  name_entry: tkinter.ttk.Entry, money_entry: tkinter.ttk.Entry, health_entry: tkinter.ttk.Entry,
                  strength_entry: tkinter.ttk.Entry, agility_entry: tkinter.ttk.Entry, iq_entry: tkinter.ttk.Entry,
                  charisma_entry: tkinter.ttk.Entry, reputation_entry: tkinter.ttk.Entry, error_label: tkinter.Label):
        try:
            # GET VALUES FROM ENTRIES
            name = name_entry.get()
            money = money_entry.get()
            health = health_entry.get()
            strength = strength_entry.get()
            agility = agility_entry.get()
            iq = iq_entry.get()
            charisma = charisma_entry.get()
            reputation = reputation_entry.get()

            error_label['text'] = ""
            # Get json-file containing all classes
            json_file = self.class_loader.get_json()
            # Define new classes id by the number of classes
            class_id = len(json_file['Classes'])
            json_file['Classes'].append({
                "class_id": int(class_id),
                "class_name": name,
                "starting_money": round(float(money), 2),
                "health_multiplier": round(float(health), 4),
                "strength_multiplier": round(float(strength), 4),
                "agility_multiplier": round(float(agility), 4),
                "iq_multiplier": round(float(iq), 4),
                "charisma_multiplier": round(float(charisma), 4),
                "reputation_multiplier": round(float(reputation), 4)
            })
            self.class_loader.save()
        except Exception as e:
            error_label['text'] = "{}".format(e)
            messagebox.showerror(title="Virhe tallennuksessa",
                                 message="Varmista, että jokaisella kentällä on oikean tyyppinen arvo!")

    def class_edit_window(self):
        self.clear_screen()
        self.get_values()
        frame = Frame(self.master)
        frame.grid()

        classes_list = []

        if len(self.classes) > 0:
            for c in self.classes:
                classes_list.append(c.get_class_name())

            combo_box = ttk.Combobox(
                                frame,
                                width=30,
                                values=classes_list,
                                state='readonly'
                            )
            combo_box.current(0)
            combo_box.pack(padx=5, pady=5)

            class_frame = LabelFrame(self.master, text="Muokkaa sukua")
            class_frame.grid()

            # CREATE LABELS AND ENTRIES

            starting_money_label = Label(class_frame, text="Aloitus raha")
            health_multiplier_label = Label(class_frame, text="Elämä kerroin")
            strength_multiplier_label = Label(class_frame, text="Voima kerroin")
            agility_multiplier_label = Label(class_frame, text="Ketteryys kerroin")
            iq_multiplier_label = Label(class_frame, text="Älykkyys kerroin")
            charisma_multiplier_label = Label(class_frame, text="Karsima kerroin")
            reputation_multiplier_label = Label(class_frame, text="Maine kerroin")

            starting_money_entry = Entry(class_frame, width=20)
            health_multiplier_entry = Entry(class_frame, width=20)
            strength_multiplier_entry = Entry(class_frame, width=20)
            agility_multiplier_entry = Entry(class_frame, width=20)
            iq_multiplier_entry = Entry(class_frame, width=20)
            charisma_multiplier_entry = Entry(class_frame, width=20)
            reputation_multiplier_entry = Entry(class_frame, width=20)

            starting_money_type_label = Label(class_frame, text="float")
            health_multiplier_type_label = Label(class_frame, text="float")
            strength_multiplier_type_label = Label(class_frame, text="float")
            agility_multiplier_type_label = Label(class_frame, text="float")
            iq_multiplier_type_label = Label(class_frame, text="float")
            charisma_multiplier_type_label = Label(class_frame, text="float")
            reputation_multiplier_type_label = Label(class_frame, text="float")

            stat_labels = [
                starting_money_label, health_multiplier_label, strength_multiplier_label,
                agility_multiplier_label, iq_multiplier_label, charisma_multiplier_label,
                reputation_multiplier_label
            ]

            stat_entrys = [
                starting_money_entry, health_multiplier_entry, strength_multiplier_entry,
                agility_multiplier_entry, iq_multiplier_entry, charisma_multiplier_entry,
                reputation_multiplier_entry
            ]

            stat_types_labels = [starting_money_type_label, health_multiplier_type_label, strength_multiplier_type_label,
                                 agility_multiplier_type_label, iq_multiplier_type_label, charisma_multiplier_type_label,
                                 reputation_multiplier_type_label]

            # PUTS LABELS AND ENTRYS IN THE FRAME GRID

            for i in range(len(stat_labels)):
                stat_labels[i].grid(row=i, column=0)

            for i in range(len(stat_entrys)):
                stat_entrys[i].grid(row=i, column=1)
                stat_entrys[i]['validate'] = "key"
                vcmd = (stat_entrys[i].register(self.on_validate_float_entry), "%P")
                stat_entrys[i]['validatecommand'] = vcmd

            for i in range(len(stat_types_labels)):
                stat_types_labels[i].grid(row=i, column=2)

            # WHEN SELECTING A OPTION FROM COMBOBOX, CALLS FUNCTION TO DISPLAY VALUES

            combo_box.bind("<<ComboboxSelected>>",
                           lambda _: self.show_class_values(self.classes[combo_box.current()], stat_entrys))

            # CREATES FRAME FOR SAVE AND RESET BUTTONS

            button_frame = Frame(self.master)
            button_frame.grid()

            save_button = Button(button_frame, text="Tallenna", command=lambda: self.save_class(self.classes[combo_box.current()], stat_entrys))
            save_button.grid(row=1, column=0)
            try:
                reverse_button = Button(button_frame, text="Palauta", command=lambda: self.show_class_values(self.classes[combo_box.current()], stat_entrys))
            except Exception as e:
                print(e)
            reverse_button.grid(row=1, column=1)
            self.show_class_values(self.classes[combo_box.current()], stat_entrys)
        else:
            no_classes_found_label = Label(frame, text="Luokkia ei löytynyt. Lisää luokkia, jotta voit muokata niitä!")
            no_classes_found_label.grid(row=0, column=0)

        bottom_frame = Frame(self.master)
        bottom_frame.grid()
        save_button = Button(bottom_frame, text="Takaisin",
                                 command=self.main_window)
        save_button.grid(row=1, column=0)

    def validate_float_entry(self, string: str):
        regex = re.compile(r"(\+|\-)?[0-9.]*$")
        result = regex.match(string)
        return (string == ""
                or (string.count('+') <= 1
                    and string.count('-') <= 1
                    and string.count('.') <= 1
                    and result is not None
                    and result.group(0) != ""))

    def on_validate_float_entry(self, P):
        return self.validate_float_entry(P)

    def validate_integer_entry(self, string: str):
        regex = re.compile(r"^[0-9]+$")
        result = regex.match(string)
        return (string == ""
                or (string.count('+') <= 1
                    and string.count('-') <= 1
                    and string.count('.') <= 1
                    and result is not None
                    and result.group(0) != ""))

    def on_validate_integer_entry(self, P):
        return self.validate_integer_entry(P)

    def show_class_values(self, c: Class, entrys: []) -> bool:
        for e in entrys:
            e.delete(0, END)
        try:
            entrys[0].insert(0, c.get_starting_money())
            entrys[1].insert(0, c.get_health_multiplier())
            entrys[2].insert(0, c.get_strength_multiplier())
            entrys[3].insert(0, c.get_agility_multiplier())
            entrys[4].insert(0, c.get_iq_multiplier())
            entrys[5].insert(0, c.get_charisma_multiplier())
            entrys[6].insert(0, c.get_reputation_multiplier())
            return True
        except Exception as e:
            print(e)
        return False

    def save_class(self, c: Class, entries: []) -> bool:
        try:
            c.set_starting_money(float(entries[0].get()))
            c.set_health_multiplier(float(entries[1].get()))
            c.set_strength_multiplier(float(entries[2].get()))
            c.set_agility_multiplier(float(entries[3].get()))
            c.set_iq_multiplier(float(entries[4].get()))
            c.set_charisma_multiplier(float(entries[5].get()))
            c.set_reputation_multiplier(float(entries[6].get()))

            json_file = self.class_loader.get_json()
            for obj in json_file['Classes']:
                if obj['class_id'] == c.get_class_id():
                    obj['starting_money'] = c.get_starting_money()
                    obj['health_multiplier'] = c.get_health_multiplier()
                    obj['strength_multiplier'] = c.get_strength_multiplier()
                    obj['agility_multiplier'] = c.get_agility_multiplier()
                    obj['iq_multiplier'] = c.get_iq_multiplier()
                    obj['charisma_multiplier'] = c.get_charisma_multiplier()
                    obj['reputation_multiplier'] = c.get_reputation_multiplier()
                    self.class_loader.save()
                    return True
        except:
            messagebox.showerror(title="Virhe tallennuksessa",
                                 message="Varmista, että jokaisella kentällä on oikean tyyppinen arvo!")
        return False


class Main:
    root = Root()
    editor = GameDataEditor(root)
    editor.main_window()
    root.run_loop()


if "__name__" == "__main__":
    Main()
