from flask import Flask, request, jsonify
from flask_cors import CORS
from datascience import query, linear_regression, callProc, generate_query, table
from itertools import combinations
import operator

app = Flask(__name__)
CORS(app)

# Returns a list of regressions using all possible permutations
# of the independent variables in "table"
# curl http://localhost:8080/reglist
@app.route('/reglist')
def reglist():
    global table
    keyList = list(table.keys())
    results = []
    count = 0
    for x in range(len(keyList)):
        comb = combinations(keyList, (x+1))
        for c in list(comb):
            try:
                q = generate_query(c)
                #results.append(linear_regression(generate_query(list(c))))
                count +=1
                print(count,":", list(c));
                print(q)
                print("---------------")
                results.append(linear_regression(generate_query(list(c))))
            except:
                print('Error: ')
                print('\tlist: ', list(comb))
                print(q)
    results.sort(key=operator.itemgetter('kfolds_R^2'), reverse=True)
    return jsonify(results)
        

# Goal is to return JSON after using the methods in datascience.py
# Example usage: http://localhost:8080/regression?vars=MBS,U
@app.route('/regression')
def regression():
    global table
    independent_vars = request.args['vars'].split(',')
    query = generate_query(independent_vars)
    results = linear_regression(query)
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

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
