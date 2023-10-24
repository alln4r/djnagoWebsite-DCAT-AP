
import re
from django.http import JsonResponse
import requests
import json

class CKANImporter:
    def __init__(self, ckan_url, ckan_token, json_ld):

        if not ckan_token or not ckan_url:
            raise ValueError('Both fields must be filled')
        
        try:
            response = requests.get(ckan_url)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            raise ValueError('Invalid CKAN URL')



        self.ckan_url = ckan_url
        self.ckan_token = ckan_token
        self.json_ld = json_ld
        self.headers = {
            'Authorization': ckan_token
        }

    @staticmethod
    def format_ckan_name(input_name):
        formatted_name = input_name.replace(' ', '-')
        formatted_name = re.sub(r'[^a-z0-9-]', '', formatted_name.lower())
        return formatted_name

    def create_organization(self, org_name, org_title, org_description, org_image_url):
        check_org_exists = requests.get(
            f"{self.ckan_url}/api/3/action/organization_show", params={"id": org_name}, headers=self.headers)

        if check_org_exists.status_code == 200:
            return check_org_exists.json()

        org_data = {
            "name": org_name,
            "title": org_title,
            "description": org_description,
            "image_url": org_image_url
        }

        response = requests.post(
            f"{self.ckan_url}/api/3/action/organization_create", json=org_data, headers=self.headers)
        return response.json()

    def import_to_ckan(self):
        org_data = None

        for item in self.json_ld["@graph"]:
            if "@type" in item and item["@type"] == "dcat:Catalog":
                org_data = self.create_organization(
                    self.format_ckan_name(item["@id"].rstrip('/').split("/")[-1]),
                    item.get("dcat:name", ""),
                    item.get("dcat:description", ""),
                    item.get("dcat:image", "")
                )
                break

        if org_data and "success" in org_data and org_data["success"] is True:
            org_name = org_data["result"]["name"]
            print("Organização criada/recuperada com sucesso. Usando a organização com nome:", org_name)

            for item in self.json_ld["@graph"]:
                if "@type" in item:
                    if item["@type"] == "dcat:Dataset":
                        dataset_name = self.format_ckan_name(item["@id"].rstrip('/').split("/")[-1])
                        dataset_data = {
                            "name": dataset_name,
                            "title": item.get("dcterms:title", item.get("dcat:title", dataset_name)),
                            "notes": item.get("dcat:description", ""),
                            "owner_org": org_name,
                            "tags": [{"name": keyword} for keyword in item.get("dcat:keywords", [])],
                        }

                        check_dataset_exists = requests.get(
                            f"{self.ckan_url}/api/3/action/package_show", params={"id": dataset_name}, headers=self.headers)

                        if check_dataset_exists.status_code == 200:
                            dataset_id = check_dataset_exists.json()["result"]["id"]

                            for assoc in item.get("dcat:distribution", []):
                                for dist in self.json_ld["@graph"]:
                                    if dist.get("@id") == assoc.get("@id"):
                                        distribution_name = self.format_ckan_name(
                                            dist["@id"].rstrip('/').split("/")[-1])
                                        distribution_data = {
                                            "package_id": dataset_id,
                                            "name": distribution_name,
                                            "url": dist.get("dcat:contentUrl", ""),
                                            "notes": dist.get("dcat:description", ""),
                                            "owner_org": org_name,
                                            "format": dist.get("dcat:encodingFormat", ""),
                                            "License": dist.get("dcat:license", ""),
                                        }
                                        response = requests.post(
                                            f"{self.ckan_url}/api/3/action/resource_create", json=distribution_data, headers=self.headers)
                                        if response.status_code != 200:
                                            #print("Erro ao criar/atualizar a distribuição:", response.text)
                                            return JsonResponse({'message': 'Error creating/updating distribution'}, status=400)
                        else:
                            response = requests.post(
                                f"{self.ckan_url}/api/3/action/package_create", json=dataset_data, headers=self.headers)

                            if response.status_code == 200:
                                dataset_id = response.json()["result"]["id"]
                                for assoc in item.get("dcat:distribution", []):
                                    for dist in self.json_ld["@graph"]:
                                        if dist.get("@id") == assoc.get("@id"):
                                            distribution_name = self.format_ckan_name(
                                                dist["@id"].rstrip('/').split("/")[-1])
                                            distribution_data = {
                                                "package_id": dataset_id,
                                                "name": distribution_name,
                                                "url": dist.get("dcat:contentUrl", ""),
                                                "notes": dist.get("dcat:description", ""),
                                                "owner_org": org_name,
                                                "format": dist.get("dcat:encodingFormat", ""),
                                                "License": dist.get("dcat:license", ""),
                                            }
                                            response = requests.post(
                                                f"{self.ckan_url}/api/3/action/resource_create", json=distribution_data, headers=self.headers)
                                            if response.status_code != 200:
                                                #print("Erro ao criar a distribuição:", response.text)
                                                return JsonResponse({'message': 'Error creating distribution'}, status=400)
                            else:
                                #print("Erro ao criar o dataset:", response.text)
                                return JsonResponse({'message': 'Error creating dataset'}, status=400)

            #print("Importação concluída!")
            return JsonResponse({'message': 'Import completed successfully'}, status=200)
        else:
            #print("Erro ao criar/recuperar a organização:", org_data)
            return JsonResponse({'message': 'Error creating/retrieving organization'}, status=400)
