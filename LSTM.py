# text generation model

import re
import csv
import string
import pickle
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
import tensorflow.keras.utils 

'''
https://machinelearningmastery.com/text-generation-with-lstm-in-pytorch/
https://www.kaggle.com/code/ilhansevval/text-generation-with-lstm-and-n-gram-sequences

'''
from data_api import DataAPI


# TODO
