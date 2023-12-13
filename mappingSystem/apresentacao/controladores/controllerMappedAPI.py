
import json
import os

from mappingSystem.dominio.servicos.mapIntermediateModel_Impl import MapIntermediateModel
from mappingSystem.dominio.servicos.tratarJson_Impl import TratarJson

from ...dominio.modelos.customField import CustomField
from ...apresentacao.validador.apiUrlForm import apiUrlForm
from ...dominio.modelos.fieldMapping import FieldMapping
from ...dominio.servicos.toCKAN import CKANImporter
from ...dominio.modelos.mappedApi import MappedApi

from django.shortcuts import redirect, render
from django.http import JsonResponse, QueryDict
from django.db import transaction


def mappedAPI_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        
        if request.method == 'POST' and request.is_ajax():
            type = request.POST.get('type')
            if type=="TO_CKAN":
                # Obtenha os dados do formulário
                ckan_token = request.POST.get('ckanToken')
                ckan_url = request.POST.get('ckanURL')

                
            
                dcat_jsonld = MappedApi.objects.get(id=request.POST.get('subResponseId')).dcat_jsonld

                try:
                    ckan_importer = CKANImporter(ckan_url, ckan_token, json.loads(dcat_jsonld))
                    # Continue o processamento normal se a inicialização ocorrer sem erros
                except ValueError as e:
                    # Se ocorrer um erro, capture a exceção ValueError e retorne uma resposta de erro
                    error_message = str(e)
                    response_data = {'message': error_message}
                    return JsonResponse(response_data, status=400)

                #ckan_importer = CKANImporter(ckan_url, ckan_token, json.loads(dcat_jsonld) )

                return ckan_importer.import_to_ckan()
                
            
            if type=="TO_DELETE_MAP":
                
                try:
                    with transaction.atomic():
                        # Get the MappedApi record to delete
                        mapped_api = MappedApi.objects.get(id= request.POST.get('subResponseId'))
                        
                        # Check if the field_id is unique in MappedApi
                        field_id_count = MappedApi.objects.filter(fieldMappingID=mapped_api.fieldMappingID).count()
                        
                        if field_id_count == 1:
                            # If the field_id is unique, delete the corresponding OtherTable record
                            FieldMapping.objects.get(id=mapped_api.fieldMappingID_id).delete()
                        else:
                            # Delete the MappedApi record
                            mapped_api.delete()
                        
                        return JsonResponse({'message': "Record deleted successfully."})
                
                except MappedApi.DoesNotExist:
                    return JsonResponse({'message': "Record not found. It couldn't be deleted."}, status=400)
                except FieldMapping.DoesNotExist:
                    return JsonResponse({'message': "Record not found."}, status=400)
                except Exception as e:
                    return JsonResponse({'message': f"An error occurred: {str(e)}"}, status=500)
                
        elif request.method == 'POST' and request.POST.get('type') =="TO_EDIT_MAP":

            # Get the MappedApi record to delete
            mapped_api = MappedApi.objects.get(id= request.POST.get('subResponseId'))
            field_mapping = FieldMapping.objects.get(id=mapped_api.fieldMappingID_id)
            existingLinks = json.loads(mapped_api.my_json_object)

            
            custom_querydict = QueryDict('', mutable=True)
            custom_querydict.update( {"url": field_mapping.data_api_link, 
                                "urlMetaData": field_mapping.metadata_api_link,
                                "csrfmiddlewaretoken": request.POST["csrfmiddlewaretoken"],
                                "headers": field_mapping.data_api_header,
                                "headersMeta": field_mapping.metadata_api_header, 
                                "flexRadioDefault": existingLinks["flexRadioDefault"], 
                                "TO_Edit":True
                                })
           
            
            form = apiUrlForm(custom_querydict)
                      
            if form.is_valid():
            
                apiResponse=form.cleaned_data
                apiData = apiResponse["responseAPI"]
                apiMetaData = apiResponse["response_metaData"]
                schemeFiwareModel = apiResponse["response_fiwareModel"]
                formData = apiResponse["formData"]


                with open(os.path.join(os.path.dirname(__file__), 'doc', 'metaDataIntermediate.json'), "r") as f:
                    # Load the JSON data from the file
                    schemeMetaDataIntermediate = json.load(f)

                intermediateModelFields = MapIntermediateModel().makeIntermediateModelFields(schemeFiwareModel,schemeMetaDataIntermediate)

                # intermediateModelFields tem todos os campos que vao ser apresentados do lado direito 
                # ou seja os campos escolhidos para o dcat-ap e foram unidos sem repetição com os campos dos mapeamentos existente na bd        
                values_with_to = [item['to'] for item in existingLinks['links'] if 'to' in item]
                intermediateModelFields = list(set(intermediateModelFields) | set(values_with_to))
                
                # Print the loaded data
               
                apiModelFields, vkApiData = TratarJson().fieldsToShowInGUI(apiData)


                values_with_from = [item['from'] for item in existingLinks['links'] if 'from' in item]
                apiModelFields = list(set(apiModelFields[0]) | set(values_with_from))
                apiModelFields=[apiModelFields]
               
                #existingLinks = MapIntermediateModel().getMappedLinks(intermediateModelFields, schemeMetaDataIntermediate, apiMetaData, apiModelFields[0])
                request.session['apiData'] = apiData
                request.session['vkApiData'] = vkApiData
                request.session['intermediateModelFields'] = intermediateModelFields
                request.session['apiModelFields'] = apiModelFields
                request.session['apiMetaData'] = apiMetaData
                request.session['schemeMetaDataIntermediate'] = schemeMetaDataIntermediate

                request.session['urlMetaData'] = apiResponse["urlMetaData"]
                request.session['url'] = apiResponse["url"]
                request.session['formData'] = apiResponse["formData"]
                #
             
                #return render(request,'home.html', {'data':data})
                intermediateModelFields=json.dumps(intermediateModelFields)
                #apiModelFields=json.dumps(apiModelFields)
                #vkApiData=json.dumps(vkApiData)
                DefValueLinks = json.dumps(existingLinks['linksByDefValue'])
                existingLinks=json.dumps(existingLinks['links'])



                # Filtra as instâncias de CustomField relacionadas ao user logado
                customFields = CustomField.objects.filter(user=request.user)

                # Seleciona apenas a coluna 'fieldName'
                fieldNames = json.dumps(list( customFields.values('fieldName','id') ))

                             
                return render(request,'home.html', {
                                        'form': form, 
                                        'apiModelFields':json.dumps(apiModelFields[0]), 
                                        "vkApiData":json.dumps(vkApiData[0]), 
                                        "existingLinks": existingLinks, 
                                        "intermediateModelFields":intermediateModelFields, 
                                        "formData":formData, 
                                        "fieldNames":fieldNames, 
                                        "edit_sub_id": request.POST.get('subResponseId'),
                                        "DefValueLinks": DefValueLinks
                                    })
        else:           
            response_list = []
            # Recupere todas as linhas do modelo A
            field_mapping = FieldMapping.objects.filter(user=request.user).order_by('-id')
            

            # Itere sobre as linhas do modelo fieldMapping
            for fieldMapping_row in field_mapping:
                a={
                    "name": fieldMapping_row.name,
                    "id": fieldMapping_row.id,
                    "sub_responses": []
                }
                
                # Acesse as linhas relacionadas da tabela mappedApi usando a relação 'field_mapping'
                mappedApi_items = fieldMapping_row.field_mapping.all().order_by('-id')
                if mappedApi_items:
                    for mappedApi_row in mappedApi_items:
                        a["sub_responses"].append({
                            "id": mappedApi_row.id,
                            "name": mappedApi_row.name,
                            "jsonld": mappedApi_row.dcat_jsonld,
                            "ttl": mappedApi_row.dcat_ttl
                        })
                    
                    response_list.append(a)
   
            # return render(request, 'addFields.html', context)
            return render(request, 'mappedAPI.html', {'response_list': response_list})
