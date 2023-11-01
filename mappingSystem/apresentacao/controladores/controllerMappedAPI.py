
import json
from ...dominio.modelos.fieldMapping import FieldMapping
from ...dominio.servicos.toCKAN import CKANImporter
from ...dominio.modelos.mappedApi import MappedApi

from django.shortcuts import redirect, render
from django.http import JsonResponse
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
                        print(mapped_api.fieldMappingID)
                        
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
                
            
                    
            if type=="TO_EDIT_MAP":
                return JsonResponse({'type': type}) 
        else:           
            response_list = []
            # Recupere todas as linhas do modelo A
            field_mapping = FieldMapping.objects.filter(user=request.user)
            

            # Itere sobre as linhas do modelo fieldMapping
            for fieldMapping_row in field_mapping:
                a={
                    "name": fieldMapping_row.name,
                    "id": fieldMapping_row.id,
                    "sub_responses": []
                }
                
                # Acesse as linhas relacionadas da tabela mappedApi usando a relação 'field_mapping'
                mappedApi_items = fieldMapping_row.field_mapping.all()
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
