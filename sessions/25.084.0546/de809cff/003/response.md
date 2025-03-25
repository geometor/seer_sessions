```python
"""
1.  **Identify Regions:** Identify contiguous regions of non-white (non-zero) pixels.

2.  **Boundary Detection:** For each region, examine its boundary pixels (pixels adjacent to a pixel of a different color or to the white(0) background).

3. **Color change based on neighbor**: Change lower value to azure. If a boundary pixel's value is not 0 and 8, and the neighboring pixel value is *higher*, change lower color to azure (8).

4. White(0) and azure(8) pixels should be skipped and unchanged in the first place.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on color adjacency rules at region boundaries.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # Iterate through each pixel
    for r in range(rows):
        for c in range(cols):
            current_color = input_grid[r, c]

            # Skip if the current pixel is white or azure
            if current_color == 0 or current_color == 8:
                continue

            # Check all eight neighbors
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue  # Skip the pixel itself

                    nr, nc = r + dr, c + dc

                    # Check if the neighbor is within bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbor_color = input_grid[nr, nc]

                        # Apply the color change rule: If neighbor is different and has *higher* value
                        if neighbor_color > current_color:
                            output_grid[r,c] = 8


    return output_grid
```