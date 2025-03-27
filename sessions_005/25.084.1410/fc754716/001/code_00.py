import numpy as np

"""
Create a border around the grid using the color of the single non-background pixel found in the input.

1.  Determine the height (H) and width (W) of the input grid.
2.  Scan the input grid to find the single pixel that is not white (0). Record the color of this pixel; let this be border_color.
3.  Create a new grid with the same dimensions (H x W) as the input grid, initialized with white (0).
4.  Fill the entire perimeter of the new grid with border_color. This means:
    *   Set all pixels in the first row (row index 0) to border_color.
    *   Set all pixels in the last row (row index H-1) to border_color.
    *   Set all pixels in the first column (column index 0) to border_color.
    *   Set all pixels in the last column (column index W-1) to border_color.
5.  The resulting grid is the output (the interior is already white from initialization).
"""

def find_non_background_color(grid):
  """
  Scans the grid to find the first non-zero pixel color.
  Assumes there is exactly one non-zero pixel.
  """
  for r in range(grid.shape[0]):
    for c in range(grid.shape[1]):
      if grid[r, c] != 0:
        return grid[r, c]
  # Should not happen based on task description, but return 0 as fallback
  return 0 

def transform(input_grid):
    """
    Transforms the input grid by creating a border using the color 
    of the single non-background pixel.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # 1. Determine the height (H) and width (W) of the input grid.
    H, W = input_array.shape
    
    # 2. Scan the input grid to find the border_color.
    border_color = find_non_background_color(input_array)
    
    # 3. Create a new grid with the same dimensions, initialized with white (0).
    output_grid = np.zeros((H, W), dtype=int)
    
    # 4. Fill the entire perimeter of the new grid with border_color.
    # Fill top row
    output_grid[0, :] = border_color
    # Fill bottom row
    output_grid[H-1, :] = border_color
    # Fill first column
    output_grid[:, 0] = border_color
    # Fill last column
    output_grid[:, W-1] = border_color
    
    # 5. The interior is already filled with white (0) from initialization.
    
    # Return the output grid (converting back to list of lists if necessary, 
    # though numpy array is often fine)
    return output_grid.tolist() 