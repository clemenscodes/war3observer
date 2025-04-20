from time import sleep
from .game import Game

class Observer():
  def __init__(self):
    self.game = Game()

  def observe(self):
    print("Observing War3StatsObserverSharedMemory")
    while True:
      print("Reading ObserverGame")
      sleep(3)
      # game = self.game.read_game()
      # sleep(1)
      # print(game)
