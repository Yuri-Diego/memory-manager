from block import Block


class MemoryManager:
    def __init__(self, total_size=128, block_size=2):
        self.block_size = block_size
        self.total_blocks = total_size // block_size
        self.head = self._create_blocks()

    def _create_blocks(self):
        head = Block(0, self.block_size)
        current = head
        for i in range(1, self.total_blocks):
            new_block = Block(i, self.block_size)
            current.next = new_block
            current = new_block
        return head

    def display(self):
        current = self.head
        line = []
        while current:
            line.append(repr(current))
            current = current.next
        print(" -> ".join(line))
        print("-" * 80)

    def allocate(self, process, size, strategy="first"):
        blocks_needed = (size + self.block_size - 1) // self.block_size  # arredonda pra cima

        if strategy == "first":
            return self._first_fit(process, blocks_needed)
        elif strategy == "best":
            return self._best_fit(process, blocks_needed)
        elif strategy == "worst":
            return self._worst_fit(process, blocks_needed)
        else:
            raise ValueError("Estratégia inválida! Use 'first', 'best' ou 'worst'.")

    def deallocate(self, process):
        current = self.head
        freed = False
        while current:
            if not current.free and current.process == process:
                current.free = True
                current.process = None
                freed = True
            current = current.next
        return freed

    def _find_free_sequences(self):
        """Encontra sequências contínuas de blocos livres"""
        sequences = []
        current = self.head
        start = None
        length = 0
        while current:
            if current.free:
                if start is None:
                    start = current
                length += 1
            else:
                if start:
                    sequences.append((start, length))
                    start = None
                    length = 0
            current = current.next
        if start:
            sequences.append((start, length))
        return sequences

    def _first_fit(self, process, blocks_needed):
        sequences = self._find_free_sequences()
        for start, length in sequences:
            if length >= blocks_needed:
                self._allocate_blocks(start, process, blocks_needed)
                return True
        return False

    def _best_fit(self, process, blocks_needed):
        sequences = self._find_free_sequences()
        best = None
        best_len = float("inf")
        for start, length in sequences:
            if length >= blocks_needed and length < best_len:
                best = start
                best_len = length
        if best:
            self._allocate_blocks(best, process, blocks_needed)
            return True
        return False

    def _worst_fit(self, process, blocks_needed):
        sequences = self._find_free_sequences()
        worst = None
        worst_len = -1
        for start, length in sequences:
            if length >= blocks_needed and length > worst_len:
                worst = start
                worst_len = length
        if worst:
            self._allocate_blocks(worst, process, blocks_needed)
            return True
        return False

    def _allocate_blocks(self, start, process, blocks_needed):
        current = start
        for _ in range(blocks_needed):
            current.free = False
            current.process = process
            current = current.next
