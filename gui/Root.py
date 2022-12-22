import tkinter


class GuiRoot:

    def __init__(self, details):
        self.DETAILS = details
        self.root = tkinter.Tk()
        self.root.title(self.DETAILS.GAME_NAME)
        self.root.geometry("540x420")

    def getRoot(self) -> tkinter.Tk:
        return self.root

    def loop(self):
        self.root.mainloop()
