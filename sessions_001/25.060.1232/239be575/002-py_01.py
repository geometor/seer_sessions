"""
Analyzes an input grid and returns a single pixel value (0 or 8) based on the count of azure (8) pixels.

1.  **Analyze the input grid:** Count the number of pixels of each color (white, red, and azure).
2.  **Determine the output:**
    *   If the count of azure pixels is greater than or equal to 11, the output is azure (8).
    *   Otherwise, the output is white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the count of azure pixels.
    """
    # Count the number of azure (8) pixels.
    azure_count = np.count_nonzero(input_grid == 8)

    # Determine the output based on the azure count.
    if azure_count >= 11:
        output_pixel = 8
    else:
        output_pixel = 0

    return output_pixel