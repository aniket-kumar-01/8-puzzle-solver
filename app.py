#app.py

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash


import cProfile

from aStar import *

# Create a Flask app instance
app = Flask(__name__)


@app.route('/')
def home():

    return render_template('home.html')


@app.route('/get_json_data', methods=['GET'])
def get_json_data():
    # Get the initial and final matrices from the GET request parameters
    initial_matrix_str = request.args.get('initialMatrix')
    final_matrix_str = request.args.get('finalMatrix')

    # Convert the matrix strings to lists of integers
    initial_matrix = [[int(digit) for digit in initial_matrix_str[i:i+3]] for i in range(0, len(initial_matrix_str), 3)]
    final_matrix = [[int(digit) for digit in final_matrix_str[i:i+3]] for i in range(0, len(final_matrix_str), 3)]

    # Perform the solving process with the provided matrices
    result = solve(initial_matrix, final_matrix)
    solution_node = result["solution_node"]
    all_nodes = result["all_nodes"]
    all_edges = edge_gen_fx(all_nodes)

    # Generate nodes dictionary list
    all_nodes = nodes_dict_list_generator(all_nodes)

    # Generate solution nodes
    sol_nodes = sol_node_gen_fx(solution_node)

    # Add colors to nodes based on the solution
    colored_nodes = color_adder(all_nodes, sol_nodes)

    data = {"nodes": colored_nodes, "edges": all_edges, "sol": sol_nodes}
    return jsonify(data)

def main():
    # Your code inside the if __name__ == "__main__": block
    app.run(debug=True)

if __name__ == '__main__':
    # cProfile.run("main()", sort="cumulative")
    app.run(debug=True)
