```python
import numpy as np
from collections import Counter

"""
The transformation rule depends on the presence of the color Azure (8) in the input grid.

Rule 1: If Azure (8) is present in the input grid:
- Replace all pixels with the color Azure (8) with white (0).
- All other pixels remain unchanged.

Rule 2: If Azure (8) is NOT present in the input grid:
- Iterate through all possible 3x3 subgrids within the input grid.
- For each 3x3 subgrid:
    - Count the occurrences of each non-white color.
    - Find the non-white color 'C' that appears most frequently.
    - Check if this color 'C' is the unique most frequent non-white color (no ties for the highest frequency among non-white colors).
    - Check if the count of color 'C' is 6 or greater.
    - If both conditions (unique dominant color and count >= 6) are met:
        - In the corresponding 3x3 area of the output grid, replace any white (0) pixels with the dominant color 'C'. Note: Use the original input grid to identify the white pixels to change, but apply the change to the output grid.
- Pixels not part of such qualifying 3x3 squares, or non-white pixels within qualifying squares, remain unchanged.
"""

def transform(input_grid):
    """
    Applies the conditional transformation rule based on the presence of Azure (8).

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid_np = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # Check if Azure (color 8) is present
    azure_present = np.any(input_grid_np == 8)

    if azure_present:
        # Rule 1: Remove Azure pixels
        # Find all locations where the input grid has color 8
        azure_locations = (input_grid_np == 8)
        # Set those locations to white (0) in the output grid
        output_grid_np[azure_locations] = 0
    else:
        # Rule 2: Fill dense 3x3 squares
        # Iterate through all possible top-left corners (r, c) of 3x3 squares
        for r in range(height - 2):
            for c in range(width - 2):
                # Extract the 3x3 subgrid from the input
                subgrid = input_grid_np[r:r+3, c:c+3]

                # Count non-white colors in the subgrid
                non_white_pixels = subgrid[subgrid != 0]
                if non_white_pixels.size == 0:
                    continue # Skip if the subgrid is all white

                colors, counts = np.unique(non_white_pixels, return_counts=True)

                # Find the maximum count among non-white colors
                max_count = np.max(counts)

                # Check if the count threshold is met (>= 6)
                if max_count >= 6:
                    # Check if the maximum count is unique (only one color has this max count)
                    if np.sum(counts == max_count) == 1:
                        # Find the unique dominant color
                        dominant_color = colors[np.argmax(counts)]

                        # Identify white pixels within this 3x3 subgrid in the input
                        white_mask_in_subgrid = (subgrid == 0)

                        # Apply the dominant color to the corresponding white pixels in the output grid's subgrid
                        output_subgrid = output_grid_np[r:r+3, c:c+3]
                        output_subgrid[white_mask_in_subgrid] = dominant_color

    # Convert the final NumPy array back to a list of lists
    return output_grid_np.tolist()

```