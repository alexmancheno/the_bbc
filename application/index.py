from flask import Flask, request, jsonify
from flask_cors import CORS
from datascience import query, linear_regression, callProc, generate_query

app = Flask(__name__)
CORS(app)

# Goal is to return JSON after using the methods in datascience.py
# Example usage: http://localhost:8080/regression?vars=MBS,U
@app.route('/regression')
def regression():
    global table
    independent_vars = request.args['vars'].split(',')
    query = generate_query(independent_vars)
    results = linear_regression(query)
    return jsonify(results)

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
