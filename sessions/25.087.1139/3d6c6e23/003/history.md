
Previous Code:
```python
"""
Transforms an input grid by performing a "gravity" operation on colored pixels.

1.  Identifies all unique non-background (non-white/0) colors in the input grid.
2.  For each color, counts its pixels, determines the column they occupy, and finds the lowest row index (max_row) of any pixel of that color.
3.  Sorts the colors based on their max_row in descending order (lowest in input goes to the bottom of the output).
4.  Initializes an output grid of the same size as the input, filled with the background color (0).
5.  Iterates through the sorted colors:
    a.  Calculates the required layer widths for the pyramid structure using a greedy approach: starting with the largest possible odd width layer that fits the remaining pixel count, then the next largest odd width for the remainder, and so on. Layers are stacked widest at the bottom, narrowest at the top.
    b.  Draws the layers for the current color onto the output grid, starting from the current available base row and moving upwards. The structure is centered horizontally based on the original column of the pixels.
    c.  Updates the available base row for the next structure to be stacked on top.
6.  Returns the final output grid.
"""

import numpy as np
from collections import defaultdict

def get_layer_widths(pixel_count):
    """
    Determines the odd widths of layers required to form a pyramid
    structure totaling pixel_count pixels. Uses a greedy approach,
    starting with the largest possible odd width layer.

    Args:
        pixel_count: The total number of pixels for the structure.

    Returns:
        A list of integers representing the odd widths of the layers,
        ordered from the top layer (narrowest) to the bottom layer (widest).
        e.g., for pixel_count=9, returns [1, 3, 5].
        e.g., for pixel_count=4, returns [1, 3].
        e.g., for pixel_count=5, returns [5].
    """
    layers_base_to_top = []
    remaining_pixels = pixel_count
    
    # Find potential odd layer widths <= pixel_count
    potential_widths = []
    w = 1
    while w <= pixel_count:
        potential_widths.append(w)
        w += 2

    # Greedily select largest possible odd widths starting from the largest potential
    for width in reversed(potential_widths):
        if remaining_pixels >= width:
            layers_base_to_top.append(width)
            remaining_pixels -= width
        if remaining_pixels == 0:
            break
            
    # Return layers ordered top-to-bottom (narrowest to widest)
    return list(reversed(layers_base_to_top))


def transform(input_grid):
    """
    Applies the gravity and pyramid formation transformation.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A numpy array representing the output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.zeros_like(input_np)

    # --- Step 1 & 2: Find colors, count pixels, find column and max_row ---
    color_data = defaultdict(lambda: {'coords': [], 'max_row': -1, 'col': -1})
    unique_colors = []

    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color != 0:  # If not background
                if color not in color_data:
                    unique_colors.append(color)
                color_data[color]['coords'].append((r, c))
                color_data[color]['max_row'] = max(color_data[color]['max_row'], r)
                # Assume all pixels of one color are in the same column
                if color_data[color]['col'] == -1:
                     color_data[color]['col'] = c
                # Optional: Add check if column changes for a color (error?)
                # elif color_data[color]['col'] != c:
                #     print(f"Warning: Color {color} found in multiple columns.")


    # Prepare data for sorting: list of (color, count, col, max_row)
    processed_colors = []
    for color in unique_colors:
        data = color_data[color]
        count = len(data['coords'])
        col = data['col']
        max_row = data['max_row']
        processed_colors.append({'color': color, 'count': count, 'col': col, 'max_row': max_row})

    # --- Step 3: Sort colors by max_row descending ---
    sorted_colors = sorted(processed_colors, key=lambda x: x['max_row'], reverse=True)

    # --- Step 4 & 5: Initialize output and draw structures ---
    current_base_row = height - 1 # Start drawing from the bottom row

    for item in sorted_colors:
        color = item['color']
        pixel_count = item['count']
        center_col = item['col']

        # --- Step 5a: Determine layer widths ---
        layer_widths = get_layer_widths(pixel_count) # Gets widths [top, ..., bottom] e.g. [1, 3, 5]

        # --- Step 5b & 5c: Draw layers onto output grid ---
        # Iterate through layers from bottom to top (widest to narrowest)
        # to place them correctly relative to current_base_row
        row_to_draw = current_base_row
        for layer_width in reversed(layer_widths): # Process [5, 3, 1] for example
            if row_to_draw < 0:
                 # Should not happen with valid inputs based on ARC constraints
                 print("Warning: Attempting to draw above grid top.")
                 break

            start_col = center_col - (layer_width // 2)
            end_col = start_col + layer_width # Slicing goes up to, but not including, end_col

            # Ensure drawing is within grid bounds horizontally
            draw_start_col = max(0, start_col)
            draw_end_col = min(width, end_col)
            
            # Check if the calculated slice is valid before applying
            if draw_start_col < draw_end_col and draw_start_col >= 0 and draw_end_col <= width:
                 output_grid[row_to_draw, draw_start_col:draw_end_col] = color
            else:
                 # This case might indicate an issue if shapes are expected to go off-grid
                 # or if calculations are wrong. For now, just print a warning.
                 print(f"Warning: Layer slice ({draw_start_col}:{draw_end_col}) out of bounds or invalid for row {row_to_draw}.")


            row_to_draw -= 1 # Move up for the next layer (narrower one)

        # Update the base row for the *next* structure to be stacked on top
        # The next structure starts one row above the top-most row just drawn
        current_base_row = row_to_draw


    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 7 7 7 7 7 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 7 7 7 0 0
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 3.8461538461538396

## Example 2:
Input:
```
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 7 7 7 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 7 7 7 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
```
0 0 0 0 4 0 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 7 7 7 0 0 0
0 0 6 6 6 6 6 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 7 7 7 0 0 0
0 0 6 6 6 6 6 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
**General Assessment**

The provided code successfully solves two out of the three training examples. The failure on the first example indicates a misunderstanding of how the pyramid shapes are constructed from the pixel counts.

The core logic of identifying colors, counting pixels, finding their original column, determining the lowest point (max row), sorting them by this lowest point (gravity), and stacking them seems correct based on examples 2 and 3 passing.

The error lies specifically in the `get_layer_widths` function. The initial implementation used a greedy approach, taking the largest possible odd width layer first. However, Example 1 demonstrates that for 9 pixels, the output should be layers of width 1, 3, and 5, not a single layer of width 9.

The revised hypothesis is that the shape construction depends on whether the pixel count is a perfect square:
1.  If the pixel count `N` is a perfect square (e.g., 1, 4, 9, 16...), the shape is a symmetric pyramid built from layers with widths `1, 3, 5, ..., 2*sqrt(N)-1`.
2.  If the pixel count `N` is *not* a perfect square, the shape is a single horizontal line of width `N`.

This revised logic correctly predicts the shapes in all three examples:
*   Example 1: 9 pixels (Orange). 9 is 3\*3 (perfect square). Layers: 1, 3, 5.
*   Example 2: 4 pixels (Orange). 4 is 2\*2 (perfect square). Layers: 1, 3.
*   Example 3:
    *   Yellow: 1 pixel. 1 is 1\*1 (perfect square). Layer: 1.
    *   Orange: 3 pixels. Not a perfect square. Layer: 3.
    *   Magenta: 5 pixels. Not a perfect square. Layer: 5.

The strategy is to modify the `get_layer_widths` function to implement this perfect square check and generate the appropriate layer widths based on the outcome.

**Metrics**


*code_execution:*
```python
import numpy as np
from collections import defaultdict
import math

