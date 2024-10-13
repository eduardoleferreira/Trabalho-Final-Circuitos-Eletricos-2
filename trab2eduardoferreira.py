import numpy as np
import matplotlib.pyplot  as plt

#Sendo um sistema matricial: gn * e = fontes
#gn eh a matriz de condutancias, transcondutancias, resistencias, transresistencias, zeros, uns e ganhos
#e eh o vetor de incognitas de tensao e corrente
#fontes eh o vetor de fontes de corrente e tensao independentes 

#Definindo a Estampas dos Elementos: 

def estampaResistor(gn, a, b, r):     #estampa de um resistor conectado entre os nos a e b
	gn[a][a] = gn[a][a] + 1/r         #r eh o valor da resistencia
	gn[a][b] = gn[a][b] - 1/r
	gn[b][a] = gn[b][a] - 1/r
	gn[b][b] = gn[b][b] + 1/r
	return gn

def estampaTranscondutor(gn, a, b, c, d, gm): #estampa de um transcondutor conectado entre os nos a e b com controle entre os nos c e d
	gn[a][c] = gn[a][c] + gm                  #gm eh o valor da transcondutancia    
	gn[a][d] = gn[a][d] - gm              
	gn[b][c] = gn[b][c] - gm
	gn[b][d] = gn[b][d] + gm
	return gn

def estampaCapacitor(gn, a, b, c, omega): #estampa de um capacitor conectado entre os nos a e b
    gn[a][a] += 1j*omega*c                #c eh o valor da capacitancia
    gn[a][b] -= 1j*omega*c                #omega eh a frequencia angular
    gn[b][a] -= 1j*omega*c
    gn[b][b] += 1j*omega*c
    return gn

def estampaIndutor(gn, fontes, a, b, l, omega): #estampa de um indutor conectado entre os nos a e b
    numDeNos = len(gn)                          #l eh o valor da indutancia
                                                #omega eh a frequencia angular
    #criar matriz gn aumentada
    gn_exp = np.zeros((numDeNos + 1, numDeNos + 1), dtype=complex)
    for i in range(numDeNos):
        for j in range(numDeNos):
            gn_exp[i][j] = gn[i][j]

    #adicionar coluna
    gn_exp[a][numDeNos] = 1
    gn_exp[b][numDeNos] = -1

    #adicionar linha
    gn_exp[numDeNos][a] = -1
    gn_exp[numDeNos][b] = 1
    gn_exp[numDeNos][numDeNos] = 1j*omega*l

    #criar vetor de fontes independentes aumentado
    fontes_exp = np.zeros(numDeNos + 1, dtype=complex)
    for i in range(numDeNos):
        fontes_exp[i] = fontes[i]

    return gn_exp, fontes_exp

def estampaFonteDeTensaoCtrlPorTensao(gn, fontes, a, b, c, d, ganho):
#estampa de uma fonte de tensao controlada ligada aos nos a e b com controle entre os nos c e d

    numDeNos = len(gn)  

    #criar matriz gn aumentada
    gn_exp = np.zeros((numDeNos + 1, numDeNos + 1), dtype = complex)
    for i in range(numDeNos):
        for j in range(numDeNos):
            gn_exp[i][j] = gn[i][j]

    #adicionar coluna
    gn_exp[a][numDeNos] = 1
    gn_exp[b][numDeNos] = -1

    #adicionar linha
    linha = np.zeros(numDeNos + 1, dtype = complex)
    linha[a] = -1
    linha[b] = 1
    linha[c] = ganho
    linha[d] = -ganho
    gn_exp[numDeNos] = linha

    #criar vetor de fontes independentes aumentado
    fontes_exp = np.zeros(numDeNos + 1, dtype = complex)
    for i in range(numDeNos):
        fontes_exp[i] = fontes[i]

    return gn_exp, fontes_exp


def estampaFonteDeCorrenteCtrlPorCorrente(gn, fontes, a, b, c, d, ganho):
#estampa de uma fonte de corrente controlada ligada aos nos a e b com controle entre os nos c e d
    numDeNos = len(gn)

    #criar matriz gn aumentada
    gn_exp = np.zeros((numDeNos + 1, numDeNos + 1), dtype=complex)
    for i in range(numDeNos):
        for j in range(numDeNos):
            gn_exp[i][j] = gn[i][j]

    #adicionar coluna
    gn_exp[a][numDeNos] = ganho
    gn_exp[b][numDeNos] = -ganho
    gn_exp[c][numDeNos] = 1
    gn_exp[d][numDeNos] = -1

    #adicionar linha
    linha = np.zeros(numDeNos + 1, dtype=complex)
    linha[c] = -1
    linha[d] = 1
    gn_exp[numDeNos] = linha

    #criar vetor de fontes independentes aumentado
    fontes_exp = np.zeros(numDeNos + 1, dtype=complex)
    for i in range(numDeNos):
        fontes_exp[i] = fontes[i]

    return gn_exp, fontes_exp


