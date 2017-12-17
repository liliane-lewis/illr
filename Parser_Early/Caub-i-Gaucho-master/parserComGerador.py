
# - Carrega bibliotecas e funcoes usadas: -

import sys
import os
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
# Funcao para limpar a tela:
def clear():
  os.system('cls')
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
          gramatica.regras[vEsq] = []  # Cria lista de producoes a direita, para esta variavel.
        # Copia producoes a direita para a lista da var correspondente:
        start = l.find('[',end)+2  # Start guarda a posicao do primeiro caractere da producao. 
        while start > 1:  # Quando find nao encontrar mais '[', entao retorna -1 em start, +2 = 1.
          end = l.find(']',start)-1
          pDir = l[start:end]
          lTermos.append(pDir)
          start = l.find('[',end)+2
        # Adiciona a lista gerada nas producoes a direita da variavel correspondente.
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
  varsAtestar = []  # Lista de variaveis que podem ser derivadas a esquerda, nas regras adicionadas.
  for i in gramatica.regras[gramatica.inicial]: # Adiciona regras da variavel inicial.
    nova = i[:]
    nova.append('\\0')
    nova.insert(0,mark)
    nova.insert(0,gramatica.inicial)
    D[0].append(nova)
    if (nova[2] in gramatica.vars) and not (nova[2] == gramatica.inicial) and not (nova[2] in varsAtestar):
      # Se pode derivar alguma variavel a esquerda na regra adicionada, adiciona esta variavel na lista
      #  de variavels que podem ser derivadas, para adicionar as suas regras ao conjunto.
      varsAtestar.append(nova[2]) 

  # Processo de adicionar todas as regras que podem ser derivadas mais a esquerda, a partir do simbolo inicial
  #  e regras ja adicionadas a D0.
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

    sizeDi = 0  # Variavel que vai guardar o tamanho do conjunto Di, para teste de parada das iteracoes a seguir.
    while len(D[i]) - sizeDi:  # Ate que o cardinal de Di nao aumente:
      sizeDi = len(D[i])
      for j in D[i]:
        proxvar = markprox(j)
        if proxvar in gramatica.vars:  # Simbolo a seguir do marcador e variavel:
          for k in gramatica.regras[proxvar]:
            nova = k[:]
            nova.append('\\'+str(i))
            nova.insert(0,mark)
            nova.insert(0,proxvar)
            if not nova in D[i]:
              D[i].append(nova)
        elif markprox(j)[0] == '\\':  # Simbolo a seguir do marcador e barra:
          A = j[0]
          s = int(markprox(j)[1:])
          for k in D[s]:
            proxvar = markprox(k)
            if proxvar == A:
              nova = k[:]
              movemark(nova)
              if not nova in D[i]:
                D[i].append(nova)
  # -----------------------------------------

  # Testa se aceitou a palavra:
  aceita = 0
  for i in D[-1]:
    ultmark = markprox(i)
    if (i[0] == gramatica.inicial) and (ultmark[0] == '\\') and (int(ultmark[1:]) == 0):
      aceita = 1

  # Guarda o resultado da computacao numa string, para exibir ao usuario e escrever no arquivo de saida.
  resultadoEarley = ''

  cn = 0
  for i in D:
    resultadoEarley += '------------- D' + str(cn) + ' ------------\n'
    cn += 1
    for j in i:
      resultadoEarley += j[0] + ' -> '
      for w in j[1:]:
        if w == mark: # Para exibir ao usuario, converte o numero marcador para '.':
          resultadoEarley += '. '
        else:
          resultadoEarley += w + ' '
      resultadoEarley += '\n'
    resultadoEarley += 29*'-'+'\n'
  # Exibe o resultado da aplicacao do algoritmo:
  if aceita:  
    resultadoEarley += '       --- ACEITA ---\n'
  else:
    resultadoEarley += '       --- REJEITA ---\n'

  if exibir:
    print(resultadoEarley)

  if arquivos:
    sentencaStr = ' '.join(sentenca)
    outEarley.write('\n - Sentenca:\n\n' + sentencaStr + '\n\n')
    outEarley.write(resultadoEarley)
    outEarley.write('\n'+70*'*'+'\n')

  return aceita
# -------------------------------------------------------------------------------------

