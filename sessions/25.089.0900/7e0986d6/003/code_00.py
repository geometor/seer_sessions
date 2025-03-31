import numpy as np
from collections import Counter

"""
Identifies the non-background color (any color other than 0) that appears least 
frequently in the input grid. Replaces all instances of this least frequent 
non-background color with the background color (0). All other pixels retain 
their original colors.
"""

def find_least_frequent_non_background_color(grid):
    """
    Finds the non-background color with the minimum count in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        int or None: The color value with the minimum count, or None if no
                     non-background colors are present or only one exists.
                     If multiple colors share the minimum count, returns one of them.
    """
    # Flatten the grid to easily count colors
    flat_grid = grid.flatten()

    # Count occurrences of each color
    color_counts = Counter(flat_grid)

    # Filter out the background color (0)
    non_background_counts = {color: count for color, count in color_counts.items() if color != 0}

    # If there are no non-background colors, return None
    if not non_background_counts:
        return None

    # Find the color with the minimum count among non-background colors
    # Using min() with a lambda function is a concise way to find the key (color)
    # associated with the minimum value (count) in the dictionary.
    least_frequent_color = min(non_background_counts, key=non_background_counts.get)
    
    return least_frequent_color

def transform(input_grid):
    """
    Transforms the input grid by replacing the least frequent non-background
    color with the background color (0).
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)

    # Find the target color (least frequent non-background color)
    target_color = find_least_frequent_non_background_color(input_np)

    # If no non-background colors exist or only one does,
    # or target_color is None for any reason, return the original grid copy
    if target_color is None:
        # Return a copy to avoid modifying the original input list outside the function
        return [row[:] for row in input_grid] 

    # Create the output grid as a copy of the input grid
    # We will modify this copy
    output_np = np.copy(input_np)

    # Identify the background color (assumed to be 0)
    background_color = 0

    # Replace all instances of the target color with the background color
    # Using boolean indexing for efficiency
    output_np[output_np == target_color] = background_color

    # Convert the NumPy array back to a list of lists for the final output
    output_grid = output_np.tolist()

    return output_grid