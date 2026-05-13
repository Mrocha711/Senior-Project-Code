# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 10:21:16 2026

@author: victo
"""
import numpy as np
import matplotlib.pyplot as plt
import math

#test varriables
L = 2
P = np.array([1])
P_L = np.array([0.5])
W = np.array([])
W_L = np.array([])

def Simply_Supported(P, P_L, W, W_L, L):
    # getting all inch values along the beam
    number_of_x = round(L*12+1)
    x_line = np.zeros(number_of_x)
    for i in range(len(x_line)):
        x_line[i] = i/12
    # combining all the distances for loads into one array
    Load_L = np.append([P_L], [W_L])
    Load_L = np.append(np.unique([Load_L]), np.unique([P_L]))
    
    # combining the lengtharray with all the distance arrays for loads to have all important points.
    x_line = np.append([x_line],[Load_L])

    # sorting all the distances into numerical order
    x_line = np.sort([x_line])
    
    # combining multiple arrays creates a 2D array need it to be a 1D array
    x_line = x_line.flatten()
    
    #creating arrays to hold values of shear moment and deflection
    V = np.zeros(len(x_line))
    M = np.zeros(len(x_line))
    
    #Solving for if it has any point loads on the beam
    for i in range(len(P)):
        counter = 0
        for y in range(len(x_line)):
            if x_line[y] <= P_L[i] and counter == 0:
                V[y] = P[i]*(L-P_L[i])/2
                if x_line[y] == P_L[i]:
                    counter = 1
            else:
                V[y] = -P[i]*(L-(L-P_L[i]))/2
    #Shear plot
    plt.plot(x_line, V, color='blue', linestyle='-',)
    # Add title and labels
    plt.title("Shear Diagram")
    plt.xlabel("Length (ft)")
    plt.ylabel("Shear (K)")
    # Show the plot
    plt.show()
    
    
    
    
    
    
    """#Solving for V and M of respected beam type across all of the beam
    V = np.zeros(number_of_x)
    M = np.zeros(number_of_x)
    if beam_type == "Simply Supported":
        #solving
        for i in range(number_of_x):
            # Equation for point Shear @ mid
            if (x_line[i] < L/2):
                V[i] = P/2
            elif (x_line[i] > L/2):
                V[i] = -P/2
            #solving for Moment for point load @ mid
            if (x_line[i] < L/2):
                M[i] = P*x_line[i]/2
            elif (x_line[i] > L/2):
                M[i] = P*(L-x_line[i])/2
            elif (x_line[i] == L/2):
                M[i] = P*L/4
            # Equation for unit load shear along whole beam
            V[i] += W*(L/2-x_line[i])
            # Equation for unit load Moment along whole beam
            M[i] += W*x_line[i]/2*(L-x_line[i])
    elif beam_type == "Cantilever":
            #solving
            for i in range(number_of_x):
                # Equation for point Shear @ tip
                V[i] = -P
                #solving for Moment for point load @ tip
                M[i] = P*x_line[i]
                # Equation for unit load shear along whole beam
                V[i] += -W*x_line[i]
                # Equation for unit load Moment along whole beam
                M[i] += W*x_line[i]**2/2
    
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
P_L = np.array([1,1.5])
W_L = np.array([0.5,2])
# getting all inch values along the beam
number_of_x = round(L*12+1)
x_line = np.zeros(number_of_x)
for i in range(len(x_line)):
    x_line[i] = i/12
# combining all the distances for loads into one array
Load_L = np.append([P_L], [W_L])
Load_L = np.append(np.unique([Load_L]), np.unique([P_L]))

# combining the lengtharray with all the distance arrays for loads to have all important points.
x_line = np.append([x_line],[Load_L])

# sorting all the distances into numerical order
x_line = np.sort([x_line])"""

















