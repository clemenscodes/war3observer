import struct
import mmap
import time

from war3structs.observer import ObserverGame

class SharedMemoryFile():
  def __init__(self, offset, size, write=False):
    self._seek_offset = offset % mmap.ALLOCATIONGRANULARITY
    self._mmap = mmap.mmap(
      -1,
      (size + self._seek_offset),
      "War3StatsObserverSharedMemory",
      offset=(offset - self._seek_offset),
      access=(mmap.ACCESS_WRITE if write else mmap.ACCESS_READ))

  def data(self):
    self._mmap.seek(self._seek_offset)
    return self._mmap.read()

  def write_data(self, data):
    self._mmap.seek(self._seek_offset)
    self._mmap.write(data)

  def close(self):
    self._mmap.close()

class Game():
  _refresh_rate = 2000
  _game_size = ObserverGame.sizeof()

  def __init__(self):
    print("Initializing game...")
    print("Game size: %s", self._game_size)
    self._game_mm = None
    print("Setting refresh rate...")
    mm = SharedMemoryFile(4, 4, write=True)
    mm.write_data(struct.pack("<I", self._refresh_rate))
    mm.close()

  def read_game(self):
    if self._game_mm is None:
      self._game_mm = SharedMemoryFile(4, self._game_size)

    parsed = ObserverGame.parse(self._game_mm.data())
    del parsed._io

    return parsed

class Server():
  def __init__(self):
    self.game = Game()

  def serve(self):
    print("Observing War3StatsObserverSharedMemory")
    while True:
      time.sleep(1)
      print("Reading ObserverGame")
      game = self.game.read_game()
      time.sleep(1)
      print(game)

def main():
  server = Server()
  server.serve()

if __name__ == 'war3observer':
  main()
