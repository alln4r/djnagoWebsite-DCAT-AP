from django.db import models
from django.contrib.auth.models import User



class FieldMapping(models.Model):
    name = models.CharField(max_length=400, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data_api_link = models.URLField()
    metadata_api_link = models.URLField()
    data_api_header = models.TextField()
    metadata_api_header = models.TextField()     
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    '''
    def save(self, *args, **kwargs):
        
        if not self.name:
            print()
            super().save(*args, **kwargs)
            self.name = f"API_{self.id}"
          
        super(FieldMapping, self).save(*args, **kwargs)
    '''       
    
    # def as_json(self):
    #    import json
    #    return json.loads(self.my_json_object)


# Realize a migração: Depois de criar o modelo, você precisa criar uma migração usando o
# comando python manage.py makemigrations e, em seguida, aplique a migração usando o comando python manage.py migrate.

# $ python manage.py makemigrations modelos
# $ python manage.py migrate

# usar o sqlite python manage.py dbshell
# .tables

'''
como fazer select:

# Selecionar todos os objetos do modelo
todos_objetos = MinhaNovaTabela.objects.all()

# Selecionar um objeto do modelo com id igual a 1
objeto = MinhaNovaTabela.objects.get(id=1)

# Selecionar objetos do modelo que atendem a determinados critérios
objetos_filtrados = MinhaNovaTabela.objects.filter(usuario__username='johndoe')


como inserir:

# Criar uma nova instância do modelo
novo_objeto = MinhaNovaTabela(usuario=user, campo1='valor1', campo2='valor2')

# Salvar o novo objeto no banco de dados
novo_objeto.save()



como atualizar:

# Selecionar o objeto a ser atualizado
objeto = MinhaNovaTabela.objects.get(id=1)

# Alterar o valor de um campo
objeto.campo1 = 'novo_valor'

# Salvar as alterações no banco de dados
objeto.save()



como eliminar:

# Selecionar o objeto a ser excluído
objeto = MinhaNovaTabela.objects.get(id=1)

# Excluir o objeto do banco de dados
objeto.delete()

'''
