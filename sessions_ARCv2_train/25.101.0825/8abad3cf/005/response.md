```python
"""
Transforms an input grid based on color frequencies and arrangement rules.

1.  Analyzes the input grid to count occurrences of each color.
2.  Identifies three types of colors:
    a.  'dominant_color': The color appearing most frequently.
    b.  'pixel_color': Any color appearing exactly once (assumed to be at most one).
    c.  'block_colors': All other colors (count > 1, not dominant).
3.  Calculates the height 'H' for the output grid: H = (number of block colors) + (1 if pixel_color exists) + 1.
4.  For each block_color, calculates its width 'W_i' = floor(sqrt(count)).
5.  Determines the horizontal arrangement order of elements (pixel_color and block_colors):
    a.  If pixel_color exists: Order is [pixel_color] + [block_colors sorted descending by color index].
    b.  If no pixel_color exists: Order is [block_colors sorted ascending by color index].
6.  Calculates the total output width 'W_total' by summing element widths (1 for pixel_color, W_i for block_colors) and adding 1 for each gap between elements.
7.  Creates an output grid of size H x W_total, initially filled with the dominant_color.
8.  Places the elements into the output grid according to the order:
    a.  pixel_color is placed only at row H-1 in its column (width 1).
    b.  block_colors fill the entire H x W_i rectangle.
    c.  A 1-column gap filled with dominant_color separates adjacent elements.
"""

import math
import numpy as np
from collections import Counter

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the rules derived from examples.
    """
    input_array = np.array(input_grid, dtype=int)

    # Handle empty input grid
    if input_array.size == 0:
        return []

    # 1. Analyze Colors & Counts
    unique_colors, counts = np.unique(input_array, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    # Handle single color input grid
    if len(color_counts) == 1:
         # Rules imply no elements to place, resulting in zero width.
         # A grid with height > 0 and width 0 is represented as [[], [], ...]
         # Calculate height: H = 0 blocks + 0 pixel + 1 = 1
         return [[]] # Represents a 1x0 grid

    # 2. Identify Color Types
    dominant_color = max(color_counts, key=color_counts.get)

    pixel_color = None
    pixel_color_candidates = [color for color, count in color_counts.items() if count == 1]
    if pixel_color_candidates:
        pixel_color = pixel_color_candidates[0] # Assume only one

    block_colors = {}
    for color, count in color_counts.items():
        if color != dominant_color and color != pixel_color and count > 1:
             block_colors[color] = count

    # 3. Calculate Output Height
    output_height = len(block_colors) + (1 if pixel_color is not None else 0) + 1
    if output_height <= 0: # Should not happen with the +1, but safe check
        return []

    # 4. Calculate Block Widths
    block_widths = {color: math.floor(math.sqrt(count)) for color, count in block_colors.items()}

    # 5. Determine Arrangement Order
    ordered_elements = []
    if pixel_color is not None:
        sorted_block_colors = sorted(block_colors.keys(), reverse=True)
        ordered_elements = [pixel_color] + sorted_block_colors
    else:
        sorted_block_colors = sorted(block_colors.keys())
        ordered_elements = sorted_block_colors

    # 6. Calculate Output Width
    output_width = 0
    num_elements = len(ordered_elements)
    element_widths = {} # Store calculated width for each element in order

    if num_elements > 0:
        for i, element_color in enumerate(ordered_elements):
            width = 0
            if element_color == pixel_color:
                width = 1
            elif element_color in block_widths:
                 width = block_widths[element_color]
                 # If sqrt(count) < 1, width is 0. Don't place these blocks.
                 if width == 0:
                     continue # Skip elements with zero width for width calculation

            element_widths[element_color] = width # Store effective width
            output_width += width

            # Add gap width if not the last element AND current element has non-zero width
            if i < num_elements - 1 and width > 0 :
                 # Check if the *next* element also has non-zero width before adding gap
                 next_element_color = ordered_elements[i+1]
                 next_width = 1 if next_element_color == pixel_color else block_widths.get(next_element_color, 0)
                 if next_width > 0:
                     output_width += 1

    # Filter out elements with zero calculated width for placement
    elements_to_place = [(el, element_widths[el]) for el in ordered_elements if element_widths.get(el, 0) > 0]
    num_elements_to_place = len(elements_to_place)

    # Recalculate width based only on elements being placed
    output_width = 0
    if num_elements_to_place > 0:
        output_width = sum(w for _, w in elements_to_place) # Sum widths
        output_width += max(0, num_elements_to_place - 1) # Add gaps

    # Handle zero output width case
    if output_width <= 0:
         # Return list of empty lists matching the calculated height
         return [[] for _ in range(output_height)]

    # 7. Create Output Grid initialized with dominant color
    output_grid = np.full((output_height, output_width), dominant_color, dtype=int)

    # 8. Place Elements into the output grid
    current_col = 0
    for i, (element_color, width) in enumerate(elements_to_place):
        # Ensure width is positive (already filtered, but safe check)
        if width <= 0:
             continue

        # Check bounds before placing
        if current_col >= output_width:
            break # Should not happen if width calculation is correct

        if element_color == pixel_color:
            # Place pixel color at the bottom row of the current column
            if output_height > 0: # Ensure height is valid
                 output_grid[output_height - 1, current_col] = pixel_color
            # Only this single pixel is changed for the pixel_color element
        elif element_color in block_colors: # It's a block color
            # Place the block (fill H x W rectangle)
            # Ensure dimensions are valid before slicing
            if output_height > 0 and current_col + width <= output_width:
                output_grid[0:output_height, current_col:current_col + width] = element_color
            # else: Block won't fit (error in width calc or logic)

        # Advance column position by the width of the placed element
        current_col += width

        # Add gap if not the last element to be placed
        if i < num_elements_to_place - 1:
             # Ensure we don't advance past the calculated edge
            if current_col < output_width:
                 current_col += 1 # Skip one column for the gap

    # 9. Return Output as list of lists
    return output_grid.tolist()
```