def estampaTransresistor(gn, fontes, a, b, c, d, rm):
    #estampa de uma fonte de tensao controlada por corrente ligada aos nos a e b controlada entre os nos c e d
    #rm eh a transresistencia  
    numDeNos = len(gn)

    #criar matriz gn aumentada
    gn_exp = np.zeros((numDeNos + 2, numDeNos + 2), dtype=complex)
    for i in range(numDeNos):
        for j in range(numDeNos):
            gn_exp[i][j] = gn[i][j]

    #adicionar coluna para a corrente de controle
    gn_exp[c][numDeNos] = 1
    gn_exp[d][numDeNos] = -1

    #adicionar coluna para a fonte de tensao controlada
    gn_exp[a][numDeNos + 1] = 1
    gn_exp[b][numDeNos + 1] = -1

    #adicionar linha para a corrente de controle
    linha1 = np.zeros(numDeNos + 2, dtype=complex)
    linha1[c] = -1
    linha1[d] = 1
    gn_exp[numDeNos] = linha1

    #adicionar linha para a fonte de tensao controlada
    linha2 = np.zeros(numDeNos + 2, dtype=complex)
    linha2[a] = -1
    linha2[b] = 1
    linha2[numDeNos] = rm
    gn_exp[numDeNos + 1] = linha2

    #criar vetor de fontes independentes aumentado
    fontes_exp = np.zeros(numDeNos + 2, dtype=complex)
    for i in range(numDeNos):
        fontes_exp[i] = fontes[i]

    return gn_exp, fontes_exp

def estampaTransformador(gn, fontes, a, b, c, d, l1, l2, m, omega): 

 #estampa de um transformador com primeiro enrolam. entre os nos a e b                                                                    
 #o segundo enrolam. entre os nos c e d                                                                   
 #indutancia mutua entre a e c
 #l1 eh a indutancia do primeiro, l2 eh a do segundo e m eh a indut. mutua
 #omega eh a frequencia angular 

    numDeNos = len(gn)                                          
    
    #criar matriz gn aumentada
    gn_exp = np.zeros((numDeNos + 2, numDeNos + 2), dtype=complex)
    for i in range(numDeNos):
        for j in range(numDeNos):
            gn_exp[i][j] = gn[i][j]

    #adicionar as novas colunas 
    gn_exp[a][numDeNos] = 1
    gn_exp[b][numDeNos] = -1
    gn_exp[c][numDeNos + 1] = 1
    gn_exp[d][numDeNos + 1] = -1

    #adicionar as novas linhas 
    linha1 = np.zeros(numDeNos + 2, dtype=complex)
    linha1[a] = -1
    linha1[b] = 1
    linha1[numDeNos] = 1j*omega*l1
    linha1[numDeNos + 1] = 1j *omega*m
    gn_exp[numDeNos] = linha1

    linha2 = np.zeros(numDeNos + 2, dtype=complex)
    linha2[c] = -1
    linha2[d] = 1
    linha2[numDeNos] = 1j *omega*m
    linha2[numDeNos + 1] = 1j*omega*l2
    gn_exp[numDeNos + 1] = linha2

    #criar vetor de fontes independentes aumentado
    fontes_exp = np.zeros(numDeNos + 2, dtype=complex)
    for i in range(numDeNos):
        fontes_exp[i] = fontes[i]

    return gn_exp, fontes_exp

def estampaFonteDeCorrenteDC(fontes, a, b, valor): #estampa de uma fonte de corrente DC entre os nos a e b 
    fontes[a] -= valor                             
    fontes[b] += valor    
    return fontes
 
def estampaFonteDeTensaoDC(gn, fontes, a, b, valor): #estampa de uma fonte de tensão DC ligada aos nos a e b
    numDeNos = len(gn)

    #criar matriz gn aumentada
    gn_exp = np.zeros((numDeNos + 1, numDeNos + 1), dtype=complex)
    for i in range(numDeNos):
        for j in range(numDeNos):
            gn_exp[i][j] = gn[i][j]

    #adicionar coluna
    gn_exp[a][numDeNos] = 1
    gn_exp[b][numDeNos] = -1

    #adicionar linha
    linha = np.zeros(numDeNos + 1, dtype=complex)
    linha[a] = -1
    linha[b] = 1
    gn_exp[numDeNos] = linha

    #criar vetor de fontes independentes aumentado
    fontes_exp = np.zeros(numDeNos + 1, dtype=complex)
    for i in range(numDeNos):
        fontes_exp[i] = fontes[i]
    
    #adicionar valor da fonte de tensão ao vetor de fontes
    fontes_exp[numDeNos] = -valor

    return gn_exp, fontes_exp

