
#Test your code here
from text_processing.ParallelTextHandler import ParallelTextHandler
from text_processing.DataFrameUtils import DataFrameUtils

if __name__ == '__main__':


    print('-------LENDO CSV-------------------')
    data_frame = DataFrameUtils.read_data()

    print('-------EXECUÇÃO PARALELA-------------------')
    paralelo = ParallelTextHandler(data_frame)
    paralelo.handle_batch_processing()