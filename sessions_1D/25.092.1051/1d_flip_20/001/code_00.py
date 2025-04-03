import numpy as np
from collections import Counter

"""
Identifies a contiguous sequence of non-white pixels (the figure) in the single-row input grid. 
Within this figure, there is one pixel of a unique color and a block of pixels of another color. 
The transformation swaps the position of the unique pixel and the block of pixels within the figure's original location, leaving the background pixels unchanged.
"""

def find_figure_bounds(grid_row):
    """Finds the start and end indices of the contiguous non-white figure."""
    non_white_indices = [i for i, pixel in enumerate(grid_row) if pixel != 0]
    if not non_white_indices:
        return None, None
    return min(non_white_indices), max(non_white_indices)

def transform(input_grid):
    """
    Swaps a single unique-colored pixel with an adjacent block of same-colored pixels
    within a contiguous non-white sequence in a single-row grid.

    Args:
        input_grid (list): A list representing a single row grid.

    Returns:
        list: The transformed grid row.
    """
    # Ensure input is a list (representing the single row)
    if isinstance(input_grid, np.ndarray):
        grid_row = input_grid.tolist()
        if isinstance(grid_row[0], list): # Handle potential nested list from numpy array conversion
             grid_row = grid_row[0]
    elif isinstance(input_grid, list) and isinstance(input_grid[0], list):
         grid_row = input_grid[0] # Extract the single row if passed as a list of lists
    else:
         grid_row = list(input_grid) # Assume it's already a flat list or convert tuple/etc.

    # Initialize output_grid as a copy of the input row
    output_grid_row = list(grid_row)

    # Find the bounds of the non-white figure
    start_index, end_index = find_figure_bounds(grid_row)

    # If no figure is found, return the original grid
    if start_index is None:
        return [output_grid_row] # Return as list of lists for ARC standard

    # Extract the figure sequence
    figure = grid_row[start_index : end_index + 1]

    # Count the colors within the figure
    color_counts = Counter(figure)

    # Identify the unique pixel color and the block color
    unique_pixel_color = None
    block_color = None
    for color, count in color_counts.items():
        if count == 1:
            unique_pixel_color = color
        else:
            block_color = color # Assuming only two colors in the figure

    if unique_pixel_color is None or block_color is None:
        # This case shouldn't happen based on examples, but handle defensively
        return [output_grid_row] # Return original if figure structure is unexpected

    # Create the block sequence
    block_sequence = [block_color] * color_counts[block_color]

    # Determine the order in the original figure
    if figure[0] == unique_pixel_color:
        # Unique pixel is first
        new_figure = block_sequence + [unique_pixel_color]
    else:
        # Block is first
        new_figure = [unique_pixel_color] + block_sequence

    # Replace the original figure portion in the output grid with the new figure
    output_grid_row[start_index : end_index + 1] = new_figure

    # Return the transformed row, wrapped in a list to represent a 2D grid
    return [output_grid_row]