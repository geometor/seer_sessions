"""
This program counts the number of distinct horizontal line segments of Green (3)
and Red (2) colors in the input grid. It then represents these counts in a
fixed 2x3 output grid. The output grid is filled sequentially: first with
Green pixels equal to the count of Green segments, then with Red pixels equal
to the count of Red segments. Any remaining cells are filled with White (0).
"""

import numpy as np

def find_horizontal_segments(grid, color):
    """
    Finds and counts distinct horizontal segments of a given color.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        int: The count of distinct horizontal segments of the specified color.
    """
    rows, cols = grid.shape
    count = 0
    visited = np.zeros_like(grid, dtype=bool) # Keep track of visited pixels within segments

    for r in range(rows):
        for c in range(cols):
            # Check if this pixel is the start of a new segment of the target color
            if not visited[r, c] and grid[r, c] == color:
                # Check if it's the beginning of a horizontal line
                # (either at the left edge or the pixel to the left is different)
                if c == 0 or grid[r, c-1] != color:
                    count += 1
                    # Mark all pixels in this segment as visited to avoid recounting
                    current_c = c
                    while current_c < cols and grid[r, current_c] == color:
                        visited[r, current_c] = True
                        current_c += 1
    return count

def transform(input_grid):
    """
    Counts Green (3) and Red (2) horizontal line segments in the input_grid
    and represents the counts in a 2x3 output grid.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The 2x3 output grid representing the counts.
    """
    input_array = np.array(input_grid, dtype=int)

    # Count the number of green and red horizontal segments
    green_line_count = find_horizontal_segments(input_array, 3)
    red_line_count = find_horizontal_segments(input_array, 2)

    # Initialize the 2x3 output grid with white (0)
    output_grid = np.zeros((2, 3), dtype=int)

    # Define the filling sequence coordinates
    fill_coords = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    
    current_index = 0

    # Fill with green pixels
    for _ in range(green_line_count):
        if current_index < len(fill_coords):
            r, c = fill_coords[current_index]
            output_grid[r, c] = 3
            current_index += 1
        else:
            break # Stop if we exceed the output grid size

    # Fill with red pixels
    for _ in range(red_line_count):
        if current_index < len(fill_coords):
            r, c = fill_coords[current_index]
            output_grid[r, c] = 2
            current_index += 1
        else:
            break # Stop if we exceed the output grid size

    # Convert back to list of lists for the required output format
    return output_grid.tolist()