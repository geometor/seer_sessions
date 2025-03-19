import numpy as np

def find_seed_pixel(grid):
    # Find the coordinates of the azure (8) pixel.
    rows, cols = np.where(grid == 8)
    if len(rows) > 0:
        return rows[0], cols[0]
    return None

def array_to_string(arr):
     return '\n'.join([' '.join(map(str, row)) for row in arr])


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.zeros_like(input_grid)
    
    # output_grid[:] = input_grid[:] # start with a zero grid rather than copying input

    # Find the seed pixel.
    seed_coords = find_seed_pixel(input_grid)
    if seed_coords is None:
        return output_grid # return if no seed pixel

    seed_row, seed_col = seed_coords

    # set seed pixel
    output_grid[seed_row, seed_col] = 8

    # Get grid dimensions.
    height, width = input_grid.shape

    # Expand diagonally.
    for i in range(1, max(height, width)):
        # Up-left
        if seed_row - i >= 0 and seed_col - i >= 0:
            output_grid[seed_row - i, seed_col - i] = 8
        # Up-right
        if seed_row - i >= 0 and seed_col + i < width:
            output_grid[seed_row - i, seed_col + i] = 8
        # Down-left
        if seed_row + i < height and seed_col - i >= 0:
            output_grid[seed_row + i, seed_col - i] = 8
        # Down-right
        if seed_row + i < height and seed_col + i < width:
            output_grid[seed_row + i, seed_col + i] = 8

    return output_grid


task = {
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[8, 0, 0, 0, 0, 0, 0, 0, 8], [0, 8, 0, 0, 0, 0, 0, 8, 0], [0, 0, 8, 0, 8, 0, 8, 0, 0], [0, 0, 0, 8, 0, 8, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0]]},
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0], [8, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0]]},
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 8, 0, 8, 0, 0, 0, 0], [0, 0, 8, 0, 0, 0, 8, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 8, 0, 0], [8, 0, 0, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0, 0, 0, 0], [0, 0, 8, 0, 0, 0, 0, 0, 0, 0]]}
    ],
    'test': [
        {'input': [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], 'output': []}
    ]
}

for i, example in enumerate(task['train']):
  input_grid = np.array(example['input'])
  expected_output = np.array(example['output'])
  actual_output = transform(input_grid)
  
  print(f"Example {i+1}:")
  print("Input:")
  print(array_to_string(input_grid))
  print("Expected Output:")
  print(array_to_string(expected_output))
  print("Actual Output:")
  print(array_to_string(actual_output))
  print("Correct:", np.array_equal(actual_output, expected_output))
  print("-" * 20)