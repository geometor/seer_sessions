```python
"""
Identifies pairs of blue pixels (1) aligned horizontally or vertically within the input grid. 
Fills the segment of white pixels (0) strictly between each aligned pair with azure pixels (8) in the output grid. 
Blue pixels (1) remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by connecting aligned blue pixels with azure lines.

    Args:
        input_grid (list of lists or np.ndarray): The input grid containing 0s and 1s.

    Returns:
        np.ndarray: The transformed grid with azure lines (8) connecting blue pixels (1).
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()  # Start with a copy of the input
    
    rows, cols = grid.shape
    
    # --- Horizontal Scan ---
    # Iterate through each row
    for r in range(rows):
        # Find column indices of blue pixels in the current row
        blue_cols = np.where(grid[r, :] == 1)[0]
        
        # Sort the column indices (they should already be sorted from np.where)
        # blue_cols.sort() # np.where returns sorted indices
        
        # If there are 2 or more blue pixels, process pairs
        if len(blue_cols) >= 2:
            # Iterate through adjacent pairs of blue pixels in the row
            for i in range(len(blue_cols) - 1):
                col1 = blue_cols[i]
                col2 = blue_cols[i+1]
                
                # Fill the segment strictly between col1 and col2 with azure (8)
                # Slicing [col1 + 1 : col2] correctly handles adjacent blue pixels (empty slice)
                # This overwrites only the pixels between the blue ones. Since output_grid 
                # started as a copy, only original white pixels (0) will become azure (8).
                output_grid[r, col1 + 1 : col2] = 8
                
    # --- Vertical Scan ---
    # Iterate through each column
    for c in range(cols):
        # Find row indices of blue pixels in the current column
        blue_rows = np.where(grid[:, c] == 1)[0]
        
        # Sort the row indices (they should already be sorted)
        # blue_rows.sort() # np.where returns sorted indices
        
        # If there are 2 or more blue pixels, process pairs
        if len(blue_rows) >= 2:
             # Iterate through adjacent pairs of blue pixels in the column
            for i in range(len(blue_rows) - 1):
                row1 = blue_rows[i]
                row2 = blue_rows[i+1]
                
                # Fill the segment strictly between row1 and row2 with azure (8)
                output_grid[row1 + 1 : row2, c] = 8

    return output_grid.tolist() # Return as list of lists per ARC standard
```