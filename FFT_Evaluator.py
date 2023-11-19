import numpy as np
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations
import time

# testing
from Live_Stream import Stream
import matplotlib
from matplotlib import pyplot as plt


class classifier:
    '''
    Classifies a stream's data. 
    The stream must be instantiated before passing it to this class' __init__.

    Parameters
    ----------
    stream : Stream class object
        data stream to call get_data() from and perform FFT
    '''

    def __init__(self, stream):
        '''
        Instantiates classifier class object

        Parameters
        ----------
        stream : class object
            data stream to perform FFT on
        '''
        self.stream = stream
        self.channels = stream.get_channels()

    def evaluate(self, window_size):
        '''
        On call, preprocess data and 
        Performs a bandpass 1-60Hz, then performs a FFT, then 

        Parameters
        ----------
        window_size: int
            length/size in seconds of time window to examine

        Returns
        -------
        bandpowers : arrays of tuples (float, float)
            ordered array of tuples with power and std. dev
            bands are defined with Hz ranges 0.5-4, 4-8, 8-12, 12-35, 35-60
        '''
        time.sleep(window_size)
        data = self.stream.board.get_current_board_data(
            DataFilter.get_nearest_power_of_two(self.stream.get_sample_rate()))
        # data = data / 1e6  # uV to V
        channels = self.stream.get_channels()
        
        prepped = data # preprocessed data array
        for channel in prepped:
            channel = DataFilter.perform_fft(channel,
                                              WindowOperations(2))
            #plt.plot(channel)
            #plt.show()
        bandpowers = DataFilter.get_custom_band_powers(prepped,
                                                        [(0.5, 4), (4,8), (8,12), (12,35), (35,60)],
                                                        channels,
                                                        self.stream.get_sample_rate(),
                                                        True)
        return bandpowers

'''
stream = Stream()
meka = classifier(stream)
meka.evaluate(6)
'''