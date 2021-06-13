# -*- coding: utf-8 -*-
"""
Created 2021.03.04
by Jin, Shaoye

Modified 2021.03.14
by Jin, Shaoye

1. Otto cycle, expension process, changed from UV to SV
2. add inputs: step number, N

Modified 2021.03.26
by Jin, Shaoye

1. add LHV output
"""

import numpy   as np
import cantera as ct


def Gen_Comp(fuel:str,diluent:str,Lbd:float,DR:float,OR:float):
    '''
    
    Parameters
    ----------
    fuel : str
        name of fuel.
    diluent : str
        name of diluent.
    Lbd : float
        excess oxygen ratio.
    DR : float
        dilution ratio, D/(D + O2), (0, 1).
    OR : float
        oxygen ratio in stoichiometric mixture, O2: fuel.

    Returns
    -------
    Comp : str
        composition of reactants in Cantera format.

    '''
    
    nD =DR
    nO2=1-DR
    nF =nO2/OR/Lbd
    
    Comp=fuel+':'+"%.6f"%nF+',O2:'+"%.6f"%nO2+','+diluent+':'+"%.6f"%nD
    
    return Comp


def Otto(CR:float, P1:float, T1:float, Comp:str, N:int=50, Mech:str='gri30.cti'):
    '''
    
    Parameters
    ----------
    CR : float
        compression ratio.
    P1 : float
        initial pressure, kPa_G.
    T1 : float
        initial temperature, degC.
    Comp : str
        composition of reactants in Cantera format.
    N : int
        step number of compression and expension process
    Mech : str, optional
        mechanism file. The default is 'gri30.cti'.

    Returns
    -------
    Ef_Ot : float
        thermochemical conversion efficiency of Otto cycle.
    P : array of float
        parameter of the thermochemical cycle.
        pressure, Pa
    T : array of float
        parameter of the thermochemical cycle.
        temperature, K
    V : array of float
        parameter of the thermochemical cycle.
        specific volume, m^3/kg
    H : array of float
        parameter of the thermochemical cycle.
        specific enthalpy, J/kg
    U : array of float
        parameter of the thermochemical cycle.
        specific internal energy, J/kg
    S : array of float
        parameter of the thermochemical cycle.
        specific entropy, J/K/kg

    '''

    # Initialization
    P1 = (P1+101)*1E3                     # kPa_G to Pa_A
    T1 = T1+273.15                        # degC to K
    
    gas       = ct.Solution(Mech)
    Spec_Name = gas.species_names
    Spec_Num  = len(Spec_Name)
    
    gas.TPX = T1,P1,Comp
    
    D1 = gas.density
    V1 = gas.volume_mass
    U1 = gas.int_energy_mass
    S1 = gas.entropy_mass
    
    P = np.zeros(2*N+1)
    T = np.zeros(2*N+1)
    V = np.zeros(2*N+1)
    H = np.zeros(2*N+1)
    U = np.zeros(2*N+1)
    S = np.zeros(2*N+1)
    X = np.zeros([2*N+1,Spec_Num])
    
    # Process 1-2
    V2  = V1/CR
    V12 = np.linspace(V1,V2,N)
    
    for i in range(N):
        gas.SV = S1,V12[i]
        
        P[i]   = gas.P
        T[i]   = gas.T
        V[i]   = gas.volume_mass
        H[i]   = gas.enthalpy_mass
        U[i]   = gas.int_energy_mass
        S[i]   = gas.entropy_mass
        X[i,:] = gas.X
    
    # Process 3-4
    V34 = V12[::-1]
    gas.equilibrate('UV')
    S3  = gas.entropy_mass
    
    for i in range(N,2*N):
        gas.SV = S3,V34[i-N]
        gas.equilibrate('SV')
        
        P[i]   = gas.P
        T[i]   = gas.T
        V[i]   = gas.volume_mass
        H[i]   = gas.enthalpy_mass
        U[i]   = gas.int_energy_mass
        S[i]   = gas.entropy_mass
        X[i,:] = gas.X
    
    U4=gas.int_energy_mass
    
    # State 5
    gas.TD = T1,D1
    gas.equilibrate('TV')

    P[-1]   = gas.P
    T[-1]   = gas.T
    V[-1]   = gas.volume_mass
    H[-1]   = gas.enthalpy_mass
    U[-1]   = gas.int_energy_mass
    S[-1]   = gas.entropy_mass
    X[-1,:] = gas.X
    
    # LHV
    gas2     = ct.Solution(Mech)
    gas2.TPX = 298.15, 1.01E5, Comp
    H1       = gas2.enthalpy_mass
    
    gas2.equilibrate('TP')
    H2 = gas2.enthalpy_mass
    
    LHV = H1-H2
    
    # Efficiency
    Ef_Ot    = 100*(U1-U4)/LHV
    
    return Ef_Ot,P,T,V,H,U,S,X,LHV