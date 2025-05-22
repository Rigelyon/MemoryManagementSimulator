import time
import threading


class MemoryBlock:
    """
    Kelas yang merepresentasikan sebuah blok memori dalam sistem.

    Kelas ini menyimpan informasi tentang blok memori, termasuk lokasi, ukuran,
    status ketersediaan, dan proses yang menggunakan blok tersebut. Setiap blok
    memori memiliki alamat awal dan akhir yang digunakan untuk melacak posisinya
    dalam memori fisik.

    Attributes:
        start (int): Alamat awal blok memori dalam MB
        size (int): Ukuran blok memori dalam MB
        is_free (bool): Status apakah blok memori tersedia untuk dialokasikan
        process (Process): Proses yang menggunakan blok memori (None jika blok kosong)
        end (int): Alamat akhir blok memori dalam MB (start + size - 1)
        partition_id (int): ID partisi yang dimiliki blok memori (None jika tidak dipartisi)
    """

    def __init__(self, start, size, is_free=True, process=None, partition_id=None):
        """
        Inisialisasi objek MemoryBlock baru.

        Method ini membuat instance baru dari kelas MemoryBlock dengan parameter yang diberikan.
        Alamat akhir blok dihitung secara otomatis berdasarkan alamat awal dan ukuran.

        Args:
            start (int): Alamat awal blok memori dalam MB
            size (int): Ukuran blok memori dalam MB
            is_free (bool, optional): Status ketersediaan blok. Defaults to True.
            process (Process, optional): Proses yang menggunakan blok. Defaults to None.
            partition_id (int, optional): ID partisi. Defaults to None.

        Raises:
            ValueError: Jika start atau size bernilai negatif
        """
        self.start = start
        self.size = size
        self.is_free = is_free
        self.process = process
        self.end = start + size - 1
        self.partition_id = partition_id


