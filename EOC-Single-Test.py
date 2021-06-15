# import numpy as np
import TherChemCycle     as tcc
import matplotlib.pyplot as plt

CR   = 12.5
Pini = 0
Tini = 25

fuel1   = 'CH4'
# fuel2   = 'H2'
diluent = 'Ar'
Lbd     = 1
DR      = 0.79
OR1     = 2
# OR2     = 0.5

Comp1 = tcc.Gen_Comp(fuel1, diluent, Lbd, DR, OR1)
# Comp2 = tcc.Gen_Comp(fuel2, diluent, Lbd, DR, OR2)
print(Comp1)
# print(Comp2)

Ef_Eoc1,P1,T1,V1,H1,U1,S1,X1,LHV1 = tcc.Otto(CR,Pini,Tini,Comp1,2,'gri30.cti')
# Ef_Eoc2,P2,T2,V2,H2,U2,S2,LHV2 = tcc.Otto(CR,Pini,Tini,Comp2,2,'2015_Varga-trans.cti')

print(Ef_Eoc1)
# print(Ef_Eoc2)

# plt.figure(1)
# plt.title('P-V')
# plt.plot(V1,P1)
# # plt.plot(V2,P2)

# plt.figure(2)
# plt.title('T-V')
# plt.plot(V1,T1)
# # plt.plot(V2,T2)

# plt.figure(3)
# plt.title('S-V')
# plt.plot(V1,S1)
# # plt.plot(V2,S2)

# plt.figure(4)
# plt.title('U-V')
# plt.plot(V1,U1)
# # plt.plot(V2,U2)

# plt.figure(5)
# plt.title('H-V')
# plt.plot(V1,H1)
# # plt.plot(V2,H2)