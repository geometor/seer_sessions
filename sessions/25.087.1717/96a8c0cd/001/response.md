```python
import collections
import copy

def find_start_pixel(grid, target_color):
  """Finds the coordinates of the first pixel with the target color."""
  height = len(grid)
  width = len(grid[0])
  for r in range(height):
    for c in range(width):
      if grid[r][c] == target_color:
        return r, c
  return None # Should not happen based on task description

def transform(input_grid):
  """
  Performs a flood fill operation starting from the single red pixel (2).
  The fill spreads to orthogonally adjacent white pixels (0), changing them to red (2).
  The fill stops at grid boundaries and any non-white pixels (blue=1, original red=2, green=3).
  """
  
  # Make a deep copy to avoid modifying the original input grid
  output_grid = copy.deepcopy(input_grid)
  height = len(output_grid)
  width = len(output_grid[0])
  
  # Define the color to fill with and the color of the source
  fill_color = 2
  source_color = 2
  fillable_color = 0 # White
  
  # Find the starting pixel (the single red pixel)
  start_coord = find_start_pixel(input_grid, source_color)
  if start_coord is None:
      # Handle case where the source pixel isn't found, though based on
      # the examples, it should always be present.
      return output_grid 
      
  start_row, start_col = start_coord
  
  # Initialize a queue for Breadth-First Search (BFS) flood fill
  queue = collections.deque([start_coord])
  
  # Keep track of visited coordinates to avoid cycles and redundant checks
  # We only need to track the pixels we intend to fill (originally white)
  # The start pixel is already red, so we don't add it to visited initially,
  # but the fill logic won't process it anyway because it's not white.
  # However, adding the start pixel to visited prevents reprocessing if the fill
  # somehow loops back to it, which shouldn't happen with orthogonal movement.
  # Let's start visited set empty and add cells as they are filled.
  visited = set()

  # Define orthogonal directions (right, left, down, up)
  directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
  
  # Start the flood fill process
  while queue:
    current_row, current_col = queue.popleft()
    
    # Explore neighbors
    for dr, dc in directions:
      neighbor_row, neighbor_col = current_row + dr, current_col + dc
      neighbor_coord = (neighbor_row, neighbor_col)
      
      # Check if the neighbor is within the grid boundaries
      if 0 <= neighbor_row < height and 0 <= neighbor_col < width:
        # Check if the neighbor pixel in the *original* input grid is white (fillable)
        # and if we haven't already visited/filled this neighbor
        if input_grid[neighbor_row][neighbor_col] == fillable_color and neighbor_coord not in visited:
          # Change the neighbor's color in the output grid to red
          output_grid[neighbor_row][neighbor_col] = fill_color
          # Mark this neighbor as visited
          visited.add(neighbor_coord)
          # Add the neighbor to the queue to explore from it later
          queue.append(neighbor_coord)
          
  return output_grid
```