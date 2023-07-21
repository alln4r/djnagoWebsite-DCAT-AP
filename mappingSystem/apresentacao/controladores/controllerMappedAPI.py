
from ...apresentacao.validador.addFieldsForm import MyForm
from ...dominio.modelos.customField import CustomField

from django.shortcuts import render
from django.http import JsonResponse
import json


def mappedAPI_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = MyForm(request.POST)

            metaD = {}
            for key, value in request.POST.items():
                if key.startswith('namespace_'):
                    namespace = value
                    term = request.POST.get(f'term_{key.split("_")[1]}')
                    field_name = request.POST.get(
                        f'fieldName_{key.split("_")[1]}')
                    parent = request.POST.get(
                        f'parent_{key.split("_")[1]}')

                    # Cria uma instância de CustomField
                    custom_field = CustomField(
                        user=request.user,
                        namespace=namespace,
                        term=term,
                        parent=parent,
                        fieldName=field_name
                    )

                    # Salva no banco de dados
                    custom_field.save()

                    metaD[field_name] = {
                        "type": namespace,
                        "term": term,
                        "parent": parent
                    }

            return JsonResponse({'metaD': metaD})

        elif request.method == 'GET' and request.is_ajax():
            namespace = request.GET.get('namespace')
            terms = MyForm().get_terms(namespace)
            term_list = [term for term in terms]
            return JsonResponse({'terms': term_list})

        else:
            print("estou aqui")

            # Converter o dicionário de namespaces em uma lista de tuplas (value, label)

            response_list = [
                {"name": "kaka",
                 "id": 1,
                 "sub_responses": [
                         {
                             "id": 0,
                             "name": "kaka111",
                             "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                             "ttl": '@prefix dcat: <http://www.w3.org/ns/dcat#> .'

                                    + '<http://example.org/catalog> a dcat:Catalog ;'
                                     + '   dcat:creator "Othmane El Arbaoui" ;'
                                      + '  dcat:dataset <http://example.org/dataset/> ;'
                                      + '  dcat:dateModified "Novembro 12, 2022, 15:28 (Europe/Lisbon)" ;'
                                      + '  dcat:description "descrição catalogo" ;'
                                      + '  dcat:language "https://publications.europa.eu/resource/authority/language/POR" ;'
                                      + '  dcat:license "CC BY-SA" ;'
                                      + '  dcat:name "titulo Catalogo" ;'
                                      + '  dcat:publisher "http://lisboaaberta.cm-lisboa.pt" ;'
                                      + '  dcat:title "" .'
                         },

                     {
                             "id": 1,
                             "name": "kaka111",
                             "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                             "ttl": "ttl"
                             },
                     {"id": 2,
                             "name": "kaka111",
                             "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                             "ttl": "ttl"
                      },

                     {
                             "id": 3,
                             "name": "kaka111",
                             "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                             "ttl": 'ttl'
                     },

                     {
                             "id": 4,
                             "name": "kaka111",
                             "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                             "ttl": "ttl"
                     }
                 ]
                 },
                {"name": "kaka2",
                 "id": 2,
                 "sub_responses": [
                     {
                         "id": 0,
                         "name": "kaka111",
                         "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                         "ttl": "ttl"
                     }
                 ]
                 },

                {"name": "kaka3",
                 "id": 3,
                 "sub_responses": [
                     {
                         "id": 0,
                         "name": "kaka111",
                         "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                         "ttl": "ttl"
                     }
                 ]
                 },

                {"name": "kaka2",
                 "id": 4,
                 "sub_responses": [
                     {
                         "id": 0,
                         "name": "kaka111",
                         "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                         "ttl": "ttl"
                     }
                 ]
                 },

                {"name": "kaka3",
                 "id": 5,
                 "sub_responses": [
                     {
                         "id": 0,
                         "name": "kaka111",
                         "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                         "ttl": "ttl"
                     }
                 ]
                 },

                {"name": "kaka2",
                 "id": 6,
                 "sub_responses": [
                     {
                         "id": 0,
                         "name": "kaka111",
                         "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                         "ttl": "ttl"
                     }
                 ]
                 },

                {"name": "kaka3",
                 "id": 7,
                 "sub_responses": [
                     {
                         "id": 0,
                         "name": "kaka111",
                         "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                         "ttl": "ttl"
                     }
                 ]
                 },

                {"name": "kaka2",
                 "id": 8,
                 "sub_responses": [
                     {
                         "id": 0,
                         "name": "kaka111",
                         "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                         "ttl": "ttl"
                     }
                 ]
                 },

                {"name": "kaka3",
                 "id": 9,
                 "sub_responses": [
                     {
                         "id": 0,
                         "name": "kaka111",
                         "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                         "ttl": "ttl"
                     }
                 ]
                 },

                {"name": "kaka2",
                 "id": 10,
                 "sub_responses": [
                     {
                         "id": 0,
                         "name": "kaka111",
                         "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                         "ttl": "ttl"
                     }
                 ]
                 },

                {"name": "kaka3",
                 "id": 11,
                 "sub_responses": [
                     {
                         "id": 0,
                         "name": "kaka111",
                         "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                         "ttl": "ttl"
                     }
                 ]
                 },

                {"name": "kaka2",
                 "id": 12,
                 "sub_responses": [
                     {
                         "id": 0,
                         "name": "kaka111",
                         "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                         "ttl": "ttl"
                     }
                 ]
                 },

                {"name": "kaka3",
                 "id": 12,
                 "sub_responses": [
                     {
                         "id": 0,
                         "name": "kaka111",
                         "jsonld": json.dumps({"oi": "oioioi", "number": 123, "lista": ["as", "asd", "sds"]}),
                         "ttl": "ttl"
                     }
                 ]
                 },


            ]

            # return render(request, 'addFields.html', context)
            return render(request, 'mappedAPI.html', {'response_list': response_list})
