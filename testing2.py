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



#######################################################################################################################################################################################################################################################################################
##                                                                  ENVIRONMENT INFO                                                               ########
#######################################################################################################################################################################################################################################################################################
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
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
#######################
## SETS UP CUMULATIVE FIGURE WITH MULTIPLE SUBPLOTS
##fig1, axes = plt.subplots(nrows=2)

import matplotlib.gridspec as gridspec
fig = plt.figure()
gs = gridspec.GridSpec(2,3)

axltop = fig.add_subplot(gs[0,0])
axlbottom = fig.add_subplot(gs[1,0])
axrlarge = fig.add_subplot(gs[:, 1:3])


axltop.set

plt.show()
########################################################