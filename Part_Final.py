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
Estado = [] #Lista de estados Dk para Algoritmo de Earley
x = input('Informe o nome do arquivo a ser usado\n')
sentenca = input('Informe uma sentenca\n')

arq = open(x, 'r')
todas_linhas = arq.readlines() #string que contem todas as linhas do arquivo
cc = 0 #controle de cabecalho (sessao) para leitura do arquivo

class Regra: #classe de Regras

    def __init__(self, variavel, producoes): #ao definir uma classe, passar como parametro a variavel e sua lista de producoes
        self.var = variavel
        self.prod = producoes

def simplifica():
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
    for i in range(len(l_Regras_simple)):
        if len(l_Regras_simple[i].prod) == 1:
            if l_Regras_simple[i].prod[0] in Variaveis_simple:
                for j in range(len(l_Regras_simple)):
                    if l_Regras_simple[j].var == l_Regras_simple[i].prod[0]:
                        nova_regra = Regra(l_Regras_simple[i].var,l_Regras_simple[j].prod)
                        l_Regras_simple.append(nova_regra)
    regras_excluir = []  # guarda os indices das regras com producoes unitarias, para serem excluidas depois
    n_excluidos = 0
    for e in range(len(l_Regras_simple)): #guarda em regras_excluir os indices de l_Regras_simple a serem removidos
        if (len(l_Regras_simple[e].prod) == 1):
            if l_Regras_simple[e].prod[0] in Variaveis_simple:
                regras_excluir.append(e)

    for r in range(len(regras_excluir)): #exclui todas regras com producao unitaria (produz uma Variavel)
        if n_excluidos == 0:
            l_Regras_simple.remove(l_Regras_simple[regras_excluir[r]])
            n_excluidos = n_excluidos + 1
        else:
            l_Regras_simple.remove(l_Regras_simple[regras_excluir[r]-n_excluidos])
            n_excluidos = n_excluidos + 1
    #---- Exclusão dos simbolos inúteis                   ----"
    #---- Dividido em duas etapas                         ----"
    #---- Etapa 1: qualquer variável gera terminais       ----"
    #V1 = {}
    controle_etapa1 = 0
    V1 = []
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
                        if anexar_variavel and variavel not in V1:
                            V1.append(variavel)
        controle_etapa1 += 1
        if contagem_inicial == len(V1):
            break
    #---- Após obter o novo conjunto de variáveis, remover as regras que não serão mais utilizadas ----#
    for regra in l_Regras_simple:
        remover_regra = False
        for prod in regra.prod:
            if prod not in Terminais and prod not in V1:
                remover_regra = True
        if remover_regra:
            l_Regras_simple.remove(regra)
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
        if contagem_inicial_V2 == len(V2) and contagem_inicial_T2 == len(T2):
            break
    #---- Após obter o novo conjunto de variáveis, remover as regras que não serão mais utilizadas ----#
    for regra in l_Regras_simple:
        remover_regra = False
        for prod in regra.prod:
            if prod not in T2 and prod not in V2:
                remover_regra = True
        if remover_regra:
            l_Regras_simple.remove(regra)


def gera_var(new_var,l_var): #Gera uma nova variável que ainda não está utilizada
    new = ''
    for i in new_var:
        if not(i in l_var):
            new = i

    l_var.append(new)
    return new #retorna uma variavel nova
######FNC SEPARADO EM 3 ETAPAS ##########
#1 - SIMPLIFICACAO = OK
#2 - troca os terminais nao sozinhos por novas variaveis e cria nova regra contendo a variavel nova criada e o terminal substituido como producao dela
def etapa_dois(regra, l_term, l_var, new_var): 
    
    aux = ''
    for i in range(len(regra)):
        for j in range(len(regra[i].prod)):
            existe = 0
            prod_nova = []
            if regra[i].prod[j] in l_term:
                if len(regra[i].prod) > 1:
                    for k in range(len(listaT)):
                        v = listaT[k].var
                        p = listaT[k].prod
                        if regra[i].prod[j] in p:
                            var_criada = v
                            existe = 1
                    if existe == 1:
                        regra[i].prod[j] = var_criada
                    else:
                        aux = gera_var(new_var,l_var) #NOVA VARIAVEL
                        prod_nova.append(regra[i].prod[j]) #PRODUCAO = TERMINAL
                        aux1 = Regra(aux,prod_nova) #NOVA REGRA CRIADA
                        regra[i].prod[j] = aux #ATUALIZA O TERMINAL
                        listaT.append(copy.deepcopy(aux1)) #joga o terminal na listaT
                        regra.append(aux1) #lista de regras atualizada
    return regra

