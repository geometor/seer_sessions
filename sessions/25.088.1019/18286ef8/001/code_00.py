import numpy as np

"""
Transformation Rule:
1. Locate the unique magenta (6) pixel and the unique maroon (9) pixel in the input grid.
2. In the output grid, change the color of the magenta pixel to maroon.
3. Determine the relative direction from the maroon pixel to the magenta pixel (considering only the sign of the row and column differences).
4. Identify the gray (5) pixel adjacent (including diagonals) to the original maroon pixel in the calculated direction.
5. Swap the colors of the original maroon pixel and the identified adjacent gray pixel in the output grid. The original maroon pixel becomes gray, and the adjacent gray pixel becomes maroon.
"""

def find_pixel(grid, color):
    """Finds the coordinates (row, col) of the first pixel with the given color."""
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color:
                return r, c
    return None # Should not happen based on problem description

def sign(x):
    """Returns the sign of a number: -1 for negative, 1 for positive, 0 for zero."""
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    # Convert input to numpy array for easier manipulation and copying
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = output_grid.shape

    # 1. Locate the unique magenta (6) and maroon (9) pixels
    magenta_coord = find_pixel(input_np, 6)
    maroon_coord = find_pixel(input_np, 9)

    if magenta_coord is None or maroon_coord is None:
        # Should not happen based on examples, but good practice
        return input_grid # Return original if key pixels are missing

    r_mag, c_mag = magenta_coord
    r_mar, c_mar = maroon_coord

    # 2. In the output grid, change the color of the magenta pixel to maroon.
    output_grid[r_mag, c_mag] = 9

    # 3. Determine the relative direction from the maroon pixel to the magenta pixel.
    # Note: We want the direction *from* maroon *towards* magenta to find the adjacent gray.
    # However, the description derived it the other way. Let's stick to the derived logic:
    # dr = sign(r_mag - r_mar)
    # dc = sign(c_mag - c_mar)
    # The target swap location is then r_mar + dr, c_mar + dc
    dr = sign(r_mag - r_mar)
    dc = sign(c_mag - c_mar)

    # 4. Identify the gray (5) pixel adjacent to the original maroon pixel in the calculated direction.
    r_swap_target = r_mar + dr
    c_swap_target = c_mar + dc

    # 5. Swap the colors of the original maroon pixel and the identified adjacent gray pixel.
    # Check if the target swap coordinates are within grid bounds
    if 0 <= r_swap_target < height and 0 <= c_swap_target < width:
        # Check if the pixel at the target coordinates is indeed gray (5) in the *original* input
        if input_np[r_swap_target, c_swap_target] == 5:
            # Perform the swap in the output grid
            output_grid[r_swap_target, c_swap_target] = 9 # Gray becomes maroon
            output_grid[r_mar, c_mar] = 5               # Original maroon becomes gray
        else:
            # This case wasn't observed in the examples, implies an issue with the rule or input.
            # For now, we assume the target pixel is always gray.
            # If it's not gray, the current logic doesn't modify output_grid[r_mar, c_mar]
            # or output_grid[r_swap_target, c_swap_target] further than the magenta->maroon change.
             pass # Or raise an error, or handle differently if needed.
    else:
        # This case means the calculated swap target is outside the grid,
        # which also wasn't observed.
        pass # Or raise an error

    # Convert back to list of lists for the expected ARC format
    return output_grid.tolist()