#######################################################################################################################################################################################################################################################################################
##                                                                  LIBRARIES                                                               ########
#######################################################################################################################################################################################################################################################################################
###################################################
## MATH RELATED LIBS
import sympy as sp
from sympy import sin, cos
import numpy as np
import math
###################################################
## FILE GENERATION RELATED LIBS
import csv
import pandas as pd
###################################################
## MATPLOTLIB LIBRARY
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
##############################################
###################################################
## ALL DATABASE/FLASK RELATED LIBS
import os ## FOR REFRESHING DB FILE

import sqlite3 ## FOR ACCESSING SQLite3 (database library for using sql)

from flask import g ## Idk why its called "g" but this is the global object for storing data (db)
from flask import Flask, render_template, request, jsonify, redirect, url_for, request ## Routing related libs
###################################################

#######################################################################################################################################################################################################################################################################################
##                                                                  INITIALIZATIONS                                                               ########
#######################################################################################################################################################################################################################################################################################
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
    ##print('INSERTING')
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



#######################################################################################################################################################################################################################################################################################
##                                                                  ENVIRONMENT INFO                                                               ########
#######################################################################################################################################################################################################################################################################################
## ANTENNA INFORMATION ##
antenna1 = { ## Antenna at (0,0)
    "x": 0,
    "y": 0,
    "z": 0,
    "frequency": 5,
    "wavelength": 2,
    "phase": 0
}
antenna2 = { ## Antenna at (1,0)
    "x": 1,
    "y": 0,
    "z": 1,
    "frequency": 5,
    "wavelength": 2,
    "phase": np.pi/4
}
antenna3 = { ## Antenna at (-1,0)
    "x": -1,
    "y": 0,
    "z": 1,
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
    "y": 8,
    "z": 0
}
sensor2 = { ## Sensor at (5,5)
    "id": 1,
    "x": 5,
    "y": 5,
    "z": 0
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
##fig1, axes = plt.subplots(nrows=2)
import matplotlib.gridspec as gridspec ## This library makes it really efficient to make good systems of plots i.e. it translates the pop-up window into a grid system that you can set cells to certain subplots and such. In this case, a couple of the plots are for the time series, and a large section is for the 3d animation.
fig = plt.figure(figsize=(15, 10)) ## initializes the pop-up window basically. figsize represents the size of the window as it displays on the monitor.
gs = gridspec.GridSpec(2,3) ## this function uses the library to initialize the grid specifications, gs, as a gridSpec of 2 rows and 3 columns. Hence, the (2,3) represents (# rows, # columns).

axltop = fig.add_subplot(gs[0,0]) ## add_subplot creates a subfigure for a specific space in the grid spec. For this one, it takes the first column (column 0) and the first row (row 0). Hence, this subplot takes up row 0, column 0, and is just a single cell, essentially.
axlbottom = fig.add_subplot(gs[1,0]) ## Same concept, but it creates it on the second row (row 1) and the first column (column 0). For reference, use flask run to view the window. These first two are going to be used by the time series. 
## i.e. for each time series, it takes up once cell as per the grid spec.
column1 = [axltop, axlbottom] ## this just throws the two cells used by time series into a list so it's easy to use in a "For" Loop. See time series function for reference.
ax3d = fig.add_subplot(gs[:, 1:], projection='3d') ## This initializes a subplot for the 3d figure. it uses a spec of all rows (represented by ":") and all columns including and after the second column (column 1)
## therefore the window will look like:
##
## | Time Series1 | 3d plot  | 3d plot
## | Time Series2 | 3d plot  | 3d plot
##


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


        column1[s['id']].set(xlim=[ll,hl], ylim=[-5,5], title=f"Time Series at ({s['x']}, {s['y']})", ylabel='Y-axis', xlabel='X-Axis') ## Intializes the subplot.
        column1[s['id']].plot(times, amplitudes, color='red') ## Plots times against amplitudes in red.
        ## ^^ For this, since the id is either 0 or 1, each sensor adds to a unique subplot in the pop-up window. I.E, this function will end up looking like:
        ## column1[0]... << represents the first cell (0,0)
        ## column1[1]... << represents the second cell (1,0)

        ## the function starts by setting the criteria for the plot. Xlim is how many xvalues it process and ylim is the same. title and labels are straightforward.
        ## second line plots it obviously.
######################################################################



######################################################################
## CREATES 3D ANIMATION OF WAVE PROPAGATION
## PS NEED TO EDIT TO ADD TO CUMULATIVE CHART
################################################

from skimage import measure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

x = np.linspace(-10, 10, 50) ## describes the x values as from -10 to positive 10 in 100 steps.
y = np.linspace(-10, 10, 50) ## same concept
z = np.linspace(-10, 10, 50)

X, Y, Z = np.meshgrid(x, y, z, indexing='ij') ## initializes the x and y values as an x,y coordinate system essentially

##def field(time):
    ##waves = np.zeros_like(X) ## intializes Z as a 0 matrix, i.e. it starts with a fresh grid with no data.
    ##for antenna in antennas:
        ##R = np.sqrt((X - antenna["x"])**2 + 
                    ##(Y - antenna["y"])**2 + 
                    ##(Z - antenna['z'])**2) ## initializes a matrix representing all distances from the antenna.
        ##waves += np.sin(antenna['k']*R - antenna['omega']* time *0.45 + antenna["phase"]) ## describes the wave at a certain point in the grid. This is given by the distance at each point, R, and the "frame*0.45" represents the time. the 0.45 represents that the wave will propagate at 45% speed so its easier to see whats goin on.
    ##print(waves)
    ##return waves
##simwaves = field(0)
simwaves = np.load('waves.npy')
fig.patch.set_facecolor('grey')
ax3d.set_facecolor('grey')
ax3d.set_facecolor('grey') ## Styling
ax3d.set_xlim(-10,10) ## Sets the 3d box x, y, and z specifications
ax3d.set_ylim(-10,10)
ax3d.set_zlim(-10,10)


np.save("waves.npy", simwaves)

verts, faces, murks, _ = measure.marching_cubes(simwaves**2, level=2)
dx = x[1] - x[0]
dy = y[1] - y[0]
dz = z[1] - z[0]

verts[:,0] = x[0] + verts[:,0] * dx
verts[:,1] = y[0] + verts[:,1] * dy
verts[:,2] = z[0] + verts[:,2] * dz
ax3d.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], cmap='jet', lw=1)
ax3d.axis('on'); 
for antenna in antennas:
    ax3d.scatter(
        antenna['x'],
        antenna['y'],
        antenna['z'],
        c='red'
    )
## sets up a function for animating per frame
plt.show() ## finally displays the plot

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

