import logging
logging = logging.getLogger('ML_stream')

import numpy as np

from braindecode.preprocessing import (Preprocessor,
                                       exponential_moving_standardize,
                                       preprocess)

class classifier:
    '''
    Entire object of the ML algorithm processing the streamed data
    '''
    def __init__(self, high_cut=50,
                 low_cut=3,
                 factor_new=1e-3,
                 init_block_size=1000):
        '''
        Initializes classifier object with parameters, hyperparameters, 
        and preprocessing operations
        
        Parameters
        ----------
        high_cut : int, default 50
        low_cut : int, default 3
            Hz range to include; data outside this range will be removed
        factor_new : float, default 1e-3
            weight for recent points
        init_block_size : int, default 1000
            size of data block to observe
        
        Attributes
        ----------
        preprocessors : list of Preprocessor objects 
            operations to perform on the data before ML model training/evaluation
        '''
        self.high_cut = high_cut
        self.low_cut = low_cut
        self.factor_new = factor_new
        self.init_block_size = init_block_size
        
        self.preprocessors = [
            Preprocessor("pick types", eeg=True, meg=False, stim=False),
            Preprocessor(lambda data, factor: np.multiply(data, factor), factor=1e6),
            Preprocessor("filter", self.low_cut, self.high_cut),
            Preprocessor(exponential_moving_standardize, 
                         factor_new=self.factor_new, 
                         init_block_size=self.init_block_size)
            ]
    
    def preprocess(self, data):
        '''
        Perform preprocessing operations listed in self.preprocessors
        on provided data file
        
        Parameters
        ----------
        data : file object
            data to be evaluated by the algorithm
        '''
        preprocess(data, self.preprocessors, n_jobs=-1)
    
    def trial_eval(self, data, tag=None):
        '''
        Post-hoc training on game-initiating data
        
        Parameters
        ----------
        data : file object
            data to be evaluated by the algorithm
        tag : str, optional
            assign the data to a group using string tags
        '''