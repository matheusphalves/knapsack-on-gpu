from multiprocessing import Process
from text_processing.utils.TextProcessingUtils import TextProcessingUtils

class ParallelTextProcessing(Process):
    """Classe responsável por fazer o pré-processamento e geração de tokens lemmatizados para um DataFrame"""

    data_filter = None

    def __init__(self, nlp, stopwords, queue_result) -> None:
        super().__init__()
        self.nlp = nlp
        self.stopwords = stopwords
        self.queue_result = queue_result


    def run(self):
        self.proccess_data_frame(self.data_filter)


    def proccess_data_frame(self, data_frame, targetColumns = ['PEDIDO']):
        if(not data_frame.empty):
            for column_item in targetColumns:
                data_frame[column_item] = TextProcessingUtils.apply_regex(data_frame, column_item)
                data_frame[column_item] = data_frame[column_item].apply(lambda x: TextProcessingUtils.remove_stop_words(str(x).split(' '), self.stopwords))
                data_frame[column_item] = data_frame[column_item].apply(lambda x: TextProcessingUtils.lemmatize(self.nlp(''.join(str(item.lower()) for item in x))))
            
            #Coloca data frame processado na fila
            self.queue_result.put(data_frame)
    