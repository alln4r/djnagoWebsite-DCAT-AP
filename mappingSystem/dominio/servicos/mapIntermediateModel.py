import abc


class MapIntermediateModel_interface(abc.ABC):
    @abc.abstractmethod
    def getMappedLinks(self, intermediateModelFields, schemeMetaDataIntermediate, APImetaData, data):
        pass

    @abc.abstractmethod
    def makeIntermediateModelFields(self, schemeFiwareModel, schemeMetaDataIntermediate):
        pass

    @abc.abstractmethod
    def getMappedData(self, linksWithpath, APIdata, vkApiData):
        pass

    @abc.abstractmethod
    def getIntermediateModelData(self, json_data):
        pass
