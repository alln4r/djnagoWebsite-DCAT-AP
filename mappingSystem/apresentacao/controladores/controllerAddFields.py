
from ...apresentacao.validador.addFieldsForm import MyForm
from ...dominio.modelos.customField import CustomField

from django.shortcuts import redirect, render
from django.http import JsonResponse


def add_field_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST' and request.is_ajax():
            
            metaD = {}
            for key, value in request.POST.items():
                if not value:
                    return JsonResponse({'message': 'All fields must have a defined value.'}, status=400)
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

                    # guardar na BD
                    custom_field.save()

                    metaD[field_name] = {
                        "type": namespace,
                        "term": term,
                        "parent": parent
                    }

            return JsonResponse({'message': 'Field/s created successfully!'})

        elif request.method == 'GET' and request.is_ajax():
            namespace = request.GET.get('namespace')
            terms = MyForm().get_terms(namespace)
            term_list = [term for term in terms]
            return JsonResponse({'terms': term_list})

        else:
            # Converter o dicionário de namespaces em uma lista de tuplas (value, label)

            form = MyForm()

            # return render(request, 'addFields.html', context)
            return render(request, 'addFields.html', {'form': form})
