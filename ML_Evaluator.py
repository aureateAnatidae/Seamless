import logging
logging = logging.getLogger('ML_stream')

import numpy as np
import time

from braindecode.preprocessing import (Preprocessor,
                                       exponential_moving_standardize,
                                       preprocess,
                                       create_windows_from_events)
import asyncio
#import livedata.xdf, easydata.xdf, mediumdata.xdf <- WRITE DATA IN THIS ROOT FOLDER

class classifier:
    '''
    Entire object of the ML algorithm processing the streamed data
    '''
    def __init__(self, high_cut=55,
                 low_cut=1,
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
        self.window_size : int, start at 0.5
        self.last_eval_time : int, start at 0
            integers determining how long into the past to evaluate when
            live_eval is called
        
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
        self.window_size = 0
        self.last_eval_time = time.time()
    
    def preprocess(self, data):
        '''
        Perform preprocessing operations listed in self.preprocessors
        on provided data file
        
        Parameters
        ----------
        data : file object
            data to be evaluated by the algorithm
            
        Returns
        -------
        prepped_data : BaseConcatDataset object
            data that has undergone preprocessing operations in .mne or .epoch
        '''
        prepped_data = preprocess(data, self.preprocessors, n_jobs=-1)
        return prepped_data
    
    def live_eval(self, data, dataset, tag=None):
        '''
        Live post-hoc (yes) training on game-initiating data
        Generates window from window_size (time from last evaluation), 
        async evaluation on the timespan window_size
        
        Parameters
        ----------
        data : file object
            data to be evaluated by the algorithm
        dataset : file objects
            old data to compare new data to
        tag : str, optional
            assign the data to a group using string tags
            
        Attributes
        ----------
        window_size : int
            determines how large of a time window to evaluate
        last_eval_time : int
            last time the data was evaluated
        '''
        self.window_size = time.time() - self.last_eval_time()
        self.last_eval_time = time.time()
        self.sfreq = dataset.datasets[0].raw.info["sfreq"]
        assert all([ds.raw.info["sfreq"] == sfreq for ds in dataset.datasets])
        trial_start_offset_samples = int(self.window_size*sfreq)
        
        windows_dataset = create_windows_from_events(
            dataset,
            trial_start_offset_samples=trial_start_offset_samples,
            trial_stop_offset_samples=0,
            preload=True
        )
        
        
        
        
        
        
        