"""
Generates an output grid by projecting lines from the locations of specific colored pixels (azure and orange) in the input grid and marking their intersections.

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with white pixels (0).
2.  Scan the input grid to find the coordinates (row R_az, column C_az) of the single azure pixel (8).
3.  Scan the input grid to find the coordinates (row R_or, column C_or) of the single orange pixel (7).
4.  Fill the entire column C_az of the output grid with azure pixels (8).
5.  Fill the entire row R_az of the output grid with azure pixels (8).
6.  Fill the entire column C_or of the output grid with orange pixels (7).
7.  Fill the entire row R_or of the output grid with orange pixels (7).
8.  Set the pixel at the intersection coordinates (R_or, C_az) in the output grid to red (2). (This overwrites any previous color at this location).
9.  Set the pixel at the intersection coordinates (R_az, C_or) in the output grid to red (2). (This overwrites any previous color at this location).
10. The resulting grid is the final output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the positions of azure (8) and orange (7) pixels,
    drawing corresponding rows/columns and marking specific intersections red.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Define colors
    WHITE = 0
    AZURE = 8
    ORANGE = 7
    RED = 2

    # 1. Initialize an output grid with the same dimensions as the input grid, filled entirely with white pixels (0).
    output_grid = np.full((rows, cols), WHITE, dtype=int)

    # 2. Scan the input grid to find the coordinates (row R_az, column C_az) of the single azure pixel (8).
    azure_coords = np.where(input_np == AZURE)
    if len(azure_coords[0]) == 0:
        # Handle case where azure pixel is not found (should not happen based on task description)
        return output_grid.tolist() 
    r_az = azure_coords[0][0]
    c_az = azure_coords[1][0]


    # 3. Scan the input grid to find the coordinates (row R_or, column C_or) of the single orange pixel (7).
    orange_coords = np.where(input_np == ORANGE)
    if len(orange_coords[0]) == 0:
        # Handle case where orange pixel is not found (should not happen based on task description)
        return output_grid.tolist()
    r_or = orange_coords[0][0]
    c_or = orange_coords[1][0]

    # Apply the drawing rules. Order matters for implicit overwriting at intersections like (r_az, c_az) and (r_or, c_or).
    # Alternatively, one could draw all lines and then explicitly set all four key intersection points.
    # We follow the natural language program order.

    # 4. Fill the entire column C_az of the output grid with azure pixels (8).
    output_grid[:, c_az] = AZURE

    # 5. Fill the entire row R_az of the output grid with azure pixels (8).
    # This ensures output_grid[r_az, c_az] becomes AZURE, overwriting white or previous azure.
    output_grid[r_az, :] = AZURE

    # 6. Fill the entire column C_or of the output grid with orange pixels (7).
    # This might overwrite azure pixels placed in steps 4 or 5.
    output_grid[:, c_or] = ORANGE

    # 7. Fill the entire row R_or of the output grid with orange pixels (7).
    # This ensures output_grid[r_or, c_or] becomes ORANGE, overwriting white or previous orange.
    # It also potentially overwrites azure pixels at (r_or, c_az).
    output_grid[r_or, :] = ORANGE

    # 8. Set the pixel at the intersection coordinates (R_or, C_az) in the output grid to red (2).
    # This specifically overwrites the color at this intersection (potentially orange from step 7 or azure from step 4).
    output_grid[r_or, c_az] = RED

    # 9. Set the pixel at the intersection coordinates (R_az, C_or) in the output grid to red (2).
    # This specifically overwrites the color at this intersection (potentially orange from step 6 or azure from step 5).
    output_grid[r_az, c_or] = RED

    # 10. The resulting grid is the final output.
    # Convert back to list of lists as required by the environment
    return output_grid.tolist()