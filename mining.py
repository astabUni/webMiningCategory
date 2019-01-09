from SPARQLWrapper import SPARQLWrapper, JSON
from graphviz import Graph
import re
import matplotlib.pyplot as plt
import pandas as pd


# Get dataset from dbpedia
sparql = SPARQLWrapper("http://dbpedia-live.openlinksw.com/sparql")
sparql.setReturnFormat(JSON)

sparql.setQuery("""
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dbr_cat: <http://dbpedia.org/resource/Category:>

SELECT ?paradigm ?lang where { 
    SELECT DISTINCT ?paradigm ?lang where {
        ?paradigm dct:subject/skos:broader{0,5} dbr_cat:Programming_paradigms.
        ?lang dct:subject/skos:broader{0,5} dbr_cat:Programming_languages.
        ?lang dbp:paradigm ?paradigm.  
        ?lang a dbo:ProgrammingLanguage.
        MINUS {?paradigm a dbo:Language}
        MINUS {?paradigm a dbo:ProgrammingLanguage}
		}  ORDER BY ASC(?paradigm) ASC(?lang)
	} LIMIT 100000 
	OFFSET 0
""")

dataDump = sparql.query().convert()
resultDict = {}
nodeList = []
plotDict = {}


# Prepare data for visualization
for result in dataDump["results"]["bindings"]:
	pdgm = result["paradigm"]["value"].replace("http://dbpedia.org/resource/", "").replace("_", " ").replace("-", " ").replace("programming", "").replace("language", "")
	lang = result["lang"]["value"].replace("http://dbpedia.org/resource/", "").replace("_", " ").replace("-", " ")
	reLang = re.sub(r'\([^)]*\)', '', lang)

	nodeList.append((pdgm, reLang))

	if not pdgm in resultDict:
		resultDict[pdgm] = []
	if not lang in resultDict[pdgm]:
		resultDict[pdgm].append(reLang)
	
for key, value in resultDict.items():
	if not key in plotDict:
		plotDict[key] = len(value)
	print("Paradigm: ", key,": ")
	print(value)
	print()




# Create Bar Chart with pandas
df = pd.DataFrame.from_dict(plotDict, orient='index', columns= ['#Languages'])
df.transpose()
df = df.sort_values(by='#Languages',ascending=True).nlargest(5, '#Languages')
df.plot.barh(rot=0)
plt.savefig('resultBar.png', bbox_inches='tight')



# Create graph with graphviz
resultGraph = Graph(filename='resultGraph.gv', engine='sfdp', format='png')
resultGraph.attr(overlap='false')
resultGraph.node_attr.update(color='indianred1', style='filled')

for renderMe in nodeList:
	resultGraph.edge(renderMe[0], renderMe[1])

resultGraph.render()

print("Bar Chart and Graph created!")