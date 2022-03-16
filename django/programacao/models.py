from django.db import models
from django.contrib.auth.models import User

# Representa uma igreja do campus ADMJI
class Igreja(models.Model):
    nome = models.CharField('Nome', max_length=50)

    def __str__(self):
        return self.nome

# Representa um evento na programação
class Evento(models.Model):
    nome = models.CharField('Nome', max_length=50)
    data = models.DateTimeField('Data')
    # Todo evento é relacionado a uma igreja especifica
    # Campo devido a relação "One-To-Many" (Um para muitos) com o model Igreja
    igreja = models.ForeignKey('Igreja', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome + ' | ' + self.data.strftime("%d/%m - %Hh%M") + ' | ' + self.igreja.nome


class Administrador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Todo administrador é relacionado a uma igreja especifica
    # Campo devido a relação "One-To-Many" (Um para muitos) com o model Igreja
    igreja = models.ForeignKey('Igreja', on_delete=models.CASCADE)

    def __str__(self):
        return self.igreja.nome

