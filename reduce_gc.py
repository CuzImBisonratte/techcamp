# Import libraries
from Maix import utils
import machine

# Change the GarbageCollector Heap Size
utils.gc_heap_size(256*1024)

# Reset board
machine.reset()
