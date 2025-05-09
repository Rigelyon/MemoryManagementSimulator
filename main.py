import customtkinter as ctk
from config import PRIMARY_COLOR, SECONDARY_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT
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

        partition_frame = ctk.CTkFrame(self.left_panel)
        partition_frame.pack(fill="x", padx=10, pady=10)
        
        partition_label = ctk.CTkLabel(partition_frame, text="Memory Partitions:", 
                                     font=ctk.CTkFont(weight="bold"))
        partition_label.pack(pady=5)
        
        partition_control_frame = ctk.CTkFrame(partition_frame)
        partition_control_frame.pack(fill="x", padx=5, pady=5)
        
        num_partitions_label = ctk.CTkLabel(partition_control_frame, text="Number of Partitions:")
        num_partitions_label.pack(side="left", padx=5)
        
        self.partition_count_var = ctk.StringVar(value="1")
        partition_values = ["1", "2", "3", "4", "5", "6"]
        partition_dropdown = ctk.CTkOptionMenu(partition_control_frame, values=partition_values, 
                                            variable=self.partition_count_var,
                                            command=self.update_partition_ui)
        partition_dropdown.pack(side="left", padx=5)
        
        self.partition_sliders_frame = ctk.CTkFrame(partition_frame)
        self.partition_sliders_frame.pack(fill="x", padx=5, pady=5)
        
        apply_partitions_btn = ctk.CTkButton(partition_frame, text="Apply Partitions", 
                                            command=self.apply_partitions,
                                            fg_color=PRIMARY_COLOR)
        apply_partitions_btn.pack(pady=5)
        
        self.update_partition_ui("1")

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

        time_label = ctk.CTkLabel(process_frame, text="Duration (seconds):")
        time_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        self.process_time_var = ctk.StringVar(value="120")
        time_entry = ctk.CTkEntry(process_frame, textvariable=self.process_time_var, width=150)
        time_entry.grid(row=2, column=1, padx=5, pady=5)
        
        algo_label = ctk.CTkLabel(process_frame, text="Algorithm:")
        algo_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.algorithm_var = ctk.StringVar(value="First Fit")
        algorithms = ["First Fit", "Best Fit", "Worst Fit"]
        algo_dropdown = ctk.CTkOptionMenu(process_frame, values=algorithms, variable=self.algorithm_var)
        algo_dropdown.grid(row=3, column=1, padx=5, pady=5)
        
        add_btn = ctk.CTkButton(process_frame, text="Add Process", command=self.add_process)
        add_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        process_list_frame = ctk.CTkFrame(self.left_panel)
        process_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        list_label = ctk.CTkLabel(process_list_frame, text="Process Queue:", 
        font=ctk.CTkFont(weight="bold"))
        list_label.pack(pady=5)
        
        self.process_list_scroll = ctk.CTkScrollableFrame(process_list_frame, width=250, height=200)
        self.process_list_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.process_ui_elements = {}

        clear_btn = ctk.CTkButton(self.left_panel, text="Clear All", 
                            command=self.clear_all, fg_color=SECONDARY_COLOR)
        clear_btn.pack(pady=10)

        self.right_panel = ctk.CTkFrame(self.main_frame)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.memory_visualizer = MemoryVisualizer(self.right_panel)

        self.status_var = ctk.StringVar(value="Ready")
        status_bar = ctk.CTkLabel(self.root, textvariable=self.status_var, anchor="w")
        status_bar.pack(side="bottom", fill="x", padx=10, pady=5)

    def update_partition_ui(self, choice):
        pass

    def apply_partitions(self):
        pass

    def add_process(self):
        pass

    def clear_all(self):
        pass

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MemoryManagementApp()
    app.run()
