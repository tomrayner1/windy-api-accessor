from src import __main__
import time

# Run the code every 4 hours

if __name__ == "__main__":
  while True:
    __main__.main()
    
    time.sleep(60 * 60 * 4)