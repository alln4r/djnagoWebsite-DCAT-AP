from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import apiUrlForm
import json
import sys, os, pathlib

from .models import InputModel

BASE_DIR = pathlib.Path(__file__).parent.resolve()
path=os.path.join(BASE_DIR, "servicos")
sys.path.insert(0, path )

from tratarJson_Impl import tratarJson
from mapDataToMyModel_Impl import mapDataToMyModel
from MapJsonToDCATFiles import MapJsonToDCATFiles

def home(request):
    if not request.user.is_authenticated:
        #return redirect('login')
        print("_____________________nÃO eSTÁ LOGADO_______________________________________")
    
    if request.is_ajax():
        print("ajaxxxxxxxx")
        dt = request.session.get('data') 
        inMdl = request.session.get('InModel') 
        Vlk= request.session.get('Vk') 
        
        #print(Vlk["DeviceModel"])

       
      
        linksWithpath=json.loads( request.POST.get('links' ) )
       
        modelData = mapDataToMyModel().mapDataTo(linksWithpath,dt,Vlk)

        #jsonFile=ckanEXT.Extract().run()
        #_____________________________________
        MapJsonToDCATFiles(modelData).doMap()

        return HttpResponse(  json.dumps( {'resp': "dentro ajaxxxxxxx", "data": dt, "Vk": Vlk, "inputMDL": inMdl } ) )
        #return HttpResponse({'resp': "dentro ajaxxxxxxx"}) #render(request,'home.html', {'resp': "dentro ajaxxxxxxx"})

    
    data={}
    inputMdl={}
    Vk={}
    existingLinks=[]
    InModel=[]
    if request.method == "POST":
        form, data, inputMdl, Vk, existingLinks,InModel = process(request)        
    elif request.method == "GET":
        form = apiUrlForm()
    else:
        raise NotImplementedError
  

    return render(request,'home.html', {'form': form, 'data':data, 'inputMdl':inputMdl, "Vk":Vk, "existingLinks":existingLinks, "InModel":InModel})

def process(request):

    form = apiUrlForm(request.POST)
 
    data=None
    inputMdl=None
    Vk=None
    existingLinks=None
    InModel=None
  

    if form.is_valid():
    #if data:   
        #url=form.cleaned_data.get('url')
        dt=form.cleaned_data
        data=dt["responseAPI"]
        APImetaData=dt["response_metaData"]
   
        #esta é o schema do model device
        #schema={
                 

        #digamos que esta é minha esquema extendida, o que preciso
        #extendedSchema={
	
        #APImetaData={                          

        request.session['data'] = data

        InModel = mapDataToMyModel().MyInputModel(schema,extendedSchema)

        data, Vk =tratarJson().jsonToPrintNaGUI(data)
        existingLinks = mapDataToMyModel().mapTo(InModel,schema,extendedSchema, APImetaData,data, Vk)
        existingLinks=json.dumps(existingLinks)

        request.session['InModel'] = InModel
        #não passar para cima
        InModel=json.dumps(InModel)
        ###############################3
        #data, Vk =tratarJson().jsonToPrintNaGUI(data)        
        data=json.dumps(data)
        
        request.session['Vk'] = Vk
        Vk = list(Vk.values())        
        Vk=json.dumps(Vk)
       
        
        inputMdl = InputModel().__dict__
        request.session['inputMdl'] = inputMdl
        inputMdl = list(inputMdl.keys())
        
        inputMdl=json.dumps(inputMdl)
        print(inputMdl)
        
        #NestedDictValues(data,Vkeys,listKey,listLastKeys)
        #data=json.dumps(listLastKeys)
        '''print(response_API.status_code)
        data = response_API.text
        parse_json = json.loads(data)
        active_case = parse_json['Andaman and Nicobar Islands']['districtData']['South Andaman']['active']
        print("Active cases in South Andaman:", active_case)'''

        #print("______________dentro do process "+str(data))
        #print(form)
    #return data
    return form, data, inputMdl, Vk, existingLinks, InModel
#process()

'''
def NestedDictValues(d,Vkeys,listKey,listLastKeys):

    for k,v in d.items():
        #print(v)
        listKey.append(k)
        if isinstance(v, dict):
            #print(listKey)
            NestedDictValues(v,Vkeys,listKey,listLastKeys)
        else:
            listLastKeys.append(k)
            value=list(listKey)
            Vkeys.update({v:value})
            listKey.pop()


def home(request):
    return home(request)
    if request.method == "POST":
        print("dentro do post")
        form = apiUrlForm(request.POST)
       
        if form.is_valid():
            pass
        
    elif request.method == "GET":
        form = apiUrlForm()
    else:
        raise NotImplementedError
    return render(request,'home.html', {'form': form})
'''
