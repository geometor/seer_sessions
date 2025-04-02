import numpy as np

def find_fill_color(grid_row):
    """Finds the primary non-white (0), non-azure (8) color."""
    for pixel in grid_row:
        if pixel != 0 and pixel != 8:
            return pixel
    return None # Should not happen based on examples

def find_last_occurrence(grid_row, color):
    """Finds the index of the rightmost occurrence of a color."""
    indices = [i for i, pixel in enumerate(grid_row) if pixel == color]
    if not indices:
        return -1 # Color not found
    return max(indices)

def find_first_occurrence(grid_row, color):
    """Finds the index of the leftmost occurrence of a color."""
    try:
        return grid_row.index(color)
    except ValueError:
        return -1 # Color not found

def transform(input_grid):
    """
    Identifies a primary 'fill color' (non-white, non-azure) and an 'azure' (8) marker pixel in a 1D grid (row).
    Finds the rightmost pixel of the fill color and the leftmost azure pixel.
    Fills the gap between these two positions (exclusive of the azure pixel) with the fill color.
    """
    # Since ARC grids are lists of lists, even for 1D cases, extract the row.
    # Assuming input is always a single row based on examples.
    input_row = list(input_grid[0]) # Work with a mutable list copy
    output_row = list(input_row)   # Create a copy for modification

    # 1. Scan the input grid to identify the primary non-white, non-azure color (the "fill color").
    fill_color = find_fill_color(input_row)
    if fill_color is None:
        # Handle cases where no fill color is found (though unlikely based on examples)
        return input_grid # Return original if no transformation applicable

    # 2. Find the index (position) of the rightmost pixel that has the fill color.
    last_fill_index = find_last_occurrence(input_row, fill_color)

    # 3. Find the index (position) of the leftmost pixel that has the azure color (8).
    azure_index = find_first_occurrence(input_row, 8)

    # Check if both markers were found and in the expected order
    if last_fill_index != -1 and azure_index != -1 and last_fill_index < azure_index:
        # 5. Iterate through the indices of the output grid from last_fill_index + 1 up to (but not including) azure_index.
        for i in range(last_fill_index + 1, azure_index):
            # 6. For each index in this range, set the pixel color in the output grid to the identified "fill color".
            # Check if the pixel to change is currently white (optional, but matches pattern)
            # if output_row[i] == 0: # Only change white pixels - safer based on desc.
            output_row[i] = fill_color

    # 7. Return the modified output grid (wrapping the row back into a list of lists).
    return [output_row]