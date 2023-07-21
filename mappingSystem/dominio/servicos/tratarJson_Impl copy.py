def find_values(data, path="", result={}):
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            find_values(value, new_path, result)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}.{i}" if path else str(i)
            find_values(item, new_path, result)
    else:
        result[path] = data


def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


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
    }
]

Vkeys = {}
for data in inputAPIdata:
    find_values(data, result=Vkeys)


def get_suffixes_and_prefix(key):
    parts = key.split('.')
    suffixes = []
    for part in reversed(parts):
        if part.isdigit():
            suffixes.insert(0, int(part))
        else:
            prefixe = part
            break
    return prefixe, suffixes


def merge_duplicate_keys(data):
    result = {}
    for key, value in data.items():
        base_key, suffixes = get_suffixes_and_prefix(key)
        print(base_key)
        len_suffixes = len(suffixes)

        if base_key not in result:
            if len_suffixes < 2:  # 0 ou 1
                result[base_key] = []
            else:
                result[base_key] = multi_dim_list = [[]
                                                     for _ in range(len_suffixes)]

        if len_suffixes < 2:  # 0 ou 1
            result[base_key].append(value)
        else:
            result[base_key][suffixes[0]].append(value)

    return result


Vkeys = merge_duplicate_keys(Vkeys)


# o output tem que ser igula a :
# listLastKeys = ['titleD', 'descriptionD', "b", "c", "f", "w", "r", "keyword_tagD",'descriptionDist', 'formatDist', 'partOfD']
# Vkeys={'titulo dataset': ['titleD'], 'descrição dataset': ['descriptionD'], "bbb": ["a","b"], '["c1", "c2"]':["a","c"], "dfdf":["a","d",0,"f"], "g":["w"], "rrr":[,"w",1,"r"], '["tagA", "tagB", "tagC"]': [ "keyword_tagD", 0], '["tag2", "tag1"]': [ "keyword_tagD", 1], '["descrição distribuição","descriçao22"]':["descriptionDist"], '["GeoJSON","json"]':["formatDist"], '[0,0]':["partOfD"]}


# {'titulo dataset': ['titleD'], 'descrição dataset': ['descriptionD'], "bbb": ["b"], '["c1", "c2"]':["c"], "dfdf":["f"], "g":["w"], "rrr":["r"], '["tagA", "tagB", "tagC"]': [ "keyword_tagD"], '["descrição distribuição","descriçao22"]':["descriptionDist"], '["GeoJSON","json"]':["formatDist"], '[0,0]':["partOfD"]}
