# -*- coding: utf8 -*-

"""

    A type system for Dynamical Systems.
    
    ProbMeasures(A)
                A >= Space
                
    Sequences(A; t) 
                A >= Space
                t >= Positive
    
    D(B;A;t) ~= Sequences(B × A; t) → ProbMeasures(B)
                
    BB(Y;U;t)   discrete-time 
                black box with input in U and output in U, 
    
                Y,U >= Space
                t >= Positive
                
    DS(Y;U;X;t) discrete-time dynamical system 
    = 
        R(o -> X)
        f:(X, U -> X) 
        h:(X, U -> Y)
        


    SP(Y;t)     Stochastic process  
    
                Y,U >= Space
                t >= Positive



"""
from .bb import *
from .stochastic_process import *
