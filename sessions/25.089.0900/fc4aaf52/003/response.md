```python
"""
Transformation Rule:
1. Determine the background color by identifying the most frequent color in the input grid (expected to be azure, 8).
2. Identify all pixels in the input grid that are not the background color; these form the 'source object'. Collect their coordinates (row, col) and original colors.
3. Identify the set of unique colors present in the source object (expected to be exactly two distinct non-background colors).
4. Find the 'anchor pixel' of the source object: the pixel with the minimum row index, and among those, the minimum column index. Note its color ('anchor_color').
5. Determine the horizontal shift distance (`dx`) based on the `anchor_color`: if white (0), `dx` is 3; if blue (1), `dx` is 5.
6. Create a 'color map' dictionary: map the first non-background color found in the object to the second, and map the second back to the first.
7. Create a new output grid of the same dimensions as the input grid, filled entirely with the background color.
8. For each pixel from the source object at input coordinate (row, col) with an `original_color`:
    a. Look up its corresponding `mapped_color` using the color map.
    b. Calculate the target column: `new_col = col + dx`.
    c. If `new_col` is within the grid's width boundaries, set the pixel at coordinate (row, `new_col`) in the output grid to the `mapped_color`.
9. The resulting grid is the final output.
"""

import numpy as np
from collections import Counter

def find_object_pixels_and_colors(grid, background_color):
    """
    Finds all non-background pixels and the unique non-background colors.

    Args:
        grid (np.array): The input grid.
        background_color (int): The identified background color.

    Returns:
        tuple: A tuple containing:
            - list: A list of (row, col, color) tuples for each object pixel.
            - set: A set of unique non-background colors found.
            Returns ([], set()) if no object pixels are found.
    """
    height, width = grid.shape
    object_pixels = []
    object_colors = set()
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != background_color:
                object_pixels.append((r, c, color))
                object_colors.add(color)
    return object_pixels, object_colors

def find_anchor_pixel(object_pixels):
    """
    Finds the anchor pixel (top-most, then left-most) of an object.

    Args:
        object_pixels (list): A list of (row, col, color) tuples.

    Returns:
        tuple: The (row, col, color) of the anchor pixel, or None if list is empty.
    """
    if not object_pixels:
        return None

    min_row = min(p[0] for p in object_pixels)
    top_row_pixels = [p for p in object_pixels if p[0] == min_row]
    min_col = min(p[1] for p in top_row_pixels)

    # Find the specific pixel matching min_row and min_col
    for p in top_row_pixels:
        if p[1] == min_col:
            return p # Returns (row, col, color)

    return None # Should not happen if object_pixels is not empty

def get_shift_amount(anchor_color):
    """
    Determines the horizontal shift based on the anchor color.

    Args:
        anchor_color (int): The color of the anchor pixel.

    Returns:
        int: The horizontal shift distance (dx). Returns 0 if color is unmapped.
    """
    if anchor_color == 0: # white
        return 3
    elif anchor_color == 1: # blue
        return 5
    else:
        # Default or error case - return 0 shift if color not mapped
        print(f"Warning: Unhandled anchor color {anchor_color}, returning shift 0.")
        return 0

def create_color_swap_map(object_colors):
    """
    Creates a map to swap the two colors found in the object.

    Args:
        object_colors (set): A set containing the two unique non-background colors.

    Returns:
        dict: A dictionary mapping color_a -> color_b and color_b -> color_a.
              Returns an empty dict if not exactly two colors are provided.
    """
    if len(object_colors) != 2:
        print(f"Warning: Expected exactly 2 object colors, found {len(object_colors)}. Cannot create swap map.")
        return {}
    color_list = list(object_colors)
    return {color_list[0]: color_list[1], color_list[1]: color_list[0]}


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape

    # 1. Identify background color (most frequent)
    colors, counts = np.unique(input_grid_np, return_counts=True)
    background_color = colors[np.argmax(counts)]

    # 2. Find object pixels and their unique colors
    source_object_pixels, source_object_colors = find_object_pixels_and_colors(input_grid_np, background_color)

    # Handle cases where no object is found
    if not source_object_pixels:
        print("Warning: No object pixels found. Returning input grid.")
        return input_grid # Or return a grid filled with background_color

    # 3. Create the color swap map
    color_map = create_color_swap_map(source_object_colors)
    if not color_map:
         print("Warning: Could not create color map. Returning input grid.")
         return input_grid # Cannot proceed without a valid map

    # 4. Find the anchor pixel and its color
    anchor = find_anchor_pixel(source_object_pixels)
    if not anchor:
        # This case should technically be covered by the check for empty source_object_pixels
        print("Warning: Could not find anchor pixel. Returning input grid.")
        return input_grid
    anchor_color = anchor[2]

    # 5. Determine the horizontal shift (dx)
    dx = get_shift_amount(anchor_color)

    # 6. Create the output grid, initialized with background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # 7. Translate the object, applying the color swap
    for r, c, original_color in source_object_pixels:
        # a. Look up mapped color
        mapped_color = color_map.get(original_color, original_color) # Default to original if somehow not in map

        # b. Calculate new column
        new_c = c + dx

        # c. Place mapped color if within bounds
        if 0 <= new_c < width:
            output_grid[r, new_c] = mapped_color
        else:
             # Optional: Handle pixels moving out of bounds
             # print(f"Info: Pixel at ({r}, {c}) moved out of bounds to ({r}, {new_c}).")
             pass

    return output_grid.tolist()
```