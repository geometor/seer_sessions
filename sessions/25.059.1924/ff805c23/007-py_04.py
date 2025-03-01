import numpy as np

def get_subgrid(input_grid):
    # Find coordinates of pixels with color 0 or 3
    coords = np.where((input_grid == 0) | (input_grid == 3))
    if len(coords[0]) > 0:
        # Find min and max row/col to define the subgrid
        min_row, min_col = np.min(coords, axis=1)
        max_row, max_col = np.max(coords, axis=1)
        subgrid = input_grid[min_row:max_row + 1, min_col:max_col + 1]
        return subgrid, min_row, min_col
    else:
        return np.array([]), -1, -1  # Return empty array if no 0 or 3 pixels

def transform(input_grid):
    # Get the subgrid containing all 0 and 3 pixels
    subgrid, _, _ = get_subgrid(input_grid)

    # Initialize a 5x5 output grid filled with 0s
    output_grid = np.zeros((5, 5), dtype=int)

    if subgrid.size > 0:  # Check if subgrid is not empty
        # Iterate through the subgrid and copy 0 and 3 pixels to output_grid
        for i in range(min(subgrid.shape[0], 5)):
            for j in range(min(subgrid.shape[1], 5)):
                if subgrid[i, j] == 0 or subgrid[i, j] == 3:
                    output_grid[i, j] = subgrid[i, j]

    return output_grid

# Training examples (replace with actual data from the task)
train_examples = [
    (np.array([[7, 7, 7, 7, 7, 7, 7],
              [7, 7, 7, 7, 7, 7, 7],
              [7, 7, 0, 0, 0, 7, 7],
              [7, 7, 0, 3, 0, 7, 7],
              [7, 7, 0, 0, 0, 7, 7],
              [7, 7, 7, 7, 7, 7, 7],
              [7, 7, 7, 7, 7, 7, 7]]), np.array([[0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0],
                                            [0, 0, 3, 0, 0],
                                            [0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0]])),
    (np.array([[5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 0, 0, 5, 5],
              [5, 5, 5, 5, 0, 3, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5]]), np.array([[0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0],
                                            [0, 0, 0, 3, 0]])),
    (np.array([[5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 0, 0, 5, 5, 5],
              [5, 5, 5, 0, 3, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5]]), np.array([[0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0],
                                            [0, 0, 0, 3, 0],
                                            [0, 0, 0, 0, 0]])),
    (np.array([[0, 3, 0, 0, 0, 5, 5, 5],
              [0, 0, 0, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5]]), np.array([[0, 3, 0, 0, 0],
                                            [0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0]]))
]

for input_grid, expected_output in train_examples:
    actual_output = transform(input_grid)
    print(f"Input:\n{input_grid}\nExpected Output:\n{expected_output}\nActual Output:\n{actual_output}\nMatches: {np.array_equal(actual_output, expected_output)}\n---")