'''
# Exemplo de uso:
ckan_url = 'http://localhost:5000'
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJQYjNaOEkybDh5NlJHOEpkaEFqSi1IYmRxVVIxM3FqZE5USGhwUDF0Q0k0IiwiaWF0IjoxNjk3ODE4NDY5fQ.biRgaFp2AawuHWqD-DSURY3LApwxU0D7UqPTh_aTm3A'
json_ld = {
    "@context": {
        "dcat": "http://www.w3.org/ns/dcat#",
        "dcterms": "http://purl.org/dc/terms/",
        "foaf": "http://xmlns.com/foaf/0.1/"
    },
    "@graph": [
        {
            "@id": "http://example.org/distribution/descriçao22",
            "@type": "dcat:Distribution",
            "dcat:contentUrl": "https://www.teste.com",
            "dcat:description": "descriçao22",
            "dcat:encodingFormat": "json",
            "dcat:license": "https://creativecommons.org/licenses/by-nc-nd/4.0/"
        },
        {
            "@id": "http://example.org/distribution/descrição-distribuição",
            "@type": "dcat:Distribution",
            "dcat:contentUrl": "https://services.arcgis.com/1dSrzEWVQn5kHHyK/ArcGIS/rest/services/Administracao_Publica/FeatureServer/0/query?where=1%3D1&outFields=*&f=pgeojson",
            "dcat:description": "descrição distribuição",
            "dcat:encodingFormat": "GeoJSON",
            "dcat:license": "https://creativecommons.org/licenses/by-nc/4.0/"
        },
        {
            "@id": "http://example.org/dataset/",
            "@type": "dcat:Dataset",
            "dcat:accessRights": "GrupA",
            "dcat:contactPoint": "contacto",
            "dcat:dateModified": "Novembro 12, 2022, 15:28 (Europe/Lisbon)",
            "dcat:description": "descrição dataset",
            "dcat:distribution": [
                {
                    "@id": "http://example.org/distribution/descrição-distribuição"
                },
                {
                    "@id": "http://example.org/distribution/descriçao22"
                }
            ],
            "dcat:keywords": [
                "tagA",
                "tagB",
                "tagC"
            ],
            "dcat:publisher": "http://lisboaaberta.cm-lisboa.pt",
            "dcat:sample": "https://geodados-cml.hub.arcgis.com/"
        },
        {
            "@id": "http://example.org/catalog",
            "@type": "dcat:Catalog",
            "dcat:creator": "Othmane El Arbaoui",
            "dcat:dataset": [
                {
                    "@id": "http://example.org/dataset/"
                }
            ],
            "dcat:dateModified": "Novembro 12, 2022, 15:28 (Europe/Lisbon)",
            "dcat:description": "descrição catalogo",
            "dcat:language": "https://publications.europa.eu/resource/authority/language/POR",
            "dcat:license": "CC BY-SA",
            "dcat:name": "titulo Catalogo",
            "dcat:publisher": "http://lisboaaberta.cm-lis-lisboa.pt",
            "dcat:title": ""
        }
    ]
}

ckan_importer = CKANImporter(ckan_url, api_key, json_ld)
ckan_importer.import_to_ckan()'''
