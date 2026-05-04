# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 10:21:16 2026

@author: victo
"""
p = 0
w = 2
L= 13
import numpy as np
import matplotlib.pyplot as plt
import math
def newmarks_average( beam_type, p, w, L):
    #creating length array of the beam at every inch of the beam
    number_of_x = round(L*12+1)
    x_line = np.zeros(number_of_x)
    for i in range(number_of_x):
        x_line[i] = i/12
        if i == number_of_x-1:
            x_line[i] = L
    #Solving for V and M of respected beam type across all of the beam
    V = np.zeros(number_of_x)
    M = np.zeros(number_of_x)
    if beam_type == "Simply Supported":
        #solving
        for i in range(number_of_x):
            # Equation for point Shear @ mid
            if (x_line[i] < L/2):
                V[i] = p/2
            elif (x_line[i] > L/2):
                V[i] = -p/2
            #solving for Moment for point load @ mid
            if (x_line[i] < L/2):
                M[i] = p*x_line[i]/2
            elif (x_line[i] > L/2):
                M[i] = p*(L-x_line[i])/2
            elif (x_line[i] == L/2):
                M[i] = p*L/4
            # Equation for unit load shear along whole beam
            V[i] += w*(L/2-x_line[i])
            # Equation for unit load Moment along whole beam
            M[i] += w*x_line[i]/2*(L-x_line[i])
    elif beam_type == "Cantilever":
            #solving
            for i in range(number_of_x):
                # Equation for point Shear @ tip
                V[i] = -p
                #solving for Moment for point load @ tip
                M[i] = p*x_line[i]
                # Equation for unit load shear along whole beam
                V[i] += -w*x_line[i]
                # Equation for unit load Moment along whole beam
                M[i] += w*x_line[i]**2/2
    
    #Shear plot
    plt.plot(x_line, V, color='blue', linestyle='-',)
    # Add title and labels
    plt.title("Shear Diagram")
    plt.xlabel("Length (ft)")
    plt.ylabel("Shear (K)")
    # Show the plot
    plt.show()
    #moment plot
    plt.plot(x_line, M, color='blue', linestyle='-',)
    # Add title and labels
    plt.title("Moment Diagram")
    plt.xlabel("Length (ft)")
    plt.ylabel("Moment (K-ft)")
    # Show the plot
    plt.show()      
    return V, M


L = 2
P_L = 1
number_of_x = round(L+1)
x_line = np.zeros(number_of_x+P_L)
i = 0
while i < len(x_line):
    if P_L-1 < i and i < P_L:
        x_line[i] = P_L
        x_line[i+1] = i
        i += 2
    else:
        x_line[i] = i
        i += 1

















