from src import __main__
import time

# Run the code every 6 hours

if __name__ == "__main__":
  print("-"*80 + "\nWindy API Accessor\n" + "-"*80)

  while True:
    __main__.main()
    
    time.sleep(60 * 60 * 6)