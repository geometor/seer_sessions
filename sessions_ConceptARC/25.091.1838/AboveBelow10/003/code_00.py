"""
Transforms an input grid based on a diagonal line of a single non-white color.
1. Identifies the non-white color (fill_color) and the coordinates of the pixels forming a diagonal line.
2. Determines if the line is a 'main' diagonal (top-left to bottom-right) or an 'anti' diagonal (top-right to bottom-left).
3. Creates an output grid filled with white (0).
4. Fills pixels (r_out, c_out) in the output grid with fill_color based on the diagonal type:
    - If 'main' diagonal: Fill if there exists an input pixel (r_in, c_in) such that r_out >= r_in AND c_out <= c_in.
    - If 'anti' diagonal: Fill if there exists an input pixel (r_in, c_in) such that r_out >= r_in AND c_out >= c_in.
"""

import numpy as np

def find_color_and_coords(grid_np):
    """
    Finds the single non-white color and its coordinates in the grid.
    Assumes there is exactly one non-white color forming a line.
    """
    # Find unique non-zero colors
    non_white_colors = np.unique(grid_np[grid_np != 0])

    if len(non_white_colors) == 0:
        # No non-white color found
        return 0, []
    elif len(non_white_colors) > 1:
        # Warning if multiple colors found, proceed with the lowest value > 0
        # print(f"Warning: Multiple non-white colors found: {non_white_colors}. Using {non_white_colors[0]}.")
        fill_color = non_white_colors[0]
    else:
        # Exactly one non-white color found
        fill_color = non_white_colors[0]

    # Find coordinates of the fill color
    coords = list(zip(*np.where(grid_np == fill_color))) # Returns list of (row, col) tuples
    
    # Ensure coords are sorted primarily by row, then by column for consistent diagonal detection
    coords.sort()
    
    return int(fill_color), coords

def determine_diagonal_type(coords):
    """
    Determines the type of diagonal based on the coordinates.
    Assumes coords are sorted by row, then column.
    """
    if len(coords) <= 1:
        # Cannot determine diagonal type from a single point or no points
        # Defaulting to 'main' might work for single points if the rule applies,
        # but 'unknown' is safer. Based on examples, we expect lines.
        return "unknown" 

    first_pixel = coords[0]
    last_pixel = coords[-1]

    delta_r = last_pixel[0] - first_pixel[0]
    delta_c = last_pixel[1] - first_pixel[1]

    if delta_r > 0 and delta_c > 0:
        return "main"  # Row increases, Col increases
    elif delta_r > 0 and delta_c < 0:
        return "anti"  # Row increases, Col decreases
    elif delta_r == 0 and delta_c != 0 :
        return "horizontal" # Not expected based on examples
    elif delta_r !=0 and delta_c == 0:
        return "vertical" # Not expected based on examples
    else: # delta_r == 0 and delta_c == 0 (should only happen if len(coords)==1)
         return "unknown"


def transform(input_grid):
    """
    Applies the fill transformation based on the identified diagonal line.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Identify the fill color and the coordinates of the input line pixels
    fill_color, input_coords = find_color_and_coords(input_np)

    # Handle edge case: no fill color found or no coordinates
    if fill_color == 0 or not input_coords:
        return np.zeros_like(input_np).tolist() # Return all white grid

    # 2. Determine the type of diagonal
    diagonal_type = determine_diagonal_type(input_coords)

    # If diagonal type is unknown (e.g., single point, horizontal, vertical),
    # the behavior is undefined by the examples. Returning the original grid
    # or a white grid might be options. Let's return a white grid for now.
    if diagonal_type not in ["main", "anti"]:
         # Maybe handle single point as a special case if needed later
         # For now, assume valid diagonals based on training data.
         # print(f"Warning: Unknown or non-diagonal line type '{diagonal_type}'. Returning white grid.")
         return np.zeros_like(input_np).tolist()


    # 3. Initialize output grid with white (0)
    output_grid = np.zeros_like(input_np, dtype=int)

    # 4. Iterate through each pixel position in the potential output grid
    for r_out in range(height):
        for c_out in range(width):
            # 5. Check the condition based on diagonal type against all input coordinates
            fill_pixel = False
            for r_in, c_in in input_coords:
                if diagonal_type == "main":
                    if r_out >= r_in and c_out <= c_in:
                        fill_pixel = True
                        break # Found a condition match for this output pixel
                elif diagonal_type == "anti":
                     if r_out >= r_in and c_out >= c_in:
                        fill_pixel = True
                        break # Found a condition match for this output pixel
            
            # 6. If the condition was met, fill the output pixel
            if fill_pixel:
                output_grid[r_out, c_out] = fill_color
            # Otherwise, it remains white (0) as initialized

    # Convert back to list of lists for the required output format
    return output_grid.tolist()