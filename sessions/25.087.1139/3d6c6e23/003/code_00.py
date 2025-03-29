"""
Transforms an input grid by applying a gravity-like effect and reshaping pixel groups.

1.  Identifies unique non-background pixel colors in the input grid.
2.  For each color, counts its total pixels (N), finds the column index of its pixels (assuming they are all in one column), and determines the maximum row index (lowest point) of any pixel of that color.
3.  Sorts these color groups based on their maximum row index in descending order (lowest in input goes to the bottom of the output).
4.  Initializes an output grid of the same size as the input, filled with the background color (0).
5.  Iterates through the sorted color groups:
    a.  Determines the shape for the current color group based on its pixel count N:
        i.  If N is a perfect square (e.g., 1, 4, 9), the shape is a symmetric pyramid with layer widths [1, 3, 5, ..., 2*sqrt(N)-1] from top to bottom.
        ii. If N is not a perfect square, the shape is a single horizontal line of width N.
    b.  Draws the determined shape onto the output grid, starting from the current available base row and moving upwards. The shape is centered horizontally based on the original column of the pixels. Pyramids are drawn layer by layer, widest at the bottom.
    c.  Updates the available base row for the next shape to be stacked directly on top of the one just drawn.
6.  Returns the final output grid.
"""

import numpy as np
from collections import defaultdict
import math

def get_layer_widths(pixel_count):
    """
    Determines the widths of layers for the shape based on pixel count.

    Args:
        pixel_count: The total number of pixels (N) for the shape.

    Returns:
        A list of integers representing the widths of the layers,
        ordered from the top layer (narrowest) to the bottom layer (widest).
        - If N is a perfect square s*s, returns [1, 3, ..., 2*s-1].
        - If N is not a perfect square, returns [N].
    """
    sqrt_count_int = math.isqrt(pixel_count)
    if sqrt_count_int * sqrt_count_int == pixel_count:
        # Perfect square -> Pyramid shape
        side = sqrt_count_int
        # Generate widths: 1, 3, 5, ..., 2*side - 1
        return [2 * i - 1 for i in range(1, side + 1)]
    else:
        # Not a perfect square -> Line shape
        return [pixel_count]

def transform(input_grid):
    """
    Applies the gravity and shape formation transformation.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A numpy array representing the output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    # Step 1: Initialize output_grid
    output_grid = np.zeros_like(input_np)

    # Step 2 & 3: Find colors, count pixels, find column and max_row
    color_data = defaultdict(lambda: {'coords': [], 'max_row': -1, 'col': -1})
    unique_colors = []

    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color != 0:  # If not background
                if color not in color_data:
                    unique_colors.append(color)
                    # Assume all pixels of one color are in the same column, set on first encounter
                    color_data[color]['col'] = c
                color_data[color]['coords'].append((r, c))
                color_data[color]['max_row'] = max(color_data[color]['max_row'], r)
                # Optional: Add check if column changes for a color
                # elif color_data[color]['col'] != c:
                #     print(f"Warning: Color {color} found in multiple columns. Using first encountered column {color_data[color]['col']}.")


    # Prepare data for sorting: list of {'color', 'count', 'col', 'max_row'}
    processed_colors = []
    for color in unique_colors:
        data = color_data[color]
        count = len(data['coords'])
        col = data['col']
        max_row = data['max_row']
        processed_colors.append({'color': color, 'count': count, 'col': col, 'max_row': max_row})

    # Step 4: Sort colors by max_row descending (gravity)
    sorted_colors = sorted(processed_colors, key=lambda x: x['max_row'], reverse=True)

    # Step 5: Initialize drawing parameters
    current_base_row = height - 1 # Start drawing from the bottom row

    # Step 6: Iterate through sorted colors and draw shapes
    for item in sorted_colors:
        color = item['color']
        pixel_count = item['count']
        center_col = item['col'] # Original column acts as center

        # Step 6a & 6b: Determine layer widths based on pixel count
        layer_widths = get_layer_widths(pixel_count) # Gets widths [top, ..., bottom] e.g. [1, 3, 5] or [N]

        # Step 6c: Draw layers onto output grid
        # Iterate through layers from bottom to top (widest to narrowest)
        # to place them correctly relative to current_base_row
        row_to_draw = current_base_row
        for layer_width in reversed(layer_widths): # Process widest layer first
            if row_to_draw < 0:
                 # Avoid drawing above the grid
                 print(f"Warning: Attempting to draw color {color} above grid top (row {row_to_draw}). Skipping layer.")
                 break # Stop drawing layers for this color if it goes off top

            # Calculate horizontal placement centered around original column
            start_col = center_col - (layer_width // 2)
            end_col = start_col + layer_width # Numpy slice goes up to, but not including, end_col

            # Ensure drawing stays within grid bounds horizontally
            draw_start_col = max(0, start_col)
            draw_end_col = min(width, end_col)
            
            # Check if the calculated slice is valid before applying
            if draw_start_col < draw_end_col and 0 <= row_to_draw < height:
                 output_grid[row_to_draw, draw_start_col:draw_end_col] = color
            else:
                 # This case might indicate an issue if shapes are expected to go off-grid
                 # or if calculations are wrong. Print a warning.
                 print(f"Warning: Layer slice ({draw_start_col}:{draw_end_col}) out of bounds or invalid for row {row_to_draw}.")

            # Move up for the next layer (narrower one)
            row_to_draw -= 1 

        # Step 6d: Update the base row for the *next* structure to be stacked on top
        # The next structure starts one row above the top-most row just drawn
        current_base_row = row_to_draw

    # Step 7: Return the final grid
    return output_grid