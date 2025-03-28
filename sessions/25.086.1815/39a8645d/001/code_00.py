import numpy as np

"""
Create a 3x3 '+' pattern output grid. The color of the '+' is determined 
by analyzing the non-white colors present in the input grid and identifying 
which of them form 3x3 '+' shapes.

If there are 3 unique non-white colors in the input, the output '+' color 
is the one that *does not* form a '+' shape in the input.

If there are 2 unique non-white colors in the input, the output '+' color 
is always Azure (8).
"""

def _find_non_white_colors(grid):
    """
    Finds all unique non-white colors in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        set: A set of unique non-white color integers.
    """
    unique_colors = np.unique(grid)
    return set(color for color in unique_colors if color != 0)

def _check_plus_shape(grid, color):
    """
    Checks if a 3x3 '+' shape of the specified color exists anywhere in the grid.
    A '+' shape has the given color at the center and its 4 cardinal neighbors,
    and white (0) at the 4 corner positions relative to the center.

    Args:
        grid (np.ndarray): The input grid.
        color (int): The non-white color to check for.

    Returns:
        bool: True if at least one '+' shape of the given color is found, False otherwise.
    """
    rows, cols = grid.shape
    # Iterate through possible center points (r, c) of a 3x3 shape
    # We need to leave a 1-pixel border around the grid
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            # Check center pixel
            if grid[r, c] == color:
                # Check cardinal neighbors
                if (grid[r-1, c] == color and
                    grid[r+1, c] == color and
                    grid[r, c-1] == color and
                    grid[r, c+1] == color):
                    # Check corner neighbors (must be white)
                    if (grid[r-1, c-1] == 0 and
                        grid[r-1, c+1] == 0 and
                        grid[r+1, c-1] == 0 and
                        grid[r+1, c+1] == 0):
                        return True  # Found a plus shape
    return False # No plus shape found for this color

def transform(input_grid):
    """
    Transforms the input grid based on the presence of non-white colors
    and whether they form '+' shapes.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The 3x3 output grid with a '+' pattern.
    """
    
    # Convert input to numpy array for easier handling
    grid = np.array(input_grid, dtype=int)

    # Step 1: Identify the set of all unique non-white colors
    non_white_colors = _find_non_white_colors(grid)

    # Step 2: Count the number of unique non-white colors
    num_non_white_colors = len(non_white_colors)

    output_color = 0 # Default to white if logic fails or doesn't apply

    # Step 3: Determine the output_color based on the count
    if num_non_white_colors == 3:
        # Find the color that does NOT form a plus shape
        color_without_plus = -1 # Sentinel value
        found = False
        for color in non_white_colors:
            if not _check_plus_shape(grid, color):
                # Assuming exactly one color will not form a plus
                if found: 
                    # Error case: more than one color doesn't form a plus?
                    # Based on examples, this shouldn't happen. Defaulting for now.
                    print(f"Warning: Found multiple colors without '+' shapes ({color_without_plus}, {color}). Using the first found.")
                    break 
                color_without_plus = color
                found = True
        if found:
             output_color = color_without_plus
        else:
            # Error case: all 3 colors form a plus? Or no colors found?
             print("Warning: Could not find a unique color without a '+' shape among 3 non-white colors.")
             # Defaulting to 0, but could choose differently.

    elif num_non_white_colors == 2:
        # Output color is always Azure (8)
        output_color = 8
        
    # Handle other cases if necessary, currently defaults output_color to 0
    elif num_non_white_colors < 2 or num_non_white_colors > 3:
         print(f"Warning: Found {num_non_white_colors} non-white colors. Logic only defined for 2 or 3.")
         # Defaulting to 0, maybe a different strategy needed for other counts.
         output_color = 0


    # Step 4 & 5: Construct the 3x3 output grid initialized with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Step 6 & 7: Set the '+' shape pixels to the determined output_color
    if output_color != 0: # Only draw if a valid output color was determined
        output_grid[1, 1] = output_color  # Center
        output_grid[0, 1] = output_color  # Top
        output_grid[2, 1] = output_color  # Bottom
        output_grid[1, 0] = output_color  # Left
        output_grid[1, 2] = output_color  # Right

    # Step 8: Return the output grid
    return output_grid.tolist() # Return as list of lists per ARC standard