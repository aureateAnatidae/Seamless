import numpy as np
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations
import time

#testing 
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
        bands : list of tuples containing str, float
            ordered list of tuples with band name and frequency band magnitude
        '''
        time.sleep(window_size)
        data = self.stream.get_data()
        #data = data / 1e6  # uV to V
        
        for channel in self.channels:
            DataFilter.perform_bandpass(data[channel],
                                        self.stream.get_sample_rate(),
                                        start_freq=1.0, 
                                        stop_freq=60.0,
                                        order=3,
                                        filter_type=FilterTypes.BUTTERWORTH,
                                        ripple=0
                                        )
            fft_data = data[channel]
            #print(fft_data)
            plt.plot(fft_data)
            plt.show()
            fft_data = DataFilter.perform_fft(data[channel],
                                              WindowOperations(2))
            print(fft_data)
            plt.plot(fft_data)
            plt.show()
        
stream = Stream()
meka = classifier(stream)
meka.evaluate(5)