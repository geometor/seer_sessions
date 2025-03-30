```python
import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating horizontal and vertical blue lines.
    For each row containing two or more blue pixels in the input grid, a horizontal 
    blue line is drawn connecting the leftmost to the rightmost blue pixel in that row.
    For each column containing two or more blue pixels in the input grid, a vertical 
    blue line is drawn connecting the topmost to the bottommost blue pixel in that column.
    These lines overwrite any existing pixels (including red) in their path.
    Pixels not part of these generated lines retain their original color from the input grid.
    """

    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_np = np.copy(input_np)
    
    rows, cols = input_np.shape
    blue_color = 1

    # Find coordinates of all blue pixels in the original input grid
    blue_pixels_coords = np.argwhere(input_np == blue_color)

    # --- Process Rows ---
    # Iterate through each row index
    for r in range(rows):
        # Find the column indices of blue pixels in this row from the original input
        row_blue_cols = blue_pixels_coords[blue_pixels_coords[:, 0] == r][:, 1]
        
        # Check if there are two or more blue pixels in this row
        if len(row_blue_cols) >= 2:
            # Determine the minimum and maximum column index for the blue pixels
            c_min = np.min(row_blue_cols)
            c_max = np.max(row_blue_cols)
            
            # Draw the horizontal blue line segment in the output grid
            output_np[r, c_min : c_max + 1] = blue_color

    # --- Process Columns ---
    # Iterate through each column index
    for c in range(cols):
        # Find the row indices of blue pixels in this column from the original input
        col_blue_rows = blue_pixels_coords[blue_pixels_coords[:, 1] == c][:, 0]
        
        # Check if there are two or more blue pixels in this column
        if len(col_blue_rows) >= 2:
            # Determine the minimum and maximum row index for the blue pixels
            r_min = np.min(col_blue_rows)
            r_max = np.max(col_blue_rows)
            
            # Draw the vertical blue line segment in the output grid
            output_np[r_min : r_max + 1, c] = blue_color

    # Convert the final numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```