import sympy as sp
from flask import Flask, render_template, request, jsonify, redirect, url_for, request
from sympy import sin, cos
import numpy as np
import csv
import math
from flask_sqlalchemy import SQLAlchemy

## run "pip install matplotlib" in cmd terminal
import matplotlib.pyplot as plt



x = np.linspace(-10, 10, 400)
y = np.linspace(-10, 10, 400)

X, Y = np.meshgrid(x, y)



## ANTENNA INFORMATION ##


antenna1 = {
    "x": 0,
    "y": 0,
    "frequency": 5,
    "wavelength": 2
}

antenna2 = {
    "x": 2,
    "y": 0,
    "frequency": 5,
    "wavelength": 2
}

antenna3 = {
    "x": 5,
    "y": 5,
    "frequency": 5,
    "wavelength": 2
}
antennas = [antenna1, antenna2, antenna3]
## SENSOR INFORMATION ##
sensor_x = 5
sensor_y = 0





for t in np.linspace(0, 5, 100):    
    Z = np.zeros_like(X)
    for antenna in antennas:
        antenna_x = antenna["x"]
        antenna_y = antenna["y"]
        frequency = antenna["frequency"]
        wavelength = antenna["wavelength"]

        k = 2 * np.pi / wavelength ## k is the wave number, which is 2*pi/wavelength
        omega = 2 * np.pi * frequency ## omega is the angular frequency, which is 2*pi*frequency
        R = np.sqrt((X - antenna_x)**2 + (Y - antenna_y)**2)
        Z += np.cos(k*R - omega*t)

    plt.clf() ## clrs frame for each time step
    plt.contourf(X, Y, Z, levels=100, cmap='gray') ## displays wave as a contour plot
##plt.scatter(sensor_x, sensor_y, color='blue', label='Sensor')
    for antenna in antennas:
        antenna_x = antenna["x"]
        antenna_y = antenna["y"]
        plt.scatter(antenna_x, antenna_y, color='red', label='Antenna') ## Displays antenna on grid
    
    plt.grid(True)
    plt.xlim(-10, 10)## displays an easy grid (x,y) bound from (0,0) to (10,10)
    plt.ylim(-10, 10)
    plt.axhline(0, linewidth=2, color='black')
    plt.axvline(0, linewidth=2, color='black') 
    plt.pause(0.03)
plt.show()




## simple html page to display results of any kinds of data transformations.
## It makes it easy to see without spamming print statements
app = Flask(__name__)
@app.route('/')
def home():
    result = result
    return render_template('index.html', info=result)


class antenna(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
##

## Recieve xm (Time Series)

## Perform FFT on xm by using an FFT library (easiest)

##

## Create the Cross-Spectral Density Matrix, G(f)

## Use Eigenvalue Decomposition to get G = VDV^H

## Get the Eigenmodes, vi by using vi = sqrt(eigenvalue(i))*ui



# Process of IBF and stuff













## Getting xm, need to see if there is a FFT library 