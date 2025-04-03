import collections
import numpy as np # Using numpy for potential future grid operations, although lists suffice here.

"""
This transformation rearranges elements of a 1D input grid based on the positions 
of a background color (0), a unique marker color (7), and a single contiguous 
object block of another color.

1. Identify the background color (0), marker color (7), and the object color 
   (the single color that is not 0 or 7).
2. Locate the contiguous block of the object color.
3. Find the index of the marker color (7).
4. Count the number of leading background pixels (L) at the start of the input.
5. Count the number of background pixels (N) immediately preceding the marker.
6. Count the number of background pixels (T) immediately following the marker.
7. Construct the output grid by concatenating:
    a. (L + N) background pixels.
    b. The object block.
    c. The marker pixel (7).
    d. T background pixels.
"""

# --- Helper Functions ---

def find_marker_index(grid, marker_color):
    """Finds the index of the first occurrence of the marker_color."""
    for i, pixel in enumerate(grid):
        if pixel == marker_color:
            return i
    return -1 # Should not happen based on task description

def find_object_block(grid, background_color, marker_color):
    """Finds the contiguous block of the object color."""
    object_color = -1
    start_index = -1
    end_index = -1

    # First pass to find the object color
    for pixel in grid:
        if pixel != background_color and pixel != marker_color:
            object_color = pixel
            break
    
    if object_color == -1:
        return [] # No object found

    # Second pass to find the block boundaries
    in_block = False
    object_block_list = []
    for i, pixel in enumerate(grid):
        if pixel == object_color and not in_block:
            start_index = i
            in_block = True
        elif pixel != object_color and in_block:
            end_index = i - 1
            break
    # Handle case where object block goes to the end of the grid
    if in_block and end_index == -1:
         end_index = len(grid) - 1
         
    if start_index != -1 and end_index != -1:
        return grid[start_index : end_index + 1]
    else:
        # Handle case where object might be a single pixel
        for i, pixel in enumerate(grid):
             if pixel == object_color:
                 return [pixel] # Return single pixel object
        return [] # Should not happen if object color was found


def count_leading_background(grid, background_color):
    """Counts consecutive background pixels from the start of the grid."""
    count = 0
    for pixel in grid:
        if pixel == background_color:
            count += 1
        else:
            break
    return count

def count_preceding_marker_background(grid, marker_index, background_color):
    """Counts consecutive background pixels immediately before the marker index."""
    count = 0
    idx = marker_index - 1
    while idx >= 0 and grid[idx] == background_color:
        count += 1
        idx -= 1
    return count

def count_trailing_background(grid, marker_index, background_color):
    """Counts consecutive background pixels immediately after the marker index."""
    count = 0
    idx = marker_index + 1
    while idx < len(grid) and grid[idx] == background_color:
        count += 1
        idx += 1
    return count

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the rearrangement transformation to the input grid.

    Args:
        input_grid (list): A list of integers representing the 1D input grid.

    Returns:
        list: A list of integers representing the transformed 1D output grid.
    """
    
    # Define constant colors
    background_color = 0
    marker_color = 7

    # 1. & 3. Identify marker and its index
    marker_index = find_marker_index(input_grid, marker_color)
    if marker_index == -1:
         # Handle error: marker not found, though examples guarantee it exists
         return [] # Or raise an error

    # 2. Find the object block
    object_block = find_object_block(input_grid, background_color, marker_color)
    if not object_block:
         # Handle error: object not found
         return [] # Or raise an error

    # 4. Count leading background pixels (L)
    leading_bg_count = count_leading_background(input_grid, background_color)

    # 5. Count background pixels immediately preceding the marker (N)
    preceding_marker_bg_count = count_preceding_marker_background(input_grid, marker_index, background_color)

    # 6. Count background pixels immediately following the marker (T)
    trailing_bg_count = count_trailing_background(input_grid, marker_index, background_color)

    # 7. Construct the output grid
    output_grid = []

    # 7a. Add (L + N) background pixels
    total_leading_bg = leading_bg_count + preceding_marker_bg_count
    output_grid.extend([background_color] * total_leading_bg)

    # 7b. Add the object block
    output_grid.extend(object_block)

    # 7c. Add the marker pixel
    output_grid.append(marker_color)

    # 7d. Add T background pixels
    output_grid.extend([background_color] * trailing_bg_count)

    return output_grid