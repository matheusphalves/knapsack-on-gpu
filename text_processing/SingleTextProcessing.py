import pt_core_news_sm
import re
import nltk
from nltk.stem import RSLPStemmer



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
                data_frame[column_item] = self.apply_regex(data_frame, column_item)
                data_frame[column_item] = data_frame[column_item].apply(lambda x: self.remove_stop_words(str(x).split(' ')))
                data_frame[column_item] = data_frame[column_item].apply(lambda x: self.lemmatize_stemmer(self.nlp(''.join(str(item.lower()) for item in x))))
            
            return data_frame


    def apply_regex(self, dataFrame, column):
        dfSize = len(dataFrame)
        coluna_tmp = [0] * dfSize
        for i in range(dfSize):
            coluna_tmp[i] = dataFrame.iloc[i][column]
            coluna_tmp[i] = re.sub(r'([áàãâ])', 'a', str(coluna_tmp[i]))
            coluna_tmp[i] = re.sub(r'([éê])', 'e', str(coluna_tmp[i]))
            coluna_tmp[i] = re.sub(r'([í])', 'i', str(coluna_tmp[i]))
            coluna_tmp[i] = re.sub(r'([óôõ])', 'o', str(coluna_tmp[i]))
            coluna_tmp[i] = re.sub(r'([ú])', 'u', str(coluna_tmp[i]))
            coluna_tmp[i] = re.sub(r'([ç])', 'c', str(coluna_tmp[i]))
            coluna_tmp[i] = re.sub(r'[/(){}\[\]\|@,;]', '', str(coluna_tmp[i]))
            coluna_tmp[i] = re.sub(r'(["-.,;:º@!?&%1234567890])', '', str(coluna_tmp[i]))
        return coluna_tmp


    def lemmatize_stemmer(self, str_data_frame, length = 3):
        stemmer = RSLPStemmer()
        temp = ''
        for token in str_data_frame:
            if len(token) > length:
                temp = temp + ' ' + stemmer.stem(token.lemma_).strip()
        return temp


    def remove_stop_words(self, str_data_frame):
        phrase = []
        for word in str_data_frame:
            if word not in self.stopwords:
                phrase.append(word)
        return ' '.join(str(item) for item in phrase)
    