from ..servicos.tratarJson import TratarJson_interface
# import abc


# implement em pythom é passar por parrametro a calass
class TratarJson(TratarJson_interface):

    def fieldsToShowInGUI(self, data):

        vkeys = []
        listLastKeys = []
        for dt in data:
            vk = {}
            self.find_values(dt, result=vk)
            vk, lastKeys = self.merge_duplicate_keys(vk)
            vkeys.append(vk)
            listLastKeys.append(lastKeys)

        return listLastKeys, vkeys  # self.listLastKeys,

    def find_values(self, data, path="", result={}):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                self.find_values(value, new_path, result)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{path}.{i}" if path else str(i)
                self.find_values(item, new_path, result)
        else:
            result[path] = data

    def merge_duplicate_keys(self, data):
        result = {}
        keys = []
        for key, value in data.items():
            base_key, suffixes = self.get_suffixes_and_prefix(key)
            len_suffixes = len(suffixes)

            if base_key not in result:
                keys.append(base_key)

                if len_suffixes < 2:  # 0 ou 1
                    result[base_key] = []
                else:
                    result[base_key] = multi_dim_list = [[]
                                                         for _ in range(len_suffixes)]

            if len_suffixes < 2:  # 0 ou 1
                result[base_key].append(value)
            else:
                result[base_key][suffixes[0]].append(value)

        return result, keys

    def get_suffixes_and_prefix(self, key):
        parts = key.split('.')
        suffixes = []
        for part in reversed(parts):
            if part.isdigit():
                suffixes.insert(0, int(part))
            else:
                prefixe = part
                break
        return prefixe, suffixes


'''
inputAPIdata = [
    {
        "titleD": "titulo dataset",
        "descriptionD": "descrição dataset",
        "a": {
            "b": "bbb",
            "c": ["c1", "c2"],
            "d": [{"f": "dfdf"}]
        },
        "w": ["g", {"r": "rrr"}],
        "keyword_tagD": [["tagA", "tagB", "tagC"], ["tag2", "tag1"]],
        "descriptionDist": ["descrição distribuição", "descriçao22"],
        "formatDist": ["GeoJSON", "json"],
        "partOfD": [0, 0]
    },
    {
        "othane": "AAAAAAAAAAAAAAAAAAAAAAAA",
    }
]


print(TratarJson().fieldsToShowInGUI(inputAPIdata))'''
