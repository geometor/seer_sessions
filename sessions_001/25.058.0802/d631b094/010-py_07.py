"""
1.  **Identify** all red (value '2') pixels in the input grid.
2.  **Count** the number of contiguous red pixels in the horizontal direction.
3. **Construct** output with all red pixels, arranged in a single row, preserving the horizontal contiguity.
4.  **Discard** all non-red pixels (in this case, only black pixels were present).
"""

import numpy as np

def _count_contiguous_red_pixels(row):
    """Counts contiguous red (value 2) pixels in a row."""
    count = 0
    current_run = 0
    for pixel in row:
        if pixel == 2:
            current_run += 1
        else:
            count = max(count, current_run)
            current_run = 0
    count = max(count, current_run)  # Handle runs at the end of the row
    return count

def transform(input_grid):
    # Find all red pixels and their coordinates.
    red_pixels = []
    for r_idx, row in enumerate(input_grid):
        for c_idx, pixel in enumerate(row):
            if pixel == 2:
                red_pixels.append((r_idx, c_idx))

    # Determine the lengths of contiguous red pixel groups
    contiguous_counts = []
    if red_pixels:
        for row in input_grid:
            contiguous_counts.append(_count_contiguous_red_pixels(row))
        
    max_contiguous = 0
    if (len(contiguous_counts) > 0):
      max_contiguous = max(c for c in contiguous_counts if c > 0)

    # Create the output grid.
    if max_contiguous > 0:
      output_grid = np.full((1, max_contiguous), 2)
    else:
      output_grid = np.array([[0]])

    return output_grid