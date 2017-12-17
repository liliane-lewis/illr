import sys
from itertools import chain, repeat
from random import choice

# -------------------------------------------------------------------------------------
# Classe base para Gramatica Livre de Contexto.
#  - Conjunto de regras:
#  As regras da gramatica serao armazenadas em um objeto do
#   tipo 'dicionario', no seguinte formato:
#  (exemplo de uma regra com duas producoes do lado direito):  
#
#  Uma regra "Variavel > Prod1 | Prod2" sera armazenada como "Variavel : [[Prod1],[Prod2]]"
#
#  Ou seja, a variavel a esquerda da regra correspondera a chave
#   no dicionario, e o valor retornado por esta chave sera uma
#   lista contendo as suas producoes a direita.
#
#  Prod1 e Prod2 serao listas que armazenam os elementos de cada producao a direita em ordem.
#  (exemplo):
#
#  " VP > V NP | V "   ->   " VP : [ [V,NP] , [V] ]"
#
class GLC():
  def __init__(self):
    self.vars = set()   # Conjunto de variaveis.
    self.terms = set()  # Conjunto de terminais.
    self.inicial = None # Simbolo inicial da gramatica.
    self.regras = {}    # Dicionario de regras.
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# - Recebe uma GLC e uma lista com as linhas do arquivo que descrevem
#    a gramatica. Preenche a gramatica recebida com as informacoes
#    lidas do arquivo.
def preencheGramatica(gramatica,linhas):
  linhasSC = []  # Lista das linhas quando forem removidos os comentarios.

  # Secoes do arquivo em ordem: Terminais ('t'), Variaveis ('v'), Inicial ('i'), Regras ('r').
  # Variavel que vai guardar qual a secao atual sendo lida:
  atual = None

  # Copia para linhasSC as linhas sem comentarios:
  for l in linhas:
    if '#' in l: 
      newline = l[:l.index('#')]
      linhasSC.append(newline)
    else:
      linhasSC.append(l)

  # Preenche a gramatica:
  for l in linhasSC:
    # Verifica se esta comecando nova secao:
    if 'Terminais' in l:
      atual = 't'
    elif 'Variaveis' in l:
      atual = 'v'
    elif 'Inicial' in l:
      atual = 'i'
    elif 'Regras' in l:
      atual = 'r'      
    # Se esta lendo informacao da gramatica:
    elif l[0]=='[' and ']' in l:
      # Le para secao correta do objeto da gramatica:
      if atual == 't':
        gramatica.terms.add( l [ 2 : (l.index(']') - 1) ])
      elif atual == 'v':
        gramatica.vars.add( l [ 2 : (l.index(']') - 1) ])
      elif atual == 'i':
        gramatica.inicial = ( l [ 2 : (l.index(']') - 1) ])
      elif atual == 'r':
        # Le as regras:
        start = 2
        lTermos = []  # Lista que vai conter os termos a direita da regra atual.
        end = l.find(']',start)-1
        vEsq = l[start:end]
        if not vEsq in gramatica.regras.keys():  # Se ainda nao tem regra com esta variavel:
          gramatica.regras[vEsq] = []  # Cria lista de producoes a direita.
        # Copia producoes a direita para a lista da var correspondente:
        start = l.find('[',end)+2
        while start > 1:  # Quando find nao encontrar mais '[', entao retorna -1 em start, +2 = 1.
          end = l.find(']',start)-1
          pDir = l[start:end]
          lTermos.append(pDir)
          start = l.find('[',end)+2  
        # Adiciona a lista gerada, a de producoes a direita da variavel correspondente.
        gramatica.regras[vEsq].append(lTermos)
