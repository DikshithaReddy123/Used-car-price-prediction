# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 16:58:27 2020

@author: Mamidi Dikshitha
"""

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('car_random_forest_regression_model_.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    fuel_type_diesel=0
    if request.method == 'POST':
        year = int(request.form['year'])
        priceUSD=int(request.form['priceUSD'])
        mileage=float(request.form['mileage'])
        volume=request.form['volume']
        segment=(request.form['segment'])
        condition_with_mileage=request.form['condition_with_mileage']
        if(condition_with_mileage=='with mileage'):
            condition_with_mileage=1
            condition_with_damage=0
        elif(condition_with_mileage=='with damage'):
            condition_with_mileage=0
            condition_with_damage=1
        else:
            condition_with_mileage=0
            condition_with_damage=0
        fuel_type_petrol=request.form['fuel_type_petrol']
        if(fuel_type_petrol=='petrol'):
                fuel_type_petrol=1
                fuel_type_diesel=0
        elif(fuel_type_petrol=='diesel'):
                fuel_type_petrol=0
                fuel_type_diesel=1
        else:
            fuel_type_petrol=0
            fuel_type_diesel=0
        year=2020-year
        color_black=request.form['color_black']
        if(color_black=='black'):
            color_black=1
            color_white=0
        elif(color_black=='white'):
            color_black=0
            color_white=1
        else:
            color_black=0
            color_white=0
        drive_unit_front_wheel_drive=request.form['drive_unit_front_wheel_drive']
        if(drive_unit_front_wheel_drive=='front-wheel drive'):
            drive_unit_front_wheel_drive=1
            drive_unit_all_wheel_drive=0
        elif(drive_unit_front_wheel_drive=='all-wheel drive'):
            drive_unit_front_wheel_drive=0
            drive_unit_all_wheel_drive=1
        else:
            drive_unit_front_wheel_drive=0
            drive_unit_all_wheel_drive=0
        transmission_mechanics=request.form['transmission_mechanics']
        if(transmission_mechanics=='mechanics'):
            transmission_mechanics=1
        else:
            transmission_mechanics=0
        prediction=model.predict([[priceUSD,mileage,condition_with_mileage,condition_with_damage,drive_unit_front_wheel_drive,drive_unit_all_wheel_drive,color_black, color_white,volume,segment,year,fuel_type_diesel,fuel_type_petrol,transmission_mechanics]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

