# Assuming 'train_pairs' is a list of dictionaries,
# each with 'input' and 'output' keys holding numpy arrays.

import numpy as np

def get_shape(grid):
    return f"{grid.shape[0]}x{grid.shape[1]}"

results = []

for i, pair in enumerate(train_pairs):
    input_grid = np.array(pair['input'])
    expected_output_grid = np.array(pair['output'])
    predicted_output_grid = transform(input_grid)

    match = np.array_equal(predicted_output_grid, expected_output_grid)
    results.append({
        "example": i,
        "input_shape": get_shape(input_grid),
        "output_shape": get_shape(expected_output_grid),
        "predicted_output_shape":get_shape(predicted_output_grid),
        "match": match
     })

for result in results:
    print(result)