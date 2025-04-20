from war3observer import __version__
from war3observer.observer import Observer

def main():
  print("war3observer", __version__)
  observer = Observer()
  observer.observe()

if __name__ == '__main__':
  main()
