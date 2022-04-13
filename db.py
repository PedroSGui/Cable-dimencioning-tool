
import sqlite3
import math
import random
import copy
import time

from sqlite3 import Error


def create_connection(path):

    connection = None

    try:

        connection = sqlite3.connect(path)

        print("Connection to SQLite DB successful")

    except Error as e:

        print(f"The error '{e}' occurred")


    return connection

connection = create_connection(".\sm_app.sqlite")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

create_users_table = """
CREATE TABLE IF NOT EXISTS cabos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  material INTEGER NOT NULL,
  section INTEGER NOT NULL,
  perfil INTEGER NOT NULL,
  conductors INTEGER NOT NULL
);
"""
execute_query(connection, create_users_table)  



create_users = """
INSERT INTO
  cabos (material, section, perfil, conductors)
VALUES
  (1, 90, 1, 1),
  (0, 40, 1, 1),
  (1, 45, 1, 3);
"""

execute_query(connection, create_users)





def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


# Começa a partir daqui


menu_options = {
    1: 'Exit',
    2: 'Ver tabela',
    3: 'Calculo de secção',
    4: 'Adicionar itens',
}

class cabo:
    def __init__(self): 
        self.U = int(input('Qual o nivel de tensao: '))
        self.Scc = int(input('Qual a potencia de cc: '))
        self.S = int(input('Qual a potencia nominal: '))
        self.Perf = int(input('Qual o perfil: '))
        self.Disp = int(input('Qual a disposicao: '))
        self.Cond = int(input('Quantos condutores: '))
        self.Mat = int(input('Qual o material (0 - Cu,  1 - Al, 2 - Cu pintado, 3 - Al pintado): '))
        self.D = int(input('Qual a distãncia: '))
        self.Is = self.S / ( 1.732 * self.U )


def fator_ar(iz, delta1, delta2):
    return iz * math.sqrt(delta1/delta2) 

def fator_temp(iz, teta1, teta2):
    return iz * math.sqrt(teta1/teta2)

def fator_alt(iz, h):
    if h<1000:
        iz = iz * 1
    elif h>=1000 & h<2000:
        iz = iz * 1
    elif h>=2000 & h<3000:
        iz = iz * 0.99
    elif h>=3000 & h<4000:
        iz = iz * 0.96    
    else:
        iz = iz * 0.9
    return iz

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def option4():
    material = input('Qual o material (0 pra cobre e 1 pra aluminio): ')
    section = input('Qual a secção: ')
    perfil = input('Qual o perfil: ')
    conductors = input('Quantos condutores: ')
    cabo_a_adicionar = "(" + material + ", " + section + ", "+ perfil + ", "+conductors + ")"
    create_users = "INSERT INTO cabos (material, section, perfil, conductors) VALUES " + cabo_a_adicionar
    print(cabo_a_adicionar)
    execute_query(connection, create_users)

def option2():
    select_cabos = "SELECT * from cabos"
    cabos = execute_read_query(connection, select_cabos)
    print("\n\n")
    for cabos in cabos:
        print(cabos)
    print("\n\n")

def option3():
    # Entrada de dados
    meu_cabo  = cabo() 
    # Fim da entrada de dados

    # Fase 2 - bersão base - Contas regime permanente
    delta1=1
    delta2=1
    teta1=1
    teta2=1
    h=0
    permanente = int(input('Tem condições diferentes da padrao (1 se sim e 0 se não): '))
    if permanente == 1:
        h =int(input('Qual a altitude: ')) # colocar outras correções
    
    
    select_cabos = "SELECT * FROM cabos WHERE perfil = "+ str(meu_cabo.Perf) +" AND material = "+ str(meu_cabo.Mat) +""
    cabos = execute_read_query(connection, select_cabos)
    for cabos in cabos:
        print(cabos)
    print(select_cabos)
    print("\n\n")
    for i in cabos:
        print(i)
    print("\n\n")
    iz = 100

    iz = fator_ar(iz, delta1, delta2)
    iz = fator_temp(iz, teta1, teta2)
    iz = fator_alt(iz, h)

    # Fim Contas regime permanente


if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option == 1:
            print('Thanks message before exiting')
            exit()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            option4()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')


# Não escreve daqui pra baixo