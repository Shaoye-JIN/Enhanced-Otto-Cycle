import EnhancedOttoCycle as EOC
import matplotlib.pyplot as plt

fuel='H2'
OR=0.5
lbd=1

comp=EOC.Gen_Comp(fuel,lbd,OR)
print(comp)

Ef_EOC,P,T,V,H,U,S,N,X,LHV = EOC.Otto(12.5,0,25,comp)