# -------------------------------------------------------------------------------------
# - Algoritmo de Earley:
#  - Recebe uma descricao de uma GLC em objeto 'gramatica' e uma lista de terminais em 'sentenca'.
#  - Retorna 1 se a sentenca for aceita pela gramatica. Se nao, retorna 0.
def earley(gramatica,sentenca,exibir=False):

  D = [[] for x in range(len(sentenca)+1)]  # Lista que vai conter os conjuntos D gerados.
  mark = 0  # Marcador usado no Earley. Tipo numero, para evitar incompatibilidade com terminais strings.

  def markprox(listaregra):   # Retorna o elemento seguinte a marcacao na regra.
    return listaregra[listaregra.index(mark)+1]

  def imarkprox(listaregra):  # Retorna o indice do elemento seguinte a marcacao.
    return listaregra.index(mark)+1

  def movemark(listaregra):   # Move a marcacao uma posicao para a frente na regra.
    i = imarkprox(listaregra)
    listaregra[i], listaregra[i-1] = listaregra[i-1], listaregra[i]
    return


  # --- Construcao de D0: ---
  varsAtestar = []  # Lista de variaveis que podem ser derivadas a esquerda.
  for i in gramatica.regras[gramatica.inicial]:
    nova = i[:]
    nova.append('\\0')
    nova.insert(0,mark)
    nova.insert(0,gramatica.inicial)
    D[0].append(nova)
    if (nova[2] in gramatica.vars) and not (nova[2] == gramatica.inicial) and not (nova[2] in varsAtestar):
      varsAtestar.append(nova[2]) 

  for i in varsAtestar:
    for j in gramatica.regras[i]:
      nova = j[:]
      nova.append('\\0')
      nova.insert(0,mark)
      nova.insert(0,i)
      D[0].append(nova)
      if (nova[2] in gramatica.vars) and not (nova[2] == gramatica.inicial) and not (nova[2] in varsAtestar):
        varsAtestar.append(nova[2])
  del varsAtestar[:]
  

  # --- Construcao dos outros Dn: ---

  for i in range(1,len(sentenca)+1):
    for j in D[i-1]:
      if markprox(j) == sentenca[i-1]:  # Marcacao esta diretamente antes do terminal sendo processado.
        nova = j[:]
        movemark(nova)
        if not nova in D[i]:
          D[i].append(nova)

    sizeDi = 0
    while len(D[i]) - sizeDi:  # Ate que o cardinal de Dr nao aumente:
      sizeDi = len(D[i])
      for j in D[i]:
        proxvar = markprox(j)
        if proxvar in gramatica.vars:
          for k in gramatica.regras[proxvar]:
            nova = k[:]
            nova.append('\\'+str(i))
            nova.insert(0,mark)
            nova.insert(0,proxvar)
            if not nova in D[i]:
              D[i].append(nova)

      for j in D[i]:
        if markprox(j)[0] == '\\':
          A = j[0]
          s = int(markprox(j)[1])
          for k in D[s]:
            proxvar = markprox(k)
            if proxvar == A:
              nova = k[:]
              movemark(nova)
              if not nova in D[i]:
                D[i].append(nova)
  # -----------------------------------------

  # Exibe conjuntos Dn, formatados para o usuario:
  if exibir:
    cn = 0
    for i in D:
      print('------------- D%d' %cn,'------------')
      cn += 1
      for j in i:
        print(j[0] + ' -> ', end='') # Exibe variavel a esquerda da regra.
        for w in j[1:]:
          if w == mark: # Para exibir ao usuario, converte o numero marcador para '.':
            print('. ', end = '')
          else:
            print(w,' ', end = '')
        print('\n', end = '')
      print('-----------------------------')

  # Testa se aceitou a palavra:
  aceita = 0

  for i in D[-1]:
    ultmark = markprox(i)
    if (i[0] == gramatica.inicial) and (ultmark[0] == '\\') and (ultmark[1] == '0'):
      aceita = 1
  
  # Exibe o resultado da aplicacao do algoritmo:
  if exibir:
    if aceita:  
      print('       --- ACEITA ---')
    else:
      print('       --- REJEITA ---')

  return aceita
# -------------------------------------------------------------------------------------

