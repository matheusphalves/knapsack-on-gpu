import spacy
from threading import Thread
import re
import nltk
from nltk.stem import RSLPStemmer
from multiprocessing import Process
import os



class TextProcessing(Process):
    """Classe responsável por fazer o pré-processamento e geração de tokens lemmatizados para um DataFrame"""

    data_filter = None
    pID =  os.getpid()

    def run(self):
        self.log_task_id('Processo iniciado!')
        self.data_filter = self.preproccess_data_frame(self.data_filter)
        self.log_task_id('Processo finalizado!')

    def join(self):
        Process.join(self)
        return self.data_filter

    def preproccess_data_frame(self, dataFrame, targetColumns = ['PEDIDO']):
        if(not dataFrame.empty):
            for columnItem in targetColumns:
                dataFrame[columnItem] = dataFrame[columnItem].map(lambda x: x.lower())
                dataFrame[columnItem] = self.applyRegex(dataFrame, column = columnItem)
                dataFrame[columnItem] = self.filterWordsByLength(dataFrame, column = columnItem)
                dataFrame[columnItem] = self.lemmatize(dataFrame, columnItem)
                dataFrame[columnItem] = self.remove_stop_words(dataFrame, columnItem)
                dataFrame[columnItem] = dataFrame[columnItem].map(lambda x: x.lower())

                dfReturn = dataFrame.dropna(subset=targetColumns, axis=0) #remover dps
                #dfReturn.to_csv(f'tmp/perguntasProcessadas{self.thread_id}.csv')
                return dfReturn

        return None


    def applyRegex(self, dataFrame, column):
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

    def filterWordsByLength(self, dataFrame, column, length = 3):
        dfSize = len(dataFrame)
        coluna_tmp = [0] * dfSize
        for i in range(dfSize):
            str_data = dataFrame.iloc[i][column]
            tokens = str(str_data).split()
            word_tmp = ""
            for word in tokens:
                if len(word) > length:
                    word_tmp = word_tmp + " " + word
            coluna_tmp[i] = word_tmp
        return coluna_tmp

    def lemmatize(self, dataFrame, columnName):

        #self.log_task_id('Aplicando Lemmatização')
        nlp = spacy.load('pt_core_news_sm')
        lemmaWords = []
        for pedido in dataFrame[columnName]:
            doc = nlp(''.join(str(item) for item in pedido))
            temp = ''
            for token in doc:
                temp = temp + ' ' + token.lemma_
            lemmaWords.append(temp.strip())

        #self.log_task_id('Lemmatização concluída')
        return lemmaWords


    def remove_stop_words(self, dataFrame, columnName):
        #self.log_task_id('Removendo stopwords')
        tam_length = len(dataFrame)
        coluna_tmp = [0] * tam_length
        for i in range(tam_length):
            coluna_tmp[i] = self.remove_stop_words_aux(str(dataFrame.iloc[i][columnName]))
        
        #self.log_task_id('Stopwords removidas')
        return coluna_tmp

    def remove_stop_words_aux(self, sentence):
        stopwords = nltk.corpus.stopwords.words('portuguese')
        phrase = []
        for word in sentence.split(' '):
            if word not in stopwords:
                phrase.append(word)
        return ' '.join(str(item) for item in phrase)

    def log_task_id(self, message):
        print(f'[PID {self.pID}]      {message}\n')
    