import abc


class TratarJson_interface(abc.ABC):

    @abc.abstractmethod
    def fieldsToShowInGUI(self, data):
        pass

    @abc.abstractmethod
    def find_values(self, data, path="", result={}):
        pass

    @abc.abstractmethod
    def merge_duplicate_keys(self, data):
        pass

    @abc.abstractmethod
    def get_suffixes_and_prefix(self, key):
        pass
