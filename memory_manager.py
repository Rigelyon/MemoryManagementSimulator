class MemoryBlock:
    def __init__(self, start, size, is_free=True, process=None, partition_id=None):
        self.start = start
        self.size = size
        self.is_free = is_free
        self.process = process
        self.end = start + size - 1
        self.partition_id = partition_id


class MemoryManager:
    def __init__(self, total_memory=1024):
        self.total_memory = total_memory
        self.memory_blocks = [MemoryBlock(0, total_memory)]
        self.processes = {}
        self.block_callbacks = []
        self.process_callbacks = []
        self.partitioned = False
        self.partitions = []

    def notify_callbacks(self):
        for callback in self.block_callbacks:
            callback(self.memory_blocks)

    def notify_process_expired(self, process_name):
        for callback in self.process_callbacks:
            callback(process_name)

    def resize_memory(self, new_size):
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

    def clear_all(self):
        if self.partitioned and self.partitions:
            self.create_partitions(self.partitions)
        else:
            self.partitioned = False
            self.partitions = []
            self.memory_blocks = [MemoryBlock(0, self.total_memory)]

        self.processes = {}
        self.timer_running = False
        self.notify_callbacks()
