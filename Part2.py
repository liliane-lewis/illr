#usando python 3.6
#!/usr/bin/python
#-*- coding: ISO-8859-1 -*-
#-*- coding: UTF-8 -*-
#Trabalho LINGUAGENS FORMAIS E AUTOMATOS - Parte 1

import sys, os, re
#import msvcrt 
import copy


Terminais = []
Variaveis = []
Inicial = []
Regras = []
l_Regras = [] #lista de Regras criadas
listaT = []
listaV = []
x = input('Informe o nome do arquivo a ser usado\n')
sentenca = input('Informe uma sentenca\n')

arq = open(x, 'r')
todas_linhas = arq.readlines() #string que contem todas as linhas do arquivo
cc = 0 #controle de cabecalho (sessao) para leitura do arquivo

class Regra: #classe de Regras

    def __init__(self, variavel, producoes): #ao definir uma classe, passar como parametro a variavel e sua lista de producoes
        self.var = variavel
        self.prod = producoes

def simplificacao():
    #---- Ordem de simplificação                          ----"
    #---- Exclusão de produções vazias                    ----"
    # V eh a palavra vazia.
    Prod_vazias= [] # guardas as variaveis que produzem o vazio de forma direta
    contador = 0
    for i in range(len(l_Regras_simple)): #pega as variáveis que geram o vazio diretamente
        if l_Regras_simple[i].var != Inicial[0]:
            if 'V' in l_Regras_simple[i].prod:
                if l_Regras_simple[i].var not in Prod_vazias:
                    Prod_vazias.append(l_Regras_simple[i].var)
                    contador = 1
    while(contador == 1):#pega as variaveis que geram indiretamente o vazio
        contador = 0
        for i in range(len(l_Regras_simple)):
            if l_Regras_simple[i].var != Inicial[0]:
                for j in range(len(Prod_vazias)):
                    if Prod_vazias[j] in l_Regras_simple[i].prod:
                        if l_Regras_simple[i].var not in Prod_vazias:
                            Prod_vazias.append(l_Regras_simple[i].var)
                            contador = 1
    cont_removidos = 0
    for i in range(len(l_Regras_simple)):
        j = i -cont_removidos
        if 'V' in l_Regras_simple[j].prod:
            if len(l_Regras_simple[j].prod) > 1:
                l_Regras_simple[j].prod.remove('V')
                cont_removidos= cont_removidos + 1
            else:
                l_Regras_simple.remove(l_Regras_simple[j])
                cont_removidos =cont_removidos + 1
                
    for i in range(len(l_Regras_simple)):
        for j in range(len(Prod_vazias)):
            if Prod_vazias[j] in l_Regras_simple[i].prod:
                if (len(l_Regras_simple[i].prod) > 1):
                    prod_nova = copy.deepcopy(l_Regras_simple[i].prod)
                    prod_nova.remove(Prod_vazias[j])
                    regra_nova = Regra(l_Regras_simple[i].var,prod_nova)
                    if regra_nova not in l_Regras_simple:
                        l_Regras_simple.append(regra_nova)
    
    #---- Exclusão das produções que substituem variáveis ----"


    #---- Exclusão dos simbolos inúteis                   ----"
    #---- Dividido em duas etapas                         ----"
    #---- Etapa 1: qualquer variável gera terminais       ----"
    #V1 = {}
    controle_etapa1 = 0
    V1 = []
    print('Exclusão símbolos inúteis, etapa 1: iteração ' + repr(controle_etapa1))
    print('V1 = { ', end='')
    for variavel in V1:
        print(variavel)
    print('}')
    #repita V1 = V1 U { A | A -> α E P e α E (T U V1)* } até que o cardinal de V1 não aumente
    while True:
        contagem_inicial = len(V1)
        for variavel in Variaveis_simple: 
            if variavel not in V1:
                for regra in l_Regras_simple:
                    if regra.var == variavel: #A -> α E P
                        anexar_variavel = True
                        for prod in regra.prod:
                            if prod not in Terminais and prod not in V1: # A -> α E (T U V1)*
                                anexar_variavel = False
                        if anexar_variavel:
                            V1.append(variavel)
        controle_etapa1 += 1
        print('Exclusão símbolos inúteis, etapa 1: iteração ' + repr(controle_etapa1))
        print('V1 = { ', end='')
        for variavel in V1:
            print(variavel + ' ', end='')
        print('}')
        if contagem_inicial == len(V1):
            break
    print('Removendo regras que contém variáveis que não estão em V1')
    #---- Após obter o novo conjunto de variáveis, remover as regras que não serão mais utilizadas ----#
    for regra in l_Regras_simple:
        remover_regra = False
        for prod in regra.prod:
            if prod not in Terminais and prod not in V1:
                remover_regra = True
        if remover_regra:
        	l_Regras_simple.remove(regra)
    
    exibe_simplificacao()
    print(' ')
    print('Fim da etapa 1 da exclusão de símbolos inúteis.')
    #---- Etapa 2: qualquer símbolo é atingível a partir do símbolo inicial ----""
    # T2 = {}
    # V2 = { S }
    # Repita: 
    # V2 = V2 U { A | X -> α A β E P1, X E V2}
    # T2 = T2 U { a | X -> α a β E P1, X E V2}
    # até que os cardinais de T2 e V2 não aumentem
    T2 = []
    V2 = []
    V2.append(Inicial[0])
    controle_etapa2 = 0
    print('Exclusão símbolos inúteis, etapa 2: iteração ' + repr(controle_etapa2))
    print('V2 = { ', end='')
    for variavel in V2:
        print(variavel + ' ', end='')
    print('}')
    print('T2 = { ', end='')
    for terminal in T2:
        print(variavel + ' ', end='')
    print('}')

    while True:
        contagem_inicial_T2 = len(T2)
        contagem_inicial_V2 = len(V2)
        for variavel in V2:
            for regra in l_Regras_simple:
                if regra.var == variavel:
                    for producao in regra.prod:
                        if producao in V1:
                            if producao not in V2:# V2 = V2 U { A | X -> α A β E P1, X E V2}
                                V2.append(producao)
                        elif producao in Terminais:
                            if producao not in T2:# T2 = T2 U { a | X -> α a β E P1, X E V2}
                                T2.append(producao)
        controle_etapa2 += 1
        print('Exclusão símbolos inúteis, etapa 2: iteração ' + repr(controle_etapa2))
        print('V2 = { ', end='')
        for variavel in V2:
            print(variavel + ' ', end='')
        print('}')
        print('T2 = { ', end='')
        for terminal in T2:
            print(terminal + ' ', end='')
        print('}')
        if contagem_inicial_V2 == len(V2) and contagem_inicial_T2 == len(T2):
            break
    print('Removendo regras que contém variáveis que não estão em V2')
    #---- Após obter o novo conjunto de variáveis, remover as regras que não serão mais utilizadas ----#
    for regra in l_Regras_simple:
        remover_regra = False
        for prod in regra.prod:
            if prod not in T2 and prod not in V2:
                remover_regra = True
        if remover_regra:
            l_Regras_simple.remove(regra)
    
    exibe_simplificacao()
    print(' ')
    print('Fim da etapa 2 da exclusão de símbolos inúteis.')
    #---- Em V2 temos as variáveis e em T2 os terminais após as simplificações.Não manjo de python, entao vou deixar ali ----#

