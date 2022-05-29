#Test your code here
from text_processing.TextHandler import TextHandle
from text_processing.TextProcessing import TextProcessing

if __name__ == '__main__':
    
    #process = TextProcessing()
    #process.start()
    #process.join()
    
    text = TextHandle()
    print('--------SEQUENCIAL--------------')
    text.handle_single_processing()
    print('-------THREAD-------------------')
    text.handle_batch_processing()
