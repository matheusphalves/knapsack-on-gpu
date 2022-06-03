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
          DataFrameUtils.py
          ParalellTextHandler.py
          ParalelllTextProcessing.py
          SingleTextHandler.py
          SingleTextProcessing.py
          
		requirements.txt
    sequential.py
    parallel.py
		.gitignore
```

# Class description

## Handlers

```SingleTextHandler```

Description...

```ParalellTextHandler```

Description...


## Workers

```SingleTextProcessing```

Description...

```ParallelTextProcessing```

Description...

## Utilitaries

```DataFrameUtils```

Description...


# Parallel conceptr walkthough

![Multiprocessing workers](https://snipboard.io/ylpY2s.jpg)


# Comparison sequential and parallel execution
working...
