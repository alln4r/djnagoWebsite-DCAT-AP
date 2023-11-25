from django import forms
from rdflib import Graph, RDF


class MyForm(forms.Form):

    # List of namespaces
    namespaces = {
        "DCTERMS": "http://purl.org/dc/terms/",
        "FOAF": "http://xmlns.com/foaf/0.1/",
        "SKOS": "http://www.w3.org/2004/02/skos/core#",
        "Schema.org": "http://schema.org/",
        "PROV-O": "http://www.w3.org/ns/prov#",
        # Adicione os demais namespaces aqui
    }

    # namespace_choices = [(label, value) for label, value in namespaces.items()]

    namespace_0 = forms.ChoiceField(
        choices=[(label, value) for label, value in namespaces.items()],
        widget=forms.Select(
            attrs={'class': 'namespace-select form-select'})
    )
    term_0 = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'term-select form-select'}))
    fieldName_0 = forms.CharField(
        max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    parent_0 = forms.ChoiceField(choices=[("Catalog", "Catalog"), ("Dataset", "Dataset"), ("Distribution", "Distribution")], widget=forms.Select(
        attrs={'class': 'parent-select form-select'}))

    def is_valid_(self):
        # Execute as validações personalizadas
        # Inicialize o dicionário de erros com chaves vazias para todos os campos relevantes
        errors = {}
        
        for key, value in self.data.items():
            if key.startswith('namespace_') and not value:
                if key not in errors:
                    errors[key] = []
                errors.setdefault(key, []).append('Namespace is required.')

            if key.startswith('term_') and not value:
                if key not in errors:
                    errors[key] = []
                errors.setdefault(key, []).append('Term is required.')

            if key.startswith('fieldName_') and not value:
                if key not in errors:
                    errors[key] = []
                errors.setdefault(key, []).append('Field name is required.')

            if key.startswith('parent_') and not value:
                if key not in errors:
                    errors[key] = []
                errors.setdefault(key, []).append('Parent is required.')
        if len(errors)>0:
            self.is_valid==False
        return errors

    def get_terms(self, namespace, prefix=''):
        g = Graph()
        namespace_uri = self.namespaces[namespace]
        g.parse(namespace_uri)
        terms = set()
        for s, p, o in g.triples((None, RDF.type, None)):
            if str(s).startswith(namespace_uri):
                terms.add(s.lstrip(namespace_uri))
        return terms
