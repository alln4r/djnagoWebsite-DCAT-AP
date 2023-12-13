from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD


class ToDCAT_AP:
    def run(self, json_data):
       
        # Substituir os datasets no JSON original
        json_data['Catalog']['Dataset'] = [dataset for dataset in json_data['Catalog']['Dataset'] if any(dataset.values())]

        # Convertendo para DCAT-AP e serializando em Turtle
        
        graph = self.convert_to_dcat_ap(json_data)
        dcatTTL = self.serialize_to_turtle(graph, "dcat_ap.ttl")
        # Convertendo para JSON-LD e serializando em formato JSON-LD bem formatado
        dcatJsonLD = self.serialize_to_jsonld(graph, "dcat_ap.jsonld")

        print("Done.")
        return dcatTTL, dcatJsonLD

    def convert_to_dcat_ap(self, json_data):
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
        for field, value in json_data["Catalog"].items():
            if field == "Dataset":
                continue
            if isinstance(value, list):
                for item in value:
                    g.add((catalog_node, dcat[field], Literal(item)))
            else:
                g.add((catalog_node, dcat[field], Literal(value)))

        dt=0
        # Adicionando informações dos datasets
        for dataset in json_data["Catalog"]["Dataset"]:
            dt+=1
            dataset_uri = URIRef(
                "http://example.org/dataset/{}{}".format(dataset.get("title", "").replace(" ", "-"), "dt_"+str(dt)))
            
            dataset_uris.append(dataset_uri)
            g.add((dataset_uri, RDF.type, dcat.Dataset))
            for field, value in dataset.items():
                if field == "Distribution":
                    continue
                if isinstance(value, list):
                    
                    #vlue_str = ', '.join([f'"{tag}"' for tag in value])
                    # Adicionar a string ao grafo
                    #g.add((dataset_uri, dcat[field], Literal(vlue_str)))

                    for item in value:
                        g.add((dataset_uri, dcat[field], Literal(item)))
                else:
                    g.add((dataset_uri, dcat[field], Literal(value)))
                g.add((catalog_node, dcat.dataset, dataset_uri))

            if "Distribution" in dataset:
                dist=0
                for distribution in dataset["Distribution"]:
                    dist+=1
                    distribution_node = URIRef("http://example.org/distribution/{}{}".format(
                        distribution.get("description", "").replace(" ", "-"), "dist_"+str(dt)+"_"+str(dist)))
                    g.add((distribution_node, RDF.type, dcat.Distribution))
                    for field, value in distribution.items():
                        if isinstance(value, list):
                    
                            vlue_str = ', '.join([f'"{tag}"' for tag in value])
                            # Adicionar a string ao grafo
                            g.add((distribution_node, dcat[field], Literal(vlue_str)))
                        else:
                            g.add((distribution_node, dcat[field], Literal(value)))
                    g.add((dataset_uri, dcat.distribution, distribution_node))

        return g

    def serialize_to_turtle(self, graph, file_path):
        graph.serialize(file_path, format="turtle")
        return graph.serialize(format="turtle")#.replace('\\"', '"').replace('""', '"')

    def serialize_to_jsonld(self, graph, file_path):
        # Create a JSON-LD context object
        jsonld_context = {
            #"@context": {
                "dcat": "http://www.w3.org/ns/dcat#",
                "dcterms": "http://purl.org/dc/terms/",
                "foaf": "http://xmlns.com/foaf/0.1/"
            #}
        }

        # Serialize the graph to JSON-LD
        jsonld_data = graph.serialize(
            format='json-ld', context=jsonld_context, indent=2)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(jsonld_data)

        return jsonld_data

'''
jsonn={'Catalog': {
                    'title': '', 
                    'Dataset': [{
                                    'description': 'descrição dataset', 
                                    'Distribution': [
                                        {
                                            'contentUrl': 'https://services.arcgis.com/1dSrzEWVQn5kHHyK/ArcGIS/rest/services/Administracao_Publica/FeatureServer/0/query?where=1%3D1&outFields=*&f=pgeojson', 
                                            'description': 'descrição distribuição', 
                                            'encodingFormat': 'GeoJSON', 
                                            'license': 'https://creativecommons.org/licenses/by-nc/4.0/'
                                        }, 
                                        {
                                            'contentUrl': 'https://www.teste.com', 
                                            'description': 'descriçao22', 
                                            'encodingFormat': 'json', 
                                            'license': 'https://creativecommons.org/licenses/by-nc-nd/4.0/'
                                        }
                                    ], 
                                    'dateModified': 'Novembro 12, 2022, 15:28 (Europe/Lisbon)', 
                                    'contactPoint': 'contacto', 
                                    'keywords': ['tagA', 'tagB', 'tagC'], 
                                    'publisher': 'http://lisboaaberta.cm-lisboa.pt', 
                                    'accessRights': 'GrupA', 
                                    'sample': 'https://geodados-cml.hub.arcgis.com/'
                                }, 
                                {'keywords': [], 
                                'Distribution': []
                                }], 
                    'name': ['titulo Catalogo'], 
                    'description': ['descrição catalogo'], 
                    'license': ['CC BY-SA'], 
                    'publisher': ['http://lisboaaberta.cm-lisboa.pt'], 
                    'language': ['https://publications.europa.eu/resource/authority/language/POR'], 
                    'dateModified': ['Novembro 12, 2022, 15:28 (Europe/Lisbon)'], 
                    'creator': ['Othmane El Arbaoui']
                    }
    }

filtered_datasets = [dataset for dataset in jsonn['Catalog']['Dataset'] if any(dataset.values())]

# Substituir os datasets no JSON original
jsonn['Catalog']['Dataset'] = filtered_datasets

# Imprimir o resultado
print(jsonn)

dcatTTL, dcatJsonLD = ToDCAT_AP().run(jsonn)

print(dcatTTL)
'''