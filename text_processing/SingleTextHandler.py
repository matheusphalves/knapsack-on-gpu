import time
import pandas as pd
import nltk
from text_processing.SingleTextProcessing import SingleTextProcessing
from text_processing.DataFrameUtils import DataFrameUtils

class SingleTextHandler():    

    def __init__(self, data_frame) -> None:
        pd.options.mode.chained_assignment = None
        nltk.download('rslp') 
        nltk.download('wordnet')
        nltk.download('stopwords')
        self.data_filter = data_frame


    def handle_single_processing(self):
            print("Iniciando execução sequencial!")
            text_process = SingleTextProcessing()
            text_process.data_filter = self.data_filter
            start = time.time()
            data_frame = text_process.run()
            tempo = time.time() - start
            print(f'Tempo sequencial: {tempo}')
            DataFrameUtils.save_data_frame(data_frame=data_frame, execution_type='sequencial')