# Dada uma GLC, gera uma sentenca aleatoria que e aceita por esta GLC.
def geraSentenca(gramatica):
  sentenca = []  # Lista que vai conter os terminais da sentenca gerada.
  
  sentenca.append(gramatica.inicial)

  def terminouSentenca(lista):
    res = True
    for i in lista:
      if isinstance(i,str):
        if not i in gramatica.terms:
          res = False
      else:
          res = False
    return res

  print(' - Geracao da sentenca aleatoria: -')

  while not terminouSentenca(sentenca):
    print(sentenca)    
    for i in sentenca:
      if isinstance(i,str):
        if i in gramatica.regras.keys():
          index = sentenca.index(i)
          del sentenca[index]
          sentenca.insert(index,choice(gramatica.regras[i]))
      else:
        laux = list(chain.from_iterable(repeat(x,1) if isinstance(x,str) else x for x in i))
        index = sentenca.index(i)
        del sentenca[index]
        while laux:
          sentenca.insert(index,laux[-1])
          del laux[-1]

  resultado = ' '.join(sentenca)

  print('\n - Algoritmo de Earley sobre a sentenca gerada: -')
  earley(gramatica,sentenca,True)
  print('\n - Sentenca gerada: -')
  print(resultado)
  for i in sentenca:
    out.write(i + '\n')
  out.write('\n' + 80*'-' + '\n\n')

  return
# -------------------------------------------------------------------------------------

gram = GLC()  # Gramatica que sera usada.

abriuArquivo = False

out = open('sentencas.txt','w')  # Arquivo para onde serao escritas as sentencas aleatorias.

while not abriuArquivo:
  nomeArquivo = input('Digite o nome do arquivo que contem a descricao da gramatica:\n')  # Nome do arquivo para leitura da gramatica.
  try:  # Tenta abrir o arquivo, sem adicionar extensao '.txt' no nome entrado pelo usuario.
    arq = open(nomeArquivo,'r')  # Abre arquivo onde estao armazenadas as informacoes da gramatica.    
  except FileNotFoundError:
    try: # Tenta abrir o arquivo, adicionando '.txt' ao nome fornecido.
      nomeArquivo += '.txt'
      arq = open(nomeArquivo,'r')
    except:  
      print('Arquivo nao encontrado!')
    else:
      abriuArquivo = True
  else:
    abriuArquivo = True

# Le arquivo aberto:  
linhas = arq.readlines()  # Lista onde irao ficar as linhas do arquivo.
arq.close()  # Fecha o arquivo lido.

# Preenche a gramatica 'gram' com as informacoes lidas do arquivo:
preencheGramatica(gram,linhas)

loop = True
print('Arquivo:',nomeArquivo)

while loop:

  print('\n ** Digite uma opcao: **')
  print('1: Testar uma sequencia de terminais.')
  print('2: Gerar uma sequencia de terminais.')
  print('0: Sair.')

  escolha = int(input())
   
  if escolha == 0:
    loop = False

  elif escolha == 1:
    while escolha == 1:  # Testa sequencia de terminais.
      print('\n- Os terminais a serem entrados devem ser separados unicamente por um # -')
      print('- Exemplo: \nthe dog#barks.\n = (2 terminais, "the dog" e "barks.") -')

      # Pega entrada do usuario:
      entrada = input('Digite a sequencia de terminais a ser analisada por Earley:\n')

      # Separa os terminais entrados pelo usuario, usando #:
      listaEntrada = entrada.split('#')

      # Aplica o algoritmo de Earley sobre a gramatica e sentenca fornecidos:
      earley(gram,listaEntrada,True)
     
      print('\nDeseja testar mais uma sequencia de terminais?')
      print('1: Sim.')
      print('0: Nao.')
      escolha = int(input())

  elif escolha == 2:
    escolha = 1
    while escolha == 1:
      print("\nTecle 'Enter' para que a sequencia seja gerada.")
      input()
      geraSentenca(gram)
      print('\nGerar nova sentenca?')
      print('1: Sim.')
      print('0: Nao.')
      escolha = int(input())    

# -------------------------------------------------------------------------------------
out.close()
sys.exit()
