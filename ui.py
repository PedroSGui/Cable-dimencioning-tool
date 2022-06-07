import sys
from tkinter import *
from main import *
import sqlite3 
import math

class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

    def flush(self):
        pass

def root():
    root = Tk()
    root.title("Calculode barramento de substação")

    Mat = IntVar(value=0)
    Perf = IntVar(value=5)

    U = IntVar(value=15000)
    Scc = DoubleVar(value=500000000)
    S = DoubleVar(value=1250000)
    Cond = IntVar(value=1)
    t_cc = DoubleVar(value=0.5)
    a = DoubleVar(value=35)
    l = DoubleVar(value=180)
    sigma = DoubleVar(value=1800)
    h = DoubleVar(value=0)
    delta1 = DoubleVar(value=35)

    def calc():
        global meu_cabo
        print("\n\n\n\n-----------------------------------\n\n")
        db_cabo_list = []
        meu_cabo = cabo(U.get(), Scc.get(), S.get(), Perf.get(), Cond.get(), Mat.get(), a.get(), t_cc.get(), l.get(), sigma.get(), h.get(), delta1.get())
        intro(meu_cabo,db_cabo_list)
        permanente(meu_cabo,db_cabo_list)
        cc(meu_cabo,db_cabo_list)
        flexao(meu_cabo,db_cabo_list)
        ressonancia(meu_cabo,db_cabo_list)
        custo(meu_cabo,db_cabo_list)
        esfTer(meu_cabo,db_cabo_list)


    def options(parent):
        frame = Frame(parent)

        materialFrame = Frame(frame, padx=1)
        materialFrame.pack(side=LEFT, anchor=N)
        Label(materialFrame, text="Material:").pack(side=TOP, anchor=NW)
        Radiobutton(materialFrame, text="Cobre", variable=Mat, value=0).pack(side=TOP, anchor=NW)
        Radiobutton(materialFrame, text="Cobre pintado", variable=Mat, value=1).pack(side=TOP, anchor=NW)
        Radiobutton(materialFrame, text="Alumínio", variable=Mat, value=2).pack(side=TOP, anchor=NW)
        Radiobutton(materialFrame, text="Alumínio pintado", variable=Mat, value=3).pack(side=TOP, anchor=NW)
        

        profileFrame = Frame(frame, padx=1)
        profileFrame.pack(side=LEFT, anchor=N)
        Label(profileFrame, text="Perfil:").pack(side=TOP, anchor=NW)
        Radiobutton(profileFrame, text="Circular", variable=Perf, value=1).pack(side=TOP, anchor=NW)
        Radiobutton(profileFrame, text="Tubular", variable=Perf, value=2).pack(side=TOP, anchor=NW)
        Radiobutton(profileFrame, text="Retangular Horizontal", variable=Perf, value=3).pack(side=TOP, anchor=NW)
        Radiobutton(profileFrame, text="Retangular Vertical", variable=Perf, value=4).pack(side=TOP, anchor=NW)
        Radiobutton(profileFrame, text="U Vertical", variable=Perf, value=5).pack(side=TOP, anchor=NW)
        Radiobutton(profileFrame, text="U Horizontal", variable=Perf, value=6).pack(side=TOP, anchor=NW)

        numbers1Frame = Frame(frame, padx=1)
        numbers1Frame.pack(side=LEFT, anchor=N)
        Label(numbers1Frame, text="Nível de tensão (V):").pack(side=TOP, anchor=NW)
        Entry(numbers1Frame, textvariable=U).pack(side=TOP, anchor=NW)
        Label(numbers1Frame, text="Potência de CC (W):").pack(side=TOP, anchor=NW)
        Entry(numbers1Frame, textvariable=Scc).pack(side=TOP, anchor=NW)
        Label(numbers1Frame, text="Potência nominal(W):").pack(side=TOP, anchor=NW)
        Entry(numbers1Frame, textvariable=S).pack(side=TOP, anchor=NW)
        Label(numbers1Frame, text="Número de condutores:").pack(side=TOP, anchor=NW)
        Entry(numbers1Frame, textvariable=Cond).pack(side=TOP, anchor=NW)
        Label(numbers1Frame, text="Altura em relação ao mar (metros):").pack(side=TOP, anchor=NW)
        Entry(numbers1Frame, textvariable=h).pack(side=TOP, anchor=NW)

        numbers2Frame = Frame(frame, padx=1)
        numbers2Frame.pack(side=LEFT, anchor=N)
        Label(numbers2Frame, text="Tempo de CC(segundos):").pack(side=TOP, anchor=NW)
        Entry(numbers2Frame, textvariable=t_cc).pack(side=TOP, anchor=NW)
        Label(numbers2Frame, text="Distância entre fases(cm):").pack(side=TOP, anchor=NW)
        Entry(numbers2Frame, textvariable=a).pack(side=TOP, anchor=NW)
        Label(numbers2Frame, text="Comprimento do vão(cm):").pack(side=TOP, anchor=NW)
        Entry(numbers2Frame, textvariable=l).pack(side=TOP, anchor=NW)
        Label(numbers2Frame, text="Carga de segurança a flexão(cm):").pack(side=TOP, anchor=NW)
        Entry(numbers2Frame, textvariable=sigma).pack(side=TOP, anchor=NW)
        Label(numbers2Frame, text="Temperatura ambiente (Cº):").pack(side=TOP, anchor=NW)
        Entry(numbers2Frame, textvariable=delta1).pack(side=TOP, anchor=NW)

        return frame

    def output(parent):
        frame = Frame(parent)

        Label(frame, text="Saída:").pack(side=TOP, anchor=NW)

        out = Text(frame)
        out.pack(side=TOP, anchor=N)

        sys.stdout = StdoutRedirector(out)

        return frame

    def buttons(parent):
        frame = Frame(parent)

        Button(frame, text="Calcular", command=calc).grid(column=1, row=0)

        return frame

    rootFrame = Frame(root, padx=1, pady=1)
    rootFrame.pack()

    
    options(rootFrame).pack(side=TOP, pady=0)
    buttons(rootFrame).pack(side=TOP, pady=2)
    output(rootFrame).pack(side=TOP, pady=0)
    

    return root

if __name__ == '__main__':
    root().mainloop()