# --- Data from the task ---
examples = [
    { # Example 1
        "input": [
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,7,0,0,0,0,0,0],
            [0,0,0,0,0,0,7,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,7,0,0,0,0,0,0],
            [0,0,0,0,0,0,7,0,0,0,0,0,0],
            [0,0,0,0,0,0,7,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,7,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,7,0,0,0,0,0,0],
            [0,0,0,0,0,0,7,0,0,0,0,0,0],
            [0,0,0,0,0,0,7,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
        ],
        "output": [
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,7,0,0,0,0,0,0], # layer width 1
            [0,0,0,0,0,7,7,7,0,0,0,0,0], # layer width 3
            [0,0,0,0,7,7,7,7,7,0,0,0,0], # layer width 5
        ]
    },
    { # Example 2
        "input": [
            [0,0,0,0,0,7,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,7,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,7,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,7,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
        ],
        "output": [
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,7,0,0,0,0,0], # layer width 1
             [0,0,0,0,7,7,7,0,0,0,0], # layer width 3
        ]
    },
    { # Example 3
        "input": [
            [0,0,0,0,4,0,0,0,0], # Yellow (4), col 4, row 0
            [0,0,0,0,7,0,0,0,0], # Orange (7), col 4, row 1
            [0,0,0,0,7,0,0,0,0], # Orange (7), col 4, row 2
            [0,0,0,0,7,0,0,0,0], # Orange (7), col 4, row 3
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,6,0,0,0,0], # Magenta (6), col 4, row 5
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,6,0,0,0,0], # Magenta (6), col 4, row 7
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,6,0,0,0,0], # Magenta (6), col 4, row 10
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,6,0,0,0,0], # Magenta (6), col 4, row 12
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,6,0,0,0,0], # Magenta (6), col 4, row 14
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
        ],
        "output": [
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,4,0,0,0,0], # Yellow Layer width 1
            [0,0,0,7,7,7,0,0,0], # Orange Layer width 3
            [0,0,6,6,6,6,6,0,0], # Magenta Layer width 5
        ]
    }
]

