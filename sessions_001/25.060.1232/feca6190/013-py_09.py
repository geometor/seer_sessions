import numpy as np

def find_nonzero_pixels(grid):
    """Finds all non-zero pixels in a grid."""
    non_zero_indices = np.where(grid != 0)
    rows = non_zero_indices[0]
    cols = non_zero_indices[1]
    values = grid[rows, cols]
    return list(zip(rows, cols, values))

def analyze_example(input_grid, output_grid):
    input_nonzero = find_nonzero_pixels(input_grid)
    output_nonzero = find_nonzero_pixels(output_grid)
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    return {
        'input_shape': input_shape,
        'output_shape': output_shape,
        'input_nonzero': input_nonzero,
        'output_nonzero': output_nonzero,
    }

task_data = {
    'train': [
        {'input': [[0, 0, 0], [0, 3, 0], [0, 0, 0]], 'output': [[3, 0, 0], [0, 3, 0], [0, 0, 3]]},
        {'input': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 9, 0], [0, 0, 0, 0]], 'output': [[9, 0, 0, 0], [0, 9, 0, 0], [0, 0, 9, 0], [0, 0, 0, 9]]},
        {'input': [[7]], 'output': [[7]]},
        {'input': [[0, 0, 0, 0, 5]], 'output': [[5], [0], [0], [0], [0]]},
        {'input': [[0, 6], [0, 0], [0, 0], [0, 0]], 'output': [[0, 0, 0, 6], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]}
    ]
}

results = []
for example in task_data['train']:
  results.append(analyze_example(np.array(example['input']), np.array(example['output'])))

for i, r in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input shape: {r['input_shape']}")
    print(f"  Output shape: {r['output_shape']}")
    print(f"  Input non-zero pixels: {r['input_nonzero']}")
    print(f"  Output non-zero pixels: {r['output_nonzero']}")