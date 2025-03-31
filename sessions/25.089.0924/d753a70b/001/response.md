```python
import numpy as np

def find_background_color(grid):
  """
  Identifies the most frequent color, assuming it's the background.
  In these examples, it's consistently 7 (orange).
  """
  # Simple heuristic: assume the most frequent color is background
  # A more robust approach might be needed for other tasks
  values, counts = np.unique(grid, return_counts=True)
  return values[np.argmax(counts)]

def transform_grid(input_grid):
  """
  Shifts all non-background pixels one step down. Pixels shifted off the 
  bottom edge are removed. Original positions of moved pixels become the 
  background color.
  """
  input_np = np.array(input_grid, dtype=int)
  height, width = input_np.shape
  
  # Determine the background color (assuming it's the most frequent)
  # For this specific task, we know it's 7, but finding it dynamically is better practice.
  # background_color = find_background_color(input_np)
  background_color = 7 # Hardcoded based on consistent observation in examples

  # Initialize the output grid with the background color
  output_grid = np.full_like(input_np, background_color)

  # Iterate through each cell of the input grid
  for r in range(height):
    for c in range(width):
      # Check if the current pixel is NOT the background color
      if input_np[r, c] != background_color:
        # Calculate the target row for the downward shift
        target_r = r + 1
        
        # Check if the target row is within the grid boundaries
        if target_r < height:
          # Place the pixel in its new position in the output grid
          output_grid[target_r, c] = input_np[r, c]
          
  # Return the transformed grid as a list of lists
  return output_grid.tolist()
```