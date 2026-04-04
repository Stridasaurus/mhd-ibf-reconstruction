import sympy as sp
from flask import Flask, render_template, request, jsonify
from sympy import sin, cos
import numpy as np
import csv
import math





## simple html page to display results of any kinds of data transformations.
## It makes it easy to see without spamming print statements
app = Flask(__name__)
@app.route('/')
def home():
    result = result
    return render_template('index.html', info=result)

##

## Recieve xm (Time Series)

## Perform FFT on xm by using an FFT library (easiest)

##

## Create the Cross-Spectral Density Matrix, G(f)

## Use Eigenvalue Decomposition to get G = VDV^H

## Get the Eigenmodes, vi by using vi = sqrt(eigenvalue(i))*ui



# Process of IBF and stuff













## Getting xm, need to see if there is a FFT library 