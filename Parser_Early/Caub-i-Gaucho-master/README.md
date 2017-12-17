
Instituto de Informática – Universidade Federal do Rio Grande do Sul
INF05005 Linguagens Formais e Autômatos - Trabalho Prático
Profa. Aline Villavicencio
Parsing e Geração de Linguagem Natural com Earley
1) (2 pontos) Usando o formato do arquivo sample.txt disponível no Moodle da
disciplina, construa uma gramática para gerar diálogos do seu seriado/novela/filme
preferido;
2) (4 pontos) Implementar um parser seguindo o Algoritmo de Earley descrito no
livro Linguagens Formais e Autômatos de Paulo Blauth Menezes. A implementação
deve aceitar como entradas (a) um arquivo texto contendo uma gramática no
formato de sample.txt (b) e uma sentença e (c) usando o algoritmo de Earley fazer o
reconhecimento da sentença de entrada e mostrar cada uma das células
correspondentes às palavras, com as regras e localização dos ponteiros.
3) (4 pontos) Modifique o parser para que, recebendo como entrada uma gramática
no formato de sample.txt, gere randomicamente como saída textos usando a mesma
(a cada “Enter” ou click do usuário, um novo texto diferente é gerado).
4) Apresentações terão cerca de 15 minutos e devem executar o programa, discutir
as estruturas de dados usadas e os detalhes do algoritmo implementado. A presença
de todos os integrantes de cada grupo é obrigatória para a apresentação do trabalho.
A ausência de integrante resultará em desconto na nota.
A interface para o sistema é definida por cada grupo, conforme especificação acima.
Para a implementação qualquer linguagem de programação pode ser utilizada.
Os grupos deverão ter exatamente 4 integrantes, e os nomes dos integrantes deverão
ser confirmados por email até o dia 09/06/2017 (ver abaixo).
A avaliação será feita com base em apresentações dos grupos, tanto do código fonte
quanto do executável, que será testado com exemplos a serem providos durante as
apresentações.
A entrega de cada um dos módulos deverá ser feita pelo Moodle da disciplina,
através das salas de entrega apropriadas. Atraso nas data de entrega (de qualquer um
dos módulos) resultará em desconto de 0.5 pontos por dia da semana até a entrega
ser realizada.
Datas Importantes:
-Definição dos grupos: confirmadas até o dia 09/06/2017, pelo Moodle.
-Entrega da gramática especificada em 1): até o dia 13/06/2017 pelo Moodle
-Entrega do parser especificado em 2): até o dia 20/06/2017 pelo Moodle
-Data de entrega do sistema completo especificado em 3): até o dia 27/06/2017
-Data de apresentações: nos dias 29 de junho e 04 e 06 de julho conforme escala a
ser divulgada.
Boa sorte.
=====================================================
Selected grammar: early.ge
Entry string: Entry string = thegirlsawtheman
Starting Earley algorithm in order to try to parse the entry string...
D0 = ∅
S → ●NPVP \D0 ()
NP → ●DETN \D0 ()
NP → ●NPPP \D0 ()
DET → ●the \D0 ()
D1 = ∅
DET → the● \D0 (the)
NP → DET●N \D0 (DET (the)) * N
N → ●girl \D1 ()
N → ●man \D1 ()
N → ●park \D1 ()
N → ●telescope \D1 ()
D2 = ∅ \D2
N → girl● \D1 (girl)
NP → DETN● \D0 (DET (the) N (girl))
S → NP●VP \D0 (NP (DET (the) N (girl))) * VP
NP → NP●PP \D0 (DET (the) N (girl))) * PP
VP → ●VTNP \D2 ()
VP → ●VPPP \D2 ()
VP → ●VI \D2 ()
PP → ●PNP \D2 ()
VT → ●saw \D2 ()
VI → ●saw \D2 ()
P → ●with \D2 ()
P → ●in ()
D3 = ∅ \D3
VT → saw● \D2 (saw)
VI → saw● \D2 (saw)
VP → VT●NP \D2 (VT (saw)) *
VP → VI● \D2 (VI (saw))
NP → ●DETN \D3 ()
NP → ●NPPP \D3 ()
S → NPVP● \D0 (NP (DET (the) N (girl)) VP (VI (saw))
DET → ●the \D3 ()
PP → ●PNP \D3 ()
P → ●with \D3 ()
P → ●in \D3 ()
D4 = ∅ \D4
DET → the● \D3 (the)
NP → DET●N \D3 (DET (the)) *
N → ●girl \D4 ()
N → ●man \D4 ()
N → ●park \D4 ()
N → ●telescope \D4 ()
D5 = ∅ \D5
N → man● \D4 (man)
NP → DETN● \D3 (DET (the) N(man))
VP → VTNP● \D2 (VT (saw) NP (DET (the) N(man))
NP → NP●PP \D3 (NP (DET (the) N(man))*
S → NPVP● \D0 (NP (DET (the) N (girl)) VP (VT (saw) NP (DET (the)
N(man)))
VP → VP●PP VP \D2 (VT (saw) NP (DET (the) N(man)) *
PP → ●PNP \D5 ()
P → ●with \D5 ()
P → ●in \D5 () 
