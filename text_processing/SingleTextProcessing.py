import pt_core_news_sm
import spacy
import re
import nltk
from nltk.stem import RSLPStemmer
import os



class SingleTextProcessing():
    """Classe responsável por fazer o pré-processamento e geração de tokens lemmatizados para um DataFrame"""

    data_filter = None
    pID =  os.getpid()
    nlp = pt_core_news_sm.load()

    def run(self):
        self.log_task_id('Sequencial iniciado!')
        data_frame = self.proccess_data_frame(self.data_filter)
        self.log_task_id('Sequencial finalizado!')
        return data_frame

    def proccess_data_frame(self, dataFrame, targetColumns = ['PEDIDO']):
        if(not dataFrame.empty):
            for columnItem in targetColumns:
                dataFrame[columnItem] = dataFrame[columnItem].map(lambda x: x.lower())
                dataFrame[columnItem] = self.apply_regex(dataFrame, column = columnItem)
                dataFrame[columnItem] = self.filter_words_by_length(dataFrame, column = columnItem)
                dataFrame[columnItem] = self.lemmatize(dataFrame, columnItem)
                dataFrame[columnItem] = self.stemmer(dataFrame, columnItem)
                dataFrame[columnItem] = self.remove_stop_words(dataFrame, columnItem)
                dataFrame[columnItem] = dataFrame[columnItem].map(lambda x: x.lower())
            
            return dataFrame


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

    def filter_words_by_length(self, dataFrame, column, length = 3):
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
        
        lemmaWords = []
        for pedido in dataFrame[columnName]:
            doc = self.nlp(''.join(str(item) for item in pedido))
            temp = ''
            for token in doc:
                temp = temp + ' ' + token.lemma_
            lemmaWords.append(temp.strip())

        return lemmaWords

    def stemmer(self, dataFrame, columnName):

        stemmer = RSLPStemmer()
        tam_length = len(dataFrame)
        coluna_tmp = [0] * tam_length
        for i in range(tam_length):
            doc = self.nlp(str(dataFrame.iloc[i][columnName]))
            tokens = doc.text.split()
            temp = ""
            for token in tokens:
                if token != "nan":
                    temp = temp + " " + stemmer.stem(token)

            coluna_tmp[i] = temp.strip()
        return coluna_tmp


    def remove_stop_words(self, dataFrame, columnName):
        tam_length = len(dataFrame)
        coluna_tmp = [0] * tam_length
        for i in range(tam_length):
            coluna_tmp[i] = self.remove_stop_words_aux(str(dataFrame.iloc[i][columnName]))
        
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
    