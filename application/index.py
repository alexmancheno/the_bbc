from flask import Flask
import numpy
import pandas as pd
from pandas import DataFrame
import statsmodels
import pymysql
import pymysql.cursors
from sshtunnel import SSHTunnelForwarder
from sklearn import linear_model
app = Flask(__name__)

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

@app.route('/')
def hello_world():
    return 'Hello, World!' 

df = query('Select * from BBC.Mortgage_Rates as mr inner join BBC.Mortgage_Backed_Securities as mbs on mr.date = mbs.date;')
x = df
y = df['Mortgage_Rate']
lm = linear_model.LinearRegression()
model = lm.fit(x,y)
print(df)