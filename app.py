## VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVvv ##
## run "pip install matplotlib" in cmd terminal
## run "pip install sympy"
## run "pip install pandas"
## run "pip install SQLAlchemy"
##
## To run script, type "python app.py" in console
## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^##



###################################################
## MATH RELATED LIBS
import sympy as sp
from sympy import sin, cos
import numpy as np
import math
###################################################



###################################################
## FILE GENERATION RELATED LIBS
import csv
import pandas as pd
###################################################



###################################################
## MATPLOTLIB LIBRARY
import matplotlib.pyplot as plt
##############################################



###################################################
## ALL DATABASE/FLASK RELATED LIBS
import os ## FOR REFRESHING DB FILE

import sqlite3 ## FOR ACCESSING SQLite3 (database library for using sql)

from flask import g ## Idk why its called "g" but this is the global object for storing data (db)
from flask import Flask, render_template, request, jsonify, redirect, url_for, request ## Routing related libs
###################################################



###################################################
## CONSTANTLY DUMPS DATABASE SO DATA ISNT CONSTANTLY ADDED EVERY INSTANCE
if os.path.exists("app.db"):
    os.remove("app.db")
###################################################



###################################################
## INITIALIZES FLASK FOR CONTEXTUAL FUNCTIONS
app = Flask(__name__)
###################################################



###################################################
db_file = "app.db" ## Establish where the database is located. For this, make sure console is cd'ed into the mhd-ibf-reconstruction folder
def get_db(): ## Function to connect to database
    connection = g.get('db', 'null') ## Grabs the Database
    if connection == 'null': ## checks for DB connection in global object, g. If statement runs when there isnt a connection
        g.db = sqlite3.connect(db_file) ## Connects to established db file
        g.db.row_factory = sqlite3.Row ## pretyy much just db formatting. Throws the data into rows so its easy to work with.
        return g.db ## now we can use the db
    else:
        return connection ## If the db already exists, then we just reuse the existing connection :)
####################################################



####################################################
## INTIALIZES FUNCTION TO CREATE THE TIMESERIES TABLE
def create_table():
    connection = get_db()
    sql = connection.cursor()
    connection.commit()
    sql.execute('''CREATE TABLE IF NOT EXISTS timeseries (
                "time" float,
                "amplitude" float,
                "sensorid" integer,
                "dataid" integer primary key autoincrement
                )''')
###################################################



###################################################
## INITIALIZES FUNCTION FOR CREATING DATA IN TIMESERIES TABLE
def insert_time_series(time, amplitude, sensornumber):
    print('INSERTING')
    connection = get_db()
    sql = connection.cursor()

    datum = [time, amplitude, sensornumber]
    sql.execute('''
                INSERT INTO timeseries (time, amplitude, sensorid) values (?, ?, ?)
                ''', list(datum))
    connection.commit()
####################################################



####################################################
## INTIALIZES DATA DATABASE
with app.app_context():
    create_table()
####################################################



######################################################
## ANTENNA INFORMATION ##
antenna1 = { ## Antenna at (0,0)
    "x": 0,
    "y": 0,
    "frequency": 5,
    "wavelength": 2,
    "phase": 0
}
antenna2 = { ## Antenna at (1,0)
    "x": 1,
    "y": 0,
    "frequency": 5,
    "wavelength": 2,
    "phase": np.pi/4
}
antenna3 = { ## Antenna at (-1,0)
    "x": -1,
    "y": 0,
    "frequency": 5,
    "wavelength": 2,
    "phase": -np.pi/4
}
antennas = [antenna1, antenna2, antenna3] ## Array of Phased Antennas as a var
for a in antennas:
    a["k"] = 2 * np.pi / a["wavelength"] ## k is the wave number, which is 2*pi/wavelength
    a["omega"] = 2 * np.pi * a["frequency"] ## omega is
## THIS LOOPS THROUGH EACH ANTENNA AND GIVES IT A WAVE NUMBER AND ANGULAR FREQUENCY (how fast the phase rotates with time)
#########################################################################



#######################
## SENSOR INFO
sensor1 = { ## Sensor at (3,8)
    "id": 0,
    "x": 3,
    "y": 8
}
sensor2 = { ## Sensor at (5,5)
    "id": 1,
    "x": 5,
    "y": 5
}
sensors = [sensor1, sensor2]## Sensor Array
########################################



