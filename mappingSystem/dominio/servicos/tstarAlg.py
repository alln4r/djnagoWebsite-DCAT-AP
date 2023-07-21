

linksWithpath1 = {
    "error": "false",
    "errorMessage": "",
    "links": [

        {
            "from": "formatDist",
            "to": "formatDistribution"
        },

        {
            "from": "partOfD",
            "to": "partOfDataset"
        }
    ]
}

APIdata1 = [
    {


        "titleD": "titulo dataset",
        "formatDist": [
            "GeoJSON",
            "json"
        ],


        "descriptionDist":[
            "descrição distribuição",
            "descriçao22"
        ],
        "partOfD":[
            0,
            0
        ]
    }
]

vkApiData = {

    "titulo dataset": [
        "titleD"
    ],

    "['GeoJSON', 'json']": [
        "keyword_tagD",
        0,
        "formatDist"
    ],
}


dt = [{
    "a": "djkfkdj",
    "b": "sdjhdj"
}]

link = [
    {'from': 'b', 'to': 'descriptionDataset'},
    {'from': 'a', 'to': 'keyword_tagDataset'}
]

new_dt = []

for item in dt:
    new_item = {}
    for key, value in item.items():
        for link_item in link:
            if key == link_item['from']:
                new_item[link_item['to']] = value
                break

    new_dt.append(new_item)

print(new_dt)
