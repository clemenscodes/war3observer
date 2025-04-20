from time import sleep
from war3observer.game import Game

class Observer():
  def __init__(self):
    self.game = Game()

  def observe(self):
    while True:
      self.game.dump_observer_api()
      game = self.game.read_game()
      print(game)
      sleep(1)
