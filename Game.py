from gui.MainMenu import MainMenu
import Details
from threading import Thread, Lock
import time
from Essentials import GameBody


class GameGuiThread(Thread):

    def __init__(self, lock: Lock):
        Thread.__init__(self)
        self.game_body = None
        self.lock = Lock

    def run(self):
        print("GameGuiThread started")
        self.game_body = GameBody()

        main_menu = MainMenu(self.game_body)
        main_menu.load_menu()

        # Loads the GUI
        self.game_body.run_mainloop()

        print("GameGuiThread exiting")

    def get_game_body(self) -> GameBody:
        return self.game_body


class GameUpdateThread(Thread):

    def __init__(self, game_qui_thread: GameGuiThread, updates_per_second: int, lock: Lock):
        Thread.__init__(self)
        self.game_qui_thread = game_qui_thread

        # Lock used as a synchronization mechanism for variable sharing between threads
        self.lock = Lock()
        self.frequency = round(1 / updates_per_second, 4)
        self.isRunning = False

        self.time_out_time = 1  # How many seconds update thread waits qui to load before forfeiting
        self.time_out_tries = 3  # How many times update thread tries to wait for qui to load

    def run(self):
        print("GameUpdateThread started")
        self.game_qui_thread.start()
        self.isRunning = True
        self.wait_qui_to_load()
        self.debug_print()
        print("GameUpdateThread exiting")

    def wait_qui_to_load(self):
        # Thread is waiting until gui thread starts tkinter qui
        tries = 0
        while tries < self.time_out_tries:
            time.sleep(self.time_out_time)
            if self.game_qui_thread.get_game_body() is not None:
                return
            print("GameUpdateThread waiting for qui to load")
            tries += 1
        print("GameUpdateThread timed out.")
        self.isRunning = False
        self.stop()

    def stop(self):
        print("GameUpdateThread stopping")
        self.isRunning = False

    def change_updates_per_second(self, updates_per_second: int):
        self.frequency = round(1 / updates_per_second, 4)

    def debug_print(self):
        while self.isRunning and self.game_qui_thread.is_alive():
            print("GameUpdateThread updating...")
            classes = self.game_qui_thread.get_game_body().get_classes()
            for c in classes:
                print(c.get_class_name())
            #for c in classes:
            #    print(c)
            time.sleep(self.frequency)


class Main:
    # GameBody-object holds are necessary game data used by update and qui threads
    game_body = GameBody()
    lock = Lock()
    gameQuiThread = GameGuiThread(lock)
    #gameQuiThread.start()

    gameUpdateThread = GameUpdateThread(gameQuiThread, 3, lock)
    gameUpdateThread.start()


if "__name__" == "__main__":
    Main