def exibe_simplificacao():
 print('\nSimplificacao: ')
 for g in range(len(l_Regras_simple)):
     print('')
     print(l_Regras_simple[g].var, end='')
     print(' -> ', end='')
     for j in range(len(l_Regras_simple[g].prod)):
         print(l_Regras_simple[g].prod[j],end='')

def clear():
  os.system("cls")
def voltar():
    voltar = str(input('\n\nTecle 9 para voltar ou qualquer tecla para sair: '))
    if voltar == '9':
        menu_leitor()

def modulos_voltar():
    modulos_voltar = str(input('\n\nTecle 9 para voltar ou qualquer tecla para sair: '))
    if modulos_voltar == '9':
        menu_inicial()

def menu_inicial():
    clear()
    print('Modulos:\n')
    print('1 - Leitor da Gramatica')
    print('2 - Simplificação') 

    opcao_menu_inicial = str(input('Opcao: '))
    if opcao_menu_inicial == '1':
        menu_leitor()
    elif opcao_menu_inicial == '2':
        exibe_simplificacao()
        modulos_voltar()

def menu_leitor():
    clear()
    print('Opcoes de exibicao:\n')
    print('Terminais: 1')
    print('Variaveis: 2')
    print('Simbolo inicial: 3')
    print('Regras de producao: 4\n')
    print('9 para voltar ou qualquer tecla para sair')

    opcao_menu = str(input('\nOpcao: '))
    if opcao_menu == '1':
        print('\nTerminais: ',end='')
        for i in range(len(Terminais)):
            if i != (len(Terminais) - 1):
                print(Terminais[i] + ', ',end='')
            else:
                print(Terminais[i])
        voltar()
    elif opcao_menu == '2':
        print('\nVariaveis: ',end='')
        for i in range(len(Variaveis)):
            if i != (len(Variaveis) - 1):
                print(Variaveis[i] + ', ',end='')
            else:
                print(Variaveis[i])
        voltar()
    elif opcao_menu == '3':
        print('\nSimbolo inicial: ',end='')
        for i in range(len(Inicial)):
            print(Inicial[i])
        voltar()
    elif opcao_menu == '4':
        print('\nRegras:')
        for i in range(len(l_Regras)):
            variavel = l_Regras[i].var
            producoes = l_Regras[i].prod
            print('')
            print(variavel,end='')
            print(' -> ',end='')
            for j in range(len(producoes)):
                print(producoes[j],end='')
        voltar()
    elif opcao_menu == '9':
        menu_inicial()

