from brainflow.board_shim import BoardShim, BoardIds, BrainFlowInputParams


class stream:
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
        params = BrainFlowInputParams()
        params.serial_port = "COM3"
        board_id = BoardIds.GANGLION_BOARD.value
        self.board = BoardShim(board_id, params)
        self.board.prepare_session()
        self.board.start_stream()

    def get_data(self):
        data = self.board.get_board_data()
        return data