import pong as pong
import threading
import time
import random
# import ML part
import sys
sys.path.append('../Seamless')
from ..FFT_Evaluator import classifier

def callibration():
    pong.ball_speed = 4
    pong.difficulty = "easy"
    pong.main(10)

    time.sleep(5)

    pong.ball_speed = 9
    pong.difficulty = "hard"
    pong.main(10)

    time.sleep(5)


def difficulty_level():
    #   ML_thread = threading.Thread(target=ML)
    #   ML_thread.start()
    #   ML.main()

    pong.difficulty = "normal"
    while pong.running:
        # pong.difficulty = ML.get_frustration()
        if pong.difficulty == "easy":
            if pong.ball_speed >= 1:
                pong.ball_speed = pong.ball_speed + 0.5 * -3
        if pong.difficulty == "hard":
            pong.ball_speed = pong.ball_speed + 0.5 * 3

        print(pong.ball_speed)
        pong.difficulty = random.choice(["easy", "hard"])
        time.sleep(2)


# Start the background task in a separate thread
callibration()
difficulty_thread = threading.Thread(target=difficulty_level)
difficulty_thread.start()

# Run the Pygame loop on the main thread
pong.main(10)

# Wait for the background task to finish
difficulty_thread.join()
