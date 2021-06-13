# Enhanced Otto Cycle

## background
This work is based on the Otto cycle, which is a thermodynamic cycle.
The thermal conversion efficiency function of the Otto cycle is widely used to explore the thermodynamic boundary of the efficiencies of real engines.

The original Otto cycle has 2 limitations:
1)  Only the thermal equilibrium and mechanical equilibrium are considered (temperature transfer and pressure balance). 
    The chemical equilibrium is not considered (chemical energy).

2)  The specific heat ratio is constant.
    In fact, the specific heat ratio is temperature-dependent.

These 2 limitations cause an error in the calculation of thermodynamic conversion efficiency.

## main idea
To solve these 2 limitations, the Enhanced Otto Cycle (EOC) is proposed.
1)  The chemical equilibrium is additionally considered.

    The original combustion process is a constant-volume heat addition process.
    In EOC it is replaced by a constant-volume adiabatic combustion process.
    
    The expansion process and exhaust process remain as an adiabatic expansion and a constant volume heat loss process, respectively.
    However, the chemical equilibrium is also calculated in these two processes.

2)  The thermodynamic files containing temperature-dependent parameters are used, which is the same as those used in the chemical kinetic study.

## benefits
The thermodynamic theory is universal and therefore can be considered as the theoretical boundary.
The chemical equilibrium also obeys the second law of thermodynamics.
Hence, the calculation with EOC is still universal.

## published papers
The following papers describe the detailed development and application of EOC.

[1] Jin S, Deng J, Gong X, Li L. Thermodynamic analysis on factors influencing the thermal conversion efficiency of the argon power cycle engine. Transactions of CSICE 2020;38:351–8. https://doi.org/10.16236/j.cnki.nrjxb.202004046.
[2] Jin S, Deng J, Li L. Thermodynamic and Chemical Analysis of the Influence of Working Substances on the Argon Power Cycle. SAE Technical Paper 2021-01-0447, 2021. https://doi.org/10.4271/2021-01-0447.

Ref [1] is the initiation of the idea of EOC. 
The method was based on STANJAN.

Ref [2] realized the same method through MATLAB.

The code in this repository is based on Python, which is the almost same as the MATLAB version published in Ref [2], except that the expansion process is changed from 'UV' to 'SV'.

Please cite Ref [1] and Ref [2] when referencing EOC. 