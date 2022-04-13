import random
import copy
import time
import sqlite3
import math

from sqlite3 import Error

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

if __name__=='__main__':

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
    

        

    iz = 100

    iz = fator_ar(iz, delta1, delta2)
    iz = fator_temp(iz, teta1, teta2)
    iz = fator_alt(iz, h)

    # Fim Contas regime permanente

    '''
    if meu_cabo.Mat == 0 or 2:
        carga_res_flex = 1000 # 1000 a 1200
    else:
        carga_res_flex = 400 # 400 a 600  
    
    

    icc = meu_cabo.Scc / (math.sqrt(3) * meu_cabo.U)
    X = 1.8
    Ich = 0.93 * Ich3F = 0.93 * X * math.sqrt(2) * meu_cabo.icc
    F = 2.04 * (10**-2) * Ich*Ich * (l/a)

    mf = F * l/16
    W = mf/carga_res_flex
    '''
    

