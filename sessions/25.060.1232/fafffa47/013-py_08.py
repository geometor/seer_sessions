import numpy as np

def compare_grids(grid1, grid2):
    """
    Compares two grids and returns a dictionary containing:
    - are_equal: True if the grids are identical, False otherwise.
    - differences: A list of (row, col, val1, val2) tuples for each differing cell.
    """
    if not grid1 or not grid2:
      if not grid1 and not grid2:
        return {'are_equal':True, 'differences':[]}
      else:
        return {'are_equal':False, 'differences':[]}
    
    grid1 = np.array(grid1)
    grid2 = np.array(grid2)

    if grid1.shape != grid2.shape:
        return {'are_equal': False, 'differences': f"Shapes differ: {grid1.shape} vs {grid2.shape}"}

    differences = []
    for i in range(grid1.shape[0]):
        for j in range(grid1.shape[1]):
            if grid1[i, j] != grid2[i, j]:
                differences.append((i, j, grid1[i, j], grid2[i, j]))

    return {'are_equal': len(differences) == 0, 'differences': differences}

# Example Usage (replace with actual grids)
task = "868de0fa"
train_examples = [
    {
        "input": [
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        ],
        "output": [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        ],
    },
    {
        "input": [
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        ],
        "output": [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        ],
    },
    {
        "input": [
            [9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9],
        ],
        "output": [
            [2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2],
        ],
    },
    {
        "input": [[9, 9, 9, 9, 9], [9, 9, 9, 9, 9]],
        "output": [[2, 2, 2, 2, 2], [2, 2, 2, 2, 2]],
    },
    {
        "input": [[9, 9, 9, 9], [9, 9, 9, 9], [9, 9, 9, 9], [9, 9, 9, 9], [9, 9, 9, 9]],
        "output": [[2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2]],
    },
]

for i, example in enumerate(train_examples):
    input_grid = example['input']
    expected_output = example['output']
    actual_output = transform(input_grid)
    comparison_result = compare_grids(expected_output, actual_output)
    print (f"Example {i}:")
    print (f"comparison_result: {comparison_result}")