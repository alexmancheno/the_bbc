from flask import Flask, request, jsonify
from flask_cors import CORS
from datascience import query, linear_regression, callProc

app = Flask(__name__)
CORS(app)

table = {
    'CPI': {'table_name': 'BBC.Consumer_Price_Index_View', 'column_name':  'BBC.Consumer_Price_Index_View.Average_Cost'},
    'CPIHA': {'table_name': 'BBC.CPI_Housing_Average_View', 'column_name': 'BBC.CPI_Average_Housing_View.Housing_Average'},
    'DJI' : {'table_name': 'BBC.Dow_Jones_Index_View', 'column_name': 'BBC.Dow_Jones_Index_View.Close'},
    'FIR' : {'table_name': 'BBC.Federal_Interest_Rates_View', 'column_name': 'BBC.Federal_Interest_Rates_View.Prime_Rate'},
    'GDP': {'table_name': 'BBC.Gross_Domestic_Product_View', 'column_name': 'BBC.Gross_Domestic_Product_View.GDP'},
    'GSPC': {'table_name': 'BBC.GSPC_View', 'column_name': 'BBC.GSPC_View.close'},
    'MBS': {'table_name': 'BBC.Mortgage_Backed_Securities_View', 'column_name': 'BBC.Mortgage_Backed_Securities_View.Close'},
    'U': {'table_name': 'BBC.Unemployment_View', 'column_name': 'BBC.Unemployment_View.Unemployment_Rate'}
}

# Goal is to return JSON after using the methods in datascience.py
@app.route('/regression')
def regression():
    global table
    independent_vars = request.args['vars'].split(',')
    query = 'select Mortgage_Rates_View.Date, Mortgage_Rates_View.Mortgage_Rate'
    for var in independent_vars:
        query += ', %s' % table[var]['column_name']
    query += ' from BBC.Mortgage_Rates_View'
    for var in independent_vars:
        query += ' inner join %s on Mortgage_Rates_View.Date = %s.Date' % (table[var]['table_name'], table[var]['table_name']) 
    print(query + ';')
    results = linear_regression(query + ';')
    return jsonify(results)

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
