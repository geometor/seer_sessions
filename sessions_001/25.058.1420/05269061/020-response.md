# 05269061 • 020 • refine_coder

---
```python
"""
Extends existing colored diagonals in the input grid, wrapping around the edges, and using the color sequence azure, green, yellow, repeating. The sequence starts from the existing color. The extension happens in both directions (down-right and up-left).
"""

import numpy as np

def get_next_color(color):
    color_sequence = [8, 3, 4]  # Azure, Green, Yellow
    try:
        index = color_sequence.index(color)
        next_index = (index + 1) % len(color_sequence)
        return color_sequence[next_index]
    except ValueError:
        return 0 # Should not reach here, as input is assumed to use colors from color_sequence

def get_previous_color(color):
    color_sequence = [8, 3, 4]  # Azure, Green, Yellow
    try:
        index = color_sequence.index(color)
        prev_index = (index - 1) % len(color_sequence)
        return color_sequence[prev_index]
    except ValueError:
        return 0 # Should not reach here

def transform(input_grid):
    """
    Transforms the input grid by extending the diagonal color patterns, starting from existing colors.
    Extends in both directions (down-right and up-left).
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)
    color_sequence = [8, 3, 4]  # Azure, Green, Yellow

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] in color_sequence:  # If the cell is part of the sequence
                current_color = input_grid[r,c]

                # Extend diagonally downwards and to the right
                next_r, next_c = r + 1, c + 1
                next_color = get_next_color(current_color)
                while True:
                    next_r = next_r % rows
                    next_c = next_c % cols
                    if next_r == r and next_c == c:
                        break #prevent infinite loop
                    if output_grid[next_r,next_c] == 0:
                        output_grid[next_r, next_c] = next_color
                    next_r += 1
                    next_c += 1
                    next_color = get_next_color(next_color)

                # Extend diagonally upwards and to the left
                prev_r, prev_c = r - 1, c - 1
                prev_color = get_previous_color(current_color)

                while True:
                    prev_r = prev_r % rows
                    prev_c = prev_c % cols

                    if prev_r == r and prev_c == c:
                        break #prevent infinite loop
                    
                    if output_grid[prev_r, prev_c] == 0:
                        output_grid[prev_r,prev_c] = prev_color

                    prev_r -= 1
                    prev_c -= 1
                    prev_color = get_previous_color(prev_color)


    return output_grid
```