###############################
## CONTROL OF DATA RESOLUTION (amount of data points and how many timestamps are picked up)
ll = 0 ## Lower Limt (t=i=0)
hl = 10 ## Higher Limit (t=N)
resolution = 100 ## Iterations
tval = np.linspace(ll, hl, resolution)
## Variable Holding Resolution Information
#####################################################



#######################
## SETS UP CUMULATIVE FIGURE WITH MULTIPLE SUBPLOTS
fig1, axes = plt.subplots(nrows=2)
########################################################



###########################
## CREATES TIME SERIES USING A SUM OF SIGNALS FROM ALL ANTENNAS (superposition)
time_series = [] ## INITIALIZES AN EMPTY SET 
for t in tval: ## LOOPS THROUGH EACH EARLIER DEFINED TIME POINTS
    for s_id, sensor in enumerate(sensors): ## Loops through each sensor while enumerating an ID so I can identify the specific sensor data in the database later.
        amplitude = 0 ## Resets Amplitude for each calculation
        for antenna in antennas: ##LOOPS THROUGH EACH ANTENNA
            R_sensor = np.sqrt((sensor["x"] - antenna["x"])**2 + (sensor["y"] - antenna["y"])**2) ## DISTANCE BETWEEN SENSOR AND EACH ANTENNA
            ## vvvv cos(kR - ωt + phase) vvvv 
            amplitude += np.cos(antenna['k'] * R_sensor - antenna['omega'] * t + antenna["phase"]) ## += is shorthand for adding onto a variable. In this case, each iteration of this for loop (for aech antenna) is adding onto the previous amplitude, creating a sum
        time_series.append([t, s_id, amplitude])
##########################################################



############################
## UPDATES THE DATABASE WITH TIME SERIES INFORMATION
with app.app_context():
    for item in time_series:
        times = item[0]
        sensornum = item[1]
        amplitude = item[2]
        datum = [times, sensornum, amplitude]
        insert_time_series(times, amplitude, sensornum)
################################################################################



#############################
## GRABS DATABASE DATA WITH SENSOR TIME SERIES ORDERED BY SENSOR NUMBER ##
with app.app_context():
    connection = get_db()
    sql = connection.cursor()
    data1 = sql.execute('''SELECT * FROM timeseries
                        ORDER BY sensorid ASC, dataid ASC''') ## Ordering by sensorid, which was assigned earlier. It is secondarily ordered by dataid so that the data still reads sinosoidally or however you spell it
    #for row in data1.fetchall():
        #print(row["time"], row["amplitude"], row['dataid'], row['sensorid'])
################################################################################



############################
## PLOTS ALL TIME SERIES
with app.app_context():
    for s in sensors: ## Loops through each sensor
        connection = get_db() ## Establishes Database Connection
        sql = connection.cursor() ## Saves into easy to use variable for running sql

        #############################################
        ## Grabs Time and Amplitude Data from the database at the specified sensor. It identifies it by the sensor id
        datum = sql.execute('''SELECT time, amplitude
                            FROM timeseries
                            WHERE sensorid = ?''',
                            (s['id'],)).fetchall() 

        times = np.array([row['time'] for row in datum]) ## Creates a list of times
        amplitudes = np.array([row['amplitude'] for row in datum]) ## Creates a list of amplitudes

        axes[s['id']].set(xlim=[ll,hl], ylim=[-5,5], title=f"Time Series at ({s['x']}, {s['y']})", ylabel='Y-axis', xlabel='X-Axis') ## Intializes the subplot.
        axes[s['id']].plot(times, amplitudes, color='red') ## Plots times against amplitudes in red.
######################################################################



######################################################################
## CREATES 3D ANIMATION OF WAVE PROPAGATION
## PS NEED TO EDIT TO ADD TO CUMULATIVE CHART
################################################
## DEFINES THE 2D PLANE
x = np.linspace(-10, 10, 400)
y = np.linspace(-10, 10, 400)
X, Y = np.meshgrid(x, y)
################################################
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
##########################################



############################################
## Routing, prob not useful but ima keep it

@app.route('/')
def home():
    result = result
    return render_template('index.html', info=result)


## Recieve xm (Time Series)

## Perform FFT on xm by using an FFT library (easiest)

##

## Create the Cross-Spectral Density Matrix, G(f)

## Use Eigenvalue Decomposition to get G = VDV^H

## Get the Eigenmodes, vi by using vi = sqrt(eigenvalue(i))*ui

# Process of IBF and stuff

