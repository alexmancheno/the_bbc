import numpy as np
import pandas as pd
from pandas import DataFrame
import pymysql
import pymysql.cursors
from sshtunnel import SSHTunnelForwarder
from sklearn import linear_model
from sklearn.model_selection import train_test_split, KFold
from sklearn.svm import SVR
from matplotlib import pyplot as plt
import datetime as dt

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


    # run a linear regression (no techniques)
    lm = linear_model.LinearRegression()
    model = lm.fit(x,y)
    predictions = lm.predict(x)
    results['regular_linear_regression_score'] = lm.score(x,y)
    # print(predictions[0:5])

    # run a linear regression holding out 20% of data as test data
    lm = linear_model.LinearRegression()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    model = lm.fit(x_train, y_train)
    predictions = lm.predict(x_test)
    results['holdout_linear_regression_score'] = lm.score(x, y)

    # run a linear regression using K-Folds Cross Validation
    kf = KFold(n_splits=5, random_state=None, shuffle=False)
    kf.get_n_splits(x)
    scores = []
    best_svr = SVR(kernel='rbf')
    for train_index, test_index in kf.split(x):
        x_train, x_test = x.iloc[train_index], x.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        lm = linear_model.LinearRegression()
        model = lm.fit(x_train, y_train)
        predictions = lm.predict(x_test)
        scores.append(lm.score(x, y))
    
    results['kfolds_linear_regression_score'] = np.mean(scores)
    return results