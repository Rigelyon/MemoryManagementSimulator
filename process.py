class Process:
    """
    Kelas yang merepresentasikan sebuah proses dalam sistem manajemen memori.

    Kelas ini menyimpan informasi tentang proses yang berjalan dalam sistem, termasuk
    nama proses, ukuran memori yang dibutuhkan, dan durasi proses. Kelas ini juga
    melacak waktu yang telah berlalu sejak proses dimulai.

    Attributes:
        name (str): Nama unik dari proses yang digunakan untuk identifikasi
        size (int): Ukuran memori yang dibutuhkan proses dalam megabyte (MB)
        duration (int): Durasi proses dalam detik sebelum proses selesai
        elapsed_time (int): Waktu yang telah berlalu sejak proses dimulai dalam detik
    """

    def __init__(self, name, size, duration):
        """
        Inisialisasi objek Process baru.

        Method ini membuat instance baru dari kelas Process dengan parameter yang diberikan.
        Waktu yang telah berlalu diinisialisasi ke 0.

        Args:
            name (str): Nama proses yang akan digunakan untuk identifikasi
            size (int): Ukuran memori yang dibutuhkan dalam megabyte (MB)
            duration (int): Durasi proses dalam detik sebelum proses selesai

        Raises:
            ValueError: Jika size atau duration bernilai negatif atau nol
        """
        self.name = name
        self.size = size
        self.duration = duration
        self.elapsed_time = 0

    def __str__(self):
        """
        Mengembalikan representasi string dari proses.

        Method ini mengembalikan string yang berisi nama proses dan ukuran memori
        yang dibutuhkan dalam format yang mudah dibaca.

        Returns:
            str: String dalam format "nama_proses (ukuran MB)"

        Example:
            >>> process = Process("Chrome", 100, 60)
            >>> print(process)
            'Chrome (100 MB)'
        """
        return f"{self.name} ({self.size} MB)"
