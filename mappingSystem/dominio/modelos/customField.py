from django.contrib.auth.models import User
from django.db import models


class CustomField(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    namespace = models.CharField(max_length=100, null=True)
    term = models.CharField(max_length=100, null=True)
    parent = models.CharField(max_length=100, null=True)
    fieldName = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"CustomField: {self.fieldName}"


# Criar uma nova instância do modelo
# novo_objeto = CustomField(user=user, namespace='valor1', term='valor2', parent="", fieldName="")

# Salvar o novo objeto no banco de dados
# novo_objeto.save()
