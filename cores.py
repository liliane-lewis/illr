print('\033[1;33;42mOlá mundo!\033[m')
print('\033[4;32;45mOlá mundo!\033[m')
print('\033[7;30mOlá mundo!\033[m')
print('\033[1;31mOlá mundo!\033[m')
print('\033[1;32mOlá mundo!\033[m')
print('\033[1;33mOlá mundo!\033[m')
print('\033[1;34mOlá mundo!\033[m')
print('\033[1;35mOlá mundo!\033[m')
print('\033[1;36mOlá mundo!\033[m')
print('\033[1;37mOlá mundo!\033[m')
print('\033[4;35mOlá mundo!\033[m')

print('\033[0;32m-*\033[m'*20)
print('\033[0;33m-=\033[m'*20)
print('\033[0;34m#=\033[m'*20)
print('\033[0;36m-@\033[m'*20)
print('\033[0;32m-H-\033[m'*20)

nome = 'Rodrigo'
print('Muito prazer em te conhecer, {}{}{}!!!'.format('\033[1;34m', nome, '\033[m'))

salario = 1500
cores = {'vermelho':'\033[31m',
        'verde':'\033[32m',
        'azul':'\033[34m',
        'ciano':'\033[36m',
        'magenta':'\033[35m',
        'amarelo':'\033[33m',
        'preto':'\033[30m',
        'branco':'\033[37m',
        'limpa':'\033[m'}

print('Ola {}{}{} seu salario é {}R${:.2f}{} para este mês.'.format(cores['amarelo'], nome, cores['limpa'], cores['verde'], salario, cores['limpa']))
