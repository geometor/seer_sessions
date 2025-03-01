import numpy as np

def get_columns_with_color(grid, color):
    """
    Finds the indices of columns containing at least one pixel of the specified color.
    """
    cols = []
    for col in range(grid.shape[1]):
        if np.any(grid[:, col] == color):
            cols.append(col)
    return cols

def find_lowest_pixel_of_color(grid, col, color):
    """
    Finds the row index of the lowest pixel of a specified color in a given column.
    Returns -1 if the color is not found in the column.
    """
    row_indices = np.where(grid[:, col] == color)[0]
    if row_indices.size > 0:
        return row_indices[-1]
    else:
        return -1
    

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule:
    - Identifies columns with magenta pixels.
    - Finds the lowest magenta pixel in each of those columns.
    - Changes that lowest magenta pixel to yellow.
    - Keeps all other pixels the same.
    """
    output_grid = np.copy(input_grid)
    magenta_cols = get_columns_with_color(input_grid, 6)

    # Iterate through the identified columns
    for col in magenta_cols:
        # Find the lowest magenta pixel's row index in the current column
        lowest_magenta_row = find_lowest_pixel_of_color(output_grid, col, 6)

        # If a magenta pixel was found in the column, change it to yellow
        if lowest_magenta_row != -1:
          output_grid[lowest_magenta_row, col] = 4

    return output_grid

# Define the training examples (replace with actual data)
train_examples = [
    (np.array([[5, 0, 6, 5, 0, 6, 5, 0, 6],
              [0, 5, 0, 0, 5, 0, 0, 5, 0],
              [6, 0, 5, 6, 0, 5, 6, 0, 5],
              [0, 5, 0, 0, 5, 0, 0, 5, 0],
              [6, 0, 5, 6, 0, 5, 6, 0, 5]]),
     np.array([[5, 0, 4, 5, 0, 4, 5, 0, 4],
              [0, 5, 0, 0, 5, 0, 0, 5, 0],
              [4, 0, 5, 4, 0, 5, 4, 0, 5],
              [0, 5, 0, 0, 5, 0, 0, 5, 0],
              [4, 0, 5, 4, 0, 5, 4, 0, 5]])),
    
    (np.array([[6, 5, 0, 6, 0, 0, 6, 0, 5, 6, 0],
               [0, 0, 5, 5, 0, 0, 5, 6, 0, 0, 0],
               [6, 5, 0, 6, 0, 6, 6, 5, 0, 6, 0],
               [0, 0, 6, 6, 5, 5, 6, 6, 0, 5, 0],
               [0, 6, 5, 0, 0, 6, 5, 0, 6, 6, 0]]),
      np.array([[4, 5, 0, 4, 0, 0, 4, 0, 5, 4, 0],
               [0, 0, 5, 5, 0, 0, 5, 4, 0, 0, 0],
               [4, 5, 0, 4, 0, 4, 4, 5, 0, 4, 0],
               [0, 0, 4, 4, 5, 5, 4, 4, 0, 5, 0],
               [0, 4, 5, 0, 0, 4, 5, 0, 4, 4, 0]])),
    
    (np.array([[6, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 6, 5, 6, 0, 0, 6, 6],
               [0, 5, 0, 0, 0, 0, 5, 0, 6, 0, 0],
               [6, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0],
               [0, 0, 6, 0, 0, 5, 0, 0, 0, 6, 0],
               [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 6, 0, 0, 5, 0, 5, 0, 0, 0, 0]]),
      np.array([[4, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 4, 5, 4, 0, 0, 4, 4],
               [0, 5, 0, 0, 0, 0, 5, 0, 4, 0, 0],
               [4, 0, 5, 0, 0, 4, 0, 0, 0, 0, 0],
               [0, 0, 4, 0, 0, 5, 0, 0, 0, 4, 0],
               [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 4, 0, 0, 5, 0, 5, 0, 0, 0, 0]]))
]

for i, (input_grid, expected_output) in enumerate(train_examples):
    predicted_output = transform(input_grid)
    comparison = predicted_output == expected_output
    print(f"Example {i+1} Comparison (True if match, False if mismatch):")
    print(comparison)
    print(f"Number of mismatches: {np.sum(~comparison)}")
    mismatched_indices = np.where(~comparison)
    for row, col in zip(mismatched_indices[0], mismatched_indices[1]):
        print(f"Mismatch at: ({row}, {col}), Expected: {expected_output[row, col]}, Predicted: {predicted_output[row, col]}")
    print("-" * 20)