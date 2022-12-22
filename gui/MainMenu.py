from tkinter import *
from Essentials import GameBody
from gui.Units import Unit, Character
from gui.Classes import Class


class MainMenu:

    def __init__(self, game_body: GameBody):
        self.game_body = game_body
        self.master = game_body.get_gui_root()

    def clear_screen(self):
        #Clears all widgets from root
        for widget in self.master.winfo_children():
            widget.destroy()

    def load_menu(self):
        #Loads main menu
        self.clear_screen()

        label = Label(self.master, text="Päävalikko")
        label.pack()

        new_game_button = Button(self.master, text="Uusi peli", command=self.new_game)
        new_game_button.pack()

        load_game_button = Button(self.master, text="Lataa peli", command=self.load_game)
        load_game_button.pack()

    def load_game(self):
        self.clear_screen()
        label = Label(self.master, text="Lataa peli")
        label.pack()

        back_button = Button(self.master, text="Poistu", command=self.load_menu)
        back_button.pack()

    def new_game(self):
        self.clear_screen()
        label = Label(self.master, text="Uusi peli")
        label.pack()

        # Character naming

        new_name = Entry(self.master, width=40)
        new_name.focus_set()
        new_name.pack()

        # Character class type selection
        class_frame = LabelFrame(self.master, text="Valitse suku")
        class_frame.pack(fill="both", expand="yes")

        class_selection = IntVar(self.master, 0)

        classes = self.game_body.get_classes()

        # Character details
        details_frame = LabelFrame(self.master, text="Hahmon tiedot")

        details_scroll = Scrollbar(details_frame, orient=VERTICAL)
        details_listbox = Listbox(details_frame, width=50, yscrollcommand=details_scroll.set)

        for c in classes:
            class_button = Radiobutton(class_frame, text=c.get_class_name(),
                                      variable=class_selection, value=c.get_class_id(),
                                       command=lambda: self.create_preview_character(classes[class_selection.get()], details_listbox))
            class_button.pack(anchor=W)

        details_scroll.config(command=details_listbox.yview)
        details_scroll.pack(side=RIGHT, fill=Y)
        details_frame.pack(fill="both", expand=1)

        details_listbox.pack()

        back_button = Button(self.master, text="Poistu", command=self.load_menu)
        back_button.pack()

    def create_preview_character(self, character_class: Class, listbox: Listbox) -> str:
        listbox.delete(0, END)
        preview_character = Character(character_class)
        details = preview_character.get_details()
        for detail in details:
            listbox.insert(END, detail)
        return None
