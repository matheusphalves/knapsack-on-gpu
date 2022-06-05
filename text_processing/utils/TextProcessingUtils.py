import re
from nltk.stem import RSLPStemmer
from pandas import DataFrame

class TextProcessingUtils():
    """Classe possui métodos utilitários para o pré processamento textual"""
    
    @staticmethod
    def apply_regex(dataFrame: DataFrame, column):
        """Remove caracteres especiais e acentuações de cada linha do dataframe."""

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

    @staticmethod
    def lemmatize(str_data_frame:str, length = 3):
        """Aplica o processo de lematização"""
        stemmer = RSLPStemmer()
        temp = ''
        for token in str_data_frame:
            if len(token) > length:
                temp = temp + ' ' + stemmer.stem(token.lemma_).strip()
        return temp

    @staticmethod
    def remove_stop_words(str_data_frame:str, stopwords):
        """Remove as stopwords de uma sequencia textual. São removidos artigos, 
        preposições e entre outras palavras que não agregam significado semântico."""

        phrase = []
        for word in str_data_frame:
            if word not in stopwords:
                phrase.append(word)
        return ' '.join(str(item) for item in phrase)