from src import __main__
import time

# Run the code every 6 hours

if __name__ == "__main__":
    __main__.main()
    # 60 seconds
    # *
    # 60 minutes
    # *
    # 6 hours
    time.sleep(60 * 60 * 6)