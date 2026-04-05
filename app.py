import sympy as sp
from flask import Flask, render_template, request, jsonify, redirect, url_for, request
from sympy import sin, cos
import numpy as np
import csv
import math
##from flask_sqlalchemy import SQLAlchemy
import pandas as pd
## VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVvv ##
## run "pip install matplotlib" in cmd terminal
## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^##

import matplotlib.pyplot as plt



x = np.linspace(-10, 10, 400)
y = np.linspace(-10, 10, 400)

X, Y = np.meshgrid(x, y)



## ANTENNA INFORMATION ##


antenna1 = {
    "x": 0,
    "y": 0,
    "frequency": 5,
    "wavelength": 2,
    "phase": 0
}

antenna2 = {
    "x": 1,
    "y": 0,
    "frequency": 5,
    "wavelength": 2,
    "phase": np.pi/4
}

antenna3 = {
    "x": -1,
    "y": 0,
    "frequency": 5,
    "wavelength": 2,
    "phase": -np.pi/4
}
antennas = [antenna1, antenna2, antenna3]

for a in antennas:
    a["k"] = 2 * np.pi / a["wavelength"] ## k is the wave number, which is 2*pi/wavelength
    a["omega"] = 2 * np.pi * a["frequency"] ## omega is

## SENSOR INFORMATION ##
sensor1 = {
    "x": 0,
    "y": 10
}
sensor2 = {
    "x": 5,
    "y": 5
}
sensors = [sensor1, sensor2]
tval = np.linspace(0, 5, 100)

time_series = []
for t in tval:
    for s_id, sensor in enumerate(sensors):
        amplitude = 0
        for antenna in antennas:
            antenna_x = antenna["x"]
            antenna_y = antenna["y"]

            k = antenna["k"]
            omega = antenna["omega"]

            sensor_x = sensor["x"]
            sensor_y = sensor["y"]
            R_sensor = np.sqrt((sensor_x - antenna_x)**2 + (sensor_y - antenna_y)**2)
            amplitude += np.cos(k * R_sensor - omega * t + antenna["phase"]) ## signal at sensor is the sum of signals from all antennas
        time_series.append([t, s_id, amplitude])

print(time_series)

for s in sensors:
    svalues = []
    for t in tval:
        sensor_value = 0
        for antenna in antennas:
            antenna_x = antenna["x"]
            antenna_y = antenna["y"]

            k = antenna["k"]
            omega = antenna["omega"]

            sensor_x = s["x"]
            sensor_y = s["y"]
            R_sensor = np.sqrt((sensor_x - antenna_x)**2 + (sensor_y - antenna_y)**2)
            sensor_value += np.cos(k * R_sensor - omega * t + antenna["phase"]) ## signal at sensor is the sum of signals from all antennas
        svalues.append(sensor_value) ## average signal from all antennas at sensor location

    plt.figure()
    plt.plot(tval, svalues)
    plt.ylim(-5,5)
    plt.title(f"Sensor Time Series at ({s['x']},{s['y']})")
    plt.xlabel("Time")
    plt.ylabel("Signal")
    plt.grid(True)



Z_frames = []
for t in tval:  
    Z = np.zeros_like(X) ## initialize Z as a zero matrix for each time step
        
    for antenna in antennas:
        antenna_x = antenna["x"]
        antenna_y = antenna["y"]

        k = antenna["k"]
        omega = antenna["omega"]
        
        R = np.sqrt((X - antenna_x)**2 + (Y - antenna_y)**2)
        Z += np.cos(k*R - omega*t + antenna["phase"]) ## wave field at time t is the sum of contributions from all antennas
        
    Z_frames.append(Z)    
plt.ion()
fig = plt.figure()
for Z in Z_frames:
    plt.clf() ## clear the plot for the next frame
    plt.contourf(X, Y, Z, levels=50, cmap='gray') ## displays wave as a contour plot
    for antenna in antennas:
        plt.scatter(antenna["x"], antenna["y"], color='red', label='Antenna') ## Displays antenna on grid
    for sensor in sensors:
        plt.scatter(sensor["x"], sensor["y"], color='blue', label='Sensor') ## Displays sensor on grid
    plt.grid(True)
    plt.xlim(-10, 10) ## displays an easy grid (x,y) bound from (0,0) to (10,10)
    plt.ylim(-10, 10)
    plt.pause(0.01)
plt.ioff()
plt.show()







    
    


       
       
       
       




## simple html page to display results of any kinds of data transformations.
## It makes it easy to see without spamming print statements
#app = Flask(__name__)
#@app.route('/')
#def home():
#    result = result
#    return render_template('index.html', info=result)


#class antenna(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String, nullable=False)
#   location = db.Column(db.String, nullable=False)
##



## Recieve xm (Time Series)

## Perform FFT on xm by using an FFT library (easiest)

##

## Create the Cross-Spectral Density Matrix, G(f)

## Use Eigenvalue Decomposition to get G = VDV^H

## Get the Eigenmodes, vi by using vi = sqrt(eigenvalue(i))*ui



# Process of IBF and stuff













## Getting xm, need to see if there is a FFT library 