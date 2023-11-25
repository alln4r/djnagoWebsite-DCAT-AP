from django.db import models
from .fieldMapping import FieldMapping
from .customField import CustomField


class MappedApi(models.Model):    
    name = models.CharField(max_length=400, null=False)    
    my_json_object = models.TextField()
    dcat_ttl = models.TextField()
    dcat_jsonld = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fieldMappingID = models.ForeignKey(FieldMapping, related_name='field_mapping', on_delete=models.CASCADE)
    custom_fields = models.ManyToManyField(CustomField)

    def save(self, *args, **kwargs):
        if not self.name:
            super().save(*args, **kwargs)
            self.name = f"Edit_{self.id}"
        super(MappedApi, self).save(*args, **kwargs)


# Criar uma nova instância do modelo
# novo_objeto = CustomField(user=user, namespace='valor1', term='valor2', parent="", fieldName="")

# Salvar o novo objeto no banco de dados
# novo_objeto.save()