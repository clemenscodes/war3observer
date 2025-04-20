import struct
from war3observer.memory_map import MemoryMap
from war3structs.observer import ObserverGame, ObserverFile

class Game():
  def __init__(self):
    self.max_players = 28
    self.max_shops = 999
    self.refresh_rate = 2000
    self.file_offset = 0
    self.integer_size = 4
    self.version_offset = self.file_offset
    self.file_size = ObserverFile.sizeof()
    self.game_size = ObserverGame.sizeof()
    self.refresh_rate_offset = self.version_offset + self.integer_size
    self.game_offset = self.refresh_rate_offset
    self.players_offset = self.game_offset + self.game_size
 
    self.file_size = self.find_correct_mmap_size()
    self.set_refresh_rate()

  def find_correct_mmap_size(self, min_size=0, max_size=256*1024*1024):
    low = min_size
    high = max_size
    best = 0

    while low <= high:
        mid = (low + high) // 2
        try:
            mm = MemoryMap(self.file_offset, mid)
            mm.close()
            best = mid
            low = mid + 1
        except (OSError, ValueError):
            high = mid - 1

    print(f"✅ Detected mmap size: {best}")
    return best

  def set_refresh_rate(self):
    mmap = MemoryMap(self.refresh_rate_offset, self.integer_size, write=True)
    mmap.write_data(struct.pack("<I", self.refresh_rate))
    mmap.close()

  def read_file(self):
    self.file_mm = MemoryMap(self.file_offset, self.file_size)
    self.file = ObserverFile.parse(self.file_mm.data())
    del self.file._io
    return self.file

  def read_game(self):
    self.game_mm = MemoryMap(self.game_offset, self.game_size)
    self.game = ObserverGame.parse(self.game_mm.data())
    del self.game._io
    return self.game

  def dump_observer_api(self):
    print("Dumping observer API...")
    mm = MemoryMap(self.file_offset, self.file_size)
    data = mm.data()
    with open("observer_api.bin", "wb") as out:
        out.write(data)
    mm.close()