def estampaFonteDeCorrenteAC(fontes, a, b, amplitude, fase): #estampa de uma fonte de corrente AC entre os nos a e b 
    fontes[a] -= amplitude*np.exp(1j*fase)
    fontes[b] += amplitude*np.exp(1j*fase)
    return fontes 

def estampaFonteDeTensaoAC(gn, fontes, a, b, amplitude, fase): #estampa de uma fonte de tensao AC ligada aos nos a e b
    valor = amplitude * np.exp(1j * fase)
    numDeNos = len(gn)

    #criar matriz gn aumentada
    gn_exp = np.zeros((numDeNos + 1, numDeNos + 1), dtype=complex)
    for i in range(numDeNos):
        for j in range(numDeNos):
            gn_exp[i][j] = gn[i][j]

    #adicionar coluna
    gn_exp[a][numDeNos] = 1
    gn_exp[b][numDeNos] = -1

    #adicionar linha
    linha = np.zeros(numDeNos + 1, dtype=complex)
    linha[a] = -1
    linha[b] = 1
    gn_exp[numDeNos] = linha

    #criar vetor de fontes independentes aumentado
    fontes_exp = np.zeros(numDeNos + 1, dtype=complex)
    for i in range(numDeNos):
        fontes_exp[i] = fontes[i]
    
    #adicionar valor da fonte de tensao ao vetor de fontes
    fontes_exp[numDeNos] = -valor

    return gn_exp, fontes_exp


def armazenarComponentes(arqNetlist):
    with open(arqNetlist) as netlist:
        listaComponentes = netlist.readlines()
        listaComponentes = [componente for componente in listaComponentes if not (componente.startswith('*') or componente.startswith('\n'))]  # remove possiveis comentarios e linhas vazias
        if listaComponentes:  #verifica se a lista nao esta vazia
            listaComponentes = [componente[:-1] for componente in listaComponentes[:-1]] + [listaComponentes[-1]]  # remove o \n de dentro da lista, exceto o último elemento
    return listaComponentes

    
def maiorNo(listaComponentes):  #mesmo codigo do 1° trabalho; logo, para a analise modificada ele obtem o maior indice e nao o maior no
    listaDeNos = []             #obtem o maior indice para sabermos o tamanho das matrizes do sistema
    for componente in listaComponentes:      
        listaDeNos.append(int(componente.split(' ')[1]))
        listaDeNos.append(int(componente.split(' ')[2])) 
    tamanho = max(listaDeNos)                 
    return tamanho      

def estampas(gn, fontes, listaComponentes, tipo, omega):
    for componente in listaComponentes:
        componente = componente.split(' ')
        if componente[0][0] == 'R':
            gn = estampaResistor(gn, int(componente[1]), int(componente[2]), float(componente[3]))
        elif componente[0][0] == 'C':
            gn = estampaCapacitor(gn, int(componente[1]), int(componente[2]), float(componente[3]), omega)
        elif componente[0][0] == 'L':
            gn, fontes = estampaIndutor(gn, fontes, int(componente[1]), int(componente[2]), float(componente[3]), omega)
        elif componente[0][0] == 'K':
            gn, fontes = estampaTransformador(gn, fontes, int(componente[1]), int(componente[2]), int(componente[3]), int(componente[4]), float(componente[5]), float(componente[6]), float(componente[7]), omega)
        elif componente[0][0] == 'G':
            gn = estampaTranscondutor(gn, int(componente[1]), int(componente[2]), int(componente[3]), int(componente[4]), float(componente[5]))
        elif componente[0][0] == 'F':
            gn, fontes = estampaFonteDeCorrenteCtrlPorCorrente(gn, fontes, int(componente[1]), int(componente[2]), int(componente[3]), int(componente[4]), float(componente[5]))
        elif componente[0][0] == 'E':
            gn, fontes = estampaFonteDeTensaoCtrlPorTensao(gn, fontes, int(componente[1]), int(componente[2]), int(componente[3]), int(componente[4]), float(componente[5]))
        elif componente[0][0] == 'H':
            gn, fontes = estampaTransresistor(gn, fontes, int(componente[1]), int(componente[2]), int(componente[3]), int(componente[4]), float(componente[5]))
        elif componente[0][0] == 'I':
            if componente[3] == 'DC':
                fontes = estampaFonteDeCorrenteDC(fontes, int(componente[1]), int(componente[2]), 0 if tipo == 'AC' else float(componente[4]))
            else:
                fontes = estampaFonteDeCorrenteAC(fontes, int(componente[1]), int(componente[2]), 0 if tipo == 'DC' else float(componente[4]), float(componente[5]))
        elif componente[0][0] == 'V':
            if componente[3] == 'DC':
                gn, fontes = estampaFonteDeTensaoDC(gn, fontes, int(componente[1]), int(componente[2]), 0 if tipo == 'AC' else float(componente[4]))
            else:
                gn, fontes = estampaFonteDeTensaoAC(gn, fontes, int(componente[1]), int(componente[2]), 0 if tipo == 'DC' else float(componente[4]), float(componente[5]))
    return gn, fontes

