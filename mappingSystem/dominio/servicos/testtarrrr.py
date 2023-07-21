
import json
jsonesperado = {
    "Catalog": {
        "title": "titulo Catalogo",
        "Dataset": [
            {
                "title": "title",
                "keywords": ["tagA", "tagB", "tagC"],
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
                "keywords": ["aaa"],
                "Distribution": []
            }
        ],

    }
}


json_data = {
    "titleDataset": [
        "title",
        "title 2222"
    ],
    "keyword_tagDataset": [
        ["tagA", "tagB", "tagC"],
        ["aaa"]
    ],
    "titleCatalog": "titulo Catalogo",
    "descriptionDistribution": [
        "descrição distribuição",
        "descriçao22"
    ],
    "partOfDataset": [
        0,
        0
    ]
}

schemeMetaDataIntermediate = {
    "titleDataset": {
        "type": "https://schema.org/title",
        "description": "Property. Model:'https://schema.org/title. Titulo do dataset",
        "parent": "Dataset"
    },
    "keyword_tagDataset": {
        "type": "https://schema.org/keywords",
        "description": "Property. Model:'https://schema.org/keywords'. etiquetatas do dataset.",
        "parent": "Dataset"
    },
    "titleCatalog": {
        "type": "https://schema.org/title",
        "description": "Property. Model:'https://schema.org/title'. Titulo do Catalogo",
        "parent": "Catalog"
    },
    "descriptionDistribution": {
        "type": "https://schema.org/description",
        "description": "Property. Model:'https://schema.org/description '.",
        "parent": "Distribution"
    }
}

model_data = {
    "Catalog": {
        "title": "",
        "Dataset": []
    }
}

for fieldName in json_data:
    if fieldName == "partOfDataset":
        continue

    term = schemeMetaDataIntermediate[fieldName].get("type")
    if term.endswith("/"):
        term = term[:-1]
    term = term.split("/")[-1].split("#")[-1]
    parent = schemeMetaDataIntermediate[fieldName].get("parent")

    if parent == "Catalog":
        model_data["Catalog"][term] = json_data[fieldName]
    elif parent == "Dataset":
        if not isinstance(json_data[fieldName], list):
            json_data[fieldName] = [json_data[fieldName]]

        for i, element in enumerate(json_data[fieldName]):
            if i < len(model_data["Catalog"]["Dataset"]):
                model_data["Catalog"]["Dataset"][i][term] = element
            else:
                model_data["Catalog"]["Dataset"].append(
                    {term: element, "Distribution": []})

    elif parent == "Distribution":
        if not isinstance(json_data[fieldName], list):
            json_data[fieldName] = [json_data[fieldName]]

        for i, datasetIndex in enumerate(json_data["partOfDataset"]):
            if datasetIndex is not None:
                if i < len(model_data["Catalog"]["Dataset"][datasetIndex]["Distribution"]):
                    model_data["Catalog"]["Dataset"][datasetIndex]["Distribution"][i][term] = json_data[fieldName][i]
                else:
                    model_data["Catalog"]["Dataset"][datasetIndex]["Distribution"].append(
                        {term: json_data[fieldName][i]})

print(json.dumps(model_data, indent=4))

assert jsonesperado == model_data

print('niceeeeeeeeee')
