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
# tentar fazer esta parte automaticamente
    # Adicionando informações do catálogo
    catalog_node = URIRef(catalog_uri)
    g.add((catalog_node, RDF.type, dcat.Catalog))
    g.add((catalog_node, dcterms.title, Literal(
        json_data["catalog"]["title"])))
    g.add((catalog_node, dcterms.description, Literal(
        json_data["catalog"]["description"])))
    g.add((catalog_node, dcterms.license, URIRef(
        json_data["catalog"]["license"])))
    g.add((catalog_node, dcterms.language, URIRef(
        json_data["catalog"]["language"])))
    g.add((catalog_node, dcterms.publisher, URIRef(
        json_data["catalog"]["publisher"])))
    g.add((catalog_node, dcterms.rights, Literal(
        json_data["catalog"]["rights"][0])))
    g.add((catalog_node, dcterms.rights, Literal(
        json_data["catalog"]["rights"][1])))
    g.add((catalog_node, dcterms.modified, Literal(
        json_data["catalog"]["updateModification"], datatype=XSD.dateTime)))
    g.add((catalog_node, foaf.creator, Literal(
        json_data["catalog"]["creator"])))
    g.add((catalog_node, dcterms.modified, Literal(
        json_data["catalog"]["modifiedRecord"], datatype=XSD.dateTime)))

    # Adicionando informações dos datasets
    for dataset in json_data["catalog"]["dataset"]:
        dataset_uri = URIRef(
            "http://example.org/dataset/{}".format(dataset["title"].replace(" ", "-")))
        dataset_uris.append(dataset_uri)
        g.add((dataset_uri, RDF.type, dcat.Dataset))
        g.add((dataset_uri, dcterms.title, Literal(dataset["title"])))
        g.add((dataset_uri, dcterms.description,
              Literal(dataset["description"])))
        for keyword in dataset["keyword"]:
            g.add((dataset_uri, dcat.keyword, Literal(keyword)))
        g.add((dataset_uri, dcat.accessRights,
              Literal(dataset["accessRights"])))
        g.add((dataset_uri, dcat.landingPage, URIRef(dataset["sample"])))
        g.add((dataset_uri, dcat.contactPoint,
              Literal(dataset["contactPoint"])))
        g.add((catalog_node, dcat.dataset, dataset_uri))

        # Adicionando informações das distribuições
        for distribution in dataset["distribution"]:
            distribution_node = URIRef(
                "http://example.org/distribution/{}".format(distribution["format"].replace(" ", "-")))
            g.add((distribution_node, RDF.type, dcat.Distribution))
            g.add((distribution_node, dcterms.description,
                  Literal(distribution["description"])))
            g.add((distribution_node, dcat.mediaType,
                  Literal(distribution["format"])))
            g.add((distribution_node, dcterms.license,
                  URIRef(distribution["license"])))
            g.add((dataset_uri, dcat.distribution, distribution_node))

    return g


def serialize_to_turtle(graph, file_path):
    graph.serialize(file_path, format="turtle")


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
def convert_to_ckan_package(graph):
    package = {
        "name": "example_package",
        "title": "Example Package",
        "notes": "This is an example package",
        "resources": []
    }

    for s, p, o in graph.triples((None, RDF.type, graph.namespace_manager.dcat.Dataset)):
        dataset_uri = str(s)
        package["name"] = dataset_uri.split("/")[-1]

        for s2, p2, o2 in graph.triples((s, graph.namespace_manager.dcterms.title, None)):
            package["title"] = str(o2)

        for s2, p2, o2 in graph.triples((s, graph.namespace_manager.dcterms.description, None)):
            package["notes"] = str(o2)

        for s2, p2, o2 in graph.triples((s, graph.namespace_manager.dcat.distribution, None)):
            resource = {
                "name": "example_resource",
                "description": "",
                "url": "",
                "format": ""
            }

            for s3, p3, o3 in graph.triples((o2, graph.namespace_manager.dcterms.description, None)):
                resource["description"] = str(o3)

            for s3, p3, o3 in graph.triples((o2, graph.namespace_manager.dcat.mediaType, None)):
                resource["format"] = str(o3)

            for s3, p3, o3 in graph.triples((o2, graph.namespace_manager.dcterms.license, None)):
                resource["license"] = str(o3)

            for s3, p3, o3 in graph.triples((o2, graph.namespace_manager.dcat.downloadURL, None)):
                resource["url"] = str(o3)

            package["resources"].append(resource)

    return package


def insert_to_ckan(json_data, ckan_url, ckan_api_key):
    # Convertendo para DCAT-AP
    graph = convert_to_dcat_ap(json_data)

    # Convertendo para o formato de dados do CKAN
    package_data = convert_to_ckan_package(graph)

    # Enviando para o CKAN
    ckan = RemoteCKAN(ckan_url, apikey=ckan_api_key)
    ckan.action.package_create(**package_data)


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

ckan_url = "http://localhost:5000"
ckan_api_key = "YOUR_API_KEY"

insert_to_ckan(json_data, ckan_url, ckan_api_key)
'''


'''
outro
import ckanapi
def insert_or_update_in_ckan(json_data, ckan_url, api_key):
    # Convertendo para DCAT-AP
    graph = convert_to_dcat_ap(json_data)

    # Serializando em JSON-LD
    jsonld_data = graph.serialize(format='json-ld')

    # Conectando ao CKAN
    ckan = ckanapi.RemoteCKAN(ckan_url, apikey=api_key)

    # Inserindo ou atualizando o pacote
    package_id = json_data["catalog"]["id"]
    try:
        ckan.action.package_create_or_update(jsonld=jsonld_data, id=package_id)
        print("Package '{}' inserido/atualizado com sucesso no CKAN.".format(package_id))
    except ckanapi.ValidationError as e:
        print("Erro de validação ao inserir/atualizar o pacote no CKAN:")
        print(e)
    except ckanapi.NotFound:
        print("Erro: Pacote não encontrado no CKAN.")
    except ckanapi.NotAuthorized:
        print("Erro: Falha de autenticação/autorização no CKAN.")
    except ckanapi.CKANAPIError as e:
        print("Erro ao inserir/atualizar o pacote no CKAN:")
        print(e)


# Exemplo de uso
json_data = {
    "catalog": {
        "id": "meu-catalogo",
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

# Configurações do CKAN
ckan_url = 'http://example.org/ckan'
api_key = 'YOUR_API_KEY'

# Inserir ou atualizar no CKAN
insert_or_update_in_ckan(json_data, ckan_url, api_key)

print("Done.")

'''
