"""
Transforms an input grid based on color frequencies and arrangement rules.

1.  Analyzes the input grid to count occurrences of each color.
2.  Identifies three types of colors:
    a.  'dominant_color': The color appearing most frequently.
    b.  'pixel_color': Any color appearing exactly once (assumed to be at most one).
    c.  'block_colors': All other colors (count > 1, not dominant).
3.  Calculates the height 'H' for the output grid: H = (number of block colors) + (1 if pixel_color exists) + 1.
4.  For each block_color C_i, calculates its width 'W_i' = floor(sqrt(count of C_i)).
5.  Determines an initial horizontal arrangement order:
    a.  If pixel_color exists: Order is [pixel_color] + [block_colors sorted descending by color index].
    b.  If no pixel_color exists: Order is [block_colors sorted ascending by color index].
6.  Filters the initial order to create 'elements_to_place', keeping only elements with a non-zero width (1 for pixel_color, W_i > 0 for block_colors). Calculates the final output width 'W_total' based on the widths of elements_to_place and the gaps between them.
7.  Creates an output grid of size H x W_total, initially filled with the dominant_color. Handles cases where W_total is 0.
8.  Places the elements_to_place into the output grid according to the order:
    a.  pixel_color is placed only at row H-1 in its column.
    b.  block_colors fill rows 1 to H-1 within their allocated width W_i.
    c.  The top row (row 0) above a block_color remains the dominant_color, *except* for the very last element placed, *if* it is a block_color. In that specific case, the top row above the last block is filled with the last block's color.
    d.  A 1-column gap filled with dominant_color separates adjacent placed elements.
"""

import math
import numpy as np
from collections import Counter

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the derived rules.
    """
    input_array = np.array(input_grid, dtype=int)

    # Handle empty input grid
    if input_array.size == 0:
        return []

    # --- Step 1 & 2: Analyze Colors & Counts, Categorize Colors ---
    unique_colors, counts = np.unique(input_array, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    # Handle single color input grid
    if len(color_counts) == 1:
        # Only dominant color exists. No pixel, no blocks.
        # Height = 0 + 0 + 1 = 1. Width = 0.
        return [[]] # Represents a 1x0 grid

    dominant_color = max(color_counts, key=color_counts.get)

    pixel_color = None
    pixel_color_candidates = [color for color, count in color_counts.items() if count == 1]
    if pixel_color_candidates:
        pixel_color = pixel_color_candidates[0] # Assume only one

    block_colors = {}
    for color, count in color_counts.items():
        if color != dominant_color and color != pixel_color and count > 1:
             block_colors[color] = count

    # --- Step 3: Calculate Output Height ---
    output_height = len(block_colors) + (1 if pixel_color is not None else 0) + 1
    if output_height <= 0: # Safety check
        return []

    # --- Step 4: Calculate Block Widths ---
    block_widths = {color: math.floor(math.sqrt(count)) for color, count in block_colors.items()}

    # --- Step 5: Determine Initial Element Order ---
    ordered_elements_initial = []
    if pixel_color is not None:
        sorted_block_colors = sorted(block_colors.keys(), reverse=True)
        ordered_elements_initial = [pixel_color] + sorted_block_colors
    else:
        sorted_block_colors = sorted(block_colors.keys())
        ordered_elements_initial = sorted_block_colors

    # --- Step 6: Filter Elements & Calculate Output Width ---
    elements_to_place = []
    element_widths = {} # Store effective width (W > 0) for elements to be placed

    for element_color in ordered_elements_initial:
        width = 0
        if element_color == pixel_color:
            width = 1
        elif element_color in block_widths:
            width = block_widths[element_color]

        if width > 0: # Only consider elements with non-zero width
            elements_to_place.append(element_color)
            element_widths[element_color] = width

    num_elements_to_place = len(elements_to_place)
    output_width = 0
    if num_elements_to_place > 0:
        output_width = sum(element_widths[el] for el in elements_to_place) # Sum widths
        output_width += max(0, num_elements_to_place - 1) # Add gaps

    # --- Step 7: Create Output Grid ---
    if output_width <= 0:
         # Return list of empty lists matching the calculated height
         return [[] for _ in range(output_height)]

    output_grid = np.full((output_height, output_width), dominant_color, dtype=int)

    # --- Step 8: Place Elements ---
    current_col = 0
    last_element_info = None
    if elements_to_place:
         last_element_color = elements_to_place[-1]
         if last_element_color != pixel_color: # Check if last element is a block
              last_element_info = {'color': last_element_color}


    for i, element_color in enumerate(elements_to_place):
        width = element_widths[element_color] # Get pre-calculated positive width

        # Check bounds before placing (should be unnecessary if width calc is correct)
        if current_col >= output_width:
            break

        # Determine start and end columns for this element
        start_col = current_col
        end_col = current_col + width

        # --- Placement Logic ---
        if element_color == pixel_color:
            # Place pixel color only at the bottom row
            if output_height > 0:
                 output_grid[output_height - 1, start_col] = pixel_color
        elif element_color in block_colors: # It's a block color
            # Place the block in rows 1 to H-1
            if output_height > 1:
                 output_grid[1:output_height, start_col:end_col] = element_color

            # Special handling for the top row (row 0)
            if last_element_info and element_color == last_element_info['color']:
                 # If this is the last element AND it's a block, color the top row
                 output_grid[0, start_col:end_col] = element_color
            # Else (not the last element, or last element is pixel), top row remains dominant_color

        # --- Advance Column Position ---
        current_col += width

        # Add gap if not the last element to be placed
        if i < num_elements_to_place - 1:
            current_col += 1 # Skip one column for the gap

    # --- Step 9: Return Final Output ---
    return output_grid.tolist()