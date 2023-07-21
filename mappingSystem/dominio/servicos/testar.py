import json

def convert_to_dcat_ap(json_data):
    model_data = {
        "catalog": {
            "type": json_data["type"],
            "title": json_data["titleCatalog"],
            "description": json_data["descriptionCatalog"],
            "license": json_data["licenseCatalog"],
            "language": json_data["languageCatalog"],
            "publisher": json_data["publisherCatalog"],
            "rights": json_data["RightsCatalog"],
            "updateModification": json_data["update_modificationCatalog"],
            "creator": json_data["creatorCatalog"],
            "modifiedRecord": json_data["modifiedCatalogRcord"],
            "dataset": [],
        },
        
        
    }

    if not isinstance(json_data["titleDataset"], list):
        json_data["titleDataset"]=[json_data["titleDataset"]]
        json_data["descriptionDataset"]=[json_data["descriptionDataset"]]
        json_data["accessDataset"]=[json_data["accessDataset"]]
        json_data["sampleDataset"]=[json_data["sampleDataset"]]
        json_data["contactPointDataset"]=[json_data["contactPointDataset"]]
        json_data["modifiedCatalogRcord"]=[json_data["modifiedCatalogRcord"]]

    for i,element in enumerate(json_data["keyword_tagDataset"]):
        if not isinstance(element, list):
            json_data["keyword_tagDataset"][i]=[element]


    # Convertendo os campos do JSON para o formato DCAT-AP
    for i, title in enumerate(json_data["titleDataset"]):
        #name="dataset-"+"{:03d}".format(i+1)
        dataset = {
           
            "title": title,
            "description": json_data["descriptionDataset"][i],
            "keyword": json_data["keyword_tagDataset"][i],
            "accessRights": json_data["accessDataset"][i],
            "sample": json_data["sampleDataset"][i],
            "contactPoint": json_data["contactPointDataset"][i],
            "distribution1": []
        }
        model_data["catalog"]["dataset"].append(dataset)

    # Convertendo as distribuições
    for i, datasetIndex in enumerate(json_data["partOfDataset"]):

        if datasetIndex is not None:
            name="dist-"+"{:03d}".format(i+1) 
            distribution = {
                "description": json_data["descriptionDistribution"][i],
                "format": json_data["formatDistribution"][i],
                "license": json_data["licenseDistribution"][i],
                "accessURL": json_data["accessURLDistribution"][i]
            }
            
            model_data["catalog"]["dataset"][datasetIndex]["distribution1"].append(distribution)
 

    return model_data

# Exemplo de uso
json_data = {
    'type': 'DeviceModel',
    'titleDataset': ['titulo dataset 1', 'titulo dataset 2'],
    'descriptionDataset': ['descrição dataset','descrição dataset 2'],
    'keyword_tagDataset': [['tagA_1', 'tagB_1', 'tagC_1'],['tagA_2', 'tagB_2', 'tagC_2']],
    'accessDataset': ['GrupA','GrupB'],
    'sampleDataset': ['https://geodados-cml.hub.arcgis.com/',"https://www.blabla.com"],
    'contactPointDataset': ['contacto', 'contacto2'],
    'titleCatalog': 'titulo Catalogo',
    'descriptionCatalog': 'descrição catalogo',
    'licenseCatalog': 'CC BY-SA',
    'languageCatalog': 'https://publications.europa.eu/resource/authority/language/POR',
    'publisherCatalog': 'http://lisboaaberta.cm-lisboa.pt',
    'RightsCatalog': ['RightA', 'RightB'],
    'update_modificationCatalog': 'Novembro 12, 2022, 15:28 (Europe/Lisbon)',
    'creatorCatalog': 'Othmane El Arbaoui',
    'modifiedCatalogRcord': 'Novembro 14, 2022, 15:28 (Europe/Lisbon)',
    'accessURLDistribution': ['https://services.arcgis.com/1dSrzEWVQn5kHHyK/ArcGIS/rest/services/Administracao_Publica/FeatureServer/0/query?where=1%3D1&outFields=*&f=pgeojson', 'https://www.teste.com'],
    'descriptionDistribution': ['descrição distribuição', 'descriçao22'],
    'formatDistribution': ['GeoJSON', 'json'],
    'licenseDistribution': ['CC BY-NC', 'CC BY-NC-ND'],
    'partOfDataset': [0, 0]
}

model_data = convert_to_dcat_ap(json_data)
print(json.dumps(model_data, indent=2))
