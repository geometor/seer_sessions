```python
import numpy as np

def transform(input_grid):
  """
  Iterates through each cell in the input grid, focusing on cells in columns 1, 2, and 3.
  If a cell's left and right neighbors have the same non-zero value, the cell's value is changed to 0 in the output grid.
  Otherwise, the cell's original value is retained. Cells in the first (0) and last columns are never modified.
  """
  # Convert input list of lists to a numpy array for easier indexing
  input_array = np.array(input_grid)
  # Create a copy to store the output, so modifications don't affect subsequent checks
  output_array = np.copy(input_array)
  
  # Get the dimensions of the grid
  rows, cols = input_array.shape
  
  # Iterate through rows (index r)
  for r in range(rows):
    # Iterate through columns (index c) from 1 to cols-2 (inclusive)
    # This focuses on the columns that can potentially be modified (cols 1, 2, 3 for a 5x5 grid)
    for c in range(1, cols - 1):
      # Get the value of the left neighbor
      left_neighbor_value = input_array[r, c - 1]
      # Get the value of the right neighbor
      right_neighbor_value = input_array[r, c + 1]
      
      # Check if the neighbors have the same value and that value is not zero
      if left_neighbor_value == right_neighbor_value and left_neighbor_value != 0:
        # If conditions are met, set the current cell's value in the output grid to 0
        output_array[r, c] = 0
        
  # Convert the numpy array back to a list of lists for the final output format
  output_grid = output_array.tolist()
  
  return output_grid
```