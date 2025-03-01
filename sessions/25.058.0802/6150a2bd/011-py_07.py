import numpy as np

def code_execution(inputs, expected_outputs, transform_function):
    results = []
    for i, (input_grid, expected_output) in enumerate(zip(inputs, expected_outputs)):
        actual_output = transform_function(input_grid)
        
        # Check if all nested elements are comparable
        try:
            comparison = np.array(actual_output) == np.array(expected_output)
            all_match = comparison.all()
        except ValueError: # mismatch shape - which is failure
            all_match = False
        
        results.append({
            "example_index": i,
            "input_shape": np.array(input_grid).shape,
            "output_shape": np.array(expected_output).shape,
            "actual_output_shape": np.array(actual_output).shape,
            "all_match": all_match,
        })
    return results
# test grids and expected outputs will be separate inputs to the dreamer role
inputs = [
    [[1, 3, 6], [1, 3, 6], [1, 3, 6]], 
    [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]], 
    [[4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4]],
    [[4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4]],
]
expected_outputs = [
    [[1, 1, 1], [3, 3, 3], [0, 0, 0]], 
    [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]], 
    [[5,5,5,5],[5,5,5,5],[5,5,5,5],[5,5,5,5]],
    [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]
]

def transform(input_grid):
    # Rotate the grid 90 degrees clockwise.
    input_grid = np.array(input_grid)
    output_grid = np.rot90(input_grid, k=-1)

    # Apply color transformations.
    height, width = output_grid.shape
    for r in range(height):
        for c in range(width):
            if output_grid[r, c] == 3:
                output_grid[r, c] = 2
            elif output_grid[r, c] == 4:
                output_grid[r, c] = 5
            elif output_grid[r, c] == 6:
                output_grid[r, c] = 0

    return output_grid.tolist()

results = code_execution(inputs, expected_outputs, transform)
for result in results:
    print(result)
