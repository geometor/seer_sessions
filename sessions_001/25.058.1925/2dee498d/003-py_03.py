import numpy as np

# Provided input and output grids for Example 3
input_grid3 = np.array([
    [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
    [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
    [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
    [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
    [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
    [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
])

output_grid3 = np.array([
    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [1, 2, 3, 4]
])

#Function generated for example 1
def transform(input_grid):
    # Initialize output grid dimensions.
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_width = input_width // 3
    output_height = input_height
    output_grid = []

    # Iterate through rows to maintain height
    for row_index in range(output_height):
      new_row = []
      #take every third column starting at 0
      for col_index in range(0,input_width,3):
        new_row.append(input_grid[row_index][col_index])
      output_grid.append(new_row)


    return output_grid
predicted_output = transform(input_grid3)
match = np.array_equal(predicted_output, output_grid3)
print(f"match: {match}")
if not match:
    print(f"Predicted output:\n{np.array(predicted_output)}")
    print(f"Expected output:\n{output_grid3}")
