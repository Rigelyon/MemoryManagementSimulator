import customtkinter as ctk


class MemoryVisualizer:
    def __init__(self, parent):
        self.parent = parent

        self.canvas_height = 400
        self.canvas_width = 500
        self.margin = 20

        self.create_ui()

    def create_ui(self):
        title_label = ctk.CTkLabel(
            self.parent,
            text="Memory Allocation Visualization",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        title_label.pack(pady=10)