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
    'DJI' : {'table_name': 'BBC.Dow_Jones_Index_View', 'column_name': 'BBC.Dow_Jones_Index_View.DJIClose'},
    'FIR' : {'table_name': 'BBC.Federal_Interest_Rates_View', 'column_name': 'BBC.Federal_Interest_Rates_View.Prime_Rate'},
    'GDP': {'table_name': 'BBC.Gross_Domestic_Product_View', 'column_name': 'BBC.Gross_Domestic_Product_View.GDP'},
    'GSPC': {'table_name': 'BBC.GSPC_View', 'column_name': 'BBC.GSPC_View.GSPCClose'},
    'MBS': {'table_name': 'BBC.Mortgage_Backed_Securities_View', 'column_name': 'BBC.Mortgage_Backed_Securities_View.MBSClose'},
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

# parameter: a list of indepenedent variables
def linear_regression(independent_vars):
    # what will be returned at the end
    results = {'independent_variables': independent_vars}

    # build the sql query string
    q = generate_query(independent_vars)

    # query database and return results as a DataFrame
    df = query(q)
    x = df
    
    y = x['Mortgage_Rate'] # type: Series

    # drop the target variable from the x-axis
    x = x.drop('Mortgage_Rate', axis=1) # returns DataFrame

    # run a linear regression holding out 20% of data as test data
    lm = linear_model.LinearRegression()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    lm.fit(x_train.drop('Date', axis=1), y_train) # runs linear regression
    y_pred = lm.predict(x_test.drop('Date', axis=1))


    # print(x_test)
    df1 = x_test.filter(items=['Date']) # dates
    df2 = pd.DataFrame(y_pred.flatten()) # predictions
    df3 = y_test.to_frame() # actual
    
    arr1 = df1['Date'].tolist()
    arr2 = df2[0].tolist()
    arr3 = df3['Mortgage_Rate'].tolist()

    r = []
    for i in range(0, len(arr1)):
        r.append([arr1[i], arr2[i], arr3[i]])
    r = sorted(r, key=lambda x: x[0])
    for i in range(0, len(r)):
        r[i][0] = str(r[i][0])
    
    coeff_arr = []
    coeff_num_arr = lm.coef_.tolist()
    for i in range(0, len(independent_vars)):
        coeff_arr.append({'independent_var':independent_vars[i], 'coefficient':coeff_num_arr[i]})

    hlr = {}
    results['true_vs_prediction'] = r
    hlr['coefficients'] = coeff_arr
    hlr['R^2'] = lm.score(x.drop('Date', axis=1), y)
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

        lm.fit(x_train.drop('Date', axis=1), y_train)
        predictions = lm.predict(x_test.drop('Date', axis=1))
        scores.append(lm.score(x.drop('Date', axis=1), y))

    kfcv = {}
    kfcv['number_of_splits'] = k
    kfcv['R^2'] = np.mean(scores)
    results['k_folds_linear_regression'] = kfcv
    return results

def linear_regression_r_squared(q, independent_vars):
    results = {}

    x = query(q).drop('Date', axis=1)
    y = x['Mortgage_Rate']
    x = x.drop('Mortgage_Rate', axis=1)

    k = 5
    kf = KFold(n_splits=k, random_state=None, shuffle=False)
    kf.get_n_splits(x)
    scores = []
    for train_index, test_index in kf.split(x):
        x_train, x_test = x.iloc[train_index], x.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        lm = linear_model.LinearRegression()  
        lm.fit(x_train, y_train)
        y_pred = lm.predict(x_test)
        scores.append(lm.score(x, y))

    results = {
        'independent_variables': independent_vars,
        'r^2': np.mean(scores)
    }

    return results