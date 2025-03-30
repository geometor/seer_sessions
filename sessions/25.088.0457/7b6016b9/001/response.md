```python
import numpy as np
from collections import deque

# Define color constants for clarity (optional but good practice)
WHITE = 0
RED = 2
GREEN = 3

def _is_valid(r, c, height, width):
  """
  Helper function to check if coordinates (r, c) are within the grid bounds.
  
  Args:
    r: Row index.
    c: Column index.
    height: Grid height.
    width: Grid width.
    
  Returns:
    True if the coordinates are valid, False otherwise.
  """
  return 0 <= r < height and 0 <= c < width

def transform(input_grid):
  """
  Transforms the input grid by filling enclosed areas defined by non-white pixels.
  
  1. Identifies all white pixels (0) connected to the grid's border using flood fill (BFS).
  2. Colors these "outside" white pixels green (3).
  3. Colors any remaining white pixels (which must be enclosed) red (2).
  4. Leaves all non-white pixels from the input grid unchanged.
  
  Args:
    input_grid: A list of lists representing the input grid.
    
  Returns:
    A list of lists representing the transformed output grid.
  """
  # Convert input list of lists to a numpy array for efficient operations
  input_np = np.array(input_grid, dtype=int)
  output_grid = input_np.copy() # Initialize output grid as a copy of the input
  height, width = output_grid.shape

  # Use a deque for Breadth-First Search (BFS) - efficient for flood fill
  q = deque()
  
  # Step 1: Find all white pixels on the border and initialize the queue
  for r in range(height):
    for c in range(width):
      # Check if it's a border pixel
      is_border = (r == 0 or r == height - 1 or c == 0 or c == width - 1)
      # If it's a white pixel on the border, mark it as green (outside) 
      # and add it to the queue to start the flood fill.
      if is_border and output_grid[r, c] == WHITE:
        output_grid[r, c] = GREEN 
        q.append((r, c))

  # Step 2: Perform flood fill (BFS) to mark all connected white pixels as green
  while q:
    r, c = q.popleft() # Get the next pixel from the queue

    # Explore the 4 adjacent neighbors (up, down, left, right)
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
      nr, nc = r + dr, c + dc

      # Check if the neighbor is within the grid bounds
      if _is_valid(nr, nc, height, width):
        # If the neighbor is white (meaning it hasn't been visited/colored yet)
        if output_grid[nr, nc] == WHITE:
          output_grid[nr, nc] = GREEN # Mark it as green (outside)
          q.append((nr, nc)) # Add it to the queue to explore its neighbors

  # Step 3: Change any remaining white pixels (must be enclosed) to red
  # Iterate through the entire grid after the flood fill is complete.
  for r in range(height):
    for c in range(width):
      # If a pixel is still white, it wasn't reachable from the border.
      if output_grid[r, c] == WHITE:
        output_grid[r, c] = RED # Mark it as red (inside)

  # Convert the final numpy array back to a list of lists as required
  return output_grid.tolist()
```