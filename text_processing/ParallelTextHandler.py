import multiprocessing
import time
import os
import pandas as pd
import nltk
from text_processing.ParallelTextProcessing import ParallelTextProcessing
from text_processing.DataFrameUtils import DataFrameUtils

class ParallelTextHandler():    

    def __init__(self, data_frame) -> None:
        pd.options.mode.chained_assignment = None
        nltk.download('rslp') 
        nltk.download('wordnet')
        nltk.download('stopwords')
        self.data_filter = data_frame


    def handle_batch_processing(self):
            
            start = time.time()
            SIZE = len(self.data_filter)
            batch_size =  int(SIZE / (os.cpu_count()))
            process_list = []
            
            print(f'Linhas por lote: {batch_size}')
            print(f'Processos a serem criados: {int(os.cpu_count())}')
            previous = 0

            for sequence in range(batch_size, SIZE, batch_size):

                text_process = ParallelTextProcessing()

                if(sequence + batch_size <= SIZE):
                    text_process.data_filter = self.data_filter[previous:sequence]
                    
                else:
                    text_process.data_filter = self.data_filter[previous:SIZE] 

                previous = sequence
                text_process.start()
                process_list.append(text_process)
            
            data_frame = pd.DataFrame()
            for process in process_list: 
                process.join()
            
            tempo = time.time() - start
            print(f'Tempo paralelo: {tempo}')

            DataFrameUtils.save_data_frame(data_frame=data_frame, execution_type='paralela')
