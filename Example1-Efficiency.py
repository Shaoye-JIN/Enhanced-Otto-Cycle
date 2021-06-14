import EnhancedOttoCycle as EOC
import numpy             as np
# import matplotlib.pyplot as plt

Fuel    = 'H2'
LBD     = 1
OR      = 0.5
Diluent = 'Ar'
DR      = [0.9565, 0.8852, 0.7925, 0.5385, 0]
CR      = [4, 5.5, 7, 9.5, 12, 14.5]
Pi      = 0
Ti      = 25
N       = 50

nd = len(DR)
nc = len(CR)

Ef_EOC = np.zeros([nd, nc])
P2     = np.zeros([nd, nc])
T2     = np.zeros([nd, nc])
P3     = np.zeros([nd, nc])
T3     = np.zeros([nd, nc])

for i in range(nd):
    for j in range (nc):
        Comp = EOC.Gen_Comp(Fuel, LBD, OR, Diluent, DR[i])
        Ef_EOC[i,j], P, T, V, H, U, S, Spec_Name, X, LHV = EOC.Otto(CR[j], Pi, Ti, Comp, N, 'gri30.cti')
        P2[i,j] = P[N-1]
        P3[i,j] = P[N]
        T2[i,j] = T[N-1]
        T3[i,j] = T[N]
        