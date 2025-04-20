import struct
from war3observer.memory_map import MemoryMap

from war3structs.observer import ObserverGame

class Game():
  refresh_rate = 2000
  game_size = ObserverGame.sizeof()
   
  def __init__(self):
    print("Initializing game...")
    mmap = MemoryMap(4, 4, write=True)
    mmap.write_data(struct.pack("<I", self.refresh_rate))
    mmap.close()
     
  def read_game(self):
    self.game_mm = MemoryMap(4, self.game_size)
    parsed = ObserverGame.parse(self.game_mm.data())
    del parsed._io
    return parsed
