```python
import numpy as np

def reverse_row(row):
  """Reverses the order of elements in a list."""
  return row[::-1]

def transform(input_grid):
  """
  Transforms the input grid by reversing the order of pixels in each row independently.
  This corresponds to a horizontal reflection of the grid.
  """
  # Convert input grid to a NumPy array for easier slicing, if needed, 
  # but standard lists work fine for row reversal.
  # Using list comprehension for conciseness.
  
  # Initialize the output grid as an empty list
  output_grid = []
  
  # Iterate through each row in the input grid
  for row in input_grid:
      # Reverse the current row
      reversed_row = reverse_row(row)
      # Append the reversed row to the output grid
      output_grid.append(reversed_row)
      
  # Return the completed output grid
  return output_grid

```