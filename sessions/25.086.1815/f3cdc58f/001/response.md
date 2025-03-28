```python
"""
Initialize an output grid with the same dimensions as the input grid, filled with white (0).
Count the occurrences of blue (1), red (2), green (3), and yellow (4) pixels in the input grid.
For each color (1, 2, 3, 4), draw a bottom-aligned vertical bar in the corresponding column (0, 1, 2, 3) of the output grid.
The height of each bar equals the count of its corresponding color.
Column 0: blue (1)
Column 1: red (2)
Column 2: green (3)
Column 3: yellow (4)
Leave all other cells in the output grid white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by counting specific colors and drawing 
    corresponding vertical bars in the output grid.
    """
    
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output_grid with the same dimensions as input, filled with white (0)
    output_grid = np.zeros((height, width), dtype=int)
    
    # Define the colors to count and their corresponding output columns
    color_column_map = {
        1: 0, # blue -> column 0
        2: 1, # red -> column 1
        3: 2, # green -> column 2
        4: 3, # yellow -> column 3
    }
    
    # Iterate through the colors and their target columns
    for color, col_index in color_column_map.items():
        # Count the occurrences of the current color in the input grid
        count = np.count_nonzero(input_array == color)
        
        # Draw the vertical bar in the output grid if the count is greater than 0
        # and the target column index is within the grid bounds
        if count > 0 and col_index < width:
            # Calculate the start row for the bottom-aligned bar
            start_row = height - count
            # Ensure start_row is not negative (if count exceeds height, clamp to 0)
            start_row = max(0, start_row) 
            
            # Fill the corresponding column segment with the color
            output_grid[start_row:height, col_index] = color
            
    # Return the resulting grid
    return output_grid.tolist() # Convert back to list of lists if required by the environment
```