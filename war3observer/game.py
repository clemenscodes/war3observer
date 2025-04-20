class Game():
  refresh_rate = 2000
  # game_size = ObserverGame.sizeof()
  
  def __init__(self):
    print("Initializing game...")
    # mmap = MemoryMap(4, 4, write=True)
    # mmap.write_data(struct.pack("<I", self.refresh_rate))
    # mmap.close()
     
  # def read_game(self):
  #   self.game_mm = SharedMemoryFile(4, self.game_size)
  #   parsed = ObserverGame.parse(self.game_mm.data())
  #   del parsed._io
  #   return parsed
