#Test your code here
from text_processing.TextHandler import TextHandler

if __name__ == '__main__':
    
    text = TextHandler()
    print('--------SEQUENCIAL--------------')
    text.handle_single_processing()
    print('-------PARALELO-------------------')
    text.handle_batch_processing()
