from flask import Flask, request, jsonify

from datascience import query, linear_regression
app = Flask(__name__)

# Goal is to return JSON after using the methods in datascience.py
@app.route('/regression')
def hello_world():
    query = 'Select mr.Date, mr.Mortgage_Rate, mbs.Close from BBC.Mortgage_Rates as mr inner join BBC.Mortgage_Backed_Securities as mbs on mr.date = mbs.date;'

    results = linear_regression(query)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(port=8080)