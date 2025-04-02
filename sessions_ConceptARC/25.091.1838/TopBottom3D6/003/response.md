```python
"""
Transforms an input grid based on the following rules:
1. Find all unique non-white colors in the input grid.
2. For each color, determine its bounding box (min/max row/col), its dimensions (height, width), and the count of its pixels.
3. Identify colors whose bounding box height equals the input grid height.
4. If exactly one such color exists, select it as the target color.
5. If not (zero or multiple colors match the input height), find the maximum bounding box width among all non-white colors.
6. Identify all colors having this maximum width.
7. If exactly one such color exists, select it as the target color.
8. If multiple colors have the maximum width, select the one among them with the minimum pixel count.
9. Create an output grid whose dimensions match the bounding box dimensions (height, width) of the selected target color.
10. Fill the output grid entirely with the selected target color.
"""

import numpy as np
from collections import defaultdict

def find_bounding_box_and_pixels(grid_np, color):
    """
    Finds the minimum bounding box containing all pixels of a given color
    and counts the pixels of that color.

    Args:
        grid_np (np.array): The input grid as a numpy array.
        color (int): The color value to find.

    Returns:
        tuple: (min_r, min_c, max_r, max_c, height, width, pixel_count)
               Returns None for coords/dims if color not found, pixel_count is 0.
    """
    coords = np.argwhere(grid_np == color)
    pixel_count = coords.shape[0]

    if pixel_count == 0:
        return None, None, None, None, 0, 0, 0

    min_r, min_c = coords.min(axis=0)
    max_r, max_c = coords.max(axis=0)
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    return min_r, min_c, max_r, max_c, height, width, pixel_count

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a numpy array
    grid_np = np.array(input_grid, dtype=int)
    input_h, input_w = grid_np.shape

    # Find unique non-white colors and their properties
    unique_colors = np.unique(grid_np)
    non_white_colors = unique_colors[unique_colors != 0]

    if non_white_colors.size == 0:
        # Handle case with no non-white colors - return empty or based on spec
        return np.array([[]], dtype=int) # Return empty grid

    color_properties = {}
    for color in non_white_colors:
        min_r, min_c, max_r, max_c, height, width, pixel_count = find_bounding_box_and_pixels(grid_np, color)
        if pixel_count > 0:
            color_properties[color] = {
                "height": height,
                "width": width,
                "pixels": pixel_count
            }

    target_color = -1
    target_height = -1
    target_width = -1

    # --- Selection Logic ---

    # Criterion 1: Check for unique color with bounding box height matching input height
    full_height_colors = [
        color for color, props in color_properties.items()
        if props["height"] == input_h
    ]

    if len(full_height_colors) == 1:
        target_color = full_height_colors[0]
        target_height = color_properties[target_color]["height"]
        target_width = color_properties[target_color]["width"]
    else:
        # Criterion 2: Find max width among all colors
        max_width = 0
        for color, props in color_properties.items():
            if props["width"] > max_width:
                max_width = props["width"]

        max_width_colors = [
            color for color, props in color_properties.items()
            if props["width"] == max_width
        ]

        if len(max_width_colors) == 1:
            # If only one color has the max width, select it
            target_color = max_width_colors[0]
            target_height = color_properties[target_color]["height"]
            target_width = color_properties[target_color]["width"]
        elif len(max_width_colors) > 1:
            # Criterion 3 (Tie-breaking): Min pixel count among max-width colors
            min_pixels = float('inf')
            candidate_color = -1
            for color in max_width_colors:
                if color_properties[color]["pixels"] < min_pixels:
                    min_pixels = color_properties[color]["pixels"]
                    candidate_color = color
                # Optional: Add tie-breaking based on color index if pixel counts are also tied
                # elif color_properties[color]["pixels"] == min_pixels:
                #     if candidate_color == -1 or color < candidate_color: # Lower color index breaks tie
                #         candidate_color = color

            target_color = candidate_color
            if target_color != -1:
                target_height = color_properties[target_color]["height"]
                target_width = color_properties[target_color]["width"]
            else:
                 # This state should ideally not be reached if there are colors
                 return np.array([[]], dtype=int) # Failsafe


        else: # No non-white colors found (already handled) or issue finding max width
             return np.array([[]], dtype=int) # Failsafe

    # Check if a valid target was found
    if target_color == -1 or target_height <= 0 or target_width <= 0:
         # This case indicates an issue in logic or unexpected input
         # Maybe default to input or a specific small grid?
         print(f"Warning: Could not determine target color or dimensions. Target Color: {target_color}, H: {target_height}, W: {target_width}")
         return np.array([[]], dtype=int) # Failsafe empty grid


    # --- Output Generation ---
    # Create the output grid with the target dimensions and fill it with the target color
    output_grid = np.full((target_height, target_width), target_color, dtype=int)

    return output_grid
```