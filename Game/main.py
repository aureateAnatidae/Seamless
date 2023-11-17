import pong as pong
import threading
import time


def change_difficulty_later():
    pong.difficulty = "hard"
    time.sleep(5)
    pong.difficulty = "easy"


# Start the background task in a separate thread
difficulty_thread = threading.Thread(target=change_difficulty_later)
difficulty_thread.start()

# Run the Pygame loop on the main thread
pong.main(100)

# Wait for the background task to finish
difficulty_thread.join()
