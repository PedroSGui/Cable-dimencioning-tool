import sqlite3
import math

from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

connection = create_connection("sm_app.sqlite")

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
    id          PRIMARY KEY,
    material,
    section,
    perfil,
    condutores,
    maxcurrent,
    tabela,
    peso,
    inercia,
    w
);
"""
execute_query(connection, create_users_table)  


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
    3: 'Calculo Completo',
    4: 'Adicionar cabo para calculo',
    5: 'Análise de sensibilidade',
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

# Fim do menu
#Inicio das estruturas de dados

def fator_temp(iz, delta1, delta2):
    return iz * math.sqrt(delta1/delta2) 

def fator_alt(iz, h):
    if h<1000:
        iz = iz * 1
    elif h>=1000 and h<2000:
        iz = iz * 1
    elif h>=2000 and h<3000:
        iz = iz * 0.99
    elif h>=3000 and h<4000:
        iz = iz * 0.96    
    else:
        iz = iz * 0.9
    return iz

class cabolist:
    def __init__(self, id, material, section, perfil, conductors, maxcurrent, tabela, peso, inercia, w): 
        self.id = id
        self.material = material
        self.section = section
        self.perfil = perfil
        self.conductors = conductors
        self.maxcurrent = maxcurrent
        self.tabela = tabela
        self.peso = peso
        self.inercia = inercia
        self.w = w
        self.F=0
        
        if (self.material == 0) | (self.material == 1):
            self.custo = peso*4.20 #(peso/km)*preçoCU
            self.alfa = 0.000017 
        if (self.material == 2) | (self.material == 3):
            self.custo = peso*2.75 #(peso/km)*preçoAL
            self.alfa = 0.000022 
        self.E = 1.2 * 1000000
        L = meu_cabo.l*10
        self.fo = 112 * math.sqrt(10*(self.E*0.01*self.inercia*10000)/(self.peso*0.001*L*L*L*L))   
db_cabo_list = []

class cabo:
    def __init__(self, U, Scc, S, Perf, Cond, Mat, a, t_cc, l, sigma, h, delta1): 
        self.U = U
        self.Scc = Scc 
        self.S = S
        self.Perf = Perf
        self.Cond = Cond
        self.Mat = Mat
        self.a = a
        self.t_cc = t_cc
        self.l = l
        self.sigma = sigma
        self.X = 1.8

        self.Is = self.S / ( 1.732 * self.U )
        delta2=35
        self.Is = fator_temp(self.Is, delta1, delta2)
        self.Is = fator_alt(self.Is, h)

        self.Icc = self.Scc / ( 1.732 * self.U )
        self.ich = self.X * 1.41421 * self.Icc * 0.93
        self.fe=2.04*0.01*(self.ich/1000)*(self.ich/1000)*(self.l*0.01)/(self.a*0.01)
        self.mf = (self.fe* self.l)/16
        self.Ith = 0
        self.m = 0
        self.n = 0
        self.varTem=0
        if (self.Mat == 1) or (self.Mat == 0):
            self.e=(1/56)*(1+ (0.004*45))*0.001 
        if (self.Mat == 2) or (self.Mat == 3): #Isso muda pra Aluminio IMPORTANTE
            self.e=(1/34.2)*(1+ (0.004*45))*0.001 #IMPORTANTE MUDAR DEPOIS
        self.U=8.9*0.000001
        self.C=4.1868*93
        self.kLinha = self.e/(self.U*self.C) 
        
        
meu_cabo = cabo(15000,500000000,1250000,5,1,1,35,0.5,180,1200,0,35)
flag = 1 #IMPORTANTE MUDAR DEPOIS

def show_cable(cable):
    #Apresentação de resultado 
    print("Cabo de menor secção que cumpre as especificações: ")
    print("id = ", cable.id)
    if cable.material == 0:
        print("Material = Cobre não pintado")
    elif cable.material == 1:
        print("Material = Cobre pintado")
    elif cable.material == 2:
        print("Material = Aluminio não pintado")
    elif cable.material == 3:
        print("Material = Aluminio pintado")

    print("Section = ", cable.section, "mm^2")

    if cable.perfil == 1:
        print("Perfil = Circular")
    elif cable.perfil == 2:
        print("Perfil = Tubular")
    elif cable.perfil == 3:
        print("Perfil = Retangular Horizontal")
    elif cable.perfil == 4:
        print("Perfil = Retangular Vertical")
    elif cable.perfil == 5:
        print("Perfil = U Vertical")
    elif cable.perfil == 6:
        print("Perfil = U Horizontal")
    print("Nº Conductors = ", cable.conductors)
    print("Max current in the cable = ", cable.maxcurrent, "A")
    print("Tabela onde esta = ", cable.tabela)
    print("Peso/km = ", cable.peso, "kg/m")
    print("Inercia = ", cable.inercia, ", cm^4")
    print("Modulo de Flexao = ", cable.w, "cm^3")
    if cable.fo != 0:
        print("Freq de ressonancia: = ", cable.fo, "Hz")
    if cable.F != 0:
        print("F = ", cable.F, "kgf")
        print("Fk = ", cable.Fk, "kgf")
        print("Força exercida sobre os isoladores nas extremidades = ",cable.extremidade, "kgf")
        print("Força exercida sobre os isoladores intermedios = ",cable.intermedio, "kgf")
    if cable.custo != 0:
        print("O cabo custa ", round(cable.custo,2)," euros/m")
    # Fim da Apresentação de resultado

def caso():
    # Entrada de dados
    U = int(input('Qual o nivel de tensao: '))
    Scc = int(input('Qual a potencia de cc: '))
    S = int(input('Qual a potencia nominal: '))
    Perf = int(input('Qual o perfil: '))
    Cond = int(input('Quantos condutores: '))
    Mat = int(input('Qual o material (0 - Cu,  1 - Al, 2 - Cu pintado, 3 - Al pintado): '))
    t_cc = float(input('Qual o tempo do cc: '))
    a = float(input('Qual a distancia entre fases: '))
    l = float(input('Qual o comprimento do vao: '))
    sigma = int(input('Qual a carga de seguranca a flexão: '))
    h =int(input('Qual a altitude: ')) 
    delta1 =int(input('Qual a temperatura: ')) 
  
    # Fim da entrada de dados

    # Fase 2 - bersão base - Contas regime permanente
    
    temp  = cabo(U, Scc, S, Perf, Cond, Mat, a, t_cc, l, sigma, h, delta1) 
    global meu_cabo 
    global flag
    meu_cabo = temp
    flag = 1

def sensibilidade():
    global meu_cabo
    print('Análise de sensibilidade')
    varU = float(input('Variação do nível de tensão (%): '))
    varScc = float(input('Variação da potência de cc (%): '))
    varS = float(input('Variação da potência nominal (%): '))
    varA = float(input('Variação da distância entre fases (%): '))
    U = meu_cabo.U * (1 + varU / 100)
    Scc = meu_cabo.Scc * (1 + varScc / 100)
    S = meu_cabo.S * (1 + varS / 100)
    a = meu_cabo.a * (1 + varA / 100)
    meu_cabo_old = meu_cabo
    meu_cabo = cabo(U, Scc, S, meu_cabo.Perf, meu_cabo.Cond, meu_cabo.Mat, a, meu_cabo.t_cc, meu_cabo.l, meu_cabo.sigma)
    intro()
    permanente()
    cc()
    flexao()
    ressonancia()
    custo()
    esfTer()
    meu_cabo = meu_cabo_old

def custo():
    global chepest 
    chepest = min (db_cabo_list, key=lambda cabolist: cabolist.custo)
    print("\n\nCUSTO:")
    show_cable(chepest)

def ressonancia():
    for elem in db_cabo_list:
        if (elem.fo>45 and elem.fo<55) or (elem.fo>90 and elem.fo<110):
            db_cabo_list.remove(elem)

    #the one with less section
    smallest = min (db_cabo_list, key=lambda cabolist: cabolist.section)

    #Apresentação de resultado
    print("\n\nRESSONANCIA:") 
    show_cable(smallest)

def flexao():
    for elem in db_cabo_list:
        if (elem.w < ((meu_cabo.mf)/meu_cabo.sigma)):
            db_cabo_list.remove(elem)
            
    smallest = min (db_cabo_list, key=lambda cabolist: cabolist.section)

    #Apresentação de resultado
    print("\n\nFLEXAO:") 
    show_cable(smallest)


def lerDB():
    select_cabos = "SELECT * from cabos"
    cabos = execute_read_query(connection, select_cabos)
    print("\n\n")
    for cabos in cabos:
        print(cabos)
    print("\n\n")

def intro():
    if flag:
        print('\n Definiu um cabo \n')
    else:
        caso()

    # search cables in database
    select_cabos = "SELECT * FROM cabos WHERE perfil = '"+ str(meu_cabo.Perf) +".0' AND material = '"+ str(meu_cabo.Mat) +".0'"
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
            word[y]=word[y].replace("'","")
        id=int(float(word[0]))
        material= int(float(word[1]))
        section = int(float(word[2]))
        perfil = int(float(word[3]))
        conductor = int(float(word[4]))
        maxcurrent = int(float(word[5]))
        tabela = int(float(word[6]))
        peso = float(word[7])
        inercia = float(word[8])
        w = float(word[9])
        temp = cabolist(id, material, section, perfil, conductor, maxcurrent, tabela, peso, inercia, w)
        db_cabo_list.append(temp)

def permanente():
    for elem in db_cabo_list:
        if elem.maxcurrent < meu_cabo.Is:
            db_cabo_list.remove(elem)

    # the one with less section
    smallest = min (db_cabo_list, key=lambda cabolist: cabolist.section)

    #Apresentação de resultado
    print("PERMANENTE:") 
    show_cable(smallest)

    # Fim Contas regime permanente
    print("\n\n")

def cc():
    #Condição de CC
    if (meu_cabo.Mat == 0) | (meu_cabo.Mat == 1):
        #Cobre
        k_linha = 148
    elif (meu_cabo.Mat == 2) | (meu_cabo.Mat == 3):
        #Aluminio
        k_linha = 76
    else:
        print("Cabo configurado erradamente, volte a configurar")
        return 0
    
    if meu_cabo.t_cc >=0 and meu_cabo.t_cc< 0.015: 
        n=1
        m=1.5
    elif meu_cabo.t_cc >=0.015 and meu_cabo.t_cc< 0.02:
        n=0.96
        m=1.4
    elif meu_cabo.t_cc >=0.02 and meu_cabo.t_cc< 0.025:
        n=0.98
        m=1.38
    elif meu_cabo.t_cc >=0.025 and meu_cabo.t_cc< 0.03:
        m=1.2
        n=0.98
    elif meu_cabo.t_cc >=0.03 and meu_cabo.t_cc< 0.035:
        n=0.97
        m=1.10
    elif meu_cabo.t_cc >=0.035 and meu_cabo.t_cc< 0.04:
        m=1.10
        n=0.97
    elif meu_cabo.t_cc>=0.04 and meu_cabo.t_cc<0.045:
        m=0.98
        n=0.97
    elif meu_cabo.t_cc>=0.045 and meu_cabo.t_cc<0.05:
        m=0.90
        n=0.97
    elif meu_cabo.t_cc>=0.05 and meu_cabo.t_cc<0.055:
        m=0.8
        n=0.95
    elif meu_cabo.t_cc>=0.055 and meu_cabo.t_cc<0.06:
        m=0.77
        n=0.93
    elif meu_cabo.t_cc>=0.06 and meu_cabo.t_cc<0.065:
        m=0.77
        n=0.93
    elif meu_cabo.t_cc>=0.065 and meu_cabo.t_cc<0.07:
        m=0.7
        n=0.93
    elif meu_cabo.t_cc>=0.07 and meu_cabo.t_cc<0.075:
        m=0.63
        n=0.93
    elif meu_cabo.t_cc>=0.075 and meu_cabo.t_cc<0.08:
        m=0.61
        n=0.93
    elif meu_cabo.t_cc>=0.085 and meu_cabo.t_cc<0.09:
        m=0.6
        n=0.93
    elif meu_cabo.t_cc>=0.09 and meu_cabo.t_cc<0.1:	
        m=0.6
        n=0.93
    elif meu_cabo.t_cc>=0.1 and meu_cabo.t_cc<0.2:
        m=0.4
        n=0.93
    elif meu_cabo.t_cc>=0.2 and meu_cabo.t_cc<0.3:
        m=0.3
        n=0.92
    elif meu_cabo.t_cc>=0.3 and meu_cabo.t_cc<0.4:
        m=0.18
        n=0.9
    elif meu_cabo.t_cc>=0.4 and meu_cabo.t_cc<0.5:
        m=0.15
        n=0.88
    elif meu_cabo.t_cc>=0.5 and meu_cabo.t_cc<0.6:
        m=0.10
        n=0.87
    elif meu_cabo.t_cc>=0.6 and meu_cabo.t_cc<0.7:
        m=0.08
        n=0.86
    elif meu_cabo.t_cc>=0.7 and meu_cabo.t_cc<0.8:
        m=0.07
        n=0.85
    elif meu_cabo.t_cc>=0.8 and meu_cabo.t_cc<0.9:
        m=0.05
        n=0.84
    elif meu_cabo.t_cc>=0.9 and meu_cabo.t_cc<1.0:
        m=0
        n=0.83
    else:
        m=0
        n=0.6
    
    meu_cabo.m = m
    meu_cabo.n = n
    meu_cabo.Ith = meu_cabo.Icc * math.sqrt(meu_cabo.m+meu_cabo.n)
    Sec_min_cc =  meu_cabo.Ith*math.sqrt(meu_cabo.t_cc)/148
    for elem in db_cabo_list:
        if elem.section < Sec_min_cc:
            db_cabo_list.remove(elem)
    
    print("CONDIÇÃO DE CC: ")
    smallest = min (db_cabo_list, key=lambda cabolist: cabolist.section)
    show_cable(smallest)

    # pra cada valor de db_cabo_list precisa ver se é maior do que a secção

def esfTer():
    global chepest
    meu_cabo.varTem = (meu_cabo.kLinha * (meu_cabo.Ith/chepest.section)*(meu_cabo.Ith/chepest.section)*meu_cabo.t_cc) + 45 
    chepest.F = chepest.section * (chepest.E*0.01) * chepest.alfa * meu_cabo.varTem
    chepest.Fk = (3.14159*3.14159*chepest.E*chepest.inercia/(meu_cabo.l*meu_cabo.l)) 
    if chepest.F > chepest.Fk:
        chepest.F = (10*chepest.E*chepest.inercia)/(meu_cabo.l*(1+(chepest.alfa*meu_cabo.varTem))*meu_cabo.l*(1+(chepest.alfa*meu_cabo.varTem)))
    chepest.extremidade = math.sqrt((chepest.F*chepest.F)/4+(meu_cabo.fe*meu_cabo.fe)/4)
    chepest.intermedio = meu_cabo.fe
    print("\n\nESFORÇO TERMICO:")
    show_cable(chepest)


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
            lerDB()
        elif option == 3:
            intro()
            permanente()
            cc()
            flexao()
            ressonancia()
            custo()
            esfTer()
        elif option == 4:
            caso()
        elif option == 5:
            sensibilidade()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')


# Não escreve daqui pra baixo
