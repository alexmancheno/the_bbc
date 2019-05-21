from flask import Flask, request, jsonify
from flask_cors import CORS
from datascience import query, linear_regression, callProc, generate_query, table, linear_regression_r_squared
from itertools import combinations
import operator

app = Flask(__name__)
CORS(app)

# Returns a list of regressions using all possible permutations
# of the independent variables in "table"
# curl http://localhost:8080/reglist
@app.route('/reglist')
def reglist():
    print('attempting to run /reglist')
    global table
    keyList = list(table.keys())
    results = []
    count = 0
    errors = 0
    for x in range(len(keyList)):
        comb = combinations(keyList, (x+1))
        for c in list(comb):
            try:
                q = generate_query(c)
                results.append(linear_regression_r_squared(q, list(c)))
                count +=1
            except:
                errors +=1
    print('success count: ', count, ', error count: ', errors)
    
    #print(results)
    results.sort(key=lambda x: x['r^2'], reverse = True)
    return jsonify(results)
        

# Goal is to return JSON after using the methods in datascience.py
# Example usage: http://localhost:8080/regression?vars=MBS,U
@app.route('/regression')
def regression():
    global table
    independent_vars = request.args['vars'].split(',')
    results = linear_regression(independent_vars)
    return jsonify(results)

@app.route('/actualData')
def actualData():
    global table
    results = query('SELECT * FROM BBC.Mortgage_Rates_View;')
    return jsonify(results.to_dict())

# Returns a list of the independent variables we can use
@app.route('/vars')
def vars():
    global table
    print('vars request received')
    arr = []
    for key in table.keys():
        arr.append(key)
    return jsonify(arr)

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

# Returns the R^2 value for the k-folds cross validation linear regression based in the independent values
# Example: http://localhost:8080/r_squared?vars=MBS,GDP,U
@app.route('/r_squared')
def r_squared():
    global table
    independent_vars = request.args['vars'].split(',')
    query = generate_query(independent_vars)
    results = linear_regression_r_squared(query, independent_vars)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
