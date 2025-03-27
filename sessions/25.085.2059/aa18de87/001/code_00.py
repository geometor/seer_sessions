import numpy as np

"""
For each row in the input grid:
1. Identify all unique non-white colors present.
2. For each unique non-white color found:
   a. Find the leftmost (minimum column index) and rightmost (maximum column index) 
      occurrences of this color in the row.
   b. If the color appears at least twice (i.e., min and max indices are different 
      or there are multiple occurrences), fill all white (0) pixels located 
      horizontally strictly between these leftmost and rightmost occurrences 
      with red (2).
3. Leave all other pixels unchanged.
"""

def transform(input_grid):
    """
    Applies a horizontal fill transformation based on color spans within each row.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    num_rows, num_cols = input_grid.shape
    
    # Define the background color and the fill color
    background_color = 0
    fill_color = 2

    # Iterate through each row of the grid
    for r in range(num_rows):
        row_data = input_grid[r, :]
        
        # Find unique non-background colors in the current row
        unique_colors = np.unique(row_data[row_data != background_color])
        
        # Process each unique non-background color found in the row
        for color in unique_colors:
            # Find all column indices where this color appears
            indices = np.where(row_data == color)[0]
            
            # Check if the color appears at least twice in the row
            if len(indices) >= 2:
                # Determine the minimum and maximum column index for this color
                min_col = np.min(indices)
                max_col = np.max(indices)
                
                # Iterate through the columns between the min and max indices (exclusive)
                for c in range(min_col + 1, max_col):
                    # If the pixel in the output grid at this position is the background color,
                    # change it to the fill color.
                    if output_grid[r, c] == background_color:
                        output_grid[r, c] = fill_color
                        
    # Return the modified grid
    return output_grid