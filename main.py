import customtkinter as ctk
from config import WINDOW_WIDTH, WINDOW_HEIGHT

class MemoryManagementApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Memory Management Simulator")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MemoryManagementApp()
    app.run()