results = []

for i, ex in enumerate(examples):
    input_np = np.array(ex["input"], dtype=int)
    height, width = input_np.shape
    color_data = defaultdict(lambda: {'coords': [], 'max_row': -1, 'col': -1})
    unique_colors = []
    example_result = {'id': i + 1, 'colors': []}

    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color != 0:  # If not background
                if color not in color_data:
                    unique_colors.append(color)
                    color_data[color]['col'] = c # Assume first encounter sets the column
                color_data[color]['coords'].append((r, c))
                color_data[color]['max_row'] = max(color_data[color]['max_row'], r)


    processed_colors = []
    for color in unique_colors:
        data = color_data[color]
        count = len(data['coords'])
        col = data['col']
        max_row = data['max_row']
        # Check if pixel count is perfect square
        sqrt_count = math.isqrt(count)
        is_perfect_square = (sqrt_count * sqrt_count == count)

        processed_colors.append({'color': color, 'count': count, 'col': col, 'max_row': max_row, 'is_perfect_square': is_perfect_square})

    # Sort colors by max_row descending
    sorted_colors = sorted(processed_colors, key=lambda x: x['max_row'], reverse=True)
    example_result['sorted_colors_analysis'] = sorted_colors

    results.append(example_result)

print(results)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
[{'id': 1, 'colors': [], 'sorted_colors_analysis': [{'color': np.int64(7), 'count': 9, 'col': 6, 'max_row': 12, 'is_perfect_square': True}]}, {'id': 2, 'colors': [], 'sorted_colors_analysis': [{'color': np.int64(7), 'count': 4, 'col': 5, 'max_row': 9, 'is_perfect_square': True}]}, {'id': 3, 'colors': [], 'sorted_colors_analysis': [{'color': np.int64(6), 'count': 5, 'col': 4, 'max_row': 14, 'is_perfect_square': False}, {'color': np.int64(7), 'count': 3, 'col': 4, 'max_row': 3, 'is_perfect_square': False}, {'color': np.int64(4), 'count': 1, 'col': 4, 'max_row': 0, 'is_perfect_square': True}]}]

```
**Facts**


```yaml
task_context:
  description: Transform scattered pixels of the same color into stacked shapes at the bottom of the grid, influenced by their original vertical position and quantity.
  grid_properties:
    - size: Variable height and width (up to 30x30).
    - background: Color 0 (white) is the background and is ignored in processing.
