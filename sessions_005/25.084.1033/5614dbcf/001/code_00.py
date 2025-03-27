import numpy as np
from collections import Counter

"""
Transforms a 9x9 input grid to a 3x3 output grid by summarizing 3x3 subgrids.
The output cell color is the most frequent color in the corresponding 3x3 input subgrid,
excluding white (0) and gray (5). If no single dominant significant color exists
(meaning the subgrid only contained white and/or gray, or there was a tie among 
significant colors), the output cell is set to white (0).
"""

def get_dominant_color(subgrid):
    """
    Finds the most frequent significant color in a subgrid.

    Args:
        subgrid: A 2D numpy array representing the 3x3 subgrid.

    Returns:
        The integer color value of the most frequent significant color,
        or 0 (white) if no significant color exists, none is dominant,
        or there's a tie.
    """
    # Flatten the subgrid to easily count elements
    flat_subgrid = subgrid.flatten()

    # Count frequencies of all colors
    color_counts = Counter(flat_subgrid)

    # Filter out white (0) and gray (5)
    significant_counts = {color: count for color, count in color_counts.items() if color != 0 and color != 5}

    # If no significant colors are present
    if not significant_counts:
        return 0 # Return white

    # Find the maximum frequency among significant colors
    max_count = 0
    for count in significant_counts.values():
        if count > max_count:
            max_count = count

    # Find all colors that have the maximum frequency
    dominant_colors = [color for color, count in significant_counts.items() if count == max_count]

    # If there's a unique dominant color
    if len(dominant_colors) == 1:
        return dominant_colors[0]
    else:
        # Return white if there's a tie or no significant colors were dominant (handled implicitly)
        return 0

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input 9x9 grid.

    Returns:
        A list of lists representing the output 3x3 grid.
    """
    # Convert input to numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # Ensure input is 9x9 as expected by the rule derivation
    if input_height != 9 or input_width != 9:
        # Handle unexpected input dimensions if necessary, or raise error
        # For now, assume valid 9x9 input based on examples
        pass 

    output_height, output_width = input_height // 3, input_width // 3

    # Initialize output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input grid using 3x3 steps to define subgrids
    for r_out in range(output_height):
        for c_out in range(output_width):
            # Calculate the starting row and column for the subgrid
            r_start = r_out * 3
            c_start = c_out * 3
            
            # Extract the 3x3 subgrid
            subgrid = input_np[r_start:r_start+3, c_start:c_start+3]

            # Determine the dominant color for this subgrid
            dominant_color = get_dominant_color(subgrid)

            # Assign the determined color to the corresponding output cell
            output_grid[r_out, c_out] = dominant_color

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()