"""
1.  **Identify Separators:** Find all pixels with the color grey (5). These are the separators.
2.  **Left Region:** The region to the left of the *first* grey separator is the "left region". Replace all colors other than 5 (grey) in this region with 8 (azure).
3.  **Middle Region:** The region between the *first* and *last* grey separators is the "middle region". Replace all colors other than 5 within this region with 6 (magenta).
4.  **Right Region:** The region to the right of the *last* grey separator is the "right region". Replace all colors other than 5 within this region with 9 (maroon).
5. **Preserve Separator** The grey separators (5) remain unchanged.
6. **Single Separator:** If there is only a single grey separator, then the "middle region" does not exist.
"""

import numpy as np

def get_separator_indices(grid, separator_color=5):
    """Finds the column indices of separator pixels."""
    return np.where(grid == separator_color)[1]

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Separators
    separator_indices = get_separator_indices(input_grid)

    # Handle cases with no or one separator
    if len(separator_indices) == 0:
        return output_grid  # No separators, no change
    
    first_separator = separator_indices[0]
    last_separator = separator_indices[-1]

    # 2. Left Region
    output_grid[:, :first_separator] = 8

    # 3. Middle Region (only if there's more than one separator)
    if len(separator_indices) > 1:
        output_grid[:, first_separator + 1:last_separator] = 6

    # 4. Right Region
    output_grid[:, last_separator + 1:] = 9
    
    # 5. Preserve grey separators
    output_grid[input_grid == 5] = 5 # ensure separators are kept

    return output_grid