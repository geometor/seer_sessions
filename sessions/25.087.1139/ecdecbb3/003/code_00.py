import numpy as np
import math

"""
Transformation Rule Natural Language Description:

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all locations `(r, c)` in the input grid containing a red (2) pixel. These are the source points.
3.  Identify all locations in the input grid containing an azure (8) pixel. Store these potential target points for efficient lookup (e.g., in a set).
4.  For *each* red source point `(r, c)`:
    a.  **Independently** search in *each* of the four cardinal directions (right, left, down, up) starting from `(r, c)`.
    b.  For a given direction, find the location `(target_r, target_c)` of the *first* azure (8) pixel encountered along that path.
    c.  If an azure target `(target_r, target_c)` is found for that specific direction:
        i.  Calculate the distance (number of steps) from `(r, c)` to `(target_r, target_c)`.
        ii. Determine the unit direction vector `(dr, dc)` from the source `(r, c)` towards the target `(target_r, target_c)`.
        iii. Draw a line of red (2) pixels in the output grid starting *at* the source point `(r, c)` and moving `distance - 1` steps in the direction `(dr, dc)`. Each pixel on this path (including the start, excluding the target) overwrites the existing pixel with red (2).
        iv. At the target point's location `(target_r, target_c)`, draw a 3x3 square pattern in the output grid:
            1.  The center pixel `(target_r, target_c)` becomes red (2).
            2.  The 8 surrounding pixels (within grid bounds) become azure (8). This pattern overwrites existing pixels in the 3x3 area centered on the target.
    d. Repeat steps 4b and 4c for all four cardinal directions for the current red source point `(r,c)`.
5.  Return the modified output grid.
"""

def find_pixels(grid_np, color):
    """Finds all coordinates (row, col) of pixels with a specific color."""
    coords = np.argwhere(grid_np == color)
    # Convert numpy array rows to tuples for easier handling
    return [tuple(coord) for coord in coords]

def transform(input_grid):
    """
    Applies the transformation rule to the input grid. For each red pixel,
    finds the nearest azure pixel in each cardinal direction, draws a red line
    towards it, and marks the azure pixel with a 3x3 pattern (azure border, red center).
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np) # Initialize output grid
    height, width = input_np.shape

    # Find source (red) and potential target (azure) pixels
    red_pixels = find_pixels(input_np, 2)
    azure_pixels = find_pixels(input_np, 8)
    azure_set = set(azure_pixels) # Use a set for faster lookup

    # Define cardinal directions (dr, dc): right, left, down, up
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Process each red pixel
    for r, c in red_pixels:
        
        # Search independently in each cardinal direction
        for dr, dc in directions:
            
            # Search for the first azure pixel in this direction
            curr_r, curr_c = r, c
            distance = 0
            found_target = None

            while True:
                # Move one step in the current direction
                curr_r += dr
                curr_c += dc
                distance += 1

                # Check if out of bounds
                if not (0 <= curr_r < height and 0 <= curr_c < width):
                    break # Stop searching in this direction if out of bounds

                # Check if the current pixel is an azure target
                if (curr_r, curr_c) in azure_set:
                    found_target = (curr_r, curr_c)
                    break # Found the first target in this direction

            # If a target was found in this direction, perform actions
            if found_target is not None:
                target_r, target_c = found_target

                # Draw the red line from source towards target, stopping before target
                # The line has 'distance' number of segments including the starting point,
                # so we draw 'distance' red pixels starting from (r, c).
                line_r, line_c = r, c
                for _ in range(distance):
                     # Check bounds (should be okay due to search logic, but safe)
                    if 0 <= line_r < height and 0 <= line_c < width:
                       output_np[line_r, line_c] = 2 # Draw red pixel
                    else:
                        # This case should ideally not be reached if search worked correctly
                        break 
                    # Move to the next pixel along the line (towards the target)
                    line_r += dr
                    line_c += dc

                # Draw the 3x3 pattern centered at the target location
                for r_offset in range(-1, 2):
                    for c_offset in range(-1, 2):
                        pr, pc = target_r + r_offset, target_c + c_offset
                        # Check if the pattern pixel is within grid bounds
                        if 0 <= pr < height and 0 <= pc < width:
                            if r_offset == 0 and c_offset == 0:
                                # Center pixel (the original target location) becomes red
                                output_np[pr, pc] = 2
                            else:
                                # Surrounding pixels become azure
                                output_np[pr, pc] = 8

    # Convert the result back to a list of lists
    return output_np.tolist()