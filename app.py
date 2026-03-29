import sympy as sp
from flask import Flask, render_template, request, jsonify
from sympy import sin, cos
import numpy as np
import csv
import math

app = Flask(__name__)

@app.route('/')
def home():
    result = result
    return render_template('index.html', info=result)