from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from ...apresentacao.validador.apiUrlForm import apiUrlForm

from ...dominio.modelos.fieldMapping import FieldMapping
from ...dominio.modelos.customField import CustomField
from ...dominio.modelos.mappedApi import MappedApi

from ...dominio.servicos.tratarJson_Impl import TratarJson
from ...dominio.servicos.mapIntermediateModel_Impl import MapIntermediateModel
#from ...dominio.servicos.MapJsonToDCATFiles import MapJsonToDCATFiles
from ...dominio.servicos.toDCAT_AP import ToDCAT_AP
import json
import os

def home(request):
    if not request.user.is_authenticated:
        print("_____________________nÃO eSTÁ LOGADO_______________________________________")
        return redirect('login')
        
    else:

        ##mostrar a pagina com o formulario inicial
        if request.method == "GET" and not request.is_ajax():
            form = apiUrlForm()
            return render(request,'home.html', {'form': form, 'formData':{}})

        if request.method == "POST" and not request.is_ajax():
            form = apiUrlForm(request.POST)
            
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
                
                # Print the loaded data
               
                apiModelFields, vkApiData = TratarJson().fieldsToShowInGUI(apiData)
               
                existingLinks = MapIntermediateModel().getMappedLinks(intermediateModelFields, schemeMetaDataIntermediate, apiMetaData, apiModelFields[0])
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
                existingLinks=json.dumps(existingLinks)

              
                # Filtra as instâncias de CustomField relacionadas ao user logado
                customFields = CustomField.objects.filter(user=request.user)

                # Seleciona apenas a coluna 'fieldName'
                fieldNames = json.dumps(list( customFields.values('fieldName','id') ))

                print(fieldNames)

                
                return render(request,'home.html', {
                                                        'form': form, 
                                                        'apiModelFields':json.dumps(apiModelFields[0]), 
                                                        "vkApiData":json.dumps(vkApiData[0]), 
                                                        "existingLinks":existingLinks, 
                                                        "intermediateModelFields":intermediateModelFields, 
                                                        "formData":formData, 
                                                        "fieldNames":fieldNames
                                                    })
            else:
                return render(request,'home.html', {'form': form})   

        if request.method == "POST" and request.is_ajax(): #save
            print("ajaxxxxxxxx")
            apiData = request.session.get('apiData')
            vlk= request.session.get('vkApiData') 
            intermediateModelFields = request.session.get('intermediateModelFields') 
            #print(vlk)
            linksWithpath=json.loads( request.POST.get('links' ) )
            #print(APIdata)
           
            modelData = MapIntermediateModel().getMappedData(linksWithpath['links'],vlk)
            #print(modelData) # é uma lista de objetos com os valores da api de dados com os campos do interior do sistema
            '''for mdlData in modelData: 
                intermediateModelData = MapIntermediateModel().getIntermediateModelData(mdlData, request.session.get('schemeMetaDataIntermediate'))
                #jsonFile=ckanEXT.Extract().run()
                #_____________________________________
              
                dcatTTL, dcatJsonLD = ToDCAT_AP().run(intermediateModelData)

                print(dcatJsonLD)'''
            intermediateModelData = MapIntermediateModel().getIntermediateModelData(modelData[0], request.session.get('schemeMetaDataIntermediate'))
            dcatTTL, dcatJsonLD = ToDCAT_AP().run(intermediateModelData)

            #dar save dcatTTL, dcatJsonLD, request.POST.get('links' )
           
            print("_______________________")
           
            formData=json.loads(request.session.get('formData'))          
            # Cria uma instância de FieldMapping
            field_mapping = FieldMapping.objects.create(
                user=request.user,
                my_json_object = request.POST.get('links' ),
                #created_at = models.DateTimeField(auto_now_add=True)
                #updated_at = models.DateTimeField(auto_now=True)
                data_api_link = request.session.get('url'),
                metadata_api_link = request.session.get('urlMetaData'),
                
                data_api_header = formData['keyHeaderData'],
                metadata_api_header = formData['keyHeaderMeta'],
                #custom_fields = request.session.get('id_list_CustomFields')
                #request.session.get('formData')['flexRadioDefault']
                #mappedApiID = mapped_api #referencia com id
            )

            #id_list_CustomFields =  request.session.get('id_list_CustomFields')
            
            print(intermediateModelFields)
            print("____________-----------------_______________")
            print(request.session.get('FieldsName'))
           
            if(request.session.get('FieldsName') is not None):
                found_values = [item for item in request.session.get('FieldsName') if item in intermediateModelFields]
                if found_values:
                    custom_fields = CustomField.objects.filter(fieldName__in=found_values)
                    field_mapping.custom_fields.set(custom_fields)

            # guardar na BD
            field_mapping.save()
            if not field_mapping.name:
                field_mapping.name = f"API_{field_mapping.id}"
     

            # guardar o objeto novamente para persistir as alterações
            field_mapping.save()

            mapped_api = MappedApi(
                #name = o name está a ser definido no modelo, é para ir a null
                dcat_ttl = dcatTTL,
                dcat_jsonld = dcatJsonLD,
                fieldMappingID = field_mapping
            )

            mapped_api.save()

            return HttpResponse(  json.dumps( {'resp': "dentro ajaxxxxxxx", "apiData": apiData, "vkApiData": vlk, "inputMDL": intermediateModelFields } ) )

        
        if request.method == "GET" and request.is_ajax(): #add

            #intermediateModelFields  é os campos, só os nomes dos campos
            #schemeMetaDataIntermediate o scheme dos campos

            #o intermediateModelFields concatnar os campos novos q vao ser rececionados
            #o schemeMetaDataIntermediate para os campos novos tem q ser consultado nas base de dados
            # depois e´correr o existingLinks e contactar com o existing links antigos

            id_list_selected = json.loads( request.GET.get('id_list_selected') )
            #request.session['id_list_CustomFields'] = id_list_selected
            apiModelFields = request.session.get('apiModelFields')
            apiMetaData= request.session.get('apiMetaData') 
            intermediateModelFields = request.session.get('intermediateModelFields')
           
            selectedFields = CustomField.objects.filter(user=request.user, id__in=id_list_selected)

            request.session['FieldsName'] = list( selectedFields.values_list('fieldName', flat=True))
            schemaMetaCustomFields = {}
            intemediateCustomFields=[]

            for obj in selectedFields:
                if obj.fieldName not in intermediateModelFields:
                    schemaMetaCustomFields[obj.fieldName] = {
                            "type": obj.namespace,
                            "parent": obj.parent
                    }
                    intemediateCustomFields.append(obj.fieldName)
           
            scheme_meta_data = request.session.get('schemeMetaDataIntermediate', {})  # Obtém o valor associado à chave 'schemeMetaDataIntermediate' ou um dicionário vazio se a chave não existir

            scheme_meta_data.update(schemaMetaCustomFields)  # Atualiza o valor com os dados fornecidos em schemaMetaCustomFields

            request.session['schemeMetaDataIntermediate'] = scheme_meta_data  # Atribui o valor atualizado de volta à chave 'schemeMetaDataIntermediate' na sessão
            request.session.modified = True  # Marca a sessão como modificada
        
           
            existingLinks = MapIntermediateModel().getMappedLinks(intemediateCustomFields, schemaMetaCustomFields, apiMetaData, apiModelFields[0])
            #list extend list
            intermediateModelFields += intemediateCustomFields
            
            links=json.loads( request.GET.get('links' ) )
            #list extend list
            existingLinks= links + existingLinks
           

            return JsonResponse({
                                    'apiModelFields':apiModelFields[0], 
                                    "existingLinks":existingLinks, 
                                    "intermediateModelFields":intermediateModelFields, 
                                })