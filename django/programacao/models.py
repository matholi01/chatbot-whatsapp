from django.db import models

class Evento(models.Model):
    nome = models.CharField('Nome', max_length=50)
    data = models.DateTimeField('Data')

    def __str__(self):
        return self.nome + ' | ' + self.data.strftime("%d/%m - %Hh%M")
