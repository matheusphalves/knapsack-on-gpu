import time
import os
import pandas as pd
import nltk
import multiprocessing

from text_processing.TextProcessing import TextProcessing
from text_processing.exceptions.ExecutionException import ExecutionException
class TextHandler():    

    def __init__(self) -> None:
        pd.options.mode.chained_assignment = None
        nltk.download('rslp') 
        nltk.download('wordnet')
        nltk.download('stopwords')
        self.data_filter = self.read_data()

    #IMPORTAÇÃO DA BASE DE DADOS 
    def read_data(self, fileName = 'BaseDados', extension = "csv"):  
        try:
            filepath = f'{fileName}.{extension}'
            data = pd.read_csv(filepath, sep=',')
            print(f'Quantidade de registros encontrados: {len(data)}')
            data = data.dropna()
            print(f'Quantidade de registros válidos carregados: {len(data)}')
            return data
        except Exception as ex:
            raise ExecutionException(f'Falha ao ler arquivo\n {str(ex)}')

    def handle_batch_processing(self):
            
            start = time.time()
            SIZE = len(self.data_filter)
            batch_size =  int(SIZE / (os.cpu_count() / 2))
            process_list = []
            
            print(f'Linhas por lote: {batch_size}')
            print(f'Processos a serem criados: {int(os.cpu_count() / 2)}')
            previous = 0

            data_frame = multiprocessing.Manager().Value('data_frame', pd.DataFrame())
            lock = multiprocessing.Lock()

            for sequence in range(batch_size, SIZE, batch_size):

                text_process = TextProcessing(lock = lock, args=("Process", data_frame, lock))

                if(sequence + batch_size <= SIZE):
                    text_process.data_filter = self.data_filter.iloc[previous:sequence]
                    text_process.start()
                    process_list.append(text_process)
                else:
                    text_process.data_filter = self.data_filter[previous:SIZE] 
                    text_process.start()
                    process_list.append(text_process)

                previous = sequence
            

            
            for process in process_list:
                resultado = process.join()
                data_frame = data_frame.append(resultado)

            tempo = time.time() - start
            print(f'Tempo paralelo: {tempo}')

            self.save_data_frame(data_frame=data_frame, execution_type='paralela')

    def handle_single_processing(self):
            start = time.time()
            data_frame = multiprocessing.Manager().Value('data_frame', pd.DataFrame())
            lock = multiprocessing.Lock()
            text_process = TextProcessing(lock = lock, args=("Process", data_frame, lock))
            text_process.data_filter = self.data_filter
            text_process.start()
            data_frame = text_process.join()
            tempo = time.time() - start
            print(f'Tempo sequencial: {tempo}')

            self.save_data_frame(data_frame=data_frame, execution_type='sequencial')

            

    def save_data_frame(self, data_frame, execution_type):
        
        path = 'tmp/'

        try:
            os.mkdir(path)
        except:
            #Diretório já existe...
            pass

        if(not data_frame.empty):
            print(f'Salvando resultados da execução {execution_type}')
            data_frame.to_csv(f'{path}/texto_processado_{execution_type}.csv')
