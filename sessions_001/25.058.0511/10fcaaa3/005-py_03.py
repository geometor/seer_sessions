import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # replicate gray pixels
    for i in range(input_height):
        for j in range(input_width):
            if input_grid[i, j] == 5:
                output_grid[i * 2, j * 2] = 5
                output_grid[i * 2 + 1, j * 2] = 5
                output_grid[i * 2, j * 2 + 1] = 5
                output_grid[i * 2 + 1, j * 2 + 1] = 5

    # place azure pixels
    for i in range(output_height):
        for j in range(output_width):
            if output_grid[i, j] == 5:
                # Check for top-left position relative to each gray pixel
                if i > 0 and j > 0 and output_grid[i - 1, j - 1] != 5:
                    output_grid[i - 1, j - 1] = 8
                # checking above
                elif i > 0 and output_grid[i-1,j] != 5:
                     if (i-1)%2 == 0 and j%2 == 0:
                        output_grid[i - 1, j ] = 8
                # checking left
                elif j > 0 and output_grid[i, j - 1] != 5:
                    if i%2 == 0 and (j - 1)%2 == 0:
                      output_grid[i, j - 1] = 8

    return output_grid

def compare_grids(grid1, grid2):
    if grid1.shape != grid2.shape:
        return False
    return np.array_equal(grid1, grid2)

# Example grids (replace with actual data from the task)
example_inputs = [
    np.array([[5]]),
    np.array([[0, 0, 0, 0, 0],
              [0, 5, 0, 5, 0],
              [0, 0, 0, 0, 0],
              [0, 5, 0, 5, 0],
              [0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 0, 0, 5, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 0, 0, 5, 0],
              [0, 0, 0, 0, 0, 0, 0]])
]
example_outputs = [
    np.array([[5, 5],
              [5, 5]]),
    np.array([[8, 0, 0, 8, 0, 0],
              [0, 5, 0, 0, 5, 0],
              [0, 5, 0, 0, 5, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 5, 0, 0, 5, 0],
              [0, 5, 0, 0, 5, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
              [0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0],
              [0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0],
              [0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
]

for i, (input_grid, expected_output) in enumerate(zip(example_inputs, example_outputs)):
    transformed_grid = transform(input_grid)
    comparison_result = compare_grids(transformed_grid, expected_output)
    print(f"Example {i+1}:")
    print(f"  Comparison Result: {comparison_result}")
    if not comparison_result:
        print(f"Transformed:\n{transformed_grid}\nExpected:\n{expected_output}")
