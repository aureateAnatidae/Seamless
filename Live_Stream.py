from brainflow.board_shim import BoardShim, BoardIds, BrainFlowInputParams
import numpy as np  # Import numpy for array handling
import time

class Stream:
    '''
    Streaming object returning data from BoardShim on method get_data() call
    '''
    def __init__(self):
        params = BrainFlowInputParams()
        params.serial_port = "COM3"  # Change this to the appropriate port
        board_id = BoardIds.GANGLION_BOARD.value
        self.board = BoardShim(board_id, params)
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

def run_stream():
    with Stream() as streaming_obj:
        try:
            # Start streaming data
            while True:
                # Get data from the OpenBCI board
                time.sleep(1)
                data = streaming_obj.get_data()
                # Check if data is non-empty (has elements)
                if isinstance(data, np.ndarray) and data.size > 0:
                    print(data, end='\r')  # Print data without newline to overwrite previous output

                

        except KeyboardInterrupt:
            pass  

if __name__ == "__main__":
    run_stream()
    
