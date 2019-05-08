import numpy as np
import pandas as pd
from pandas import DataFrame
import pymysql
import pymysql.cursors
from sshtunnel import SSHTunnelForwarder
from sklearn import linear_model
from sklearn.model_selection import train_test_split, KFold
from sklearn import metrics
import matplotlib as mpl
from matplotlib import pyplot as plt
import datetime as dt

table = {
    'CPI': {'table_name': 'BBC.Consumer_Price_Index_View', 'column_name':  'BBC.Consumer_Price_Index_View.Average_Cost'},
    'CPIHA': {'table_name': 'BBC.CPI_Housing_Average_View', 'column_name': 'BBC.CPI_Housing_Average_View.Housing_Average'},
    'DJI' : {'table_name': 'BBC.Dow_Jones_Index_View', 'column_name': 'BBC.Dow_Jones_Index_View.Close'},
    'FIR' : {'table_name': 'BBC.Federal_Interest_Rates_View', 'column_name': 'BBC.Federal_Interest_Rates_View.Prime_Rate'},
    'GDP': {'table_name': 'BBC.Gross_Domestic_Product_View', 'column_name': 'BBC.Gross_Domestic_Product_View.GDP'},
    'GSPC': {'table_name': 'BBC.GSPC_View', 'column_name': 'BBC.GSPC_View.close'},
    'MBS': {'table_name': 'BBC.Mortgage_Backed_Securities_View', 'column_name': 'BBC.Mortgage_Backed_Securities_View.Close'},
    'U': {'table_name': 'BBC.Unemployment_View', 'column_name': 'BBC.Unemployment_View.Unemployment_Rate'}
}

def generate_query(independent_vars):
    query = 'select Mortgage_Rates_View.Date, Mortgage_Rates_View.Mortgage_Rate'
    for var in independent_vars:
        query += ', %s' % table[var]['column_name']
    query += ' from BBC.Mortgage_Rates_View'
    for var in independent_vars:
        query += ' inner join %s on Mortgage_Rates_View.Date = %s.Date' % (table[var]['table_name'], table[var]['table_name']) 
    return query + ';'

def callProc(procName):
    with SSHTunnelForwarder(
        ('97.107.142.134', 22), 
        ssh_username="root",
        ssh_password="the_bbc123",
        remote_bind_address=('localhost', 3306)
    ) as server:
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
    df = query(s)
    x = df.drop('Date', axis=1)

    # the target variable
    y = x['Mortgage_Rate']

    # drop the target variable from the x-axis
    x = x.drop('Mortgage_Rate', axis=1)

    # run a linear regression holding out 20% of data as test data
    lm = linear_model.LinearRegression()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    lm.fit(x_train, y_train)
    y_pred = lm.predict(x_test)

    df1 = df.filter(items=['Date']) 
    df2 = pd.DataFrame(y_pred.flatten())
    df3 = y_test.to_frame()

    # print(df1)
    # print(df2)
    # print(df3)

    hlr = {}
    hlr['R^2'] = lm.score(x, y)
    hlr['coefficients'] = pd.DataFrame(lm.coef_, x.columns, columns=['Coefficient']).to_dict()
    hlr['intercept'] = lm.intercept_
    hlr['mean_absolute_error'] = metrics.mean_absolute_error(y_test, y_pred)
    hlr['mean_squared_error'] = metrics.mean_squared_error(y_test, y_pred)
    results['holdout_linear_regression'] = hlr

    # run a linear regression using K-Folds Cross Validation
    k = 5
    kf = KFold(n_splits=k, random_state=None, shuffle=False)
    kf.get_n_splits(x)
    scores = []
    for train_index, test_index in kf.split(x):
        x_train, x_test = x.iloc[train_index], x.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        lm = linear_model.LinearRegression()
        lm.fit(x_train, y_train)
        predictions = lm.predict(x_test)
        scores.append(lm.score(x, y))



    results['number_of_splits'] = k
    results['kfolds_R^2'] = np.mean(scores)
    return results
