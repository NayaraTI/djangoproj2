from django.shortcuts import render
from .models import Pessoa
from django.views.decorators.csrf import csrf_protect

def listagem(request):
	pessoas = Pessoa.objects.all()
	return render(request, 'listagem.html', {'pessoas': pessoas})

def selecao(request, id=0):
	pessoa = Pessoa.objects.get(id=id)
	return render(request, 'listagem.html', {'pessoas': [pessoa]})

_campo = ''
def ordenacao(request, campo='id'):
	global _campo
	if campo == _campo:
		pessoas = Pessoa.objects.all().order_by(campo).reverse()
		_campo = ''
	else:
		pessoas = Pessoa.objects.all().order_by(campo)
		_campo = campo
	return render(request, 'listagem.html', {'pessoas': pessoas})

@csrf_protect
def consulta(request):
	consulta = request.POST.get('consulta')
	campo = request.POST.get('campo')

	if campo == 'nome':
		pessoas = Pessoa.objects.filter(nome__contains=consulta)
	elif campo == 'idade':
		pessoas = Pessoa.objects.filter(idade__contains=consulta)
	elif campo == 'sexo':
		pessoas = Pessoa.objects.filter(sexo__contains=consulta)
	elif campo == 'salario':
		if consulta.find(',') > 0 or consulta.find('.') > 0:
			consulta = float(consulta.replace(',', '.'))
		pessoas = Pessoa.objects.filter(salario__contains=consulta)
	else:
		pessoas = Pessoa.objects.all()

	return render(request, 'listagem.html', {'pessoas': pessoas})

def insercao(request):
	return render(request, 'insercao.html')

@csrf_protect
def salvar_insercao(request):
	Nome = request.POST.get('nome')
	Idade = request.POST.get('idade')
	Sexo = request.POST.get('sexo')
	Salario = request.POST.get('salario')
	

	objeto = Pessoa(nome=Nome, idade=Idade, sexo=Sexo, salario=Salario)
	objeto.save()

	pessoas = Pessoa.objects.all()
	return render(request, 'listagem.html', {'pessoas': pessoas})

def edicao(request, id=0):
	pessoa = Pessoa.objects.get(id=id)
	return render(request, 'edicao.html', {'pessoa': pessoa})

@csrf_protect
def salvar_edicao(request):
	Id = request.POST.get('id')
	Nome = request.POST.get('nome')
	Idade = request.POST.get('idade')
	Sexo = request.POST.get('sexo')
	Salario = request.POST.get('salario')
	

	Pessoa.objects.filter(id=Id).update(nome=Nome, idade=Idade, sexo=Sexo, salario=Salario)

	pessoas = Pessoa.objects.all()
	return render(request, 'listagem.html', {'pessoas': pessoas})

def delecao(request, id=0):
	pessoa = Pessoa.objects.get(id=id)
	return render(request, 'delecao.html', {'pessoa': pessoa})

@csrf_protect
def salvar_delecao(request):
	Id = request.POST.get('id')

	Pessoa.objects.filter(id=Id).delete()

	pessoas = Pessoa.objects.all()
	return render(request, 'listagem.html', {'pessoas': pessoas})

def graficos(request):
	pessoasM = Pessoa.objects.filter(sexo='M')
	pessoasF = Pessoa.objects.filter(sexo='F')
	pessoas = Pessoa.objects.all()

	salarioM = 0
	for m in pessoasM:
		salarioM += m.salario
	if len(pessoasM) > 0:
		salarioM = salarioM / len(pessoasM)

	salarioF = 0
	for f in pessoasF:
		salarioF += f.salario
	if len(pessoasF) > 0:
		salarioF = salarioF / len(pessoasF)

	idadeM = 0
	for m in pessoasM:
		idadeM += m.idade
	if len(pessoasM) > 0:
		idadeM = idadeM / len(pessoasM)

	idadeF = 0
	for f in pessoasF:
		idadeF += f.idade
	if len(pessoasF) > 0:
		idadeF = idadeF / len(pessoasF)

	IDs = []
	Idades = []
	for p in pessoas:
		IDs.append(p.id)
		Idades.append(p.idade)

	return render(request, 'graficos.html',
						    {'salarioM': salarioM, 'salarioF': salarioF,
						     'idadeM': idadeM, 'idadeF': idadeF,
						     'IDs': IDs, 'Idades': Idades})