# Dada uma GLC, gera uma sentenca aleatoria que e aceita por esta GLC.
def geraSentenca(gramatica):
  sentenca = []  # Lista que vai conter os terminais da sentenca gerada.
  
  sentenca.append(gramatica.inicial)  # Coloca na lista o simbolo inicial da gramatica.

  # Dicionario que armazena a quantidade de vezes que cada regra de substituicao
  #  da gramatica ja foi usada pelo gerador aleatorio, para nao gerar sequencias muito grandes.
  qtUsoRegras = {} 
  qtMaxRegras = 100  # Quantidade maxima de vezes que cada regra pode ser usada pelo gerador.

  # Atualiza qtUsoRegras, e retorna um booleano informando se a producao recebida
  #  atingiu ou nao a quantidade maxima de usos permitida.
  def maxUsada(varEsq, parteDir):
    tupla = varEsq, tuple(parteDir)
    if not tupla in qtUsoRegras.keys():
      qtUsoRegras[tupla] = 1  # Regra uma vez usada agora, no caso de ainda nao ter sido usada.
    elif qtUsoRegras[tupla] < qtMaxRegras:  # Regra ainda nao atingiu quantidade maxima de usos.
      qtUsoRegras[tupla] += 1
    elif qtUsoRegras[tupla] >= qtMaxRegras:
      # Regra ja atingiu o maximo de usos, nao pode mais ser usada pelo gerador.
      return True
    return False

  # Testa se a sequencia de simbolos aleatorios gerada contem apenas terminais.
  def terminouSentenca(lista):
    res = True
    for i in lista:
      if isinstance(i,str):
        if not i in gramatica.terms:
          res = False
      else:
          res = False
    return res

  # Armazena as regras que ja tentou substituir e nao conseguiu por motivo de 
  #  ja terem sido usadas em excesso, para checar se ainda existem producoes da 
  #  variavel que nao foram usadas o maximo de vezes permitido, para evitar 
  #  que o programa fique procurando por uma producao que ainda possa ser 
  #  usada e nao haja uma para tal.
  prodsUsadas = []

  # Estouro na geracao da sentenca: Para uma dada variavel presente na lista da derivacao em algum momento,
  #  nao ha producoes desta variavel que possam ser substituidas, pois todas producoes associadas
  #  a tal variavel ja foram usadas o maximo de vezes permitido. Portanto, nao pode continuar geracao.
  estouro = False

  # String que vai guardar os passos da geracao da sentenca, para mostrar ao usuario
  #  e escrever no arquivo de saida.
  resGeracao = '\n'

  # Gera sentenca aleatoria, comecando pelo simbolo inicial,
  #  por meio de substituicao direta das regras da gramatica.
  print(' - Geracao da sentenca aleatoria: -')
  while not terminouSentenca(sentenca) and not estouro:
    resGeracao += str(sentenca) + '\n' # Exibe etapas da geracao da sentenca aleatoria.
    for i in sentenca:
      if isinstance(i,str):
        if i in gramatica.regras.keys():  # Se simbolo atual na sentenca e uma variavel:
          index = sentenca.index(i)
          del sentenca[index]  # Remove variavel para que possa ser substituida por uma de suas producoes.
          regraAleatoria = choice(gramatica.regras[i])  # Sorteia uma das producoes da variavel.
          del prodsUsadas[:]  # Esvazia lista que guarda as producoes que ja tentou substituir.
          # Controle para escolher apenas regras que nao estouraram limite maximo de usos:
          # Caso nao haja regras que possam ser usadas para a variavel atualmente sendo substituida,
          #  nao podera continuar a geracao.
          while maxUsada(i,regraAleatoria) and len(prodsUsadas) < len(gramatica.regras[i]):
          # Enquanto a regra sorteada nao puder ser substituida pois ja foi usada a quantidade maxima
          #  de vezes, armazena esta regra e continua sorteando.
          # Se sortear todas as regras da variavel e nenhuma poder ser substituida, ocorre 'estouro'.
          # Armazena regraAleatoria em prodsUsadas, para saber que esta regra estourou limite maximo.
            if not regraAleatoria in prodsUsadas:  
              prodsUsadas.append(regraAleatoria)
            regraAleatoria = choice(gramatica.regras[i])  # Sorteia outra regra associada a variavel.
          if len(prodsUsadas) >= len(gramatica.regras[i]):
            # Se ja tentou todas substituicoes possiveis para a variavel, e nenhuma pode ser usada:
            estouro = True
            break
          else:  
            # Caso a regra ainda nao tenha estourado limite maximo de usos, pode ser usada. 
            sentenca.insert(index,regraAleatoria)
      else:  # Se elemento atual na sentenca nao e uma string, entao e uma lista.
        #  Remove a lista interna, que corresponde a parte direita de uma regra, e copia seus simbolos para a lista 
        #   de derivacao (sentenca), para que possam ser analisados.
        laux = list(chain.from_iterable(repeat(x,1) if isinstance(x,str) else x for x in i))
        index = sentenca.index(i)
        del sentenca[index]
        while laux:
          sentenca.insert(index,laux[-1])
          del laux[-1]

  print(resGeracao)
  if arquivos:
    outSentencas.write(resGeracao)

  # Se ocorreu de nao haver mais substituicoes possiveis para uma variavel na sentenca:
  if estouro:
    print('\n Nao houve mais substituicoes possiveis na sentenca,')
    print('de acordo com o valor maximo de substituicoes por regra estabelecido.\n')
    if arquivos: 
      outSentencas.write('\n\n Nao houve mais substituicoes possiveis na sentenca,\n')
      outSentencas.write('de acordo com o valor maximo de substituicoes por regra estabelecido.\n')
      outSentencas.write('\n' + 70*'-' + '\n')
    return

  indicesOndeAdicionouNovaLinha = []
  indice = -1
  # Lista auxiliar da sentenca, para nao exibir todos terminais numa mesma linha se forem muito grandes.
  sentencaPrintar = sentenca[:]  
  for i in sentencaPrintar:
    indice += len(i)
    if len(i) > 20:  # Terminais com mais de 20 caracteres: coloca um '\n' no final.
      sentencaPrintar[sentencaPrintar.index(i)] = i + '\n'
      indice += 1
      indicesOndeAdicionouNovaLinha.append(indice)

  # Resultado da geracao aleatoria, na forma de string.
  resultado = ' '.join(sentencaPrintar)
  # Remove espacos apos os '\n' adicionados anteriormente, para ficar mais legivel.
  for i in indicesOndeAdicionouNovaLinha:
    if i < len(resultado)-2:
      resultado = resultado[:i+1] + resultado[i+2:]
  
  print(' - Sentenca gerada: -\n')
  print(resultado)

  # Aplica algoritmo de Earley na sentenca gerada, e exibe ela.
  print("\n - Tecle 'Enter' para aplicar o algoritmo de Earley sobre a sequencia gerada. -")
  input()
  if arquivos:
    outEarley.write('\n - Sentenca gerada aleatoriamente -\n')
  earley(gramatica,sentenca,True)
  if arquivos:
    outSentencas.write('\n - Sentenca gerada: -\n\n')
    outSentencas.write(resultado)
    outSentencas.write('\n\n' + 70*'-' + '\n')
