```python
"""
This module transforms an input grid by identifying the least frequent non-background color, treating it as a 'frame color'. It then extracts all pixels of this frame color, determines their minimum bounding box, and creates a new output grid containing only these frame pixels (preserving their relative positions) on a white background. The output grid's size corresponds to the calculated bounding box.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Extracts a frame defined by the least frequent non-background color and 
    creates a minimal grid containing only that frame on a white background.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    background_color = 0

    # 1. Identify all unique non-background colors and their counts.
    unique_colors, counts = np.unique(input_array, return_counts=True)
    color_counts = Counter(dict(zip(unique_colors, counts)))

    # Remove background color from consideration
    if background_color in color_counts:
        del color_counts[background_color]

    # 2. Determine the "frame color" (least frequent non-background color).
    if not color_counts:
        # Handle case with only background color or empty input
        return [[background_color]] # Return a minimal 1x1 white grid

    # Find the color with the minimum count
    frame_color = min(color_counts, key=color_counts.get)

    # 3. Find coordinates of all frame color pixels.
    frame_pixels_coords = np.argwhere(input_array == frame_color)

    # 4. Handle case where no frame pixels are found (shouldn't happen if color_counts is not empty, but good practice).
    if frame_pixels_coords.shape[0] == 0:
         return [[background_color]] # Return a minimal 1x1 white grid

    # 5. Calculate the minimum bounding box.
    min_r = np.min(frame_pixels_coords[:, 0])
    max_r = np.max(frame_pixels_coords[:, 0])
    min_c = np.min(frame_pixels_coords[:, 1])
    max_c = np.max(frame_pixels_coords[:, 1])

    # 6. Calculate the height and width of the bounding box.
    h = max_r - min_r + 1
    w = max_c - min_c + 1

    # 7. Create a new output grid initialized with the background color.
    output_array = np.full((h, w), background_color, dtype=int)

    # 8. Place the frame pixels into the output grid, adjusting coordinates.
    for r, c in frame_pixels_coords:
        out_r = r - min_r
        out_c = c - min_c
        output_array[out_r, out_c] = frame_color

    # Convert back to list of lists for the required output format
    output_grid = output_array.tolist()

    return output_grid
```