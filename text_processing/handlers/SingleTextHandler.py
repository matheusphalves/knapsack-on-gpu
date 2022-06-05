from datetime import datetime
import pandas as pd
import nltk
from text_processing.workers.SingleTextProcessing import SingleTextProcessing
from text_processing.utils.DataFrameLoader import DataFrameLoader

class SingleTextHandler():    
    """Classe responsável por lidar com a execução sequêncial do processamento de texto"""

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
        start = datetime.now()
        data_frame = text_process.run()
        tempo = datetime.now() - start
        print(f'Tempo sequencial: {tempo.seconds} (s)')
        DataFrameLoader.save_data_frame(data_frame=data_frame, execution_type='sequencial')
