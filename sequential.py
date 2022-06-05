#Test your code here
from text_processing.handlers.SingleTextHandler import SingleTextHandler
from text_processing.utils.DataFrameLoader import DataFrameLoader

if __name__ == '__main__':
    

    print('-------LENDO CSV-------------------')
    data_frame = DataFrameLoader.read_data('sample data/BaseDados_20k')

    print('--------EXECUÇÃO SEQUENCIAL--------------')
    sequencial = SingleTextHandler(data_frame)
    sequencial.handle_single_processing()
