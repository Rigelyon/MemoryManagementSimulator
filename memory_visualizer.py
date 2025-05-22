import customtkinter as ctk
import random
from config import BLOCK_COLORS


class MemoryVisualizer:
    """
    Kelas yang menangani visualisasi alokasi memori dalam antarmuka grafis.

    Kelas ini bertanggung jawab untuk menampilkan representasi visual dari
    alokasi memori dalam sistem. Visualisasi mencakup:
    - Blok memori yang digunakan dan kosong
    - Partisi memori (jika ada)
    - Proses yang sedang berjalan
    - Statistik penggunaan memori

    Visualisasi ditampilkan dalam bentuk bar horizontal, di mana:
    - Setiap blok memori direpresentasikan sebagai segmen bar
    - Warna berbeda digunakan untuk membedakan proses
    - Partisi ditandai dengan warna khusus
    - Ukuran blok proporsional dengan ukuran memori yang digunakan

    Attributes:
        parent: Widget induk untuk visualisasi (biasanya frame atau window)
        memory_manager: Instance dari MemoryManager yang menyediakan data
        canvas_height (int): Tinggi canvas dalam piksel
        canvas_width (int): Lebar canvas dalam piksel
        margin (int): Margin canvas dalam piksel untuk padding
    """

    def __init__(self, parent, memory_manager):
        """
        Inisialisasi objek MemoryVisualizer baru.

        Method ini membuat instance baru dari MemoryVisualizer dan menyiapkan
        antarmuka visualisasi. Canvas dan elemen UI lainnya dibuat dan
        dikonfigurasi untuk menampilkan visualisasi memori.

        Args:
            parent: Widget induk untuk visualisasi
            memory_manager: Instance dari MemoryManager yang menyediakan data
        """
        self.parent = parent
        self.memory_manager = memory_manager
        self.canvas_height = 400
        self.canvas_width = 500
        self.margin = 20

        self.memory_manager.register_callback(self.update_visualization)

        self.create_ui()

    def create_ui(self):
        """
        Membuat elemen-elemen antarmuka pengguna untuk visualisasi.

        Method ini membuat dan mengkonfigurasi semua elemen UI yang diperlukan:
        - Canvas untuk visualisasi memori
        - Label untuk judul
        - Frame untuk statistik
        - Label untuk menampilkan informasi penggunaan memori
        """
        title_label = ctk.CTkLabel(
            self.parent,
            text="Memory Allocation Visualization",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        title_label.pack(pady=10)

        self.canvas = ctk.CTkCanvas(
            self.parent,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#2b2b2b",
            highlightbackground="#555555",
        )
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.stats_frame = ctk.CTkFrame(self.parent)
        self.stats_frame.pack(fill="x", padx=10, pady=10)

        self.stats_row1 = ctk.CTkFrame(self.stats_frame)
        self.stats_row1.pack(fill="x", padx=5, pady=5)

        self.memory_usage_var = ctk.StringVar(value="Memory Usage: 0 / 0 MB (0%)")
        memory_usage_label = ctk.CTkLabel(
            self.stats_row1, textvariable=self.memory_usage_var
        )
        memory_usage_label.pack(side="left", padx=10)

        self.fragmentation_var = ctk.StringVar(value="Fragmentation: 0%")
        fragmentation_label = ctk.CTkLabel(
            self.stats_row1, textvariable=self.fragmentation_var
        )
        fragmentation_label.pack(side="right", padx=10)

        self.stats_row2 = ctk.CTkFrame(self.stats_frame)
        self.stats_row2.pack(fill="x", padx=5, pady=5)

        self.process_count_var = ctk.StringVar(value="Active Processes: 0")
        process_count_label = ctk.CTkLabel(
            self.stats_row2, textvariable=self.process_count_var
        )
        process_count_label.pack(side="left", padx=10)

        self.largest_free_var = ctk.StringVar(value="Largest Free Block: 0 MB")
        largest_free_label = ctk.CTkLabel(
            self.stats_row2, textvariable=self.largest_free_var
        )
        largest_free_label.pack(side="right", padx=10)

        self.redraw()

    def redraw(self):
        """
        Menggambar ulang visualisasi memori.

        Method ini memicu pembaruan visualisasi dengan mengambil data terbaru
        dari memory_manager. Biasanya dipanggil setelah ada perubahan pada
        alokasi memori.
        """
        self.update_visualization(self.memory_manager.memory_blocks)

    def update_visualization(self, memory_blocks):
        """
        Memperbarui visualisasi berdasarkan blok memori saat ini.

        Method ini menggambar ulang visualisasi memori berdasarkan data blok
        memori yang diberikan. Visualisasi mencakup:
        - Blok memori yang digunakan dan kosong
        - Partisi (jika ada)
        - Label untuk setiap blok
        - Skala memori
        - Statistik penggunaan

        Args:
            memory_blocks (list): Daftar blok memori yang akan divisualisasikan
        """
        self.canvas.delete("all")

        if not memory_blocks:
            return

        total_memory = self.memory_manager.total_memory
        used_memory = sum(block.size for block in memory_blocks if not block.is_free)
        usage_percent = (used_memory / total_memory) * 100 if total_memory > 0 else 0

        free_blocks = [block for block in memory_blocks if block.is_free]
        fragmentation = 0
        if free_blocks and sum(block.size for block in free_blocks) > 0:
            fragmentation = (len(free_blocks) - 1) / len(free_blocks) * 100

        active_processes = len(self.memory_manager.processes)

        largest_free_block = max([block.size for block in free_blocks], default=0)

        self.memory_usage_var.set(
            f"Memory Usage: {used_memory} / {total_memory} MB ({usage_percent:.1f}%)"
        )
        self.fragmentation_var.set(f"Fragmentation: {fragmentation:.1f}%")
        self.process_count_var.set(f"Active Processes: {active_processes}")
        self.largest_free_var.set(f"Largest Free Block: {largest_free_block} MB")

        canvas_width = self.canvas.winfo_width() or self.canvas_width
        canvas_height = self.canvas.winfo_height() or self.canvas_height

        usable_width = canvas_width - 2 * self.margin
        usable_height = canvas_height - 2 * self.margin

        y_center = canvas_height // 2
        block_height = min(usable_height, 80)

        self.canvas.create_text(
            self.margin, self.margin - 10, text="0", fill="white", anchor="w"
        )
        self.canvas.create_text(
            canvas_width - self.margin,
            self.margin - 10,
            text=str(total_memory),
            fill="white",
            anchor="e",
        )

        partition_colors = [
            "#3a7ebf",
            "#bf3a3a",
            "#3abf7e",
            "#7e3abf",
            "#bf7e3a",
            "#7ebf3a",
        ]

        process_colors = {}

        partitions = set()

        for block in memory_blocks:
            if block.partition_id is not None:
                partitions.add(block.partition_id)

        for block in memory_blocks:
            x_start = self.margin + (block.start / total_memory) * usable_width
            x_end = (
                self.margin + ((block.start + block.size) / total_memory) * usable_width
            )

            y_top = y_center - block_height // 2
            y_bottom = y_center + block_height // 2

            if block.partition_id is not None:
                partition_color = partition_colors[
                    block.partition_id % len(partition_colors)
                ]
                self.canvas.create_rectangle(
                    x_start,
                    y_top - 10,
                    x_end,
                    y_top - 2,
                    fill=partition_color,
                    outline="",
                )

                if x_end - x_start > 50:
                    self.canvas.create_text(
                        (x_start + x_end) / 2,
                        y_top - 6,
                        text=f"P{block.partition_id}",
                        fill="white",
                        font=("Arial", 8),
                    )

            if block.is_free:
                color = "#444444"
                text_color = "white"
                text = f"Free: {block.size} MB"
            else:
                process_name = block.process.name
                if process_name not in process_colors:
                    process_colors[process_name] = random.choice(BLOCK_COLORS)
                color = process_colors[process_name]
                text_color = (
                    "black"
                    if sum(int(color[i : i + 2], 16) for i in (1, 3, 5)) > 380
                    else "white"
                )
                text = f"{block.process.name}: {block.size} MB"

            border_width = 2 if block.partition_id is not None else 1
            self.canvas.create_rectangle(
                x_start,
                y_top,
                x_end,
                y_bottom,
                fill=color,
                outline="black",
                width=border_width,
            )

            if x_end - x_start > 50:
                self.canvas.create_text(
                    (x_start + x_end) / 2,
                    (y_top + y_bottom) / 2,
                    text=text,
                    fill=text_color,
                )

            self.canvas.create_line(
                x_start, y_bottom + 5, x_start, y_bottom + 10, fill="white"
            )
            self.canvas.create_text(
                x_start,
                y_bottom + 20,
                text=str(block.start),
                fill="white",
                font=("Arial", 8),
            )

            last_pos = self.margin + usable_width
            self.canvas.create_line(
                last_pos, y_bottom + 5, last_pos, y_bottom + 10, fill="white"
            )
            self.canvas.create_text(
                last_pos,
                y_bottom + 20,
                text=str(total_memory),
                fill="white",
                font=("Arial", 8),
            )
