import numpy as np

def find_3x3_subgrid(input_grid):
    """Helper function to locate the 3x3 subgrid within the input grid."""
    rows, cols = input_grid.shape
    for r in range(rows - 2):
        for c in range(cols - 2):
            subgrid = input_grid[r:r+3, c:c+3]
            return subgrid, r, c  # Return the subgrid and its top-left corner coordinates
    return None, -1, -1 # Indicate failure if no 3x3 region can be extracted

def transform(input_grid):
    # Locate the 3x3 subgrid.
    subgrid, r_start, c_start = find_3x3_subgrid(input_grid)

    # Check if a 3x3 subgrid was found
    if subgrid is not None:
      output_grid = subgrid
    else:
      output_grid = np.zeros((3, 3), dtype=int) # a default grid

    return output_grid

def analyze_results(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        predicted_output = transform(input_grid)
        is_correct = np.array_equal(predicted_output, expected_output)
        results.append({
            'input_shape': input_grid.shape,
            'output_shape': expected_output.shape,
            'predicted_shape': predicted_output.shape,
            'is_correct': is_correct
        })
    return results
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 7, 7, 7, 0, 0], [0, 7, 7, 7, 0, 0], [0, 7, 7, 7, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[7, 7, 7], [7, 7, 7], [7, 7, 7]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 5, 5, 0], [0, 5, 5, 5, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5]]
        },
		{
            "input": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 8, 8, 0], [0, 8, 8, 8, 8, 8, 0], [0, 8, 8, 8, 8, 8, 0], [0, 0, 0, 0, 0, 0, 0]],
            "output": [[8, 8, 8, 8, 8], [8, 8, 8, 8, 8], [8, 8, 8, 8, 8]]
        },
		{
            "input": [[1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 4, 4, 4, 4, 0, 0], [0, 0, 4, 4, 4, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[4, 4, 4, 4], [4, 4, 4, 4]]
        },
    ]
}
analysis = analyze_results(task)
print(analysis)
