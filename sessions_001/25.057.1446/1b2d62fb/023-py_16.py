import numpy as np

def get_shape(grid):
    if grid.ndim == 2:
      return grid.shape
    else:
      return (0,0)

def find_blue_pixels(grid):
    # Find the row indices where blue (1) pixels exist
    rows, cols = grid.shape
    blue_rows = []
    for i in range(rows):
        if 1 in grid[i]:
            blue_rows.append(i)
    return blue_rows

def transform(input_grid):
    # Find rows with blue pixels
    blue_rows = find_blue_pixels(input_grid)

    # Determine output grid height
    if len(blue_rows) > 0:
      output_height = len(blue_rows)
    else:
      return np.zeros((0,3),dtype=int)

    # Initialize output grid
    output_grid = np.zeros((output_height, 3), dtype=int)

    # Place azure pixels in the center column
    for i in range(output_height):
        output_grid[i, 1] = 8

    return output_grid
    

# Example Data (replace with your actual data)

# first example pair
input_grid1 = np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 1, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 1, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])
output_grid1 = np.array([[0, 8, 0],
       [0, 8, 0]])

# second example pair
input_grid2 = np.array([[6, 6, 6, 6, 6, 6, 6, 6, 6],
                       [6, 6, 6, 6, 6, 6, 6, 6, 6],
                       [6, 6, 6, 6, 6, 6, 1, 6, 6],
                       [6, 6, 6, 6, 6, 6, 6, 6, 6]])
output_grid2 = np.array([[0, 8, 0]])

# third example pair
input_grid3 = np.array([[1, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                       [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                       [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                       [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                       [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                       [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                       [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 1]])
output_grid3 = np.array([[0, 8, 0]])

# fourth example pair
input_grid4 = np.array([[9, 9, 9, 9, 9, 9, 9],
                       [9, 9, 1, 9, 9, 9, 9],
                       [9, 9, 9, 9, 9, 9, 9],
                       [9, 9, 9, 9, 9, 1, 9],
                       [9, 9, 9, 9, 9, 9, 9]])
output_grid4 = np.array([[0, 8, 0],
                        [0, 8, 0]])

examples = [
    (input_grid1, output_grid1),
    (input_grid2, output_grid2),
    (input_grid3, output_grid3),
    (input_grid4, output_grid4)
]

for i, (input_grid, expected_output) in enumerate(examples):
    actual_output = transform(input_grid)
    print(f"Example {i+1}:")
    print(f"  Input Shape: {get_shape(input_grid)}")
    print(f"  Expected Output Shape: {get_shape(expected_output)}")
    print(f"  Actual Output Shape: {get_shape(actual_output)}")
    print(f"  Blue row indices: {find_blue_pixels(input_grid)}")
    print("-" * 20)
