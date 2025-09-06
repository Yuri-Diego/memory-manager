from memoryManager import MemoryManager
from gui import MemoryGUI

if __name__ == "__main__":
    manager = MemoryManager(128,2)
    gui = MemoryGUI(manager)
