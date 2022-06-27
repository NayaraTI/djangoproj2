from django.contrib import admin

# Register your models here.
from django.contrib import admin 
from .models import Pessoa


class PessoaAdmin(admin.ModelAdmin):
    list_display = ( 'nome', 'idade', 'sexo', 'salario')
    list_display_links = ('nome', 'idade')
    # list_filter = ('nome', 'sobrenome')
    list_per_page = 10
    search_fields = ('nome', 'idade', 'salario')
    #list_editable = ('salario')


admin.site.register(Pessoa, PessoaAdmin)