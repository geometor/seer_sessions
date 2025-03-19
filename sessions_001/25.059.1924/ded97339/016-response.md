# ded97339 • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Azure Pixels:** Locate all pixels with the value 8 (azure) in the input grid.
2.  **Process Each Row:** For each row in the grid:
    *   Check for Azure Pixels: Determine if the current row contains any azure pixels.
    *   If single azure pixel is found, go to next row.
    *   If any azure pixels are detected in the row: extend each group of isolated azure pixels horizontally to combine isolated pixels in the same row, forming a continuous horizontal line of azure pixels between the original pixels.
3. **Maintain all original object positions**, including original azure pixel positions.
4.  **Output:** Return the modified grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by connecting azure pixels horizontally within each row."""

    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for r in range(rows):
        # Find indices of azure pixels in the current row
        azure_indices = np.where(output_grid[r] == 8)[0]

        # If there are at least two azure pixels in the row, connect them
        if len(azure_indices) > 1:
            start = azure_indices[0]
            end = azure_indices[-1]
            output_grid[r, start:end+1] = 8  # Fill with azure

    return output_grid
```
