import spacy
import re
import nltk
from nltk.stem import RSLPStemmer
from multiprocessing import Process
import threading
import os
import time



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


    def proccess_data_frame(self, dataFrame, targetColumns = ['PEDIDO']):
        if(not dataFrame.empty):
            for columnItem in targetColumns:
                dataFrame[columnItem] = self.apply_regex(dataFrame, column = columnItem)
                dataFrame[columnItem] = self.lemmatize_stemmer(dataFrame, columnItem)
                dataFrame[columnItem] = self.remove_stop_words(dataFrame, columnItem)
            
            self.queue_result.put(dataFrame)


    def apply_regex(self, dataFrame, column):
        dfSize = len(dataFrame)
        coluna_tmp = [0] * dfSize
        for i in range(dfSize):
            coluna_tmp[i] = dataFrame.iloc[i][column]
            letra_sem_acento = "a"
            coluna_tmp[i] = re.sub(r'([áàãâ])', letra_sem_acento, str(coluna_tmp[i]))
            letra_sem_acento = "e"
            coluna_tmp[i] = re.sub(r'([éê])', letra_sem_acento, str(coluna_tmp[i]))
            letra_sem_acento = "i"
            coluna_tmp[i] = re.sub(r'([í])', letra_sem_acento, str(coluna_tmp[i]))
            letra_sem_acento = "o"
            coluna_tmp[i] = re.sub(r'([óôõ])', letra_sem_acento, str(coluna_tmp[i]))
            letra_sem_acento = "u"
            coluna_tmp[i] = re.sub(r'([ú])', letra_sem_acento, str(coluna_tmp[i]))
            letra_sem_acento = "c"
            coluna_tmp[i] = re.sub(r'([ç])', letra_sem_acento, str(coluna_tmp[i]))
            coluna_tmp[i] = re.sub(r'[/(){}\[\]\|@,;]', '', str(coluna_tmp[i]))
            coluna_tmp[i] = re.sub(r'([/\"-.,;:º@!?&%1234567890])', '', str(coluna_tmp[i]))
        return coluna_tmp


    def lemmatize_stemmer(self, dataFrame, columnName, length = 3):
        stemmer = RSLPStemmer()
        lemmaWords = []
        for pedido in dataFrame[columnName]:
            doc = self.nlp(''.join(str(item.lower()) for item in pedido))
            temp = ''
            for token in doc:
                if len(token) > length:
                    temp = temp + ' ' + stemmer.stem(token.lemma_)
            lemmaWords.append(temp.strip())

        return lemmaWords


    def remove_stop_words(self, dataFrame, columnName):

        tam_length = len(dataFrame)
        coluna_tmp = [0] * tam_length
        for i in range(tam_length):
            phrase = []
            for word in str(dataFrame.iloc[i][columnName]).split(' '):
                if word not in self.stopwords:
                    phrase.append(word)
            coluna_tmp[i] = ' '.join(str(item) for item in phrase)
        
        return coluna_tmp
    