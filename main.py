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

        memory_label = ctk.CTkLabel(
            memory_frame,
            text="Total Memory (MB)",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        memory_label.pack(side="left", padx=5)

        self.memory_size_var = ctk.StringVar(value="1024")
        memory_entry = ctk.CTkEntry(
            memory_frame,
            textvariable=self.memory_size_var,
            width=100,
        )
        memory_entry.pack(side="left", padx=5)

        update_btn = ctk.CTkButton(
            memory_frame,
            text="Update",
            command=lambda: print(f"Button ditekan, memori update: {self.memory_size_var.get()} MB"),
        )
        update_btn.pack(side="left", padx=5)

        process_frame = ctk.CTkFrame(self.left_panel)
        process_frame.pack(fill="x", padx=10, pady=10)

        name_label = ctk.CTkLabel(
            process_frame,
            text="Process Name:",
        )
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.process_name_var = ctk.StringVar()
        name_entry = ctk.CTkEntry(
            process_frame,
            textvariable=self.process_name_var,
            width=150,
        )
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        size_label = ctk.CTkLabel(process_frame, text="Process Size (MB):")
        size_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.process_size_var = ctk.StringVar()
        size_entry = ctk.CTkEntry(
            process_frame,
            textvariable=self.process_size_var,
            width=150,
        )
        size_entry.grid(row=1, column=1, padx=5, pady=5)

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
