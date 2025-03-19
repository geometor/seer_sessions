# 963e52fc • 018 • refine_coder

---
```python
"""
1.  **Identify Colored Bands:** Examine the input grid to determine if there's a *complete* horizontal or vertical band of alternating blue (1) and red (2) pixels. A complete band spans the entire width (for horizontal) or height (for vertical) of the grid. It is not enough for just two pixels to be present.
2. **Conditional Stretching:**
    *   **Horizontal Band:** If a complete horizontal band exists, stretch the grid horizontally by a factor of 2. Duplicate each column. This applies to *all* rows, including those not part of the colored band.
    *  **Vertical Band:** If a complete vertical band exists, stretch the grid vertically by a factor of 2. Duplicate each row. This applies to *all* columns including those not part of the colored band.
    *   **No Complete Band:** If neither a complete horizontal nor a complete vertical band exists, the output grid is identical to the input grid. There's no stretching.

3.  **Background:** The background (color 5, gray) is stretched along with the colored band if stretching occurs.
"""

import numpy as np

def _is_complete_alternating_band(row_or_col):
    """Checks if a row or column is a complete alternating band of 1s and 2s."""
    if not row_or_col.size:  # Empty row/column
        return False
    if row_or_col[0] != 1 and row_or_col[0] != 2:
        return False
    for i in range(row_or_col.size - 1):
        if row_or_col[i] == row_or_col[i+1] or (row_or_col[i] != 1 and row_or_col[i] != 2) or (row_or_col[i+1] != 1 and row_or_col[i+1] != 2):
            return False
    return True

def _find_complete_bands(grid):
    """Finds complete horizontal and vertical alternating bands."""
    rows, cols = grid.shape
    horizontal_band = None
    vertical_band = None

    # Check for complete horizontal band
    for r in range(rows):
        if _is_complete_alternating_band(grid[r]):
            horizontal_band = r
            break  # Only one complete band is needed

    # Check for complete vertical band (using transposed grid)
    transposed_grid = grid.T
    for c in range(cols):
        if _is_complete_alternating_band(transposed_grid[c]):
            vertical_band = c
            break  # Only one complete band is needed

    return horizontal_band, vertical_band

def transform(input_grid):
    """Transforms the input grid based on the presence of complete alternating bands."""
    rows, cols = input_grid.shape
    horizontal_band, vertical_band = _find_complete_bands(input_grid)

    # No complete band: return input as is
    if horizontal_band is None and vertical_band is None:
        return input_grid.copy()

    # Horizontal band: stretch horizontally
    if horizontal_band is not None:
        output_grid = np.zeros((rows, cols * 2), dtype=int)
        for r in range(rows):
            for c in range(cols):
                output_grid[r, 2 * c] = input_grid[r, c]
                output_grid[r, 2 * c + 1] = input_grid[r, c]
        return output_grid

    # Vertical band: stretch vertically
    if vertical_band is not None:
        output_grid = np.zeros((rows * 2, cols), dtype=int)
        for c in range(cols):
            for r in range(rows):
                output_grid[2 * r, c] = input_grid[r, c]
                output_grid[2 * r + 1, c] = input_grid[r, c]
        return output_grid
```
