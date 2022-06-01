import multiprocessing
import time
import os
import pandas as pd
import nltk
import pt_core_news_sm
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
            
            
            SIZE = len(self.data_filter)
            batch_size =  int(SIZE / (os.cpu_count()))
            process_list = []
            
            print(f'Linhas por lote: {batch_size}')
            print(f'Processos em execução: {int(os.cpu_count())}')
            previous = 0
            nlp = pt_core_news_sm.load()
            stopwords = nltk.corpus.stopwords.words('portuguese')
            queue_result = multiprocessing.Manager().Queue()
            start = time.time()
            for sequence in range(batch_size, SIZE, batch_size):

                text_process = ParallelTextProcessing(nlp=nlp, stopwords=stopwords, queue_result = queue_result)

                if(sequence + batch_size <= SIZE):
                    text_process.data_filter = self.data_filter[previous:sequence]
                    
                else:
                    text_process.data_filter = self.data_filter[previous:SIZE] 

                previous = sequence
                text_process.start()
                process_list.append(text_process)
            
            for process in process_list: 
                process.join()
            tempo = time.time() - start
            print(f'Tempo paralelo: {tempo}')

            result_df = pd.DataFrame()
            for process in process_list:
                print('Obtendo resultados de um processo')
                result_df = result_df.append(queue_result.get(timeout = 5))


            DataFrameUtils.save_data_frame(data_frame=result_df, execution_type='paralela')
