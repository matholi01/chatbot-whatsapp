from django.db import models
from django.contrib.auth.models import User
import unicodedata

# Representa uma igreja do campus ADMJI
class Igreja(models.Model):
    # Duas igrejas não podem ter o mesmo nome, por isso o campo "nome" é uma chave primária.
    nome = models.CharField('Nome', max_length=50, primary_key=True,
    help_text='Nome da igreja. Pode ser um nome simbólico que faça sentido, como por exemplo "Matriz".')
    # Campo que guarda o nome da igreja utilizando apenas caracteres ASCII e sem espaços em branco.
    nome_normalizado = models.CharField(max_length=50,blank=True,unique=True, editable=False)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):

        # Testa se o nome da igreja possui acentos ou caracteres que não estão na tabela ASCII, como o "ç"
        if self.nome.encode('ascii','ignore').decode('ascii','ignore') != self.nome:
            # Se houver caracteres que não estão na tabela ASCII, utilizamos 
            # o campo especial para guardar o nome com os caracteres substituídos 
            # por caracteres da tabela ASCII.
            self.nome_normalizado = unicodedata.normalize('NFKD', self.nome).encode('ascii', 'ignore').decode('utf8')

        # Retira os espaços em branco do nome caso tenha e salva no campo especial
        if ' ' in self.nome_normalizado:
            self.nome_normalizado = self.nome_normalizado.replace(' ','')

        return super().save(*args, **kwargs)


# Representa um evento na programação
class Evento(models.Model):
    nome = models.CharField('Nome', max_length=100,
    help_text='Nome do evento. Ex: "Culto de Adoração".')
    data = models.DateTimeField('Data')
    # Todo evento é relacionado a uma igreja especifica
    # Campo devido a relação "One-To-Many" (Um para muitos) com o model Igreja
    igreja = models.ForeignKey('Igreja', on_delete=models.CASCADE,
    help_text='Igreja onde o evento ocorrerá.')

    # Se for o início de uma hora x, ou seja, 0 minutos de uma hora específica,
    # não é mostrado os minutos.
    def __str__(self):
        data_evento = self.data
        if data_evento.minute == 0:
            return self.nome + ' | ' + self.data.strftime("%d/%m - %Hh") + ' | ' + self.igreja.nome
        else:
            return self.nome + ' | ' + self.data.strftime("%d/%m - %Hh%M") + ' | ' + self.igreja.nome


class Administrador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Todo administrador é relacionado a uma igreja especifica
    # Campo devido a relação "One-To-Many" (Um para muitos) com o model Igreja
    igreja = models.ForeignKey('Igreja', on_delete=models.CASCADE)

    def __str__(self):
        return self.igreja.nome

