# Example: Let's assume these are the actual inputs and outputs from training example 1:
input_grid_1 = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
output_grid_1 = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])

input_grid_2 = np.array([[0, 0, 0], [0, 2, 0], [0, 0, 0]])
output_grid_2 = np.array([[0, 0, 0], [0, 2, 0], [0, 0, 0]])

input_grid_3 = np.array([[3, 3], [3, 3]])
output_grid_3 = np.array([[3, 3], [3, 3]])

# and assume transform() works as defined in the prompt

def analyze_results(input_grids, expected_outputs, transform_function):
    results = []
    for i, (input_grid, expected_output) in enumerate(zip(input_grids, expected_outputs)):
        predicted_output = transform_function(input_grid)
        comparison = np.array_equal(predicted_output, expected_output)
        results.append({
            "example_number": i + 1,
            "input_shape": input_grid.shape,
            "output_shape": expected_output.shape,
            "predicted_output_shape": predicted_output.shape,
            "match": comparison,
            "differences": [] if comparison else find_differences(predicted_output, expected_output)
        })
    return results

def find_differences(predicted, expected):
     #simplified difference check
     return (predicted != expected).tolist()
    

input_grids = [input_grid_1, input_grid_2, input_grid_3]
expected_outputs = [output_grid_1, output_grid_2, output_grid_3]

results = analyze_results(input_grids, expected_outputs, transform)
print(results)

