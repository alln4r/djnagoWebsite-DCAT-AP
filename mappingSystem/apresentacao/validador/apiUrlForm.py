from django import forms
import requests
import json
import re


class apiUrlForm(forms.Form):
    url = forms.CharField(required=True, label="url", widget=forms.TextInput(
        attrs={"placeholder": "API URL..", "class": "form-control"}))
    urlMetaData = forms.CharField(required=True, label="urlMetaData", widget=forms.TextInput(
        attrs={"placeholder": "METADATA API URL..", "class": "form-control"}))


    def clean(self):
       
        cleaned_data = super().clean()

        url = cleaned_data.get('url')
        urlMetaData = cleaned_data.get('urlMetaData')
       

        if self.data.get("TO_Edit") != True:
            headers = {}
            headersMeta = {}

            # Adiciona cada cabeçalho no dicionário headers={}
            for key, value in self.data.items():
                if key.startswith('keyHeaderData'):
                    # Obtém o valor do input valueHeaderData correspondente
                    value_key = 'valueHeaderData{}'.format(key.split('Data')[1])
                    header_key = self.data.get(key)
                    header_value = self.data.get(value_key)
                    # Adiciona a chave-valor no dicionário headers={}
                    headers.setdefault(header_key, header_value)

                if key.startswith('keyHeaderMeta'):
                    # Obtém o valor do input valueHeaderData correspondente
                    value_keyMeta = 'valueHeaderMeta{}'.format(
                        key.split('Meta')[1])
                    header_keyMeta = self.data.get(key)
                    header_valueMeta = self.data.get(value_keyMeta)
                    # Adiciona a chave-valor no dicionário headers={}
                    headersMeta.setdefault(header_keyMeta, header_valueMeta)
        else:
            headers = json.loads(self.data.get('headers'))
            headersMeta = json.loads(self.data.get('headersMeta'))
            

        
        formData = {"keyHeaderData": headers, "keyHeaderMeta": headersMeta,
                    "flexRadioDefault": self.data.get("flexRadioDefault")}
        formData = json.dumps(formData)
        cleaned_data["keyHeaderData"] = headers.values()
        cleaned_data["keyHeaderMeta"] = headersMeta.values()
        cleaned_data["flexRadioDefault"] = self.data.get("flexRadioDefault")

    # def clean_url(self):

        regex = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        match = re.search(regex, url)
        if not match:
            raise forms.ValidationError(
                {"url": "Enter a valid url starting with http:// or https://"})

        match = re.search(regex, urlMetaData)
        if not match:
            raise forms.ValidationError(
                {"urlMetaData": "Enter a valid url starting with http:// or https://"})

        # if not url.startswith("http://") and not url.startswith("https://"):
        #     raise forms.ValidationError("enter a valid url starting with http:// or https://")

        try:
            # headers = {'Authorization' : 'Bearer {access_token}'}
            # headers = {'Ocp-Apim-Subscription-Key': 'ac533345bca44ec6a811cf5c1721850f' }
            response_API = requests.get(url, headers=headers)
            
            if not (response_API.json() and (isinstance(response_API.json(), list) or isinstance(response_API.json(), dict))):
                raise forms.ValidationError(
                    {"url": "The API returned an unexpected or empty structure."})
        except requests.exceptions.RequestException:
            raise forms.ValidationError(
                {"url": "Could not connect to the given URL"})
        except ValueError:
            raise forms.ValidationError(
                {"url": "The API did not return valid JSON data."})
        
        try:
            # headersMeta = {'Ocp-Apim-Subscription-Key': 'ac533345bca44ec6a811cf5c1721850f'}
            response_metaData = requests.get(urlMetaData, headers=headersMeta)
            if not (response_metaData.json() and (isinstance(response_metaData.json(), list) or isinstance(response_metaData.json(), dict))):
                raise forms.ValidationError({
                    "urlMetaData": "The API returned an unexpected or empty structure."})
        except requests.exceptions.RequestException:
            raise forms.ValidationError(
                {"urlMetaData": "Could not connect to the given URL"})
        except ValueError:
            raise forms.ValidationError(
                {"urlMetaData": "The API did not return valid JSON data."})
        
        if response_API.status_code != 200:
            raise forms.ValidationError({"url": "Code Error: "+str(response_API.status_code)+" » "+response_API.reason +
                                        ' (Please check the provided headers and ensure they have the necessary permissions.)'})

        if response_metaData.status_code != 200:
            raise forms.ValidationError({"urlMetaData": "Code Error: "+response_metaData.status_code+" » "+response_metaData.reason + +
                                        ' (Please check the provided headers and ensure they have the necessary permissions.)'})
        
        try:
            fiwareModelUrl = None
            if self.data.get("flexRadioDefault") == "AirQuality":
                fiwareModelUrl = 'https://smart-data-models.github.io/dataModel.Environment/AirQualityObserved/schema.json'
            if self.data.get("flexRadioDefault") == "device":
                fiwareModelUrl = 'https://smart-data-models.github.io/dataModel.Device/DeviceModel/schema.json'
            if self.data.get("flexRadioDefault") == "Weather":
                fiwareModelUrl = 'https://smart-data-models.github.io/dataModel.Weather/WeatherObserved/schema.json'
            # if self.data.get("flexRadioDefault")=="noneModel":

            response_fiwareModel = {}
            if fiwareModelUrl:
                response_fiwareModel = requests.get(fiwareModelUrl).json()

        except:
            raise forms.ValidationError(
                {"flexRadioDefault": "Could not get firmware model"})

        if not self.is_valid():
            return cleaned_data

        return {"responseAPI": response_API.json(), "response_metaData": response_metaData.json(), "response_fiwareModel": response_fiwareModel, "formData": formData, "url":url, "urlMetaData":urlMetaData }
