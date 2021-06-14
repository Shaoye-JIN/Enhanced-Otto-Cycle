# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 10:13:28 2021

@author: DrJin
"""

import EnhancedOttoCycle as EOC
import matplotlib.pyplot as plt

fuel='H2'
OR=0.5
lbd=1

comp=EOC.Gen_Comp(fuel,lbd,OR)
print(comp)

Ef_EOC,P,T,V,H,U,S,N,X,LHV = EOC.Otto(12.5,0,25,comp)