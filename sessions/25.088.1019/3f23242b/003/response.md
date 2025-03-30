```python
import numpy as np

"""
Transforms the input grid based on the locations of green pixels (3).
The transformation involves two main stages applied sequentially:

1.  **Initial Row Fill**:
    *   Identify all unique rows that are exactly 2 rows below any green pixel in the input grid.
    *   For each such identified row, fill the entire row in the output grid with Red pixels (color 2).

2.  **Pattern Application**:
    *   For each green pixel found in the input grid (at `r_center`, `c_center`):
        *   Apply a fixed 5-row high pattern onto the output grid, conceptually centered at (`r_center`, `c_center`).
        *   The pattern is defined by relative coordinates (`dr`, `dc`) and specific colors (Gray=5, Red=2, Green=3, Azure=8).
        *   The pattern definition:
            *   Row dr=-2: Gray pixels from dc=-2 to dc=+2.
            *   Row dr=-1: Red at dc=-2, Gray at dc=0, Red at dc=+2.
            *   Row dr=0:  Red at dc=-2, Green at dc=0, Red at dc=+2.
            *   Row dr=+1: Red at dc=-2 and dc=+2.
            *   Row dr=+2: Red at dc=-4,-3, Azure from dc=-2 to dc=+2, Red at dc=+3,+4,+5.
        *   When applying the pattern, calculate the absolute coordinates (`target_r = r_center + dr`, `target_c = c_center + dc`).
        *   If the absolute coordinates are within the grid boundaries, place the pattern's color at that location in the output grid.
        *   This pattern application overwrites any pixels previously placed, including the initial Red fill from Stage 1 (specifically where `dr=+2` pattern elements fall) and any pixels from patterns centered on other green pixels.

The final output grid reflects the result after both stages are completed for all green pixels.
"""


def transform(input_grid):
    """
    Applies a pattern centered on each green pixel, first filling the 'dr=+2'
    rows with red, then drawing the specific patterns.

    Args:
        input_grid (list of lists of int): The input grid.

    Returns:
        list of lists of int: The transformed grid.
    """
    # Convert input grid to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output grid with white pixels (0)
    output_np = np.zeros_like(input_np)

    # Find coordinates of all green pixels (color 3)
    green_pixels = np.argwhere(input_np == 3)

    # Define the full pattern as a dictionary: { (relative_row, relative_col): color }
    # This defines the specific shape to be drawn centered on each green pixel.
    pattern_map = {
        # Row -2 relative to green center
        (-2, -2): 5, (-2, -1): 5, (-2, 0): 5, (-2, 1): 5, (-2, 2): 5,
        # Row -1 relative to green center
        (-1, -2): 2, (-1, 0): 5, (-1, 2): 2,
        # Row 0 (at green center)
        (0, -2): 2, (0, 0): 3, (0, 2): 2,
        # Row +1 relative to green center
        (1, -2): 2, (1, 2): 2,
        # Row +2 relative to green center
        (2, -4): 2, (2, -3): 2, (2, -2): 8, (2, -1): 8, (2, 0): 8,
        (2, 1): 8, (2, 2): 8, (2, 3): 2, (2, 4): 2, (2, 5): 2,
    }

    # --- Stage 1: Initial Red Fill for all 'dr=+2' rows ---
    # Identify all unique row indices that correspond to r_center + 2
    # for any green pixel, ensuring they are within grid height.
    dr_plus_2_rows = set()
    for r_center, c_center in green_pixels:
        target_r = r_center + 2
        if 0 <= target_r < height:
            dr_plus_2_rows.add(target_r)

    # Fill these identified rows entirely with Red (2) in the output grid.
    # This provides the background for the dr=+2 pattern row extension.
    for row_idx in dr_plus_2_rows:
        output_np[row_idx, :] = 2

    # --- Stage 2: Apply the specific pattern for each green pixel ---
    # Iterate through each green pixel found in the input
    for r_center, c_center in green_pixels:
        # Apply the full pattern defined in pattern_map, centered at this green pixel
        for (dr, dc), color in pattern_map.items():
            # Calculate absolute target coordinates in the output grid
            target_r = r_center + dr
            target_c = c_center + dc

            # Check if the calculated coordinates are within the grid boundaries
            if 0 <= target_r < height and 0 <= target_c < width:
                # Place the pattern pixel onto the output grid.
                # This overwrites any existing pixel, including the initial Red fill
                # from Stage 1 where dr=+2 pattern elements fall, and handles
                # overlaps between patterns from different green centers correctly
                # due to the sequential processing and overwrite nature.
                output_np[target_r, target_c] = color

    # Convert the final output numpy array back to a standard list of lists
    output_grid = output_np.tolist()
    return output_grid
```