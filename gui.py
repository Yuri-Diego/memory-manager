import tkinter as tk
import random

class MemoryGUI:
    def __init__(self, manager):
        self.manager = manager

        self.root = tk.Tk()
        self.root.title("Gerenciador de Memória")
        self.canvas = tk.Canvas(self.root, width=600, height=350, bg="white")
        self.canvas.pack()

        frame = tk.Frame(self.root)
        frame.pack()

        tk.Label(frame, text="Processo:").grid(row=0, column=0)
        self.entry_proc = tk.Entry(frame, width=5)
        self.entry_proc.grid(row=0, column=1)

        tk.Label(frame, text="Tamanho (KB):").grid(row=0, column=2)
        self.entry_size = tk.Entry(frame, width=5)
        self.entry_size.grid(row=0, column=3)

        tk.Button(frame, text="First Fit", command=lambda: self.allocate("first")).grid(row=0, column=4)
        tk.Button(frame, text="Best Fit", command=lambda: self.allocate("best")).grid(row=0, column=5)
        tk.Button(frame, text="Worst Fit", command=lambda: self.allocate("worst")).grid(row=0, column=6)

        tk.Button(frame, text="Desalocar", command=self.deallocate).grid(row=0, column=7)

        self.update_display()
        self.root.mainloop()

    def update_display(self):
        self.canvas.delete("all")
        block_width = 800 // 16
        block_height = 40
        current = self.manager.head
        i = 0
        while current:
            x = (i % 8) * block_width
            y = (i // 8) * block_height
            color = "green" if current.free else "red"
            self.canvas.create_rectangle(x, y, x + block_width, y + block_height, fill=color)
            if not current.free:
                self.canvas.create_text(x + block_width/2, y + block_height/2, text=current.process, fill="white")
            current = current.next
            i += 1

    def allocate(self, strategy):
        process = self.entry_proc.get()
        try:
            size = int(self.entry_size.get())
        except ValueError:
            return
        if self.manager.allocate(process, size, strategy):
            self.update_display()

    def deallocate(self):
        process = self.entry_proc.get()
        if self.manager.deallocate(process):
            self.update_display()
