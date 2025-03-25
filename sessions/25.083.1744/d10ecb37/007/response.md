```python
"""
The transformation rule identifies the first four distinct colors in the input grid, considering the order in which they first appear during a row-major scan, and uses them to form the 2x2 output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid into a 2x2 output grid based on the first four
    distinct colors encountered in a row-major scan.
    """
    distinct_colors = []
    seen_colors = set()

    # Iterate through the input grid row by row.
    for row in input_grid:
        # Iterate through the cells of each row.
        for cell_color in row:
            # Check if the color has been seen before.
            if cell_color not in seen_colors:
                # Add the color to the seen set and distinct colors list.
                seen_colors.add(cell_color)
                distinct_colors.append(cell_color)
                # Stop if four distinct colors have been found.
                if len(distinct_colors) == 4:
                    break
        if len(distinct_colors) == 4:
            break

    # Create the 2x2 output grid.
    if len(distinct_colors) == 4:
        output_grid = np.array(distinct_colors).reshape((2, 2))
    elif len(distinct_colors) > 0:
        output_grid = np.array(distinct_colors)  # Return what colors exist
    else:
        output_grid = np.array([])  # Return empty array

    return output_grid
```