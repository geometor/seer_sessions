import numpy as np
import copy

"""
Find the two cells with value 6 in the input grid. Calculate the shortest 
Manhattan distance between these two cells. Determine the minimal bounding box 
enclosing these two cells. Iterate through all cells in the grid. If a cell 
contains 0, check if it lies on a shortest Manhattan path between the two 
markers AND if it lies on the boundary (edge rows or columns) of the bounding 
box. If both conditions are true, change the cell's value to 5 in the output 
grid. Otherwise, keep the original value.
"""

def manhattan_distance(p1, p2):
  """Calculates the Manhattan distance between two points."""
  return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_markers(grid, marker_value=6):
  """Finds the coordinates of all cells with the specified marker value."""
  coords = []
  rows, cols = grid.shape
  for r in range(rows):
    for c in range(cols):
      if grid[r, c] == marker_value:
        coords.append((r, c))
  # Expect exactly two markers based on the problem description
  if len(coords) == 2:
      return coords[0], coords[1]
  else:
      # Handle error or unexpected input case if necessary
      return None, None 

def transform(input_grid):
    """
    Transforms the input grid by filling cells with 5 based on shortest paths 
    between two markers (6) constrained to their bounding box boundary.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape

    # Find the coordinates of the two markers (value 6)
    p1, p2 = find_markers(input_np, 6)

    if p1 is None or p2 is None:
        # Handle the case where markers are not found as expected
        # For now, just return the original grid if markers aren't exactly two
        return input_grid 

    # Calculate the shortest Manhattan distance between the markers
    total_distance = manhattan_distance(p1, p2)

    # Determine the bounding box
    min_row = min(p1[0], p2[0])
    max_row = max(p1[0], p2[0])
    min_col = min(p1[1], p2[1])
    max_col = max(p1[1], p2[1])

    # Iterate through each cell in the grid
    for r in range(rows):
      for c in range(cols):
        # Check only cells that are currently 0 in the original input
        if input_np[r, c] == 0:
          current_pos = (r, c)
          
          # 1. Shortest Path Check: Is the cell on *a* shortest Manhattan path?
          dist_p1_to_current = manhattan_distance(p1, current_pos)
          dist_current_to_p2 = manhattan_distance(current_pos, p2)
          is_on_shortest_path = (dist_p1_to_current + dist_current_to_p2 == total_distance)

          # 2. Bounding Box Boundary Check: Is the cell on the boundary?
          is_on_boundary = (r == min_row or r == max_row or c == min_col or c == max_col)

          # If both conditions are true, change the cell to 5 in the output grid
          if is_on_shortest_path and is_on_boundary:
            output_grid[r, c] = 5

    # Convert numpy array back to list of lists for the expected output format
    return output_grid.tolist()
