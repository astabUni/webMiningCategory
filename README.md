# webMiningCategory

This project extracts programming languages categorized by their paradigm based on categories from dbpedia via SPARQL queries and visualizes the retrieved data into a graph using graphviz. Additionally a bar chart is created by utilizing the Pandas Library. 


# Setup

## Prerequisites
* Python 3.7
* SPARQLWrapper (https://rdflib.github.io/sparqlwrapper/)
* graphviz (https://pypi.org/project/graphviz/)
* Pandas (https://pypi.org/project/pandas/)

## How to Run

* Go to the webMiningCategory folder and run
```
$ python mining.py
```
The resulting graph and bar chart will then be saved in the same folder.