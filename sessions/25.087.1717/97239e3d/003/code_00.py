import numpy as np
from collections import defaultdict
import math

"""
Transforms the input grid by identifying non-background 'marker' pixels (colors other than white 0 or azure 8), determining a bounding box for each marker color, expanding this box to align with a conceptual grid structure (boundaries at indices 0, 4, 8, 12, ...), and then filling only the white (0) pixels within the expanded box with the marker color in the output grid.
"""

def find_marker_pixels(grid):
    """
    Finds all pixels in the grid that are not white (0) or azure (8).

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        dict: A dictionary where keys are marker colors and values are lists
              of (row, col) tuples representing their locations.
    """
    markers = defaultdict(list)
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Marker colors are non-white (0) and non-azure (8)
            if color != 0 and color != 8:
                markers[color].append((r, c))
    return markers

def get_grid_boundaries(dimension_size):
    """
    Generates the boundary indices (0, 4, 8, ...) up to the dimension size.
    Includes 0 and the last index if not already covered.

    Args:
        dimension_size (int): The height or width of the grid.

    Returns:
        list: A sorted list of boundary indices.
    """
    boundaries = set([0]) # Always include 0
    for i in range(4, dimension_size, 4):
        boundaries.add(i)
    # Ensure the last index is conceptually a boundary end-point for range calculations
    # Although the expansion logic might not explicitly need dimension_size-1,
    # having the sequence 0, 4, 8... is the core need.
    # Let's just return the sequence 0, 4, 8... up to the dimension size.
    # The expansion logic will handle finding the correct boundary from this list.
    return sorted(list(boundaries))


def expand_bounding_box(min_r, max_r, min_c, max_c, row_boundaries, col_boundaries):
    """
    Expands an initial bounding box to align with grid boundaries.

    Args:
        min_r (int): Initial minimum row index.
        max_r (int): Initial maximum row index.
        min_c (int): Initial minimum column index.
        max_c (int): Initial maximum column index.
        row_boundaries (list): Sorted list of conceptual row boundary indices (0, 4, 8...).
        col_boundaries (list): Sorted list of conceptual col boundary indices (0, 4, 8...).

    Returns:
        tuple: (final_min_r, final_max_r, final_min_c, final_max_c)
    """
    # Find final_min_r: largest boundary <= min_r
    final_min_r = row_boundaries[0] # Default to 0
    for r_bound in row_boundaries:
        if r_bound <= min_r:
            final_min_r = r_bound
        else:
            break # Since boundaries are sorted

    # Find final_max_r: smallest boundary >= max_r
    final_max_r = row_boundaries[-1] # Default to last boundary
    # Need to consider the case where max_r exceeds the last calculated boundary
    # The conceptual block extends *up to* the next boundary.
    # Let's refine: find the smallest boundary R such that R > max_r, then the range is final_min_r to R-1.
    # Or: find the smallest boundary R such that R >= max_r. The range is final_min_r to R? Check examples.
    # Ex3 Orange: max_r=3 -> smallest boundary >= 3 is 4. Fill is 0-4. Final max_r = 4.
    # Ex3 Green: max_r=12 -> smallest boundary >= 12 is 12. Fill is 8-12. Final max_r = 12.
    # Ex1 Blue: max_r=16 -> smallest boundary >= 16 is 16. Fill is 12-16. Final max_r = 16.
    # Okay, the rule is: smallest boundary >= max_r
    for r_bound in reversed(row_boundaries):
         if r_bound >= max_r:
             final_max_r = r_bound
         else:
             # If no boundary is >= max_r, this means max_r is beyond the last boundary.
             # This case shouldn't happen if boundaries include 0 up to size. Let's assume it works.
             # Example: max_r = 17, boundaries [0, 4, 8, 12, 16]. Loop finds 16. Correct.
             break # Found the smallest boundary >= max_r

    # Re-evaluate final_max_r based on the "smallest boundary >= max_r" rule
    temp_final_max_r = -1
    for r_bound in row_boundaries:
        if r_bound >= max_r:
            temp_final_max_r = r_bound
            break
    # If max_r is larger than any boundary (e.g., grid size 17, max_r 17, boundaries end at 16)
    # The expansion should arguably go to the grid edge.
    # Let's adjust `get_grid_boundaries` to potentially include grid_dim-1.
    # Or adjust logic here: if no boundary found >= max_r, use grid_height - 1?
    # Let's stick to the boundary list. If max_r=16, boundary=16 is found.

    if temp_final_max_r != -1:
         final_max_r = temp_final_max_r
    else:
         # This case implies max_r is beyond the largest boundary index.
         # This shouldn't happen if boundaries cover the grid range implicitly.
         # Fallback or error? Let's assume the boundary list is sufficient.
         pass # Keep the default from reversed loop or handle error


    # Find final_min_c: largest boundary <= min_c
    final_min_c = col_boundaries[0]
    for c_bound in col_boundaries:
        if c_bound <= min_c:
            final_min_c = c_bound
        else:
            break

    # Find final_max_c: smallest boundary >= max_c
    final_max_c = col_boundaries[-1] # Default
    temp_final_max_c = -1
    for c_bound in col_boundaries:
        if c_bound >= max_c:
            temp_final_max_c = c_bound
            break
    if temp_final_max_c != -1:
        final_max_c = temp_final_max_c
    else:
        pass # Fallback or error

    return final_min_r, final_max_r, final_min_c, final_max_c


def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Identify all marker pixels and group them by color
    markers_by_color = find_marker_pixels(input_grid)

    # Get the conceptual grid boundary indices
    row_boundaries = get_grid_boundaries(height)
    col_boundaries = get_grid_boundaries(width)
    # Add grid dimension limits conceptually for max calculation if needed,
    # although slicing handles this. Let's see if the current boundaries work.


    # Process each marker color
    for color, locations in markers_by_color.items():
        if not locations:
            continue

        # Define the initial bounding box based on marker locations
        rows = [loc[0] for loc in locations]
        cols = [loc[1] for loc in locations]
        min_r = min(rows)
        max_r = max(rows)
        min_c = min(cols)
        max_c = max(cols)

        # Expand the bounding box to align with grid boundaries
        final_min_r, final_max_r, final_min_c, final_max_c = expand_bounding_box(
            min_r, max_r, min_c, max_c, row_boundaries, col_boundaries
        )

        # Fill the white pixels within the final fill rectangle in the output_grid
        # Note: range goes up to, but does not include, the stop value. Add 1 to max values.
        for r in range(final_min_r, final_max_r + 1):
            # Ensure row index is within grid bounds
            if 0 <= r < height:
                for c in range(final_min_c, final_max_c + 1):
                     # Ensure col index is within grid bounds
                     if 0 <= c < width:
                        # Check the color in the *original* input grid
                        if input_grid[r, c] == 0: # If white
                            output_grid[r, c] = color # Change output to marker color


    return output_grid