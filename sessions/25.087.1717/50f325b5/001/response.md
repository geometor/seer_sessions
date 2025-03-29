```python
import numpy as np

def transform(input_grid):
  """
  Identifies all pixels with the value 3 (green). If any such pixel is adjacent (including diagonally) 
  to a pixel with the value 8 (azure) in the original input grid, its value is changed to 8 in the output grid. 
  All other pixels retain their original values.
  """
  # Convert input_grid list of lists to numpy array for easier manipulation
  input_array = np.array(input_grid, dtype=int)
  # Create a copy of the input array to modify and return as the output
  output_array = np.copy(input_array)
  
  # Get the dimensions of the grid
  height, width = input_array.shape
  
  # Define the offsets for the 8 neighbors (including diagonals)
  neighbors = [
      (-1, -1), (-1, 0), (-1, 1),
      (0, -1),          (0, 1),
      (1, -1), (1, 0), (1, 1)
  ]
  
  # Iterate through each cell in the input grid
  for r in range(height):
      for c in range(width):
          # Check if the current cell's color is 3 (green)
          if input_array[r, c] == 3:
              # Assume no adjacent 8 is found initially for this cell
              found_adjacent_8 = False
              # Check all 8 neighbors
              for dr, dc in neighbors:
                  nr, nc = r + dr, c + dc
                  # Check if the neighbor's coordinates are within the grid boundaries
                  if 0 <= nr < height and 0 <= nc < width:
                      # Check if the neighbor's color in the *original* input grid is 8 (azure)
                      if input_array[nr, nc] == 8:
                          found_adjacent_8 = True
                          # If an adjacent 8 is found, no need to check other neighbors
                          break 
              
              # If an adjacent 8 was found, change the corresponding cell in the output grid to 8
              if found_adjacent_8:
                  output_array[r, c] = 8
                  
  # Convert the output numpy array back to a list of lists
  return output_array.tolist()
```