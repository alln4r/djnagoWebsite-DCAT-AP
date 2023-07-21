
from ...apresentacao.validador.addFieldsForm import MyForm
from ...dominio.modelos.customField import CustomField

from django.shortcuts import render
from django.http import JsonResponse


def add_field_view(request):
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

            form = MyForm()

            # return render(request, 'addFields.html', context)
            return render(request, 'addFields.html', {'form': form})
