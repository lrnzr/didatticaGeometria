#!/usr/bin/env python 3
# Genera una rappresentazione grafica dei punti iniziali e del poligono regolare ottimale

# Il programma chiede il numero dei lati del poligono "teorico" (con centro in (0,0) e inscritto in una circonferenza di raggio
# unitario) e lo scostamento massimo di ciascuna coordinata.
# Su tale base genera i vertici di un poligono ("reale") le cui coordinate si discostano in modo random da quello teorico.
# Tramite una regressione circolare, calcola centro e raggio della circonferenza ottimale. Questa approssima nel 
# modo migliore i vertici del poligono "reale". 
# Successivamente determina il poligono geometrico regolare inscritto in tale circonferenza cosi' da minimizzare la somma dei
# quadrati delle distanze dai vertici del poligono reale.
# Infine si rappresentano graficamente:
# - il poligono teorico iniziale (in trasparenza rosso)
# - la circonferenza ottimale (con relativo centro)
# - i punti del poligono reale (crocette)
# - i vertici e il poligono ottimale
#
# @Lorenzo

# librerie necessarie
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

# definizioni delle varie funzioni
def funzione_obiettivo(argomenti, ascisse, ordinate):
    # argomenti[0] = ascissa centro,  argomenti[1] = ordinata centro, argomenti[2] = raggio,
    return np.sum((np.sqrt((ascisse-argomenti[0])**2 + (ordinate-argomenti[1])**2)-argomenti[2])**2)

def punti_cfr_ottimale(xc, yc, raggio):
    alfa = np.linspace(-np.pi, np.pi, 360)
    xp = xc + raggio*np.cos(alfa)
    yp = yc + raggio*np.sin(alfa)
    return xp, yp

# Genera il poligono regolare geometrico
def poligonoRegolare(alfa, pars):
    xPolMobile = pars[0] + pars[2]*np.cos(par[5]*(2*np.pi/pars[6])+alfa)
    yPolMobile = pars[1] + pars[2]*np.sin(par[5]*(2*np.pi/pars[6])+alfa)
    return xPolMobile, yPolMobile

def somma_quad(alfa, pars):
    # verticiUtilizzati = len(pars[5])
    xPolMobile, yPolMobile = poligonoRegolare(alfa, pars)
    somma = np.sum((pars[3]-xPolMobile)**2+(pars[4]-yPolMobile)**2)
    return somma    

# Inizio programma

alternativa = int(input("si vuole leggere i dati da un file CSV (1) o generarli dal programma (2)? "))
if alternativa==2:
    rng = np.random.default_rng()
    centro, raggio = [rng.uniform(-2,2),rng.uniform(-2,2)], rng.uniform(17,20)
    numLati = int(input('inserire il numero di lati del poligono: '))
    maxScostamento = float(input("inserire il valore massimo dell'errore (per es. 0.01): "))
    indiceVertici = np.arange(numLati)
    dati_x = centro[0] +  raggio*np.cos(2*np.pi*indiceVertici/numLati + rng.uniform(0,.1))
    dati_y = centro[1] +  raggio*np.sin(2*np.pi*indiceVertici/numLati + rng.uniform(0,.1))
elif alternativa != 2:
    nome_file = input("Inserire il nome del file CSV: ")
    # per esempio, esempio3-completo.csv
    file_in = open(nome_file, "r")
    coppie_dati = np.loadtxt(file_in, delimiter = ",", comments = '#', usecols = (0,1))
    numLati = len(coppie_dati)
    indiceVertici = np.arange(numLati)
    nparrayX_Y = coppie_dati.transpose()
    dati_x = nparrayX_Y[0]
    dati_y = nparrayX_Y[1]
    file_in.close()


# ricerca cfr ottimale
x_med = np.mean(dati_x)
y_med = np.mean(dati_y)
# stima_iniziale_raggio 
stima_iniziale_raggio =np.mean(np.sqrt((dati_x-x_med)**2 + (dati_y-y_med)**2))
x0 = np.array([x_med, y_med, stima_iniziale_raggio])
esiti = optimize.minimize(funzione_obiettivo, x0, args = (dati_x, dati_y))
# print(esiti)
xc, yc, r = esiti.x

# costruzione poligono mobile

par = [xc, yc, r, dati_x, dati_y, indiceVertici, numLati]
diz = optimize.minimize(somma_quad, 0, par)
angolo_ottimale = diz.x[0]

output = input('si vuole un file di output con i vertici del poligono regolare? (s) ')
if output=='s':
    nome_file = input("Inserisci il nome del file di output: ")
    file_out = open(nome_file, "w")
    coords = np.transpose(poligonoRegolare(angolo_ottimale, par))
    np.savetxt(file_out, coords, fmt = '%10.5f', delimiter = ',', header = 'ascissa, ordinata')
    file_out.close()

xPol, yPol = poligonoRegolare(angolo_ottimale, par)

xp, yp = punti_cfr_ottimale(xc, yc, r)


figura = plt.figure(facecolor = 'white')
plt.rcParams['figure.figsize'] = [16, 12]
plt.axis('equal')
plt.grid()
plt.plot(xp, yp, linewidth = 1, alpha = 0.5)
plt.scatter(xc, yc, c ='blue', marker = 'x')
plt.scatter(dati_x, dati_y, c = 'red', label = 'vertici iniziali poligonale', marker = 'x')
plt.scatter(xPol, yPol, c = 'blue', label = 'vertici poligono geometrico ottimale', marker = '.')
plt.fill(xPol, yPol, facecolor = 'cornflowerblue', alpha = 0.4, label = 'poligono ottimale')
plt.legend(loc = 'best', labelspacing = 0.5)
plt.title('Punti iniziali, circonferenza ottimale\n e poligono regolare ottimale')
plt.text(15,-18,'centro: ({0:6.4f}, {1:6.4f}), raggio = {2:6.4f}'.format(xc,yc,r))
plt.show()



