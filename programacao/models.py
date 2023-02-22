from django.db import models
from django.contrib.auth.models import User
import unicodedata

# Representa uma igreja do campus ADMJI
class Agenda(models.Model):
    # Duas igrejas não podem ter o mesmo nome, por isso o campo "nome" é uma chave primária.
    id_calendario = models.TextField('ID do Calendário', primary_key=True)
    igreja = models.CharField('Igreja', max_length=100,unique=True,
    help_text='Nome da igreja que o calendário está vinculado.')
    # Campo que guarda o nome da igreja utilizando apenas caracteres ASCII e sem espaços em branco.
    igreja_normalizado = models.CharField(max_length=100,blank=True, editable=False, unique=True)

    def __str__(self):
        return self.igreja

    def save(self, *args, **kwargs):

        # Testa se o nome da igreja possui acentos ou caracteres que não estão na tabela ASCII, como o "ç"
        if self.igreja.encode('ascii','ignore').decode('ascii','ignore') != self.igreja:
            # Se houver caracteres que não estão na tabela ASCII, utilizamos 
            # o campo especial para guardar o nome com os caracteres substituídos 
            # por caracteres da tabela ASCII.
            self.igreja_normalizado = unicodedata.normalize('NFKD', self.igreja).encode('ascii', 'ignore').decode('utf8')

        # Retira os espaços em branco do nome caso tenha e salva no campo especial
        if ' ' in self.igreja_normalizado:
            self.igreja_normalizado = self.igreja_normalizado.replace(' ','')

        return super().save(*args, **kwargs)

class Administrador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Todo administrador é relacionado a uma igreja especifica
    # Campo devido a relação "One-To-Many" (Um para muitos) com o model Igreja
    agenda = models.ForeignKey('Agenda', on_delete=models.CASCADE)

    def __str__(self):
        return self.agenda.igreja

