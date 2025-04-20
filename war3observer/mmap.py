import mmap

ObserverAPI = "War3StatsObserverSharedMemory"

class MemoryMap():
  def __init__(self, offset, size, write=False):
    self.offset = offset % mmap.ALLOCATIONGRANULARITY
    length = size + self.offset
    offset = offset - self.offset
    access = mmap.ACCESS_WRITE if write else mmap.ACCESS_READ
    self.mmap = mmap.mmap(-1, length, ObserverAPI, offset, access)

  def data(self):
    self.mmap.seek(self.offset)
    return self.mmap.read()

  def write_data(self, data):
    self.mmap.seek(self.offset)
    self.mmap.write(data)

  def close(self):
    self.mmap.close()
