import mmap

class MemoryMap():
  """MemoryMap class

  This opens a memory mapped file at the specified offset with the
  specified size, but takes care of having the offset conform to the
  ALLOCATIONGRANULARITY for you. Read the entire file with the data()
  method.
  """

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

