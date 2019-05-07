from flask import Flask, request, jsonify

from datascience import query, linear_regression, callProc
app = Flask(__name__)

# Goal is to return JSON after using the methods in datascience.py
@app.route('/regression')
def hello_world():

    query = 'Select mr.Date, mr.Mortgage_Rate, mbs.Close from BBC.Mortgage_Rates as mr inner join BBC.Mortgage_Backed_Securities as mbs on mr.date = mbs.date;'

    results = linear_regression(query)
    
    return jsonify(results)

@app.route('/indepents')
def targets():
    #return possible variables/columns to target from DB
    result = ["INDEPEND1","INDEPEND2"]
    return result

@app.route('/dependents')
def dependents():
    #return possible columns to depend on
    proc = callProc("GetColumns")
    result = ["DEPEND1", "DEPEND2"]
    print(proc)
    return jsonify(proc)

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
