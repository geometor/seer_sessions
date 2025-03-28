```python
import numpy as np

"""
Identifies the primary azure (8) structure, determines its bounding box and orientation (horizontal/vertical).
Creates an output grid initialized to white (0).
Copies the azure structure to the output grid.
Iterates through non-white (0), non-azure (8) pixels in the input grid.
For each such pixel, it determines a potential target projection location in the output grid, adjacent to the azure structure's bounding box based on the structure's orientation and the pixel's relative position.
Crucially, the projection only occurs if the input grid cell on the edge of the azure structure, directly corresponding to the target projection location, contains an azure (8) pixel.
- For a horizontal azure structure:
    - Pixels above (row < min_r) are potentially projected to row `min_r - 1`, column `c`. Projection happens only if `input_grid[min_r, c]` is 8.
    - Pixels below (row > max_r) are potentially projected to row `max_r + 1`, column `c`. Projection happens only if `input_grid[max_r, c]` is 8.
- For a vertical azure structure:
    - Pixels to the left (col < min_c) within the row span (`min_r <= row <= max_r`) are potentially projected to row `r`, column `min_c - 1`. Projection happens only if `input_grid[r, min_c]` is 8.
    - Pixels to the right (col > max_c) within the row span (`min_r <= row <= max_r`) are potentially projected to row `r`, column `max_c + 1`. Projection happens only if `input_grid[r, max_c]` is 8.
Overlapping projections overwrite previous values in the output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the refined azure structure projection rule.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_grid = np.zeros_like(input_np) # Initialize output with white (0)

    # 1. Identify the azure structure and its properties
    azure_coords = np.argwhere(input_np == 8)

    # Handle case where no azure pixels are found
    if azure_coords.size == 0:
        # Return the input grid unchanged if no azure structure exists
        return input_grid

    min_r, min_c = azure_coords.min(axis=0)
    max_r, max_c = azure_coords.max(axis=0)
    azure_height = max_r - min_r + 1
    azure_width = max_c - min_c + 1

    # Determine orientation (default to horizontal if square or single pixel)
    orientation = 'vertical' if azure_height > azure_width else 'horizontal'

    # 2. Create output grid (already done)

    # 3. Copy azure pixels to output grid
    for r, c in azure_coords:
        output_grid[r, c] = 8

    # 4. Examine every non-white, non-azure pixel and project it conditionally
    for r in range(rows):
        for c in range(cols):
            pixel_color = input_np[r, c]

            # Check if the pixel is neither white (0) nor azure (8)
            if pixel_color != 0 and pixel_color != 8:
                
                # Apply projection logic based on orientation
                if orientation == 'horizontal':
                    # Project pixels above the azure structure IF corresponding edge pixel is azure
                    if r < min_r and min_r > 0:
                        # Check if the azure structure pixel exists at (min_r, c)
                        if input_np[min_r, c] == 8:
                            output_grid[min_r - 1, c] = pixel_color
                    # Project pixels below the azure structure IF corresponding edge pixel is azure
                    elif r > max_r and max_r < rows - 1:
                         # Check if the azure structure pixel exists at (max_r, c)
                        if input_np[max_r, c] == 8:
                            output_grid[max_r + 1, c] = pixel_color
                
                elif orientation == 'vertical':
                    # Check if the pixel is within the row span of the azure structure
                    if min_r <= r <= max_r:
                        # Project pixels to the left of the azure structure IF corresponding edge pixel is azure
                        if c < min_c and min_c > 0:
                            # Check if the azure structure pixel exists at (r, min_c)
                            if input_np[r, min_c] == 8:
                                output_grid[r, min_c - 1] = pixel_color
                        # Project pixels to the right of the azure structure IF corresponding edge pixel is azure
                        elif c > max_c and max_c < cols - 1:
                            # Check if the azure structure pixel exists at (r, max_c)
                            if input_np[r, max_c] == 8:
                                output_grid[r, max_c + 1] = pixel_color

    # 5. Return the final output grid
    return output_grid.tolist()
```