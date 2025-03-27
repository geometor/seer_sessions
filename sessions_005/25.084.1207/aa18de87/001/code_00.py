import numpy as np

"""
Iterate through each row of the input grid. For each row, find the column indices of all non-white pixels (markers). If there are two or more markers in the row, sort their column indices. Then, for every pair of adjacent markers in the sorted list (based on their column indices), fill all the white pixels (0) located horizontally between them with the color red (2). The original markers remain unchanged. If a row has fewer than two markers, no changes are made to that row.
"""

def find_marker_columns(row):
  """Finds the column indices of non-zero pixels in a row."""
  return [idx for idx, pixel in enumerate(row) if pixel != 0]

def transform(input_grid):
    """
    Transforms the input grid by filling horizontal gaps between markers on each row with red.
    """
    # Convert input to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = input_array.copy()
    
    # Get the dimensions of the grid
    height, width = output_grid.shape

    # Iterate through each row of the grid
    for r in range(height):
        # Get the current row
        row = output_grid[r, :]
        
        # Find the column indices of all non-white pixels (markers) in the current row
        marker_cols = find_marker_columns(row)
        
        # Check if there are at least two markers in the row
        if len(marker_cols) >= 2:
            # Sort the marker column indices (already sorted by find_marker_columns)
            # Iterate through adjacent pairs of marker columns
            for i in range(len(marker_cols) - 1):
                col1 = marker_cols[i]
                col2 = marker_cols[i+1]
                
                # Iterate through the columns strictly between the two markers
                for c in range(col1 + 1, col2):
                    # Fill the pixel at (r, c) with red (2)
                    # Note: We only need to fill if it was originally white (0),
                    # but the logic implicitly handles this since markers won't be between markers.
                    # However, explicitly checking might be safer if rules change later.
                    # We modify the output_grid directly.
                    output_grid[r, c] = 2
                    
    # Convert back to list of lists if necessary, or return numpy array
    return output_grid.tolist()