class MemoryManager:
    """
    Kelas yang mengelola alokasi dan dealokasi memori dalam sistem.

    Kelas ini bertanggung jawab untuk mengelola memori sistem, termasuk:
    - Membuat dan mengelola partisi memori
    - Mengalokasikan memori untuk proses
    - Dealokasi memori ketika proses selesai
    - Menggabungkan blok memori yang kosong
    - Melacak penggunaan memori dan fragmentasi

    Kelas ini mendukung beberapa algoritma alokasi memori:
    - First Fit: Mengalokasikan ke blok pertama yang cukup besar
    - Best Fit: Mengalokasikan ke blok terkecil yang cukup besar
    - Worst Fit: Mengalokasikan ke blok terbesar yang tersedia

    Attributes:
        total_memory (int): Total ukuran memori dalam MB
        memory_blocks (list): Daftar blok memori dalam sistem
        processes (dict): Dictionary proses yang sedang berjalan (key: nama proses)
        block_callbacks (list): Daftar callback untuk perubahan blok memori
        process_callbacks (list): Daftar callback untuk perubahan proses
        timer_running (bool): Status timer proses
        partitioned (bool): Status apakah memori dipartisi
        partitions (list): Daftar persentase partisi
        time_update_callbacks (list): Daftar callback untuk update waktu
    """

    def __init__(self, total_memory=1024):
        """
        Inisialisasi objek MemoryManager baru.

        Method ini membuat instance baru dari MemoryManager dengan ukuran memori
        yang ditentukan. Memori diinisialisasi sebagai satu blok kosong besar.

        Args:
            total_memory (int, optional): Total ukuran memori dalam MB. Defaults to 1024.

        Raises:
            ValueError: Jika total_memory bernilai negatif atau nol
        """
        self.total_memory = total_memory
        self.memory_blocks = [MemoryBlock(0, total_memory)]
        self.processes = {}
        self.block_callbacks = []
        self.process_callbacks = []
        self.timer_running = False
        self.partitioned = False
        self.partitions = []
        self.time_update_callbacks = []

    def register_callback(self, callback):
        """
        Mendaftarkan callback untuk perubahan blok memori.

        Callback akan dipanggil setiap kali ada perubahan pada blok memori,
        seperti alokasi atau dealokasi. Callback menerima parameter berupa
        daftar blok memori terbaru.

        Args:
            callback (function): Fungsi yang akan dipanggil saat blok memori berubah.
                               Fungsi harus menerima parameter list[MemoryBlock]
        """
        self.block_callbacks.append(callback)

    def register_process_callback(self, callback):
        """
        Mendaftarkan callback untuk perubahan proses.

        Callback akan dipanggil setiap kali ada proses yang selesai atau dihapus.
        Callback menerima parameter berupa nama proses yang terpengaruh.

        Args:
            callback (function): Fungsi yang akan dipanggil saat proses berubah.
                               Fungsi harus menerima parameter str (nama proses)
        """
        self.process_callbacks.append(callback)

    def register_time_update_callback(self, callback):
        """
        Mendaftarkan callback untuk update waktu proses.

        Callback akan dipanggil setiap detik untuk memperbarui waktu proses.
        Callback menerima parameter berupa dictionary proses yang sedang berjalan.

        Args:
            callback (function): Fungsi yang akan dipanggil saat waktu proses berubah.
                               Fungsi harus menerima parameter dict (proses)
        """
        self.time_update_callbacks.append(callback)

    def notify_callbacks(self):
        """
        Memberitahu semua callback blok memori tentang perubahan.

        Method ini dipanggil setiap kali ada perubahan pada blok memori.
        Semua callback terdaftar akan dipanggil dengan daftar blok memori terbaru.
        """
        for callback in self.block_callbacks:
            callback(self.memory_blocks)

    def notify_process_expired(self, process_name):
        """
        Memberitahu semua callback proses tentang proses yang telah selesai.

        Method ini dipanggil ketika sebuah proses selesai atau dihapus.
        Semua callback terdaftar akan dipanggil dengan nama proses yang terpengaruh.

        Args:
            process_name (str): Nama proses yang telah selesai atau dihapus
        """
        for callback in self.process_callbacks:
            callback(process_name)

    def notify_time_update(self):
        """
        Memberitahu semua callback waktu tentang perubahan waktu proses.

        Method ini dipanggil setiap detik untuk memperbarui waktu proses.
        Semua callback terdaftar akan dipanggil dengan dictionary proses terbaru.
        """
        for callback in self.time_update_callbacks:
            callback(self.processes)

    def resize_memory(self, new_size):
        """
        Mengubah ukuran total memori.

        Method ini mengubah ukuran total memori sistem. Jika ukuran baru lebih kecil
        dari ukuran saat ini, method akan gagal jika ada proses yang menggunakan
        memori lebih dari ukuran baru. Jika memori dipartisi, semua partisi akan
        dihapus dan dibuat ulang.

        Args:
            new_size (int): Ukuran memori baru dalam MB

        Returns:
            bool: True jika berhasil mengubah ukuran, False jika gagal

        Raises:
            ValueError: Jika new_size bernilai negatif atau nol
        """
        if new_size < self.total_memory:
            used_memory = sum(
                block.size for block in self.memory_blocks if not block.is_free
            )
            if used_memory > new_size:
                return False

        self.total_memory = new_size

        if self.partitioned:
            self.clear_all()
            self.create_partitions(self.partitions)
        else:
            allocated_blocks = [
                block for block in self.memory_blocks if not block.is_free
            ]
            if not allocated_blocks:
                self.memory_blocks = [MemoryBlock(0, new_size)]
            else:
                self.memory_blocks = []
                last_end = 0

                for block in sorted(allocated_blocks, key=lambda b: b.start):
                    if block.start > last_end:
                        self.memory_blocks.append(
                            MemoryBlock(last_end, block.start - last_end)
                        )
                    self.memory_blocks.append(block)
                    last_end = block.end + 1

                if last_end < new_size:
                    self.memory_blocks.append(
                        MemoryBlock(last_end, new_size - last_end)
                    )

        self.notify_callbacks()
        return True

    def create_partitions(self, partition_percentages):
        """
        Membuat partisi memori berdasarkan persentase.

        Method ini membagi memori menjadi beberapa partisi berdasarkan persentase
        yang diberikan. Setiap partisi akan memiliki ID unik dan ukuran sesuai
        dengan persentasenya. Semua proses yang sedang berjalan akan dihapus
        ketika partisi dibuat.

        Args:
            partition_percentages (list): Daftar persentase untuk setiap partisi.
                                        Total harus 100% atau mendekati 100%

        Returns:
            bool: True jika berhasil membuat partisi, False jika gagal

        Raises:
            ValueError: Jika partition_percentages kosong atau berisi nilai negatif
        """
        if not partition_percentages:
            self.partitioned = False
            self.memory_blocks = [MemoryBlock(0, self.total_memory)]
            self.notify_callbacks()
            return True

        self.partitions = partition_percentages
        self.partitioned = True

        for process_name in list(self.processes.keys()):
            self.notify_process_expired(process_name)

        self.processes = {}
        self.memory_blocks = []

        start_pos = 0
        for i, percentage in enumerate(partition_percentages):
            size = int((percentage / 100) * self.total_memory)
            if size <= 0:
                size = 1

            if i == len(partition_percentages) - 1:
                size = self.total_memory - start_pos

            new_block = MemoryBlock(start_pos, size, is_free=True, partition_id=i)
            self.memory_blocks.append(new_block)
            start_pos += size

        self.notify_callbacks()
        return True

    def get_free_blocks(self):
        """
        Mendapatkan daftar blok memori yang tersedia.

        Method ini mengembalikan daftar semua blok memori yang saat ini tidak
        digunakan oleh proses apapun. Jika memori dipartisi, blok kosong akan
        dikelompokkan berdasarkan partisinya.

        Returns:
            list[MemoryBlock]: Daftar blok memori yang tersedia
        """
        return [block for block in self.memory_blocks if block.is_free]

    def merge_free_blocks(self):
        """
        Menggabungkan blok-blok memori yang tersedia yang berdekatan.

        Method ini mencari blok-blok memori kosong yang berdekatan dan menggabungkannya
        menjadi satu blok yang lebih besar. Ini membantu mengurangi fragmentasi
        memori. Jika memori dipartisi, penggabungan hanya dilakukan dalam partisi
        yang sama.
        """
        if not self.memory_blocks:
            return

        if self.partitioned:
            partitioned_blocks = {}
            for block in self.memory_blocks:
                if block.partition_id not in partitioned_blocks:
                    partitioned_blocks[block.partition_id] = []
                partitioned_blocks[block.partition_id].append(block)

            self.memory_blocks = []
            for partition_id, blocks in sorted(partitioned_blocks.items()):
                merged_blocks = []
                current_block = blocks[0]

                for i in range(1, len(blocks)):
                    next_block = blocks[i]
                    if (
                        current_block.is_free
                        and next_block.is_free
                        and current_block.end + 1 == next_block.start
                        and current_block.partition_id == next_block.partition_id
                    ):
                        current_block.size += next_block.size
                        current_block.end = next_block.end
                    else:
                        merged_blocks.append(current_block)
                        current_block = next_block

                merged_blocks.append(current_block)
                self.memory_blocks.extend(merged_blocks)
        else:
            merged_blocks = []
            current_block = self.memory_blocks[0]

            for i in range(1, len(self.memory_blocks)):
                next_block = self.memory_blocks[i]
                if (
                    current_block.is_free
                    and next_block.is_free
                    and current_block.end + 1 == next_block.start
                ):
                    current_block.size += next_block.size
                    current_block.end = next_block.end
                else:
                    merged_blocks.append(current_block)
                    current_block = next_block

            merged_blocks.append(current_block)
            self.memory_blocks = merged_blocks

    def allocate_process(self, process, algorithm="First Fit"):
        """
        Mengalokasikan proses ke memori menggunakan algoritma tertentu.

        Method ini mencoba mengalokasikan memori untuk proses menggunakan algoritma
        yang dipilih. Jika proses dengan nama yang sama sudah ada, proses tersebut
        akan dihapus terlebih dahulu.

        Args:
            process (Process): Proses yang akan dialokasikan
            algorithm (str, optional): Algoritma alokasi. Defaults to "First Fit".
                                    Pilihan: "First Fit", "Best Fit", "Worst Fit"

        Returns:
            bool: True jika berhasil mengalokasikan, False jika gagal

        Raises:
            ValueError: Jika algorithm tidak valid
        """
        process.algorithm = algorithm
        if algorithm == "First Fit":
            return self.first_fit(process)
        elif algorithm == "Best Fit":
            return self.best_fit(process)
        elif algorithm == "Worst Fit":
            return self.worst_fit(process)
        return False

    def first_fit(self, process):
        """
        Mengalokasikan proses menggunakan algoritma First Fit.

        Algoritma First Fit mencari blok memori kosong pertama yang cukup besar
        untuk menampung proses. Ini adalah algoritma yang paling sederhana dan
        cepat, tetapi mungkin tidak optimal dalam penggunaan memori.

        Args:
            process (Process): Proses yang akan dialokasikan

        Returns:
            bool: True jika berhasil mengalokasikan, False jika gagal
        """
        for i, block in enumerate(self.memory_blocks):
            if block.is_free and block.size >= process.size:
                return self.allocate_block(i, process)
        return False

    def best_fit(self, process):
        """
        Mengalokasikan proses menggunakan algoritma Best Fit.

        Algoritma Best Fit mencari blok memori kosong terkecil yang cukup besar
        untuk menampung proses. Ini membantu mengurangi fragmentasi memori, tetapi
        mungkin membutuhkan waktu pencarian lebih lama.

        Args:
            process (Process): Proses yang akan dialokasikan

        Returns:
            bool: True jika berhasil mengalokasikan, False jika gagal
        """
        best_block_index = -1
        best_block_size = float("inf")

        for i, block in enumerate(self.memory_blocks):
            if block.is_free and block.size >= process.size:
                if block.size < best_block_size:
                    best_block_index = i
                    best_block_size = block.size

        if best_block_index != -1:
            return self.allocate_block(best_block_index, process)
        return False

    def worst_fit(self, process):
        """
        Mengalokasikan proses menggunakan algoritma Worst Fit.

        Algoritma Worst Fit mencari blok memori kosong terbesar yang tersedia.
        Ini membantu mengurangi fragmentasi dengan memanfaatkan blok besar terlebih
        dahulu, tetapi mungkin tidak optimal untuk proses kecil.

        Args:
            process (Process): Proses yang akan dialokasikan

        Returns:
            bool: True jika berhasil mengalokasikan, False jika gagal
        """
        worst_block_index = -1
        worst_block_size = -1

        for i, block in enumerate(self.memory_blocks):
            if block.is_free and block.size >= process.size:
                if block.size > worst_block_size:
                    worst_block_index = i
                    worst_block_size = block.size

        if worst_block_index != -1:
            return self.allocate_block(worst_block_index, process)
        return False

    def get_process_partition(self, process_name):
        """
        Mendapatkan ID partisi dari proses.

        Method ini mencari partisi yang digunakan oleh proses dengan nama tertentu.
        Jika proses tidak ditemukan atau memori tidak dipartisi, method akan
        mengembalikan None.

        Args:
            process_name (str): Nama proses yang dicari

        Returns:
            int: ID partisi (0-based) atau None jika tidak ditemukan
        """
        for block in self.memory_blocks:
            if (
                not block.is_free
                and block.process
                and block.process.name == process_name
            ):
                return block.partition_id
        return None

    def allocate_block(self, block_index, process):
        """
        Mengalokasikan blok memori untuk proses.

        Method ini mengalokasikan blok memori pada indeks tertentu untuk proses.
        Jika ukuran blok lebih besar dari yang dibutuhkan, blok akan dibagi menjadi
        dua: satu untuk proses dan satu lagi sebagai blok kosong.

        Args:
            block_index (int): Indeks blok memori yang akan dialokasikan
            process (Process): Proses yang akan dialokasikan

        Returns:
            bool: True jika berhasil mengalokasikan, False jika gagal

        Raises:
            IndexError: Jika block_index tidak valid
        """
        block = self.memory_blocks[block_index]
        partition_id = block.partition_id

        if process.name in self.processes:
            self.deallocate_process(process.name)

        if block.size == process.size:
            block.is_free = False
            block.process = process
        else:
            used_block = MemoryBlock(
                block.start, process.size, False, process, partition_id
            )
            free_block = MemoryBlock(
                block.start + process.size,
                block.size - process.size,
                partition_id=partition_id,
            )

            self.memory_blocks[block_index] = used_block
            self.memory_blocks.insert(block_index + 1, free_block)

        self.processes[process.name] = process

        if not self.timer_running:
            self.start_process_timer()

        self.notify_callbacks()
        return True

    def deallocate_process(self, process_name):
        """
        Dealokasi proses dari memori.

        Method ini menghapus proses dari memori dan menandai blok memori yang
        digunakan sebagai kosong. Blok-blok kosong yang berdekatan akan digabungkan.

        Args:
            process_name (str): Nama proses yang akan dealokasi

        Returns:
            bool: True jika berhasil dealokasi, False jika proses tidak ditemukan
        """
        if process_name not in self.processes:
            return False

        for block in self.memory_blocks:
            if (
                not block.is_free
                and block.process
                and block.process.name == process_name
            ):
                block.is_free = True
                block.process = None
                del self.processes[process_name]
                self.merge_free_blocks()
                self.notify_callbacks()
                return True

        return False

    def clear_all(self):
        """
        Menghapus semua proses dan mengembalikan memori ke kondisi awal.

        Method ini menghapus semua proses yang sedang berjalan dan mengembalikan
        memori ke kondisi awal. Jika memori dipartisi, partisi akan dipertahankan
        tetapi semua blok akan dikosongkan.
        """
        if self.partitioned and self.partitions:
            self.create_partitions(self.partitions)
        else:
            self.partitioned = False
            self.partitions = []
            self.memory_blocks = [MemoryBlock(0, self.total_memory)]

        self.processes = {}
        self.timer_running = False
        self.notify_callbacks()

    def start_process_timer(self):
        """
        Memulai timer untuk menghitung waktu proses.

        Method ini memulai thread terpisah yang akan menghitung waktu untuk setiap
        proses. Thread akan berjalan setiap detik dan akan berhenti ketika tidak
        ada proses yang berjalan. Setiap detik, waktu proses akan diperbarui dan
        callback waktu akan dipanggil.
        """
        if self.timer_running:
            return

        self.timer_running = True

        def timer_thread():
            while self.processes and self.timer_running:
                processes_to_remove = []

                for name, process in list(self.processes.items()):
                    process.elapsed_time += 1
                    if process.elapsed_time >= process.duration:
                        processes_to_remove.append(name)

                self.notify_time_update()

                for name in processes_to_remove:
                    self.notify_process_expired(name)
                    self.deallocate_process(name)

                time.sleep(1)

            self.timer_running = False

        thread = threading.Thread(target=timer_thread)
        thread.daemon = True
        thread.start()
