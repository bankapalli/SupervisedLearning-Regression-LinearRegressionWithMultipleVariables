# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 05:32:52 2018

@author: venkata
"""

#importing packages
import os
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plot 

#This function is used to load CSV file from the 'data' directory 
#in the present working directly 
def loadCSV (fileName):
    scriptDirectory = os.path.dirname(__file__)
    dataDirectoryPath = "."
    dataDirectory = os.path.join(scriptDirectory, dataDirectoryPath)
    dataFilePath = os.path.join(dataDirectory, fileName)
    return pd.read_csv(dataFilePath)

def previewData (dataSet):
    print(dataSet.head())
    print("\n")

#This function is used to check for missing values in a given dataSet
def checkForMissingValues (dataSet):
    print(dataSet.isnull().sum())
    print("\n")

#This function is used to check the statistics of a given dataSet
def getStatisticsOfData (dataSet):
    print("***** Datatype of each column in the data set: *****")
    dataSet.info()
    print("\n")
    print("***** Columns in the data set: *****")
    print(dataSet.columns.values)
    print("***** Details about the data set: *****")
    print(dataSet.describe())
    print("\n")
    print("***** Checking for any missing values in the data set: *****")
    checkForMissingValues(dataSet)
    print("\n")
    
def handleMissingValues (features):
    from sklearn.preprocessing import Imputer
    imputer = Imputer(missing_values='NaN',strategy='mean',axis=0)
    imputer.fit(features)
    imputedFeatures = imputer.fit_transform(features)
    return imputedFeatures
    
#Define file names and call loadCSV to load the CSV files
dataFile = "kc_house_data.csv"
dataSet = loadCSV(dataFile)

#Preview the dataSet and look at the statistics of the dataSet
#Check for any missing values 
#so that we will know whether to handle the missing values or not
print("***** Preview the dataSet and look at the statistics of the dataSet *****")
previewData(dataSet)
getStatisticsOfData(dataSet)

#In this simple eample we want to perform linear regression for predicting the
#price of the house given the area of the house, number of bedrooms, number of bathrooms
selectedFeatures=dataSet.values[:,[3,4,5]]
#Handle missing data before training the model
selectedFeatures = handleMissingValues(selectedFeatures)
price=dataSet['price']

x = np.array(selectedFeatures)
y = np.array(price)

#Splitting the data into Train and Test
from sklearn.cross_validation import train_test_split
xtrain, xtest, ytrain, ytest = train_test_split(x,y,test_size=0.25,random_state=0)

#Fitting simple linear regression to the Training Set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(xtrain, ytrain)
#Predicting the prices
pricePredictions = regressor.predict(xtest)

# The coefficients
print 'Coefficients: ', regressor.coef_
from sklearn.metrics import mean_squared_error
print "Mean squared error: ",mean_squared_error(ytest, pricePredictions)
from sklearn.metrics import r2_score
accuracyMeassure = r2_score(ytest, pricePredictions)
print "Accuracy of model is {}%".format(accuracyMeassure*100)

#TODO : I will have to work on the Visualization techniques