input_objects:
  - type: PixelGroup
    properties:
      - color: Any color from 1-9.
      - pixels: Collection of individual pixels of the same color. Assumed to be in a single column per color in the input.
      - count: Total number of pixels for that color.
      - original_column: The column index where the pixels appear in the input.
      - max_row: The highest row index (lowest point) occupied by any pixel of that color in the input.
actions:
  - name: Identify Pixel Groups
    description: Find all unique non-background colors. For each color, determine its pixel count, original column index, and maximum row index (lowest point).
  - name: Sort Groups (Gravity)
    description: Order the identified pixel groups based on their `max_row` in descending order. Groups that were lower in the input grid will be processed first and end up at the bottom of the output stack.
  - name: Determine Output Shape
    description: For each pixel group, determine the shape based on its pixel count (`N`).
      - If `N` is a perfect square (1, 4, 9, 16,...), the shape is a symmetric pyramid with layers of width `1, 3, 5, ..., 2*sqrt(N)-1`.
      - If `N` is not a perfect square, the shape is a single horizontal line of width `N`.
  - name: Draw Shapes
    description: Create an empty output grid of the same dimensions as the input. Starting from the bottom row (`height - 1`), draw the shapes for each sorted pixel group.
    details:
      - Placement: Each shape is centered horizontally based on its `original_column`.
      - Stacking: Draw the first shape (lowest `max_row` in input) at the bottom of the output grid. Subsequent shapes are drawn directly on top of the previously drawn shape. The base row for the next shape is the row just above the topmost pixel of the previously drawn shape.
      - Layer Order (Pyramids): Pyramids (perfect square counts) are drawn layer by layer from bottom (widest) to top (narrowest).
output_objects:
  - type: StackedShapes
    properties:
      - Composed of shapes derived from the input PixelGroups.
      - Shapes are stacked vertically, ordered by the `max_row` of their corresponding input groups (descending).
      - Shapes are horizontally centered based on the `original_column` of their input group.
      - Shape structure (pyramid or line) depends on the pixel count being a perfect square or not.
```


**Natural Language Program**

1.  Initialize an empty output grid with the same dimensions as the input grid, filled with the background color (white, 0).
2.  Identify all unique non-background colored pixels in the input grid.
3.  For each unique color:
    a.  Count the total number of pixels (`N`) of this color.
    b.  Determine the column index (`original_column`) where these pixels appear (assuming all pixels of one color are in the same column).
    c.  Find the maximum row index (`max_row`) occupied by any pixel of this color.
    d.  Store this information (color, count `N`, `original_column`, `max_row`).
4.  Sort these color information records in descending order based on their `max_row`. This determines the stacking order in the output (lowest original pixels form the base).
5.  Set the initial `current_base_row` for drawing to the last row index of the grid (`height - 1`).
6.  Iterate through the sorted color records:
    a.  Get the color, count `N`, and `original_column` for the current record.
    b.  Determine the required layer widths for the shape:
        i.  Check if `N` is a perfect square.
        ii. If `N` is a perfect square, calculate the side length `s = sqrt(N)`. The layer widths are `[1, 3, 5, ..., 2*s - 1]` (from top to bottom).
        iii. If `N` is not a perfect square, the shape is a single layer with width `N`. The layer widths list is `[N]`.
    c.  Draw the shape onto the output grid:
        i.  Start drawing at the `current_base_row`.
        ii. Iterate through the determined layer widths from bottom (widest) to top (narrowest).
        iii. For each layer width `w`, calculate the horizontal start column: `start_col = original_column - (w // 2)`.
        iv. Draw a horizontal line of the current color with width `w` at the current drawing row, centered at `start_col`. Ensure drawing stays within grid bounds.
        v. Decrement the current drawing row index by 1 to move up for the next layer.
    d.  Update the `current_base_row` for the *next* shape to be the final drawing row index from step 6.c.v (which is one row above the top of the shape just drawn).
7.  Return the completed output grid.
