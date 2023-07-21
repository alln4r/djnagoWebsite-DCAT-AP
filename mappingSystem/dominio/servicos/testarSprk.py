from rdflib.namespace import FOAF
from rdflib import Graph
from rdflib.namespace import DC, RDF, XSD
# g = Graph()
# g.parse("http://xmlns.com/foaf/0.1/")

# for s, p, o in g.triples((None, None, None)):
#    if p == RDF.type:
#        print(s)


# for term in FOAF:
#    print(term)


from rdflib import Graph, RDF

# List of namespaces
namespaces = {
    "DCTERMS": "http://purl.org/dc/terms/",
    "FOAF": "http://xmlns.com/foaf/0.1/",
    "SKOS": "http://www.w3.org/2004/02/skos/core#",
    "Schema.org": "http://schema.org/",
    "PROV-O": "http://www.w3.org/ns/prov#",
    # Adicione os demais namespaces aqui
}

# Selected namespace
selected_namespace = "PROV-O"

# Get the URI of the selected namespace
namespace_uri = namespaces[selected_namespace]

# Create an RDFLib graph
g = Graph()

# Parse the RDF data from a file or URL
g.parse(namespace_uri)

# Iterate over the triples and filter by the selected namespace
terms = set()
for s, p, o in g.triples((None, RDF.type, None)):
    if str(s).startswith(namespace_uri):
        # terms.add(s)
        terms.add(s.lstrip(namespace_uri))

# Print the terms (properties) in the selected namespace
print(f"Properties in the namespace '{selected_namespace}':")
for term in terms:
    print(term)