def listaFrequencias(parametros):
    freq_inicial, freq_final, pontos_totais = parametros

    #converter frequencias inicial e final para a escala logaritmica
    log_freq_inicial = np.log10(freq_inicial)
    log_freq_final = np.log10(freq_final)

    #determinar o numero de pontos na escala logaritmica
    total_pontos = int(pontos_totais * (log_freq_final - log_freq_inicial))

    #gerar lista de frequencias logaritmicamente espacadas
    frequencias = np.logspace(log_freq_inicial, log_freq_final, total_pontos)

    return frequencias  

def main(arqNetlist, tipo, nos, parametros):
    componentes = armazenarComponentes(arqNetlist)
    indice = maiorNo(componentes)
    nos = [no - 1 for no in nos] 
    if tipo == "DC":
        omega = 0
        gn = np.zeros([int(indice) + 1, int(indice) + 1], dtype='complex_') #adicionando o no terra
        fontes = np.zeros([int(indice) + 1], dtype='complex_') #adicionando o no terra
        gn, fontes = estampas(gn, fontes, componentes, tipo, omega)
        vetor_incog = np.linalg.solve(gn[1:,1:], fontes[1:]) #remove o no terra 
        return [vetor_incog[no] for no in nos]  


    elif tipo =="AC":
        frequencias = listaFrequencias(parametros)
        omegas = 2*np.pi*frequencias
        modulos = np.zeros((len(nos), len(frequencias)))
        fases = np.zeros((len(nos), len(frequencias)))

        for i, omega in enumerate(omegas):
            gn = np.zeros([int(indice) + 1, int(indice) + 1], dtype = 'complex_') #adicionando o no terra 
            fontes = np.zeros([int(indice) + 1], dtype = 'complex_') #adicionando o no terra 
            gn, fontes = estampas(gn, fontes, componentes, tipo, omega)
            vetor_incog = np.linalg.solve(gn[1:,1:], fontes[1:]) #removendo o no terra 
            modulos[:, i] = [20*np.log10(np.abs(vetor_incog[no])) for no in nos]
            fases[:, i ] = [np.degrees(np.angle(vetor_incog[no])) for no in nos]

        plt.figure()
        plt.subplot(2, 2, 1)
        [plt.plot(frequencias, modulo) for modulo in modulos]
        plt.xscale("log")

        plt.subplot(2, 2, 2)
        [plt.plot(frequencias, fase) for fase in fases]
        plt.xscale("log")
        plt.show()
        return frequencias, modulos, fases 

#Simulacoes AC:
#main('./Trabalho2NodalModificadaAC/netlistAC1.txt','AC',[1], [0.01, 100, 100])
#main('./Trabalho2NodalModificadaAC/netlistAC2.txt','AC',[1], [0.01, 200, 100])
#main('./Trabalho2NodalModificadaAC/netlistAC3.txt','AC', [2], [0.01, 100, 100])
#main('./Trabalho2NodalModificadaAC/netlistAC4.txt','AC', [2,3], [0.01, 500, 1000])
#main('./Trabalho2NodalModificadaAC/netlistAC5.txt','AC', [3], [0.01, 1000, 1000])
#main('./Trabalho2NodalModificadaAC/netlistAC6.txt','AC', [2,5], [0.01, 2e3, 1000])
#main('./Trabalho2NodalModificadaAC/netlistAC7.txt','AC', [2,7], [0.01, 100, 1000])
#main('./Trabalho2NodalModificadaAC/netlistAC8.txt','AC', [4], [100, 100e3, 100])
main('./Trabalho2NodalModificadaAC/netlistAC9.txt','AC', [2,3,4,5,6], [0.01, 100, 1000])
#main('./Trabalho2NodalModificadaAC/netlistAC10.txt','AC', [4,5], [0.01, 500, 1000])

#Simulacoes DC:
#print(main('./Trabalho2NodalModificadaAC/netlistDC1.txt','DC', [2], []))
#print(main('./Trabalho2NodalModificadaAC/netlistDC2.txt','DC', [2,3,5,7,9,10], []))
#print(main('./Trabalho2NodalModificadaAC/netlistDC3.txt','DC', [1,2,3,4,5,6,7], []))
#print(main('./Trabalho2NodalModificadaAC/netlistDC4.txt','DC', [2], []))
#print(main('./Trabalho2NodalModificadaAC/netlistDC5.txt','DC', [2], []))
print(main('./Trabalho2NodalModificadaAC/netlistDC6.txt','DC', [3,4,5], []))



    