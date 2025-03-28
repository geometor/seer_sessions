```python
"""
1. Identify the unique non-white color present in the input grid; let this be `input_color`.
2. Determine the corresponding `output_color` based on the following mapping: 
   - if `input_color` is 8 (azure), `output_color` is 2 (red).
   - if `input_color` is 3 (green), `output_color` is 1 (blue).
   - if `input_color` is 5 (gray), `output_color` is 4 (yellow).
3. Create a new output grid with the same dimensions as the input grid.
4. Iterate through each cell (row `r`, column `c`) of the input grid.
5. If the color of the input cell at (`r`, `c`) is white (0), set the color of the output grid cell at (`r`, `c`) to `output_color`.
6. If the color of the input cell at (`r`, `c`) is `input_color`, set the color of the output grid cell at (`r`, `c`) to white (0).
7. Return the completed output grid.
"""

import numpy as np

def find_unique_non_white_color(grid):
    """Finds the single non-white (non-zero) color in the grid."""
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return color
    # Should not happen based on task description, but return a default if only white exists
    return 0 

def get_output_color(input_color):
    """Maps the input color to the corresponding output color."""
    if input_color == 8:
        return 2
    elif input_color == 3:
        return 1
    elif input_color == 5:
        return 4
    else:
        # Handle unexpected input colors if necessary, though task implies fixed mapping
        return 0 # Default to white if mapping not found

def transform(input_grid):
    """
    Transforms the input grid by inverting the pattern of the unique non-white color
    and mapping the color according to specific rules (8->2, 3->1, 5->4).
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    
    # 1. Identify the unique non-white input color
    input_color = find_unique_non_white_color(input_grid_np)
    
    # 2. Determine the corresponding output color
    output_color = get_output_color(input_color)
    
    # 3. Create the output grid, initialized as a copy (or with zeros)
    output_grid_np = np.zeros_like(input_grid_np)
    rows, cols = input_grid_np.shape
    
    # 4. Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # 5. If the input cell is white (0), set output to output_color
            if input_grid_np[r, c] == 0:
                output_grid_np[r, c] = output_color
            # 6. If the input cell is the input_color, set output to white (0)
            elif input_grid_np[r, c] == input_color:
                output_grid_np[r, c] = 0
            # Optional: Handle unexpected colors in input if needed
            # else:
            #     output_grid_np[r, c] = input_grid_np[r, c] # or some other default behavior

    # 7. Return the completed output grid (converted back to list of lists if required by framework)
    return output_grid_np.tolist()

```