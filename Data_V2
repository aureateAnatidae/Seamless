from brainflow.board_shim import BoardShim, BoardIds, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes
import numpy as np
import matplotlib.pyplot as plt
import time

params = BrainFlowInputParams()
params.serial_port = "COM3"
board_id = BoardIds.GANGLION_BOARD.value
print(board_id)

try:
    assert board_id == BoardIds.GANGLION_BOARD.value
    board = BoardShim(board_id, params)
    board.prepare_session()
    print("Successfully prepared physical board.")
except Exception as e:
    print(e)
    
    print("Device could not be found or is being used by another program, creating synthetic board.")
    board_id = BoardIds.SYNTHETIC_BOARD
    board = BoardShim(board_id, params)
    board.prepare_session()
    
board.release_session()

print("Starting Stream")
board.prepare_session()
board.start_stream()
time.sleep(5) #Wait 5 seconds
data = board.get_board_data()
print("Ending Stream")
board.stop_stream()
board.release_session()

#Isolate EEG data
eeg_channels = board.get_eeg_channels(board_id)
print(eeg_channels)
eeg_data = data[eeg_channels]
print(eeg_data.shape)

print(eeg_data)

#Plot the first EEG Channel
plt.plot(np.arange(eeg_data.shape[1]), eeg_data[0])
