import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
#from sklearn import metrics
#import csv

def svm_pred(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    data = pd.read_csv("heart.csv")
    
    train = data.drop('target', axis = 1)
    target = data.target
    
    X_train, X_test, y_train, y_test = train_test_split( train, target, test_size = 0.3, random_state = 109 )
    
    clf = svm.SVC( kernel = 'linear' )
    clf.fit(X_train, y_train)
    
    #y_pred = clf.predict(X_test)
    #print( "\nX test Output: \n", y_pred )
    
    #print( "\nAccuracy:", metrics.accuracy_score(y_test, y_pred) )
    #print( "Precision:", metrics.precision_score(y_test, y_pred) )
    #print( "Recall:", metrics.recall_score(y_test, y_pred) )
    												
		

    NewData = [[536381,21672,6,12/1/2010,1.25,15311], [InvoiceNo, StockCode, Quantity, InvoiceDate,UnitPrice, CustomerID]]
    #print( "My Test Case:\n", clf.predict(NewData) )
    # Output Extected: 1,0  [52,1,0,128,255,0,1,161,1,0,2,1,3]
    result = clf.predict(NewData)[1]
    '''
    with open("heart.csv","a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result])
    '''
    return result
    
