from rdflib import Graph, URIRef, Namespace, RDF, RDFS, Literal, BNode

# Definir namespaces
dcat = Namespace("http://www.w3.org/ns/dcat#")

# Criar um grafo RDF
g = Graph()
g.bind("dcat", dcat)

# URI do dataset
dataset_uri = URIRef("http://example.org/dataset/1")

# Lista de palavras-chave
keywords = ["tagA", "tagB", "tagC"]

# Criar uma string com a formatação desejada
keywords_str = ', '.join([f'"{tag}"' for tag in keywords])

# Adicionar a string ao grafo
g.add((dataset_uri, dcat["keywords"], Literal(keywords_str)))

# Serializar o grafo para o formato Turtle
turtle_data = g.serialize(format="turtle").replace('\\"', '"').replace('""', '"')



# Imprimir o resultado limpo
print(turtle_data)
