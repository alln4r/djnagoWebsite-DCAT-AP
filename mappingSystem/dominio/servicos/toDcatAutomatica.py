import json
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD
'''

def convert_to_dcat_ap(json_data):
    dcat = Namespace("http://www.w3.org/ns/dcat#")
    dcterms = Namespace("http://purl.org/dc/terms/")
    foaf = Namespace("http://xmlns.com/foaf/0.1/")

    g = Graph()
    g.bind("dcat", dcat)
    g.bind("dcterms", dcterms)
    g.bind("foaf", foaf)

    catalog_node = URIRef("http://example.org/catalog")
    g.add((catalog_node, RDF.type, dcat.Catalog))

    for key, value in json_data["catalog"].items():
        if key == "dataset":
            for dataset in value:
                dataset_node = URIRef(
                    "http://example.org/dataset/{}".format(dataset["title"].replace(" ", "-")))
                g.add((dataset_node, RDF.type, dcat.Dataset))
                g.add((dataset_node, dcterms.title, Literal(dataset["title"])))
                g.add((catalog_node, dcat.dataset, dataset_node))
        else:
            g.add((catalog_node, dcat[key], Literal(value)))

    return g


# Exemplo de uso
json_data = {
    "catalog": {
        "type": "DeviceModel",
        "title": "titulo Catalogo",
        "description": "descrição catalogo",
        "license": "https://creativecommons.org/licenses/by-nc/4.0/",
        "language": "https://publications.europa.eu/resource/authority/language/POR",
        "publisher": "http://lisboaaberta.cm-lisboa.pt",
        "rights": ["RightA", "RightB"],
        "updateModification": "2022-11-12T15:28:00",
        "creator": "Othmane El Arbaoui",
        "modifiedRecord": "2022-11-14T15:28:00",
        "dataset": [
            {
                "title": "titulo dataset 1",
                "description": "descrição dataset",
                "keyword": ["tagA_1", "tagB_1", "tagC_1"],
                "accessRights": "GrupA",
                "sample": "https://geodados-cml.hub.arcgis.com/",
                "contactPoint": "contacto",
                "distribution": [
                    {
                        "description": "descrição distribuição",
                        "format": "GeoJSON",
                        "license": "https://creativecommons.org/licenses/by-nc/4.0/"
                    },
                    {
                        "description": "descriçao22",
                        "format": "json",
                        "license": "https://creativecommons.org/licenses/by-nc-nd/4.0/"
                    }
                ]
            },
            {
                "title": "titulo dataset 2",
                "description": "descrição dataset 2",
                "keyword": ["tagA_2", "tagB_2", "tagC_2"],
                "accessRights": "GrupB",
                "sample": "https://www.blabla.com",
                "contactPoint": "contacto2",
                "distribution": []
            }
        ]
    }
}

graph = convert_to_dcat_ap(json_data)
print(graph.serialize(format="turtle"))
'''

import json
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD


def convert_to_dcat_ap(json_data):
    # Criação do grafo RDF
    dcat = Namespace("http://www.w3.org/ns/dcat#")
    dcterms = Namespace("http://purl.org/dc/terms/")
    foaf = Namespace("http://xmlns.com/foaf/0.1/")

    g = Graph()
    g.bind("dcat", dcat)
    g.bind("dcterms", dcterms)
    g.bind("foaf", foaf)

    # Conversão para DCAT-AP
    catalog_uri = URIRef("http://example.org/catalog")

    dataset_uris = []

    # Adicionando informações do catálogo
    catalog_node = URIRef(catalog_uri)
    g.add((catalog_node, RDF.type, dcat.Catalog))
    for field, value in json_data["catalog"].items():
        if field == "dataset":
            continue
        if isinstance(value, list):
            for item in value:
                g.add((catalog_node, dcat[field], Literal(item)))
        else:
            g.add((catalog_node, dcat[field], Literal(value)))

    # Adicionando informações dos datasets
    for dataset in json_data["catalog"]["dataset"]:
        dataset_uri = URIRef(
            "http://example.org/dataset/{}".format(dataset.get("title", "").replace(" ", "-")))
        dataset_uris.append(dataset_uri)
        g.add((dataset_uri, RDF.type, dcat.Dataset))
        for field, value in dataset.items():
            if field == "distribution":
                continue
            if isinstance(value, list):
                for item in value:
                    g.add((dataset_uri, dcat[field], Literal(item)))
            else:
                g.add((dataset_uri, dcat[field], Literal(value)))
            g.add((catalog_node, dcat.dataset, dataset_uri))

        if "distribution" in dataset:
            for distribution in dataset["distribution"]:
                distribution_node = URIRef("http://example.org/distribution/{}".format(
                    distribution.get("description", "").replace(" ", "-")))
                g.add((distribution_node, RDF.type, dcat.Distribution))
                for field, value in distribution.items():
                    g.add((distribution_node, dcat[field], Literal(value)))
                g.add((dataset_uri, dcat.distribution, distribution_node))

    return g


