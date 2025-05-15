import customtkinter as ctk
from config import PRIMARY_COLOR, SECONDARY_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT
from memory_manager import MemoryManager
from memory_visualizer import MemoryVisualizer
from process import Process

class MemoryManagementApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Memory Management Simulator")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.memory_manager = MemoryManager(total_memory=1024)

        self.active_sliders = []
        self.partition_values = []

        self.create_ui()

    def create_ui(self):
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.left_panel = ctk.CTkScrollableFrame(self.main_frame, width=400)
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
            command=self.update_memory_size,
        )
        update_btn.pack(side="left", padx=5)

        partition_frame = ctk.CTkFrame(self.left_panel)
        partition_frame.pack(fill="x", padx=10, pady=10)

        partition_label = ctk.CTkLabel(
            partition_frame, text="Memory Partitions:", font=ctk.CTkFont(weight="bold")
        )
        partition_label.pack(pady=5)

        partition_control_frame = ctk.CTkFrame(partition_frame)
        partition_control_frame.pack(fill="x", padx=5, pady=5)

        num_partitions_label = ctk.CTkLabel(
            partition_control_frame, text="Number of Partitions:"
        )
        num_partitions_label.pack(side="left", padx=5)

        self.partition_count_var = ctk.StringVar(value="1")
        partition_values = ["1", "2", "3", "4", "5", "6"]
        partition_dropdown = ctk.CTkOptionMenu(
            partition_control_frame,
            values=partition_values,
            variable=self.partition_count_var,
            command=self.update_partition_ui,
        )
        partition_dropdown.pack(side="left", padx=5)

        self.partition_sliders_frame = ctk.CTkFrame(partition_frame)
        self.partition_sliders_frame.pack(fill="x", padx=5, pady=5)

        apply_partitions_btn = ctk.CTkButton(
            partition_frame, text="Apply Partitions", command=self.apply_partitions
        )
        apply_partitions_btn.pack(pady=5)

        self.update_partition_ui("1")

        process_frame = ctk.CTkFrame(self.left_panel)
        process_frame.pack(fill="x", padx=10, pady=10)

        process_label = ctk.CTkLabel(
            process_frame, text="Process Creation:", font=ctk.CTkFont(weight="bold")
        )
        process_label.pack(pady=5)

        # Create a frame for all the process inputs using grid layout
        process_inputs_frame = ctk.CTkFrame(process_frame)
        process_inputs_frame.pack(fill="x", padx=5, pady=5)

        # Process Name
        name_label = ctk.CTkLabel(
            process_inputs_frame,
            text="Process Name:",
        )
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.process_name_var = ctk.StringVar(value="Process 1")
        name_entry = ctk.CTkEntry(
            process_inputs_frame,
            textvariable=self.process_name_var,
            width=150,
        )
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Process Size
        size_label = ctk.CTkLabel(process_inputs_frame, text="Process Size (MB):")
        size_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.process_size_var = ctk.StringVar(value="60")
        size_entry = ctk.CTkEntry(
            process_inputs_frame,
            textvariable=self.process_size_var,
            width=150,
        )
        size_entry.grid(row=1, column=1, padx=5, pady=5)

        # Duration
        time_label = ctk.CTkLabel(process_inputs_frame, text="Duration (seconds):")
        time_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.process_time_var = ctk.StringVar(value="120")
        time_entry = ctk.CTkEntry(
            process_inputs_frame, textvariable=self.process_time_var, width=150
        )
        time_entry.grid(row=2, column=1, padx=5, pady=5)

        # Algorithm
        algo_label = ctk.CTkLabel(process_inputs_frame, text="Algorithm:")
        algo_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.algorithm_var = ctk.StringVar(value="First Fit")
        algorithms = ["First Fit", "Best Fit", "Worst Fit"]
        algo_dropdown = ctk.CTkOptionMenu(
            process_inputs_frame, values=algorithms, variable=self.algorithm_var
        )
        algo_dropdown.grid(row=3, column=1, padx=5, pady=5)

        # Add Process Button
        add_btn = ctk.CTkButton(
            process_frame, text="Add Process", command=self.add_process
        )
        add_btn.pack(pady=5)

        process_list_frame = ctk.CTkFrame(self.left_panel)
        process_list_frame.pack(fill="x", padx=10, pady=10)

        list_label = ctk.CTkLabel(
            process_list_frame, text="Process Queue:", font=ctk.CTkFont(weight="bold")
        )
        list_label.pack(pady=5)

        self.process_list_scroll = ctk.CTkScrollableFrame(
            process_list_frame, width=250, height=200
        )
        self.process_list_scroll.pack(fill="x", padx=5, pady=5)

        self.process_ui_elements = {}

        clear_btn = ctk.CTkButton(
            self.left_panel,
            text="Clear All",
            command=self.clear_all,
            fg_color=SECONDARY_COLOR,
        )
        clear_btn.pack(pady=10)

        self.right_panel = ctk.CTkFrame(self.main_frame)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.memory_visualizer = MemoryVisualizer(self.right_panel, self.memory_manager)

        self.status_var = ctk.StringVar(value="Ready")
        status_bar = ctk.CTkLabel(self.root, textvariable=self.status_var, anchor="w")
        status_bar.pack(side="bottom", fill="x", padx=10, pady=5)

    def update_partition_ui(self, choice):
        for widget in self.partition_sliders_frame.winfo_children():
            widget.destroy()

        self.active_sliders = []
        num_partitions = int(choice)

        default_percentage = 100 / num_partitions

        for i in range(num_partitions):
            slider_frame = ctk.CTkFrame(self.partition_sliders_frame)
            slider_frame.pack(fill="x", padx=5, pady=2)

            label = ctk.CTkLabel(slider_frame, text=f"Partition {i+1}:")
            label.pack(side="left", padx=5)

            percentage_var = ctk.DoubleVar(value=default_percentage)
            slider = ctk.CTkSlider(
                slider_frame,
                from_=5,
                to=100,
                number_of_steps=19,
                variable=percentage_var,
                command=lambda val, idx=i: self.on_slider_change(val, idx),
            )
            slider.pack(side="left", fill="x", expand=True, padx=5)

            percentage_label = ctk.CTkLabel(
                slider_frame, text=f"{default_percentage:.1f}%", width=60
            )
            percentage_label.pack(side="left", padx=5)

            self.active_sliders.append((percentage_var, percentage_label))

        self.partition_values = [default_percentage] * num_partitions

    def on_slider_change(self, value, index):
        self.active_sliders[index][1].configure(text=f"{value:.1f}%")

        total = sum(slider_var.get() for slider_var, _ in self.active_sliders)

        if abs(total - 100) > 0.1:
            excess = total - 100

            adjustable_sliders = [
                (i, var)
                for i, (var, _) in enumerate(self.active_sliders)
                if i != index and var.get() > 5
            ]

            if adjustable_sliders:
                adjustment_per_slider = excess / len(adjustable_sliders)

                for i, var in adjustable_sliders:
                    new_value = max(5, var.get() - adjustment_per_slider)
                    var.set(new_value)
                    self.active_sliders[i][1].configure(text=f"{new_value:.1f}%")

        self.partition_values = [
            slider_var.get() for slider_var, _ in self.active_sliders
        ]

    def apply_partitions(self):
        total = sum(self.partition_values)
        if abs(total - 100) > 0.1:
            self.partition_values = [
                val * (100 / total) for val in self.partition_values
            ]

            for i, (var, label) in enumerate(self.active_sliders):
                var.set(self.partition_values[i])
                label.configure(text=f"{self.partition_values[i]:.1f}%")

        process_names = list(self.process_ui_elements.keys())

        result = self.memory_manager.create_partitions(self.partition_values)

        if result:
            for process_name in process_names:
                if process_name in self.process_ui_elements:
                    self.process_ui_elements[process_name]["frame"].destroy()

            self.process_ui_elements = {}

            self.memory_visualizer.redraw()
            self.status_var.set(
                f"Memory partitioned into {len(self.partition_values)} sections"
            )
        else:
            self.status_var.set("Failed to partition memory")

    def update_memory_size(self):
        try:
            new_size = int(self.memory_size_var.get())
            if new_size <= 0:
                self.status_var.set("Memory size must be positive")
                return

            self.memory_manager.resize_memory(new_size)
            self.memory_visualizer.redraw()
            self.status_var.set(f"Memory size updated to {new_size} MB")
        except ValueError:
            self.status_var.set("Invalid memory size")

    def add_process(self):
        try:
            name = self.process_name_var.get()
            size = int(self.process_size_var.get())
            duration = int(self.process_time_var.get())

            if not name or size <= 0 or duration <= 0:
                self.status_var.set("Please enter valid process details")
                return

            process = Process(name, size, duration)

            algorithm = self.algorithm_var.get()
            result = self.memory_manager.allocate_process(process, algorithm)

            if result:
                self.add_to_process_list(process)
                self.memory_visualizer.redraw()
                self.process_name_var.set("")
                self.process_size_var.set("")
                self.process_time_var.set("")
                self.status_var.set(f"Process '{name}' added successfully")
            else:
                self.status_var.set(f"Not enough space for process '{name}'")

        except ValueError:
            self.status_var.set("Invalid size or duration")

    def add_to_process_list(self, process):
        process_item = ctk.CTkFrame(self.process_list_scroll)
        process_item.pack(fill="x", padx=5, pady=5)
        process_item.grid_columnconfigure(0, weight=1)

        partition_id = self.memory_manager.get_process_partition(process.name)
        partition_text = (
            f" [Partition {partition_id+1}]" if partition_id is not None else ""
        )

        header_frame = ctk.CTkFrame(process_item, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=2)

        process_name_label = ctk.CTkLabel(
            header_frame, text=f"{process.name} ({process.size} MB)", anchor="w"
        )
        process_name_label.pack(side="left")

        if partition_id is not None:
            partition_colors = [
                "#3a7ebf",
                "#bf3a3a",
                "#3abf7e",
                "#7e3abf",
                "#bf7e3a",
                "#7ebf3a",
            ]
            color = partition_colors[partition_id % len(partition_colors)]
            partition_label = ctk.CTkLabel(
                header_frame,
                text=f"P{partition_id}",
                fg_color=color,
                text_color="white",
                corner_radius=10,
                width=30,
                height=20,
            )
            partition_label.pack(side="right", padx=5)

        if process.algorithm:
            algo_colors = {
                "First Fit": "#4CAF50",
                "Best Fit": "#2196F3",
                "Worst Fit": "#FF9800",
            }
            algo_color = algo_colors.get(process.algorithm, "#9C27B0")

            algo_letter = (
                "".join(word[0] for word in process.algorithm.split())
                if process.algorithm
                else "?"
            )
            algo_label = ctk.CTkLabel(
                header_frame,
                text=algo_letter,
                fg_color=algo_color,
                text_color="white",
                corner_radius=10,
                width=30,
                height=20,
            )
            algo_label.pack(side="right", padx=5)

        time_var = ctk.StringVar(
            value=f"Time: {process.elapsed_time}s / {process.duration}s"
        )
        time_label = ctk.CTkLabel(process_item, textvariable=time_var)
        time_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)

        remove_btn = ctk.CTkButton(
            process_item,
            text="Remove",
            width=70,
            height=25,
            command=lambda p=process: self.remove_process(p, process_item),
            fg_color=SECONDARY_COLOR,
        )
        remove_btn.grid(row=0, column=1, rowspan=2, padx=5, pady=2)

        self.process_ui_elements[process.name] = {
            "frame": process_item,
            "time_var": time_var,
            "process": process,
        }

    def remove_process(self, process, list_item):
        self.memory_manager.deallocate_process(process.name)
        list_item.destroy()
        if process.name in self.process_ui_elements:
            del self.process_ui_elements[process.name]
        self.memory_visualizer.redraw()
        self.status_var.set(f"Process '{process.name}' removed")

    def process_expired_callback(self, process_name):
        self.root.after(0, self.remove_expired_process_from_ui, process_name)

    def remove_expired_process_from_ui(self, process_name):
        if process_name in self.process_ui_elements:
            self.process_ui_elements[process_name]["frame"].destroy()
            del self.process_ui_elements[process_name]
            self.status_var.set(f"Process '{process_name}' completed and removed")

    def clear_all(self):
        self.memory_manager.clear_all()
        for widget in self.process_list_scroll.winfo_children():
            widget.destroy()
        self.process_ui_elements = {}
        self.memory_visualizer.redraw()
        self.status_var.set("All processes cleared")

    def start_ui_update_timer(self):
        self.update_process_times()
        self.root.after(1000, self.start_ui_update_timer)

    def update_process_times(self):
        for process_name, ui_data in self.process_ui_elements.items():
            process = ui_data["process"]
            time_var = ui_data["time_var"]
            frame = ui_data["frame"]

            if process_name in self.memory_manager.processes:
                process = self.memory_manager.processes[process_name]
                remaining_time = process.duration - process.elapsed_time
                time_var.set(
                    f"Time: {process.elapsed_time}s / {process.duration}s ({remaining_time}s left)"
                )

            else:
                time_var.set(f"Time: {process.elapsed_time}s / {process.duration}s")
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MemoryManagementApp()
    app.run()
