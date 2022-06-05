import pt_core_news_sm
import nltk
from text_processing.utils.TextProcessingUtils import TextProcessingUtils

class SingleTextProcessing():
    """Classe responsável por fazer o pré-processamento e geração de tokens lemmatizados para um DataFrame"""

    data_filter = None
    nlp = pt_core_news_sm.load()
    stopwords = nltk.corpus.stopwords.words('portuguese')

    def run(self):
        return self.proccess_data_frame(self.data_filter)

    def proccess_data_frame(self, data_frame, targetColumns = ['PEDIDO']):
        if(not data_frame.empty):
            for column_item in targetColumns:
                data_frame[column_item] = TextProcessingUtils.apply_regex(data_frame, column_item)
                data_frame[column_item] = data_frame[column_item].apply(lambda x: TextProcessingUtils.remove_stop_words(str(x).split(' '), self.stopwords))
                data_frame[column_item] = data_frame[column_item].apply(lambda x: TextProcessingUtils.lemmatize(self.nlp(''.join(str(item.lower()) for item in x))))
            
            return data_frame
    