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

def punti_cfr_corrispondenti(dati_x, dati_y, xc, yc, raggio):
    angoli = np.arctan2(dati_y-yc,dati_x-xc)
    punti = np.transpose([raggio*np.cos(angoli)+xc, raggio*np.sin(angoli)+yc])
    return punti

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

centro, raggio = np.array([0,0]), 1
print()
numLati = int(input('inserire il numero di lati del poligono: '))
maxScostamento = float(input("inserire il valore massimo dell'errore (per es. 0.01): "))
rng = np.random.default_rng()
indiceVertici = np.arange(numLati)
ascisseApprox = centro[0] +  raggio*np.cos(2*np.pi*indiceVertici/numLati + maxScostamento*rng.random())
ordinateApprox = centro[1] +  raggio*np.sin(2*np.pi*indiceVertici/numLati + maxScostamento*rng.random())
ascisse = centro[0] + raggio*np.cos(2*np.pi*indiceVertici/numLati)
ordinate = centro[1] + raggio*np.sin(2*np.pi*indiceVertici/numLati)

dati_x = ascisseApprox
dati_y = ordinateApprox
# ricerca cfr ottimale
x_med = np.mean(dati_x)
y_med = np.mean(dati_y)
stima_iniziale_raggio = np.sqrt((dati_x[0]-x_med)**2 + (dati_y[0]-y_med)**2)
x0 = np.array([x_med, y_med, stima_iniziale_raggio])
esiti = optimize.minimize(funzione_obiettivo, x0, args = (dati_x, dati_y))
# print(esiti)
xc, yc, r = esiti.x

# costruzione poligono mobile

par = [xc, yc, r, dati_x, dati_y, np.arange(numLati), numLati]
# alfa=0
xPolMobile, yPolMobile = poligonoRegolare(indiceVertici, par)
# somma_quad = np.sum((dati_x-xPolMobile)**2+(dati_y-yPolMobile)**2)
diz = optimize.minimize(somma_quad, 0, par)

print(diz)

xp, yp = punti_cfr_ottimale(xc, yc, r)

punti_cfr = punti_cfr_corrispondenti(dati_x, dati_y, xc, yc, r)
[puntiCfr_x, puntiCfr_y] = [punti_cfr[:,0], punti_cfr[:,1]]

# parte grafica
# ESPANDERE la finestra grafica a tutto schermo ed eventualmente zoomare in regioni rettangolari

figura = plt.figure(facecolor = 'white')
plt.rcParams['figure.figsize'] = [16, 12]
plt.axis('equal')
plt.grid()
xp, yp = punti_cfr_ottimale(xc, yc, r)
plt.plot(xp, yp, linewidth = 1, alpha = 0.5)
plt.scatter(xc, yc, c = 'red', marker = 'x')
plt.scatter(ascisseApprox, ordinateApprox, c = 'red', label = 'vertici iniziali (approx.ideale)', marker = 'x')
plt.scatter(poligonoRegolare(diz.x[0],par)[0], poligonoRegolare(diz.x[0],par)[1], c = 'blue', label = 'vertici poligono geometrico ottimale', marker = '.')
plt.fill(ascisse, ordinate, facecolor = 'red', alpha = 0.1, label = 'poligono ideale di partenza')
plt.fill(poligonoRegolare(diz.x[0],par)[0], poligonoRegolare(diz.x[0],par)[1], facecolor = 'cornflowerblue', alpha = 0.4, label = 'poligono ottimale')
plt.legend(loc = 'best', labelspacing = 0.5)
plt.title('Vertici iniziali approssimati, circonferenza ottimale\n e poligono geometrico regolare di regressione')
plt.show()