# -------------------------------------------------------------------------------------

loopPrincipal = True  # Loop principal do programa, que permite o usuario trocar de arquivo de gramatica.

while loopPrincipal:
  gram = GLC()  # Gramatica que sera usada.

  abriuArquivo = False  # Booleano para controlar se o usuario conseguiu abrir o arquivo de leitura da gramatica.

  while not abriuArquivo:
    # Nome do arquivo para leitura da gramatica.
    nomeArquivo = input('Digite o nome do arquivo que contem a descricao da gramatica:\n')  
    try:  # Tenta abrir o arquivo, sem adicionar extensao '.txt' no nome entrado pelo usuario.
      arq = open(nomeArquivo,'r')  # Abre arquivo onde estao armazenadas as informacoes da gramatica.    
    except FileNotFoundError:
      try: # Tenta abrir o arquivo, adicionando '.txt' ao nome fornecido.
        nomeArquivo += '.txt'
        arq = open(nomeArquivo,'r')
      except:  
        clear()
        print('Arquivo nao encontrado!\n')
      else:
        abriuArquivo = True
    else:
      abriuArquivo = True

  # Le arquivo aberto:  
  linhas = arq.readlines()  # Lista onde irao ficar as linhas do arquivo.
  arq.close()  # Fecha o arquivo lido.

  # Preenche a gramatica 'gram' com as informacoes lidas do arquivo:
  preencheGramatica(gram,linhas)

  # OBS:
  # - Ao carregar uma gramatica e criar arquivos de saida, se esta gramatica ja tiver
  #    sido carregada antes, e se foram criados arquivos de saida para esta mesma
  #    gramatica, estes arquivos criados serao apagados e re-escritos.
  # Pergunta ao usuario se ele quer que sejam criados os arquivos de saida.
  clear()
  print('Criar arquivos de saida? (Earley e sentencas aleatorias geradas).')
  print('1: Sim.')
  print('0: Nao.')
  criaArqs = input()
  clear()

  while criaArqs != '1' and criaArqs != '0':
    print('Digite uma opcao valida!\n')
    print('Criar arquivos de saida? (Earley e sentencas aleatorias geradas).')
    print('1: Sim.')
    print('0: Nao.')
    criaArqs = input()
    clear()

  if criaArqs == '1':
    arquivos = True  # Booleano para informar ao programa se esta usando arquivos ou nao para saida.

    nomeArqSentencas = '_sentencas_' + nomeArquivo
    nomeArqEarley = '_Earley_' + nomeArquivo

    if not nomeArquivo.endswith('.txt'):
      nomeArqSentencas += '.txt'
      nomeArqEarley += '.txt'

    outSentencas = open(nomeArqSentencas,'w')
    outEarley = open(nomeArqEarley,'w')
  else:
    arquivos = False

  # - - - 

  escolha = None  # Opcao entrada pelo usuario.
  loopGram = True  # Loop do programa, para uma dada gramatica selecionada.
 
  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  while loopGram:

    print('Arquivo:',nomeArquivo)

    # Solicita ao usuario que escolha uma opcao.
    print('\n ** Digite uma opcao: **')
    print('1: Testar uma sequencia de terminais.')
    print('2: Gerar uma sequencia de terminais.')
    print('3: Abrir outro arquivo de gramatica')
    print('0: Sair.')
    escolha = input()
     
    # Processa a opcao entrada pelo usuario.
    if escolha == '1':
      while escolha == '1':  # Testar sequencia de terminais.
        clear()
        print("Os terminais a serem entrados devem ser separados unicamente por um '#'.")
        print('Exemplo: \n\nthe dog#barks.\n\n = 2 terminais, "the dog" e "barks."\n' + 39 * '- ' + '-\n')

        # Pega entrada do usuario:
        entrada = input('Digite a sequencia de terminais a ser analisada por Earley:\n')

        # Separa os terminais entrados pelo usuario, usando #:
        listaEntrada = entrada.split('#')

        # Aplica o algoritmo de Earley sobre a gramatica e sentenca fornecidos:
        clear()
        print('\n\t' + ' '.join(listaEntrada) + '\n')
        earley(gram,listaEntrada,True)
       
        print('Deseja testar mais uma sequencia de terminais?')
        print('1: Sim.')
        print('0: Nao.')
        escolha = input() 
        while escolha != '0' and escolha != '1':
          clear()
          print('Digite uma opcao valida!\n')
          print('Deseja testar mais uma sequencia de terminais?')
          print('1: Sim.')
          print('0: Nao.')
          escolha = input()
        clear()

    elif escolha == '2':
      while escolha == '2':  # Gerar sentenca aleatoria.
        clear()
        geraSentenca(gram)  # Gera e exibe a sentenca.
        print('Gerar nova sentenca?')
        print('2: Sim.')
        print('0: Nao.')
        escolha = input()
        while escolha != '0' and escolha != '2':
          clear()
          print('Digite uma opcao valida!\n')
          print('Gerar nova sentenca?')
          print('2: Sim.')
          print('0: Nao.')
          escolha = input()
        clear()

    elif escolha == '3':  # Se escolha = 3, fecha a gramatica atual para abrir uma nova.
      loopGram = False

    elif escolha == '0':  # Se escolha = 0, termina o programa.
      loopGram = False
      loopPrincipal = False

    else:  # Se usuario digitou uma opcao invalida.
      clear()
      print('Opcao invalida!\n')
  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  # Fim 'while loopGram'

  clear()
  if arquivos:
    outSentencas.close()
    outEarley.close()
# -------------------------------------------------------------------------------------

sys.exit()
