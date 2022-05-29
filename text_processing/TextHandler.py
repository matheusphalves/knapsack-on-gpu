import time
import os
import pandas as pd
import nltk
from multiprocessing import Queue

from text_processing.TextProcessing import TextProcessing
class TextHandle():    

    def __init__(self) -> None:
        pd.options.mode.chained_assignment = None
        nltk.download('rslp') 
        nltk.download('wordnet')
        nltk.download('stopwords')
        self.data_filter = self.readData()
        self.queue = Queue()

        #IMPORTAÇÃO DA BASE DE DADOS 
    def readData(self, fileName = 'BaseDadosNew', extension = "csv"):  
        try:
            filepath = f'{fileName}.{extension}'
            data = pd.read_csv(filepath, sep=',')
            print(f'Quantidade de registros encontrados: {len(data)}')
            data = data.dropna()
            print(f'Quantidade de registros válidos carregados: {len(data)}')
            return data
        except:
            print.error('Falha ao ler arquivo!')
            return None

    def handle_batch_processing(self):
            
            start = time.time()
            SIZE = len(self.data_filter)
            batch_size =  int(SIZE / (os.cpu_count() / 2))
            process_list = []
            
            print(f'Lotes: {batch_size}')
            print(f'Processos a serem criados: {(os.cpu_count() / 2)}')
            previous = 0

            for sequence in range(batch_size, SIZE, batch_size):
                #print('Sequencia:' + str(sequence))
                text_process = TextProcessing()
                if(sequence + batch_size <= SIZE):
                    text_process.data_filter = self.data_filter.iloc[previous:sequence]
                    text_process.start()
                    process_list.append(text_process)
                else:
                    text_process.data_filter = self.data_filter[previous:SIZE] 
                    text_process.start()
                    process_list.append(text_process)

                previous = sequence

            print('Aguardando conclusão do processamento')
            
            
            for process in process_list:
                resultado = process.join()
                print(type(resultado))
            tempo = time.time() - start

            print(f'Tempo paralelo: {tempo}')

    def handle_single_processing(self):
            start = time.time()
            text_process = TextProcessing()
            text_process.data_filter = self.data_filter
            text_process.start()
            text_process.join()

            tempo = time.time() - start
            print(f'Tempo sequencial: {tempo}')