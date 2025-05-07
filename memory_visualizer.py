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

        self.canvas = ctk.CTkCanvas(self.parent, width=self.canvas_width, 
                                    height=self.canvas_height, bg="#2b2b2b", 
                                    highlightbackground="#555555")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.stats_frame = ctk.CTkFrame(self.parent)
        self.stats_frame.pack(fill="x", padx=10, pady=10)
        
        self.memory_usage_var = ctk.StringVar(value="Memory Usage: 0 / 0 MB (0%)")
        memory_usage_label = ctk.CTkLabel(self.stats_frame, textvariable=self.memory_usage_var)
        memory_usage_label.pack(side="left", padx=10)
        
        self.fragmentation_var = ctk.StringVar(value="Fragmentation: 0%")
        fragmentation_label = ctk.CTkLabel(self.stats_frame, textvariable=self.fragmentation_var)
        fragmentation_label.pack(side="right", padx=10)