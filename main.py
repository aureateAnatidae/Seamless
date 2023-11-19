import pong as pong
import threading
import time
import random
# import ML part
from Live_Stream import Stream
from FFT_Evaluator import classifier

def callibration(evaluator):
    pong.ball_speed = 4
    pong.difficulty = "easy"
    pong.main(10)
    eeg_score = evaluator.evaluate(10)
    easy_AG_ratio = eeg_score[0][0] / eeg_score[0][4]
    print(easy_AG_ratio)

    pong.ball_speed = 9
    pong.difficulty = "hard"
    pong.main(10)
    eeg_score = evaluator.evaluate(10)
    hard_AG_ratio = eeg_score[0][0] / eeg_score[0][4]
    print(hard_AG_ratio)

    return easy_AG_ratio + hard_AG_ratio / 2    # the average is used
                                                  


def difficulty_level(evaluator, average):
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
        eeg_score = evaluator.evaluate(2)
        AG_ratio = eeg_score[0][0] / eeg_score[0][4]  # alpha gamma ratio
        print(AG_ratio)
        pong.difficulty = "hard" if AG_ratio < average else "easy"
        time.sleep(2)


# Start the stream connecting the Ganglion before opening game
stream = Stream()
# EEG evaluator object
evaluator = classifier(stream)
# Start the background task in a separate thread
avg = callibration(evaluator)
difficulty_thread = threading.Thread(target=difficulty_level(evaluator, avg))
difficulty_thread.start()

# Run the Pygame loop on the main thread
pong.main(10)

# Wait for the background task to finish
difficulty_thread.join()
