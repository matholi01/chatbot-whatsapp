from django.db import models

class Programacao(models.Model):
    nome = models.CharField('Nome', max_length=50)
    data = models.DateField('Data', auto_now_add=True)

def __str__(self):
    return self.nome
