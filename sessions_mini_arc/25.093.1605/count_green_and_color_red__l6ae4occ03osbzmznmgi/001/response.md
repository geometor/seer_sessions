```python
"""
Counts the total number of cells with the value 3 in the input grid.
Creates an output grid of the same dimensions, initially filled with 0s.
Fills the first N cells of the output grid with the value 2, where N is the count of 3s from the input.
The filling order is top-to-bottom, left-to-right (reading order).
"""

import numpy as np

def count_value(grid, value):
  """Counts the occurrences of a specific value in the grid."""
  count = 0
  for row in grid:
    for cell in row:
      if cell == value:
        count += 1
  return count

def fill_grid(rows, cols, count, fill_value=2, default_value=0):
    """Creates and fills a grid based on a count."""
    output_grid = [[default_value for _ in range(cols)] for _ in range(rows)]
    filled_count = 0
    for r in range(rows):
        for c in range(cols):
            if filled_count < count:
                output_grid[r][c] = fill_value
                filled_count += 1
            else:
                # Optimization: can break early once count is reached
                return output_grid
    return output_grid

def transform(input_grid):
    """
    Transforms the input grid by counting the number of 3s and filling
    a new grid with that many 2s in reading order.
    """
    # Convert input to numpy array for easier handling (optional but often convenient)
    input_array = np.array(input_grid)
    rows, cols = input_array.shape

    # Count the number of cells with value 3 in the input grid
    count_of_threes = np.sum(input_array == 3) # Using numpy for efficient counting

    # Initialize the output grid with zeros
    output_array = np.zeros_like(input_array)

    # Fill the output grid with 'count_of_threes' number of 2s in reading order
    # Flatten the array, fill the first 'count_of_threes' elements, then reshape
    output_flat = output_array.flatten()
    output_flat[:count_of_threes] = 2 # Fill the first 'count_of_threes' elements with 2
    output_array = output_flat.reshape(rows, cols) # Reshape back to original dimensions

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid

# Example usage with one of the provided train cases (optional, for testing)
# input_1 = [
#     [0, 0, 3, 0, 0],
#     [0, 0, 3, 0, 0],
#     [3, 3, 3, 3, 3],
#     [0, 0, 3, 0, 0],
#     [0, 0, 3, 0, 0]
# ]
# output_1 = transform(input_1)
# print("Input 1:")
# for row in input_1: print(row)
# print("Output 1:")
# for row in output_1: print(row)

# input_2 = [
#     [3, 0, 0, 0, 0],
#     [0, 3, 0, 0, 0],
#     [0, 0, 3, 0, 0],
#     [0, 3, 0, 0, 0],
#     [3, 0, 0, 0, 0]
# ]
# output_2 = transform(input_2)
# print("\nInput 2:")
# for row in input_2: print(row)
# print("Output 2:")
# for row in output_2: print(row)

# input_3 = [
#     [3, 0, 0, 0, 3],
#     [0, 3, 3, 3, 0],
#     [0, 3, 0, 3, 0],
#     [0, 3, 3, 3, 0],
#     [3, 0, 0, 0, 3]
# ]
# output_3 = transform(input_3)
# print("\nInput 3:")
# for row in input_3: print(row)
# print("Output 3:")
# for row in output_3: print(row)
```