def exibe_gramatica():
	print('\nTerminais: ',end='')
	for i in range(len(Terminais)):
		if i != (len(Terminais) - 1):
			print(Terminais[i] + ', ',end='')
		else:
			print(Terminais[i])

	print('\nVariaveis: ',end='')
	for i in range(len(Variaveis)):
		if i != (len(Variaveis) - 1):
			print(Variaveis[i] + ', ',end='')
		else:
			print(Variaveis[i])

	print('\nSimbolo inicial: ',end='')
	for i in range(len(Inicial)):
		print(Inicial[i])

	print('\nRegras:')
	for i in range(len(l_Regras)):
		variavel = l_Regras[i].var
		producoes = l_Regras[i].prod
		print('')
		print(variavel,end='')
		print(' -> ',end='')
		for j in range(len(producoes)):
			print(producoes[j],end='')
	print('')
for linha in todas_linhas:

    #Para a linha atual, elimina todos espaços em branco, colchetes e quebras de linha indesejadas
    #e salva a string na variavel "simples"
    simples = linha.replace('[','').replace(']','').replace(' ','').replace('\t','').replace('\n','')

    if simples[0] != '#': #ignora quaisquer comentarios (seguidos de "#")
        ponto = 0
        h = 0
        while h < len(simples):
            if simples[h] == '#':
                ponto = h
                nova_string = simples[:ponto]
                simples = nova_string
            h = h + 1

    cc = cc + 1 #ajuste fino no cc para pegar somente o que vem DEPOIS da linha que contem o nome da sessão

    if simples.startswith('#Terminais'): #atribui valores ao cc para cada sessao
        cc = 10
    elif simples.startswith('#Variaveis'):
        cc = 20
    elif simples.startswith('#Inicial'):
        cc = 30
    elif simples.startswith('#Regras'):
        cc = 40

    if cc == 11: #Registra os terminais na lista Terminais
        Terminais.append(simples)
        cc = cc - 1 #reajuste fino, para seguir a lógica (de "ignorar" o titulo da sessao) na proxima iteração
    elif cc == 21: #Registra as variáveis na lista Variaveis
        Variaveis.append(simples)
        cc = cc - 1
    elif cc == 31: #Registra o simbolo inicial na lista Inicial
        Inicial.append(simples)
        cc = cc - 1
    elif cc == 41: #Registra as regras na lista Regras
        Regras.append(simples)
        prods = [] #guarda as produções separadamente (para cada variavel)
        lista_prods = []
        j = 2
        var = simples[0] #guarda em var o primeiro caractere da linha
        while (j < len(simples)): #percorre a linha para preencher a lista de producoes da variavel em questao
            p = simples[j]
            prods.append(p)
            j = j + 1
        a_regra = Regra(var,prods) #cria instancia da regra da linha atual
        l_Regras.append(a_regra) #adiciona a instancia criada à lista de regras
        cc = cc - 1
        
#Variaveis para a simplificação
Variaveis_simple = copy.deepcopy(Variaveis) #lista Variaveis para ser modificada apos algoritmo de simplificacao
l_Regras_simple = copy.deepcopy(l_Regras) #lista l_Regras para ser modificada apos algoritmo de simplificacao

#intro()
#menu_inicial()
exibe_gramatica()
simplificacao()
arq.close()

