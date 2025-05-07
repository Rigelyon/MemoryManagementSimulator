import customtkinter as ctk
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from memory_visualizer import MemoryVisualizer


class MemoryManagementApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Memory Management Simulator")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_ui()

    def create_ui(self):
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.left_panel = ctk.CTkFrame(self.main_frame)
        self.left_panel.pack(side="left", fill="y", padx=10, pady=10)

        title_label = ctk.CTkLabel(
            self.left_panel,
            text="Memory Management Simulator",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        title_label.pack(pady=10)

        memory_frame = ctk.CTkFrame(self.left_panel)
        memory_frame.pack(fill="x", padx=10, pady=10)

        process_frame = ctk.CTkFrame(self.left_panel)
        process_frame.pack(fill="x", padx=10, pady=10)

        process_list_frame = ctk.CTkFrame(self.left_panel)
        process_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.right_panel = ctk.CTkFrame(self.main_frame)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.memory_visualizer = MemoryVisualizer(self.right_panel)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MemoryManagementApp()
    app.run()
