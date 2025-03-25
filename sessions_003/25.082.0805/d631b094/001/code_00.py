"""
1.  **Identify the non-zero color:** Scan the input grid to find the single color value that is not 0 (white).
2.  **Count Non-Zero Colors:** count the instances of the identified, non-zero color
3. **Create Output** create a 1 dimension grid where the length is the count of colors
"""

import numpy as np

def transform(input_grid):
    # Find the non-zero color
    non_zero_pixels = input_grid[input_grid != 0]
    if non_zero_pixels.size == 0:
        return np.array([])  # Return empty array if input is all zeros
    
    non_zero_color = non_zero_pixels[0]

    # Count the occurrences of the non-zero color
    count = np.sum(input_grid == non_zero_color)

    # Create a 1D output grid filled with the non-zero color
    output_grid = np.full((count,), non_zero_color)

    return output_grid