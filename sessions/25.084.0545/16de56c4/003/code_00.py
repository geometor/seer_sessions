"""
1.  **Reflect Rows:** The output grid is a reflection of the input grid. The reflection appears to happen by inverting the rows - the first row becomes the last, the second row becomes the second to last, and so on.
2.  **Color Change (Conditional):** In some cases, Maroon (color 9) is consistently transformed into Magenta (color 6) during or after reflection. It appears in example 1 and 2.
3. There is no horizontal expansion of colors.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Reflect rows
    output_grid = output_grid[::-1, :]

    # Apply color change (Maroon to Magenta)
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 9:
                output_grid[r, c] = 6

    return output_grid