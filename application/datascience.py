import numpy as np
import pandas as pd
from pandas import DataFrame
import pymysql
import pymysql.cursors
from sshtunnel import SSHTunnelForwarder
from sklearn import linear_model
from sklearn.model_selection import train_test_split, KFold
from sklearn.svm import SVR
import matplotlib as mpl
from matplotlib import pyplot as plt
import datetime as dt

def callProc(procName):
    with SSHTunnelForwarder(
        ('97.107.142.134', 22), 
        ssh_username="root",
        ssh_password="the_bbc123",
        remote_bind_address=('localhost', 3306)
    )as server:
        conn = pymysql.connect(host='localhost', user='admin', password='radman', db='BBC', port=server.local_bind_port)
        cursor = conn.cursor()
        cursor.callproc(procName)
        result = cursor.fetchall()
    return result
    

def query(q):
    with SSHTunnelForwarder(
        ('97.107.142.134', 22),
        ssh_username="root",
        ssh_password="the_bbc123",
        remote_bind_address=('localhost', 3306)
    ) as server:
        conn = pymysql.connect(host='localhost', user='admin', password='radman', db='BBC', port=server.local_bind_port)
        curr = conn.cursor()
        curr.execute(q)
        df = DataFrame(list(curr.fetchall()))
        column_names = [i[0] for i in curr.description]
        df.columns = column_names
        curr.close()
        conn.close()
        return df

def linear_regression(s):
    # what will be returned at the end
    results = {}

    # query database and return results as a DataFrame
    x = query(s)
    
    # clean the format of the 'Date' column
    x['Date'] = pd.to_datetime(x['Date'])

    # the target variable
    y = x['Mortgage_Rate']

    # drop the target variable from the x-axis
    x = x.drop('Mortgage_Rate', axis=1)

    # change the data type of 'date' to a type that sklearn can read
    x['Date'] = x['Date'].map(dt.datetime.toordinal)

    # run a linear regression holding out 20% of data as test data
    lm = linear_model.LinearRegression()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    lm.fit(x_train, y_train)
    y_pred = lm.predict(x_test)
    results['holdout_linear_regression_score'] = lm.score(x, y)

    # run a linear regression using K-Folds Cross Validation
    kf = KFold(n_splits=5, random_state=None, shuffle=False)
    kf.get_n_splits(x)
    scores = []
    for train_index, test_index in kf.split(x):
        x_train, x_test = x.iloc[train_index], x.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        lm = linear_model.LinearRegression()
        model = lm.fit(x_train, y_train)
        predictions = lm.predict(x_test)
        scores.append(lm.score(x, y))
    results['kfolds_linear_regression_score'] = np.mean(scores)

    # start predicting!
    # run linear regressions for each independent variable
    independent_var_predictions = {}
    offset = x['Date'].values[-1] - x['Date'].values[-2]
    start = x['Date'][x.index.max()]
    local_x = x.filter(['Date'])
    # print('local_x: ', local_x)
    for column in x.drop('Date', axis=1):
        local_y = x.filter([column])
        # print('local_y: ', local_y)
        lm = linear_model.LinearRegression()
        lm.fit(local_x, local_y) # train the linear regression model
        arr = []
        coefficient = lm.coef_[0][0]
        intercept = lm.intercept_[0]
        # print('coef: ', coefficient)
        # print('intercept: ', intercept)
        # print('start: ', start)
        # print('offset: ', offset)
        # add the next 5 predicted values for independent values
        for i in range(1, 6):
            arr.append(coefficient * (start + i * offset) + intercept)
        independent_var_predictions[column] = arr

    # print(independent_var_predictions)
    # append the next 5 rows to the x-axis and y-axis
    length = x.index.max()
    for i in range(1, 6):
        row = []
        row.append(start + i * offset) # append the date first
        for column in x.drop('Date', axis=1):
            row.append(independent_var_predictions[column][i - 1])
        x.loc[length + i] = row 

    return results