def etapa_tres(regras_upd, variaveis):
    v_nova = ''
    n_prod = []
    x_prod = []
    existe1 = 0
    existe2 = 0
    for r in range(len(regras_upd)):
        Regra1 = copy.deepcopy(regras_upd[r])
        t = len(Regra1.prod) - 1
        controle = 1
        i = 0
        if t > 1:
            while i+1 != t:
                if i+1 != t:
                    n_prod.append(Regra1.prod[i])
                    n_prod.append(Regra1.prod[i+1])
                    var1 = Regra1.var
                    indice = 0
                    for k in range(len(listaV)):
                        if listaV[k].prod == n_prod:
                            indice = k
                            existe1 = 1
                    if existe1 == 1:
                        x_prod.append(listaV[indice].var)
                        for j in range(i+2,len(Regra1.prod)):
                            x_prod.append(Regra1.prod[j])
                        Regra1 = Regra(var1,x_prod)
                        regras_upd.append(copy.deepcopy(Regra1))
                    else:
                        v_nova = gera_var(var_nova, variaveis)
                        nova_regra0 = Regra(v_nova, n_prod)
                        x_prod.append(v_nova)
                        for j in range(i+2,len(Regra1.prod)):
                            x_prod.append(Regra1.prod[j])
                        Regra1 = Regra(Regra1.var,x_prod)
                        regras_upd.append(copy.deepcopy(nova_regra0))
                        regras_upd.append(copy.deepcopy(Regra1))
                        listaV.append(copy.deepcopy(nova_regra0))
                    t = len(Regra1.prod) - 1
                    del x_prod[:]
                    del n_prod[:]

    excluir = []
    for w in range(len(regras_upd)):
        if len(regras_upd[w].prod) > 2:
            excluir.append(w)
        elif len(regras_upd[w].prod) == 2:
            if regras_upd[w].prod[0] not in variaveis:
                excluir.append(w)
            elif regras_upd[w].prod[1] not in variaveis:
                excluir.append(w)

    n_excluidos = 0
    for r in range(len(excluir)): #
        if n_excluidos == 0:
            regras_upd.remove(regras_upd[excluir[r]])
            n_excluidos = n_excluidos + 1
        else:
            regras_upd.remove(regras_upd[excluir[r]-n_excluidos])
            n_excluidos = n_excluidos + 1

    return regras_upd

def exibe_simplificacao():
 print('\nSimplificacao: ')
 for g in range(len(l_Regras_simple)):
     print('')
     print(l_Regras_simple[g].var, end='')
     print(' -> ', end='')
     for j in range(len(l_Regras_simple[g].prod)):
         print(l_Regras_simple[g].prod[j],end='')
def exibe_fnc():
    print('\nForma Normal de Chomsky: ')
    for i in range(len(l_Regras_e3_fnc)):
        print('')
        print(l_Regras_e3_fnc[i].var, end='')
        print(' -> ',end='')
        for j in range(len(l_Regras_e3_fnc[i].prod)):
            print(l_Regras_e3_fnc[i].prod[j],end='')
            
        var = lR_Earley[i].var
        Dk = lR_Earley[i].Dk
        ponto = lR_Earley[i].ponto
        e_regra = (var,prods,Dk,ponto)
        if var == Inicial[0]:
            ERegrasAtual.append(copy.deepcopy(e_regra))
    Estado.append(copy.deepcopy(ERegrasAtual))
    

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
    print('3- FNC')
    print('4- Parser, Earley')

    opcao_menu_inicial = str(input('Opcao: '))
    if opcao_menu_inicial == '1':
        menu_leitor()
    elif opcao_menu_inicial == '2':
        exibe_simplificacao()
        modulos_voltar()
    elif opcao_menu_inicial == '3':
        exibe_fnc()
        modulos_voltar()
    elif opcao_menu_inicial == '4':
        earley(sentenca, EVariaveis)
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
var_nova = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U','X', 'Z']
simplifica()

Variaveis_simplificadas = copy.deepcopy(Variaveis_simple)  # lista Variaveis para usar na funcao de FNC
l_Regras_simplificadas = copy.deepcopy(l_Regras_simple)    # lista l_Regras para usar na funcao de FNC
l_Regras_e2_fnc = etapa_dois(l_Regras_simplificadas, Terminais, Variaveis_simplificadas, var_nova)
l_Regras_e3_fnc = etapa_tres(l_Regras_e2_fnc, Variaveis_simplificadas)
l_Regras_fnc = copy.deepcopy(l_Regras_e3_fnc)

#copiar variaveis e regras para usar no earley, melhor usar apos a simplificacao
EVariaveis = copy.deepcopy(Variaveis_simplificadas)
for v in range(len(l_Regras_fnc)):
    if l_Regras_fnc[v].var not in EVariaveis:
        EVariaveis.append(l_Regras_fnc[v].var)

for i in range(len(l_Regras_fnc)):
    var = l_Regras_fnc[i].var
    prod = l_Regras_fnc[i].prod
    Dk = 0
    ponto = 0
    e_regra = ERegra(var,prod,Dk,ponto)
    lR_Earley.append(e_regra)

menu_inicial()

arq.close()
