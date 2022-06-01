from text_processing.exceptions.ExecutionException import ExecutionException
import pandas as pd
import os


class DataFrameUtils():
    """Classe possui métodos utilitários para manipulação de DataFrames"""

    #IMPORTAÇÃO DA BASE DE DADOS 
    @staticmethod
    def read_data(fileName = 'BaseDadosNew', extension = "csv"):  
            try:
                filepath = f'{fileName}.{extension}'
                data = pd.read_csv(filepath, sep=',', skipinitialspace = True, usecols = ['PEDIDO'])
                print(f'Quantidade de registros encontrados: {len(data)}')
                data = data.dropna()
                print(f'Quantidade de registros válidos carregados: {len(data)}')
                print(data.columns)
                return data[['PEDIDO']]
            except Exception as ex:
                raise ExecutionException(f'Falha ao ler arquivo\n {str(ex)}')


    @staticmethod
    def save_data_frame(data_frame, execution_type):
            
        path = 'tmp/'

        try:
            os.mkdir(path)
        except:
                #Diretório já existe...
            pass

        if(not data_frame.empty):
            print(f'Salvando resultados da execução {execution_type}')
            data_frame.to_csv(f'{path}/texto_processado_{execution_type}.csv')