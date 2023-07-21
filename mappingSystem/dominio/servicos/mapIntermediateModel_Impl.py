from ..servicos.mapIntermediateModel import MapIntermediateModel_interface
import json
# mapDataToMyModel


# implement em pythom é passar por parrametro a calass
class MapIntermediateModel(MapIntermediateModel_interface):

    def findProperties(self, obj):
        if isinstance(obj, dict):
            if "properties" in obj:
                return obj["properties"]
            else:
                for key, value in obj.items():
                    result = self.findProperties(value)
                    if result is not None:
                        return result
        elif isinstance(obj, list):
            for item in obj:
                result = self.findProperties(item)
                if result is not None:
                    return result
        return None

    def makeIntermediateModelFields(self, schemeFiwareModel, schemeMetaDataIntermediate):

        intermediateModelFields = list(schemeMetaDataIntermediate.keys())
        properties = self.findProperties(schemeFiwareModel)
        if properties is not None:
            intermediateModelFields = list(
                properties.keys()) + intermediateModelFields
            print("============================")
            print("============================")
            print("============================")
            print("============================")
            print(intermediateModelFields)
            print("============================")
            print("============================")
            print("============================")
            print("============================")
            print("============================")

        return intermediateModelFields

    def getMappedLinks(self, intermediateModelFields, schemeMetaDataIntermediate, APImetaData, data):  # mapTo

        existingLinks = []
        element = {}

        for i in intermediateModelFields:

            # if i in schema:
            #    element=schema[i]
            if i in schemeMetaDataIntermediate:
                element = schemeMetaDataIntermediate[i]
                if isinstance(element, list):  # []
                    element = element[0]

                if not element:  # empty
                    continue
            # else:
            #    print("nao existe "+i)
            #    continue

            for x in data:
                if x not in APImetaData:  # empty
                    if x == i:
                        existingLinks.append({"from": x, "to": i})
                    continue

                if i not in schemeMetaDataIntermediate:  # nao existe
                    continue
                metadata = APImetaData[x]

                if isinstance(metadata, list):  # []
                    metadata = metadata[0]

                if metadata['type'] == element['type'] and metadata['parent'] == element['parent']:
                    existingLinks.append({"from": x, "to": i})

        return existingLinks

    def getMappedData(self, linksWithpath, vkApiData):  # mapDataTo

        modelData = []
        for item in vkApiData:
            new_item = {}
            for key, value in item.items():
                for link_item in linksWithpath:
                    if key == link_item['from']:
                        new_item[link_item['to']] = value
                        break

            modelData.append(new_item)

        return modelData

    def getIntermediateModelData(self, json_data, schemeMetaDataIntermediate):

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

        return model_data
