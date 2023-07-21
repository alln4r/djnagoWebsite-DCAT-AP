# from ..servicos import CreateTurtleFile
import json


class MapJsonToDCATFiles:
    def __init__(self, jsonFile):

        self.json = json.dumps(jsonFile, ensure_ascii=False).encode('utf-8')
        self.json = json.loads(self.json)
        print(self.json)

    def doMap(self):

        # e = self.json["e"]
        # e_page = self.json["e_page"]

        # print(json.dumps(self.json[0], indent=2))

        # ------------------CATALOGO----------------------------

        cat = {
            "title": self.json[0]["titleCatalog"],
            "description": self.json[0]["descriptionCatalog"],
            "license": self.json[0]["licenseCatalog"],
            "publisher":  self.json[0]["publisherCatalog"],
            "homePage": self.json[0]["homePageCatalog"],
            "language": self.json[0]["languageCatalog"],
            "Datasets": []
        }
        # ------------------end---------------------------------

        if not isinstance(self.json[0]["titleDataset"], list):
            self.json[0]["titleDataset"] = [self.json[0]["titleDataset"]]
            self.json[0]["descriptionDataset"] = [
                self.json[0]["descriptionDataset"]]

        dataset = []
        for i in range(len(self.json[0]["titleDataset"])):
            # numDT=numDT+1
            # nome="dataset-"+"{:03d}".format(numDT)

            dataset.append(
                {
                    "title": self.json[0]["titleDataset"][i],
                    "description": self.json[0]["descriptionDataset"][i],
                    "nome": "dataset-"+"{:03d}".format(i+1),
                    "dist": []
                }
            )

            cat["Datasets"].append("dataset-"+"{:03d}".format(i+1))

        cttl = CreateTurtleFile.CreateTurtleFile()
        cttl.Catalogo(cat)

        if not isinstance(self.json[0]["accessURLDistribution"], list):
            self.json[0]["accessURLDistribution"] = [
                self.json[0]["accessURLDistribution"]]
            self.json[0]["descriptionDistribution"] = [
                self.json[0]["descriptionDistribution"]]
            self.json[0]["formatDistribution"] = [
                self.json[0]["formatDistribution"]]
            self.json[0]["licenseDistribution"] = [
                self.json[0]["licenseDistribution"]]

        for i in range(len(self.json[0]["accessURLDistribution"])):
            dist = {
                "accessURL": self.json[0]["accessURLDistribution"][i],
                "descricao": self.json[0]["descriptionDistribution"][i],
                "formato": self.json[0]["formatDistribution"][i],
                "licenca": self.json[0]["licenseDistribution"][i],
                "nome": "dist-"+"{:03d}".format(i+1)
            }

            for dt in range(len(dataset)):
                for indexDataSet in self.json[0]["partOfDataset"]:
                    if dt == indexDataSet:
                        dataset[dt]["dist"].append(dist['nome'])

            cttl.Distribution(dist)

        for dt in dataset:
            cttl.Dataset(dt)

        catRec = {
            "modified": self.json[0]["modifiedCatalogRcord"]
        }

        cttl.CatalogoRecord(catRec)
