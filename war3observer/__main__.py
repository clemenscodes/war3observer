from war3observer import __version__
from .observer import Observer

# from war3structs.observer import ObserverGame
#
# ObserverAPI = "War3StatsObserverSharedMemory"
#
# class SharedMemoryFile():
#   def __init__(self, offset, size, write=False):
#     self._seek_offset = offset % mmap.ALLOCATIONGRANULARITY
#     length = size + self._seek_offset
#     offset = offset - self._seek_offset
#     access = mmap.ACCESS_WRITE if write else mmap.ACCESS_READ
#     self._mmap = mmap.mmap(-1, length, ObserverAPI, offset, access)
#
#   def data(self):
#     self._mmap.seek(self._seek_offset)
#     return self._mmap.read()
#
#   def write_data(self, data):
#     self._mmap.seek(self._seek_offset)
#     self._mmap.write(data)
#
#   def close(self):
#     self._mmap.close()

def main():
  observer = Observer()
  observer.observe()

if __name__ == '__main__':
  main()
