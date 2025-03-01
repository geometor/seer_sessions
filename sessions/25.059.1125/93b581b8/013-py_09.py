import numpy as np

def analyze_example(input_grid, output_grid):
    """Analyzes an input-output pair and returns a dictionary of observations."""
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    
    results = {}

    # Find largest common contiguous block
    rows, cols = input_grid.shape
    max_block_size = 0
    block_start = None
    block = None
    
    for i in range(rows):
        for j in range(cols):
            for k in range(1, min(rows - i, cols - j) + 1):
                sub_input = input_grid[i:i+k, j:j+k]
                if np.array_equal(sub_input, output_grid[i:i+k, j:j+k]):
                    if k > max_block_size:
                        max_block_size = k
                        block_start = (i, j)
                        block = sub_input

    results['block_size'] = max_block_size
    results['block_start_input'] = block_start
    results['block'] = block.tolist() if block is not None else None
    results['input_shape'] = input_grid.shape
    results['output_shape'] = output_grid.shape
    
    # find differences
    diff = input_grid != output_grid
    results['num_differences'] = np.sum(diff)
    results['diff_coordinates'] = np.argwhere(diff).tolist()
    results['input_diff_values'] = input_grid[diff].tolist()
    results['output_diff_values'] = output_grid[diff].tolist()
    

    return results
# get this from the task json
train_examples = [
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 2, 0, 0, 0], [0, 0, 0, 3, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[2, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 2, 0, 0, 0], [0, 0, 0, 3, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 5, 0, 0, 0], [0, 0, 0, 8, 3, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 0, 0, 7, 7, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[7, 0, 0, 0, 0, 0, 0, 0, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 0, 0, 7, 7, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 1, 0, 0, 0], [0, 0, 0, 0, 0, 5, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[1, 0, 0, 0, 0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 1, 0, 0, 0], [0, 0, 0, 0, 0, 5, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 5, 0, 0, 0], [0, 0, 0, 0, 0, 5, 5, 0, 0, 0]]}
]

results = [analyze_example(ex['input'], ex['output']) for ex in train_examples]

for i, r in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Block Size: {r['block_size']}")
    print(f"  Block Start (Input): {r['block_start_input']}")
    print(f"  Block: {r['block']}")
    print(f"  input shape: {r['input_shape']}")
    print(f"  output shape: {r['output_shape']}")
    print(f"  num_differences: {r['num_differences']}")
    print(f"  diff_coordinates: {r['diff_coordinates']}")    
    print(f"  input_diff_values: {r['input_diff_values']}")
    print(f"  output_diff_values: {r['output_diff_values']}")
    print("-" * 20)