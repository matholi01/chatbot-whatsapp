from django.db import models

class Igreja(models.Model):
    nome = models.CharField('Nome', max_length=50)

    def __str__(self):
        return self.nome

class Evento(models.Model):
    nome = models.CharField('Nome', max_length=50)
    data = models.DateTimeField('Data')
    igreja = models.ForeignKey('Igreja', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome + ' | ' + self.data.strftime("%d/%m - %Hh%M") + ' | ' + self.igreja.nome