def serialize_to_turtle(graph, file_path):
    graph.serialize(file_path, format="turtle")

    return graph.serialize(format="turtle")


def serialize_to_jsonld(graph, file_path):
    # Create a JSON-LD context object
    jsonld_context = {
        "@context": {
            "dcat": "http://www.w3.org/ns/dcat#",
            "dcterms": "http://purl.org/dc/terms/",
            "foaf": "http://xmlns.com/foaf/0.1/"
        }
    }

    # Serialize the graph to JSON-LD
    jsonld_data = graph.serialize(
        format='json-ld', context=jsonld_context, indent=2)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(jsonld_data)


# Exemplo de uso
json_data = {
    "catalog": {
        "type": "DeviceModel",
        "title": "titulo Catalogo",
        "description": "descrição catalogo",
        "license": "https://creativecommons.org/licenses/by-nc/4.0/",
        "language": "https://publications.europa.eu/resource/authority/language/POR",
        "publisher": "http://lisboaaberta.cm-lisboa.pt",
        "rights": ["RightA", "RightB"],
        "updateModification": "2022-11-12T15:28:00",
        "creator": "Othmane El Arbaoui",
        "modifiedRecord": "2022-11-14T15:28:00",
        "dataset": [
            {
                "title": "titulo dataset 1",
                "description": "descrição dataset",
                "keyword": ["tagA_1", "tagB_1", "tagC_1"],
                "accessRights": "GrupA",
                "sample": "https://geodados-cml.hub.arcgis.com/",
                "contactPoint": "contacto",
                "distribution": [
                    {
                        "description": "descrição distribuição",
                        "format": "GeoJSON",
                        "license": "https://creativecommons.org/licenses/by-nc/4.0/"
                    },
                    {
                        "description": "descriçao22",
                        "format": "json",
                        "license": "https://creativecommons.org/licenses/by-nc-nd/4.0/"
                    }
                ]
            },
            {
                "title": "titulo dataset 2",
                "description": "descrição dataset 2",
                "keyword": ["tagA_2", "tagB_2", "tagC_2"],
                "accessRights": "GrupB",
                "sample": "https://www.blabla.com",
                "contactPoint": "contacto2",
                "distribution": []
            }
        ]
    }
}


# Convertendo para DCAT-AP e serializando em Turtle
graph = convert_to_dcat_ap(json_data)
serialize_to_turtle(graph, "dcat_ap.ttl")

# Convertendo para JSON-LD e serializando em formato JSON-LD bem formatado
serialize_to_jsonld(graph, "dcat_ap.jsonld")

print("Done.")


'''

# Exemplo de uso
input_data = {
    "Catalog": {
        "title": "titulo Catalogo",
        "Dataset": [
            {
                "title": "title",
                "keywords": [
                    "tagA",
                    "tagB",
                    "tagC"
                ],
                "Distribution": [
                    {
                        "description": "descrição distribuição"
                    },
                    {
                        "description": "descriçao22"
                    }
                ]
            },
            {
                "title": "title 2222",
                "keywords": [
                    "aaa"
                ],
                "Distribution": []
            }
        ]
    }
}

'''
