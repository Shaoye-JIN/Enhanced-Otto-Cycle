# Enhanced Otto Cycle
# [1] Jin S. https://doi.org/10.16236/j.cnki.nrjxb.202004046
# [2] Jin S. https://doi.org/10.4271/2021-01-0447
# Cantera installation instruction: https://cantera.org/install/index.html


import numpy   as np
import cantera as ct


def Gen_Comp(fuel:str,Lbd:float,OR:float,diluent:str='N2',DR:float=0.79):
    '''
    This function is used to generate the composition of reactants in Cantera format based on the widely used parameters in the field of engine, such as excess oxygen ratio, dilution ratio, and so on.
    
    Parameters
    ----------
    fuel : str
        name of fuel.
    Lbd : float
        excess oxygen ratio.
    OR : float
        oxygen ratio in stoichiometric mixture, O2/fuel.
    diluent : str, optional
        name of diluent. The default is N2.
    DR : float, optional
        dilution ratio, D/(D + O2), (0, 1). The default is 0.79.

    Returns
    -------
    Comp : str
        composition of reactants in Cantera format.

    '''
    
    nD  = DR                # amount of diluents
    nO2 = 1-DR              # amount of O2
    nF  = nO2/OR/Lbd        # amount of fuel
    
    Comp=fuel+':'+"%.6f"%nF+',O2:'+"%.6f"%nO2+','+diluent+':'+"%.6f"%nD
                            # molar fraction in Cantera format
    return Comp


def Otto(CR:float, P1:float, T1:float, Comp:str, N:int=2, Mech:str='gri30.cti'):
    '''
    This function is used to calculate the whole process of Enhanced Otto Cycle.
    
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
    N : int, optional
        step number of compression and expension process.
        The minimum value is 2, which means at least 2 states are need for one process.
        The bigger the value N is, the more details are avaiable in the processes.
    Mech : str, optional
        mechanism file. The default is 'gri30.cti'.

    Returns
    -------
    Ef_EOC : float
        thermochemical conversion efficiency of Enhanced Otto Cycle.
    P : array of float
        pressure, Pa
    T : array of float
        temperature, K
    V : array of float
        specific volume, m^3/kg
    H : array of float
        specific enthalpy, J/kg
    U : array of float
        specific internal energy, J/kg
    S : array of float
        specific entropy, J/K/kg
    Spec_Name: list
        name list of species
    X: array of float
        molar fraction of species
    LHV: float
        lower heating value of the mixture, J/kg

    '''

    # Initialization
    P1      = (P1+101.325)*1E3          # kPa_G to Pa_A
    T1      = T1+273.15                 # degC to K
    gas     = ct.Solution(Mech)         # create the gas mixture
    gas.TPX = T1,P1,Comp                # initialization of temperature, pressure, and composition
    
    Spec_Name = gas.species_names       # name of species
    Spec_Num  = len(Spec_Name)          # number of species
    
    P = np.zeros(2*N+1)                 # array for pressure
    T = np.zeros(2*N+1)                 # array for temperature
    V = np.zeros(2*N+1)                 # array for specific volume
    H = np.zeros(2*N+1)                 # array for specific enthalpy
    U = np.zeros(2*N+1)                 # array for specific internal energy
    S = np.zeros(2*N+1)                 # array for specific entropy
    X = np.zeros([2*N+1,Spec_Num])      # array for molar fractions
    
    # Process 1-2: isentropic compression (without chemical equilibrium)
    D1 = gas.density                    # initial density
    V1 = gas.volume_mass                # initial specific volume
    U1 = gas.int_energy_mass            # initial specific internal energy
    S1 = gas.entropy_mass               # initial specific entropy
    
    V2  = V1/CR                         # specific volume at the end of compression
    V12 = np.linspace(V1,V2,N)          # specific volume in the compression process
    
    for i in range(N):                  # get parameters in the compression process
        gas.SV = S1,V12[i]              # S and V at step i in the compression process
        
        P[i]   = gas.P                  # P at step i, Pa
        T[i]   = gas.T                  # T at step i, K
        V[i]   = gas.volume_mass        # V at step i, m3/kg
        H[i]   = gas.enthalpy_mass      # H at step i, J/kg
        U[i]   = gas.int_energy_mass    # U at step i, J/kg
        S[i]   = gas.entropy_mass       # S at step i, J/K/kg
        X[i,:] = gas.X                  # X at step i
    
    # Process 2-3: constant-volume adiabatic combustion
    gas.equilibrate('UV')               # constant-volume adiabatic combustion
    S3  = gas.entropy_mass              # S after combustion
    
    # Process 3-4: isentropic expansion (with chemical equilibrium)
    V34 = V12[::-1]                     # specific volume in the expansion process
    
    for i in range(N,2*N):              # get parameters in the expansion process
        gas.SV = S3,V34[i-N]            # S and V at step i in the expansion process
        gas.equilibrate('SV')           # isentropic expansion
        
        P[i]   = gas.P                  # P at step i
        T[i]   = gas.T                  # T at step i
        V[i]   = gas.volume_mass        # V at step i
        H[i]   = gas.enthalpy_mass      # H at step i
        U[i]   = gas.int_energy_mass    # U at step i
        S[i]   = gas.entropy_mass       # S at step i
        X[i,:] = gas.X                  # X at step i
    
    U4=gas.int_energy_mass              # U at the end of expansion
    
    # Process 4-5: constant-volume heat loss (with chemical equilibrium)
    gas.TD = T1,D1                      # temperature and density at the final state
    gas.equilibrate('TV')               # chemical equilibrium

    P[-1]   = gas.P                     # P at the final state
    T[-1]   = gas.T                     # T at the final state
    V[-1]   = gas.volume_mass           # V at the final state
    H[-1]   = gas.enthalpy_mass         # H at the final state
    U[-1]   = gas.int_energy_mass       # U at the final state
    S[-1]   = gas.entropy_mass          # S at the final state
    X[-1,:] = gas.X                     # X at the final state
    
    # LHV calculation
    gas2     = ct.Solution(Mech)        # create another mixture to calculate lower heating value
    gas2.TPX = 298.15, 1.01E5, Comp     # initialization of T, P, and X
    H1       = gas2.enthalpy_mass       # initial H
    
    gas2.equilibrate('TP')              # based on the definition of LHV
    H2 = gas2.enthalpy_mass             # final H
    
    LHV = H1-H2                         # LHV, J/kg
    
    # EOC Efficiency calculation
    Ef_EOC = 100*(U1-U4)/LHV            # thermochemical conversion efficiency of EOC, detail in Ref [1] and Ref [2]
    
    return Ef_EOC,P,T,V,H,U,S,Spec_Name,X,LHV