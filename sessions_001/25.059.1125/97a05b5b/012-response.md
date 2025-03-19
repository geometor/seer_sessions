# 97a05b5b • 012 • refine_coder

---
```python
"""
The transformation extracts horizontal bands of uniform color from the input grid and represents them as single-pixel-wide lines in the output grid. Each colored band in the input is mapped to a specific row in the output, with the color of the input band preserved. The height of the output grid corresponds to the number of distinct horizontal bands found in the input.
"""

import numpy as np

def get_horizontal_bands(grid):
    """
    Detects contiguous horizontal bands of non-zero colors.
    Returns a dictionary where keys are row numbers and values are (color, start_col, end_col) tuples.
    """
    bands = {}
    rows, cols = grid.shape
    for r in range(rows):
        current_color = 0
        start_col = -1
        for c in range(cols):
            if grid[r, c] != 0:
                if current_color == 0:
                    current_color = grid[r, c]
                    start_col = c
                elif grid[r, c] != current_color:
                    # End the previous band and start a new one
                    if current_color != 0:
                        bands[r] = (current_color, start_col, c - 1)
                    current_color = grid[r, c]
                    start_col = c
            elif current_color != 0:
                # End the current band
                bands[r] = (current_color, start_col, c - 1)
                current_color = 0
                start_col = -1
        # Handle the case where a band extends to the end of the row
        if current_color != 0:
            bands[r] = (current_color, start_col, cols - 1)
    return bands

def transform(input_grid):
    # Find horizontal bands in the input
    input_grid = np.array(input_grid)
    bands = get_horizontal_bands(input_grid)

    # Determine output grid size based on the number of bands
    output_height = len(bands)
    output_width = input_grid.shape[1]  # Keep output width same as input width, to reveal errors
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Map each band to a row in the output
    for i, (row, band_info) in enumerate(bands.items()):
        color, start_col, end_col = band_info
        #Simplified output, map to column index 4
        output_grid[i, 4] = color
    return output_grid
```
