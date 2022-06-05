
#Test your code here
from text_processing.handlers.ParallelTextHandler import ParallelTextHandler
from text_processing.utils.DataFrameLoader import DataFrameLoader

if __name__ == '__main__':


    print('-------LENDO CSV-------------------')
    data_frame = DataFrameLoader.read_data('sample data/BaseDados_20k')

    print('-------EXECUÇÃO PARALELA-------------------')
    paralelo = ParallelTextHandler(data_frame)
    paralelo.handle_batch_processing()