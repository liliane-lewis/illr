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
arq = open(x, 'r')
todas_linhas = arq.readlines() #string que contem todas as linhas do arquivo
cc = 0 #controle de cabecalho (sessao) para leitura do arquivo

class Regra: #classe de Regras

    def __init__(self, variavel, producoes): #ao definir uma classe, passar como parametro a variavel e sua lista de producoes
        self.var = variavel
        self.prod = producoes


def clear():
#    os.system("clear")
    print (os.name)
    if os.name == 'nt':
        os.system("cls")
    elif os.name == 'posix':
        os.system("clear")

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

    opcao_menu_inicial = str(input('Opcao: '))
    if opcao_menu_inicial == '1':
        menu_leitor()

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



#intro()
menu_inicial()

arq.close()

