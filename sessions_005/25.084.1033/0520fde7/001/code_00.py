"""
Identify a central vertical axis column (color gray, 5). Compare pixels symmetrically across this axis. 
Create an output grid corresponding to the left side of the input grid.
For each pixel on the left side, if it matches its symmetric counterpart on the right side and is not white (0), 
set the corresponding output pixel to red (2). Otherwise, set the output pixel to white (0).
"""

import numpy as np

def find_axis_column(grid):
    """Finds the index of the vertical column acting as the symmetry axis (all gray pixels)."""
    height, width = grid.shape
    for c in range(width):
        if np.all(grid[:, c] == 5): # Check if all pixels in the column are gray (5)
            return c
    return -1 # Should not happen based on task description

def transform(input_grid):
    """
    Transforms the input grid based on symmetric comparison across a gray axis.
    """
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape

    # 1. Identify the Axis
    axis_col = find_axis_column(input_grid_np)
    if axis_col == -1:
        # Handle cases where no axis is found, though unlikely based on examples
        print("Warning: No gray axis column found.")
        # Default behavior might be needed, e.g., return input or empty grid
        # For now, let's assume axis always exists and proceed
        # As a fallback, maybe assume middle column if odd width?
        axis_col = width // 2

    # 2. Determine Output Size
    output_height = height
    output_width = axis_col # Width of the left section

    # 3. Initialize Output
    # Create a new grid filled with the background color (white, 0)
    output_grid = np.full((output_height, output_width), 0, dtype=int)

    # 4. Compare Symmetrically and 6. Set Output Pixel
    for r in range(output_height):
        for c in range(output_width):
            # 5. Check Condition
            # Calculate the symmetric column index on the right side
            sym_c = (axis_col * 2) - c
            
            # Ensure symmetric column index is within bounds (should be if axis is correct)
            if sym_c < width:
                left_pixel = input_grid_np[r, c]
                right_pixel = input_grid_np[r, sym_c]

                # Check if pixels match and are not the background color (white, 0)
                if left_pixel == right_pixel and left_pixel != 0:
                    # Set the corresponding output pixel to the match color (red, 2)
                    output_grid[r, c] = 2
            # else: # Handle edge cases or invalid axis if necessary
                # print(f"Warning: Symmetric column {sym_c} out of bounds for width {width}")
                # If sym_c is out of bounds, the comparison fails, so output remains 0 (white)

    # 7. Return Output
    return output_grid.tolist() # Convert back to list of lists if required by the environment