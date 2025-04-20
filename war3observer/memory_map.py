import mmap

ObserverAPI = "War3StatsObserverSharedMemory"

class MemoryMap():
  def __init__(self, offset, size, write=False):
    self.offset = offset
    self.granularity = mmap.ALLOCATIONGRANULARITY
    self.aligned_offset = (self.offset // self.granularity) * self.granularity
    self.seek_offset = self.offset - self.aligned_offset
    self.total_size = size + self.seek_offset
    self.access = mmap.ACCESS_WRITE if write else mmap.ACCESS_READ
    self._mmap = mmap.mmap(-1, self.total_size, ObserverAPI, self.access, self.aligned_offset)

  def data(self):
    self._mmap.seek(self.offset)
    return self._mmap.read()

  def write_data(self, data):
    self._mmap.seek(self.offset)
    self._mmap.write(data)

  def close(self):
    self._mmap.close()

