# 05269061 • 018 • refine_coder

---
```python
"""
Extends existing colored diagonals in the input grid, wrapping around the edges, and using the color sequence azure, green, yellow, repeating. The sequence starts from the existing color.
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
    

def transform(input_grid):
    """
    Transforms the input grid by extending the diagonal color patterns, starting from existing colors.
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
                while 0 <= next_r < rows and 0 <= next_c < cols:
                    if output_grid[next_r,next_c] == 0:
                        output_grid[next_r, next_c] = next_color
                    next_r += 1
                    next_c += 1
                    next_color = get_next_color(next_color)

                #wrap
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


    return output_grid
```
