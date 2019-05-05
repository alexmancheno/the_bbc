from flask import Flask
import numpy
import pandas as pd
from pandas import DataFrame
import pymysql
import pymysql.cursors
from sshtunnel import SSHTunnelForwarder
from sklearn import linear_model
import datetime as dt
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

df = query('Select mr.Date, Mortgage_Rate, Close, Volume, Open, High, Low from BBC.Mortgage_Rates as mr inner join BBC.Mortgage_Backed_Securities as mbs on mr.date = mbs.date;')
x = df
x['Date'] = pd.to_datetime(x['Date'])
x = x.drop('Mortgage_Rate', axis=1)
x['Date'] = x['Date'].map(dt.datetime.toordinal)

print(x)
y = df['Mortgage_Rate']
lm = linear_model.LinearRegression()
model = lm.fit(x,y)
predictions = lm.predict(x)
print(predictions[0:5])
print(lm.score(x, y))