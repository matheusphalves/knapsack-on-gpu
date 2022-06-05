# Parallel Text Processing

Using concurrent Processes to improve processing time for a large amount of text data.

This project implement the first step (text processing) of a text classifier engine; mostly used on data mining applications. We thougth in to write a paralllel version using ```multiprocessing.Process``` package.

Running this code, you are able to
- Remove noisy data
- Apply the lemmatization process
- Standardize text for binarization phase

# Pipeline of textual data mining
1. Initial Pre processing (this code);
2. Token's extraction from dirty data (this code);
3. Data grouping according the main delimitor;
4. Token's binarization;
5. Split data into training and test units;
6. Training using the proper algorithm such as Decision Tree's algorithm family.

# Dependency requirements 

```
spacy
pandas
nltk
```

# How to run

Please run the following commands

- pip install -r requirements.txt
- python -m spacy download pt_core_news_sm


# Project structure

```
project/
	text_processing/
		exceptions/
                	ExecutionException.py
          	handlers/
			ParallelTextHandler.py
			SingleTextHandler.py
		utils/
			DataFrameLoader.py
			TextProcessingUtils.py
		workers/
			ParallelTextProcessing.py
			SingleTextProcessing.py
          
	requirements.txt
    	sequential.py
    	parallel.py
	.gitignore
```

# Class description

## Handlers

```SingleTextHandler```: Invokes the sequential text processing algorithm.

```ParalellTextHandler```: Invokes the parallel text processing algorithm. Also, create a queue to retrive all processed data from workers. The original data frame is split into multiple batches evenly.


## Workers

```SingleTextProcessing```: Implements the sequential version of text pre processing and tokens generation algorithm.


```ParallelTextProcessing```: Implements the parallel version of text pre processing and tokens generation algorithm.

## Utilitaries

```DataFrameLoader```: Class of methods used for creation and persistence of DataFrames objects.

```TextProcessingUtils```: Class has textual properties for preprocessing such as removing noisy data and applying the lemmatization process. 



# Parallel concept walkthough

![Multiprocessing workers](https://snipboard.io/ylpY2s.jpg)


# Comparison sequential and parallel execution

In order to validate the developed algorithm, a comparison was made between the sequential and parallel execution time using 3 documents of different sizes: 5,000, 10,000 and another with 20,000 records. The following machines were available for the test battery:

|    | CPU            | Cores / Threads | OS     | RAM  | PYTHON VERSION |
| -- | -------------- | ----------------------- | ------ | ---- | ------ |
| M1 | Core i5-10210U | 4/8                     | WIN 10 | 8GB  | 3.9.5  |
| M2 | Ryzen 3200G    | 4/4                     | WIN 10 | 16GB | 3.9.4  |
| M3 | Core i5-8250U  | 4/8                     | WIN 10 | 16GB | 3.10.4 |

From then on, the algorithm in its sequential and parallel versions were executed in isolation in order to avoid any interference such as context switching due to execution overhead. For each machine, the respective time values were recorded:

| DATA AMOUNT | SEQUENTIAL (seconds) ||| PARALLEL (seconds) |||
|----------------|-----|-----|-----|-----|-----|----|
|                | M1  | M2  | M3  | M1 | M2  | M3 |
| 5000           | 83  | 72  | 88  | 48 | 40  | 40 |
| 10000          | 112 | 146 | 188 | 71 | 65  | 85 |
| 20000          | 197 | 293 | 396 | 97 | 112 | 96 |




