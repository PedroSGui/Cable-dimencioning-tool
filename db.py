
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
  conductors INTEGER NOT NULL,
  maxcurrent INTEGER NOT NULL
);
"""
execute_query(connection, create_users_table)  



create_users = """
INSERT INTO
  cabos (material, section, perfil, conductors, maxcurrent)
VALUES
  (1, 90, 1, 1, 125),
  (0, 40, 1, 1, 200),
  (1, 45, 1, 3, 100);
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
    3: 'Calculo de secção em regime permanente',
    4: 'Adicionar itens',
    5: 'Adicionar cabo para calculo',
    6: 'Calculo de secção em cc',
}
class cabolist:
    def __init__(self, id, material, section, perfil, conductors, maxcurrent): 
        self.id = id
        self.material = material
        self.section = section
        self.perfil = perfil
        self.conductors = conductors
        self.maxcurrent = maxcurrent

db_cabo_list = []

class cabo:
    def __init__(self, U, Scc, S, Perf, Disp, Cond, Mat, D, t_cc): 
        
        #depois mudar isso

        self.U = U
        self.Scc = Scc 
        self.S = S
        self.Perf = Perf
        self.Disp = Disp
        self.Cond = Cond
        self.Mat = Mat
        self.D = D
        self.t_cc = t_cc


        self.Is = self.S / ( 1.732 * self.U )
        self.Icc = self.Scc / ( 1.732 * self.U )

meu_cabo = cabo(1,1,1,1,1,1,1,1,1)
flag = 1 #IMPORTANTE MUDAR DEPOIS

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
    
    if flag:
        print('\n Definiu um cabo \n')
    else:
        option5()

    

    # search cables in database
    select_cabos = "SELECT * FROM cabos WHERE perfil = "+ str(meu_cabo.Perf) +" AND material = "+ str(meu_cabo.Mat) +""
    cabos = execute_read_query(connection, select_cabos)
    i=0
    cabo_select = []
    for cabos in cabos:
        cabo_select.append(str(cabos))
        i=i+1
    for i in range(len(cabo_select)):
        word = cabo_select[i].split()
        for y in range(len(word)):
            word[y]=word[y].replace("(","")
            word[y]=word[y].replace(",","")
            word[y]=word[y].replace(")","")
        id=word[0]
        material= int(word[1])
        section = int(word[2])
        perfil = int(word[3])
        conductor = int(word[4])
        maxcurrent = int(word[5])
        temp = cabolist(id, material, section, perfil, conductor, maxcurrent)
        if temp.maxcurrent > meu_cabo.Is:
            db_cabo_list.append(temp)

    # the one with less section
    smallest = min (db_cabo_list, key=lambda cabolist: cabolist.section)
    print("Cabo de menor secção que cumpre as especificações: ", smallest.id)
    # Fim Contas regime permanente
    print("\n\n")

def option5():
    # Entrada de dados
    U = int(input('Qual o nivel de tensao: '))
    Scc = int(input('Qual a potencia de cc: '))
    S = int(input('Qual a potencia nominal: '))
    Perf = int(input('Qual o perfil: '))
    Disp = int(input('Qual a disposicao: '))
    Cond = int(input('Quantos condutores: '))
    Mat = int(input('Qual o material (0 - Cu,  1 - Al, 2 - Cu pintado, 3 - Al pintado): '))
    D = int(input('Qual a distãncia: '))
    t_cc = int(input('Qual o tempo do cc: '))
    temp  = cabo(U, Scc, S, Perf, Disp, Cond, Mat, D, t_cc) 
    # Fim da entrada de dados

    # Fase 2 - bersão base - Contas regime permanente
    delta2=35
    teta1=1
    teta2=1 #IMPORTANTE corrigir ar
    h=0
    permanente = int(input('Tem condições diferentes da padrao (1 se sim e 0 se não): '))
    if permanente == 1:
        h =int(input('Qual a altitude: ')) # colocar outras correções
        delta1 =int(input('Qual a temperatura: ')) # colocar outras correções
        temp.Is = fator_ar(temp.Is, delta1, delta2)
        temp.Is = fator_temp(temp.Is, teta1, teta2)
        temp.Is = fator_alt(temp.Is, h)
    global meu_cabo 
    global flag
    meu_cabo = temp
    flag = 1

def option6():
    if flag:
        print('\n Definiu um cabo \n')
    else:
        option5()

    print("\n\n")
    if (meu_cabo.Mat == 0) | (meu_cabo.Mat == 2):
        #Cobre
        teta_ini = 65
        teta_fim = 200
        teta = teta_fim -  teta_ini
        k_linha = 148
        p_esp = 8.9
    elif (meu_cabo.Mat == 1) | (meu_cabo.Mat == 3):
        #Aluminio
        teta_ini = 65
        teta_fim = 150
        teta = teta_fim -  teta_ini
        k_linha = 76
        p_esp = 2.6
    else:
        print("Cabo configurado erradamente, volte a configurar")
        return 0
    
    print(teta, meu_cabo.t_cc)
    # PRECISO DE AJUDA
    if meu_cabo.t_cc >0 & meu_cabo.t_cc< 0.015: 
        n=1
    elif meu_cabo.t_cc >0.015 & meu_cabo.t_cc< 0.02:
        n=0.96
    else:
        n=0.6

    if meu_cabo.t_cc >0 & meu_cabo.t_cc< 0.015: 
        m=1.6
    elif meu_cabo.t_cc >0.015 & meu_cabo.t_cc< 0.02:
        m=1.5
    else:
        m=0.01

    Ith = meu_cabo.Icc * math.sqrt(m+n)

    Sec_min_cc = Ith*math.sqrt(meu_cabo.t_cc)/k_linha
    for i in range(len(db_cabo_list)):
        if db_cabo_list[i].section < Sec_min_cc:
            db_cabo_list.remove(db_cabo_list[i])
    # pra cada valor de db_cabo_list precisa ver se é maior do que a secção

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
        elif option == 5:
            option5()
        elif option == 6:
            option3()
            option6()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')


# Não escreve daqui pra baixo