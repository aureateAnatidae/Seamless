from brainflow.board_shim import BoardShim, BoardIds, BrainFlowInputParams
import numpy as np  # Import numpy for array handling
import time

class Stream:
    '''
    Streaming object returning data from BoardShim on method get_data() call
    PLEASE CALL WITH
    ```
    with stream as stream()
        //such a function
    -> automatic closed
    ```
    
    Attributes
    ----------
    params : ???
        set of parameters required for the OpenBCI to connect
    params.serial_port : str
        computer port to access the OpenBCI ganglion hardware - changes based on computer and OS
    board_id : int
        ganglion hardware ID
    '''
    def __init__(self):
        self.params = BrainFlowInputParams()
        self.params.serial_port = "/dev/ttyACM0"  # Change this to the appropriate port
        self.board_id = BoardIds.GANGLION_BOARD.value
        self.board = BoardShim(self.board_id, self.params)
        self.board.prepare_session()
        self.board.start_stream()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.board.stop_stream()
        self.board.release_session()

    def get_data(self):
        data = self.board.get_board_data()
        return data
    
    def get_2048_flashes(self):
        return self.board.get_current_board_data(2048)
    
    def get_sample_rate(self):
        return self.board.get_sampling_rate(self.board_id)
    
    def get_board_id(self):
        return self.board_id
    
    def get_channels(self):
        return self.board.get_eeg_channels(self.board_id)

def run_stream():
    with Stream() as streaming_obj:
        # Start streaming data
        # with Class automatically calls __exit__ on leaving context scope
        # no need to use try: except: especially since we want to release session on other exceptions too
        # to release all sessions, call release_all_sessions()
        while True:
            # Get data from the OpenBCI board
            time.sleep(1)
            data = streaming_obj.get_data()
            # Check if data is non-empty (has elements)
            if isinstance(data, np.ndarray) and data.size > 0:
                print(data, end='\r')  # Print data without newline to overwrite previous output


if __name__ == "__main__":
    run_stream()
    
