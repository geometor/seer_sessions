"""
1.  **Identify the Azure Region:** Locate the contiguous horizontal band of azure (8) pixels within the input grid. This band is horizontally centered and surrounded by grey pixels.
2. **Determine top row of Azure pixels**: find the row index of the top most row that contains any Azure pixels
3.  **Extract a 3x3 Subgrid:** Create a 3x3 grid. Populate the top row of this output grid with the colors of the first three horizontally centered Azure pixels in the Azure Region, starting at `top row of Azure pixels`.
4. fill the remainder of the output with black (0)
"""

import numpy as np

def find_azure_region(grid):
    """Finds the bounding box of the azure (8) region."""
    azure_pixels = np.where(grid == 8)
    if len(azure_pixels[0]) == 0:  # No azure pixels found
        return None
    min_row, max_row = np.min(azure_pixels[0]), np.max(azure_pixels[0])
    min_col, max_col = np.min(azure_pixels[1]), np.max(azure_pixels[1])
    return min_row, max_row, min_col, max_col

def get_top_azure_row(grid):
    """get index of the top most row that contains azure"""
    for r, row in enumerate(grid):
        if 8 in row:
            return r
    return 0

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    
    input_grid = np.array(input_grid)  # Ensure numpy array for easier manipulation
    output_grid = np.zeros((3, 3), dtype=int)  # Initialize 3x3 output grid

    # find top azure row
    top_azure_row_index = get_top_azure_row(input_grid)
    top_azure_row = input_grid[top_azure_row_index]

    # Find the azure region
    azure_region_bbox = find_azure_region(input_grid)
    if azure_region_bbox is None:
      return output_grid
    
    min_row, max_row, min_col, max_col = azure_region_bbox

    # get center of azure region
    azure_cols = np.where(top_azure_row == 8)[0]
    
    if len(azure_cols) > 0 :
      center_col_index = len(azure_cols) // 2

      # Extract up to 3 azure pixels, centered
      start_col = max(0, azure_cols[center_col_index] - 1)  # Ensure within bounds

      # get the azure pixels from input to output
      for output_col in range(3):
            input_col = start_col + output_col
            if input_col in azure_cols:
                output_grid[0, output_col] = 8
            

    return output_grid