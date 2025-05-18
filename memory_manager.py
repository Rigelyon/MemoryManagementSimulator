from process import Process
import time
import threading

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
        self.timer_running = False
        self.partitioned = False
        self.partitions = []
        self.time_update_callbacks = []

    def register_callback(self, callback):
        self.block_callbacks.append(callback)

    def register_process_callback(self, callback):
        self.process_callbacks.append(callback)

    def register_time_update_callback(self, callback):
        self.time_update_callbacks.append(callback)

    def notify_callbacks(self):
        for callback in self.block_callbacks:
            callback(self.memory_blocks)

    def notify_process_expired(self, process_name):
        for callback in self.process_callbacks:
            callback(process_name)

    def notify_time_update(self):
        for callback in self.time_update_callbacks:
            callback(self.processes)

    def resize_memory(self, new_size):
        if new_size < self.total_memory:
            used_memory = sum(block.size for block in self.memory_blocks if not block.is_free)
            if used_memory > new_size:
                return False

        self.total_memory = new_size

        if self.partitioned:
            self.clear_all()
            self.create_partitions(self.partitions)
        else:
            allocated_blocks = [block for block in self.memory_blocks if not block.is_free]
            if not allocated_blocks:
                self.memory_blocks = [MemoryBlock(0, new_size)]
            else:
                self.memory_blocks = []
                last_end = 0

                for block in sorted(allocated_blocks, key=lambda b: b.start):
                    if block.start > last_end:
                        self.memory_blocks.append(MemoryBlock(last_end, block.start - last_end))
                    self.memory_blocks.append(block)
                    last_end = block.end + 1

                if last_end < new_size:
                    self.memory_blocks.append(MemoryBlock(last_end, new_size - last_end))

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

    def get_free_blocks(self):
        return [block for block in self.memory_blocks if block.is_free]

    def merge_free_blocks(self):
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
                    if (current_block.is_free and next_block.is_free and 
                        current_block.end + 1 == next_block.start and
                        current_block.partition_id == next_block.partition_id):
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
                if (current_block.is_free and next_block.is_free and 
                    current_block.end + 1 == next_block.start):
                    current_block.size += next_block.size
                    current_block.end = next_block.end
                else:
                    merged_blocks.append(current_block)
                    current_block = next_block

            merged_blocks.append(current_block)
            self.memory_blocks = merged_blocks

    def allocate_process(self, process, algorithm="First Fit"):
        process.algorithm = algorithm
        if algorithm == "First Fit":
            return self.first_fit(process)
        elif algorithm == "Best Fit":
            return self.best_fit(process)
        elif algorithm == "Worst Fit":
            return self.worst_fit(process)
        return False

    def first_fit(self, process):
        for i, block in enumerate(self.memory_blocks):
            if block.is_free and block.size >= process.size:
                return self.allocate_block(i, process)
        return False

    def best_fit(self, process):
        best_block_index = -1
        best_block_size = float('inf')

        for i, block in enumerate(self.memory_blocks):
            if block.is_free and block.size >= process.size:
                if block.size < best_block_size:
                    best_block_index = i
                    best_block_size = block.size

        if best_block_index != -1:
            return self.allocate_block(best_block_index, process)
        return False

    def worst_fit(self, process):
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
        for block in self.memory_blocks:
            if not block.is_free and block.process and block.process.name == process_name:
                return block.partition_id
        return None

    def allocate_block(self, block_index, process):
        block = self.memory_blocks[block_index]
        partition_id = block.partition_id

        if process.name in self.processes:
            self.deallocate_process(process.name)

        if block.size == process.size:
            block.is_free = False
            block.process = process
        else:
            used_block = MemoryBlock(block.start, process.size, False, process, partition_id)
            free_block = MemoryBlock(block.start + process.size, block.size - process.size, partition_id=partition_id)

            self.memory_blocks[block_index] = used_block
            self.memory_blocks.insert(block_index + 1, free_block)

        self.processes[process.name] = process

        if not self.timer_running:
            self.start_process_timer()

        self.notify_callbacks()
        return True

    def deallocate_process(self, process_name):
        if process_name not in self.processes:
            return False

        for block in self.memory_blocks:
            if not block.is_free and block.process and block.process.name == process_name:
                block.is_free = True
                block.process = None
                del self.processes[process_name]
                self.merge_free_blocks()
                self.notify_callbacks()
                return True

        return False

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

    def start_process_timer(self):
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
