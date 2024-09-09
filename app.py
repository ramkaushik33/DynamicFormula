from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to execute the formula
def execute_formulas(data):
    results = {}
    try:
        for formula in data['formulas']:
            output_var = formula['outputVar']
            expression = formula['expression']
            inputs = formula['inputs']
            
            # Prepare to store results for this formula
            results[output_var] = []

            # Iterate over the data entries
            for entry in data['data']:
                # Create a context for evaluating the expression
                eval_context = {}
                
                # Map input variables from the entry data
                for input_var in inputs:
                    var_name = input_var['varName']
                    eval_context[var_name] = entry[var_name]
                
                # Evaluate the expression
                result = eval(expression, {}, eval_context)
                
                # Store the result
                results[output_var].append(result)
        
        # Returning success response
        return {
            "results": results,
            "status": "success",
            "message": "The formulas were executed successfully."
        }

    except Exception as e:
        # Return error message in case of exception
        return {
            "status": "failure",
            "message": f"An error occurred: {str(e)}"
        }

# API route to execute formula
@app.route('/api/execute-formula', methods=['POST'])
def execute_formula_api():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Check if data is valid
        if 'data' not in data or 'formulas' not in data:
            return jsonify({
                "status": "failure",
                "message": "Invalid input data. Missing 'data' or 'formulas'."
            }), 400
        
        # Execute the formula
        result = execute_formulas(data)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "status": "failure",
            "message": f"An error occurred: {str(e)}"
        }), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)