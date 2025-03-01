# 3aa6fb7a • 010 • refine_coder

---
```python
"""
Azure pixels are changed to blue based on adjacency to white pixels. If an azure region is
adjacent to a white pixel either above the left-most pixel, or to the
left of the top-most pixel, the *entire* contiguous block of azure pixels is changed to blue.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Create a visited grid to track processed azure pixels.
    visited = np.zeros((rows, cols), dtype=bool)

    def get_azure_region(r, c, region):
        """
        Recursively finds a contiguous region of azure pixels.
        """
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            visited[r, c] or input_grid[r, c] != 8):
            return

        visited[r, c] = True
        region.append((r, c))

        # Explore adjacent pixels
        get_azure_region(r + 1, c, region)
        get_azure_region(r - 1, c, region)
        get_azure_region(r, c + 1, region)
        get_azure_region(r, c - 1, region)


    # Iterate through each pixel in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is azure (8) and hasn't been visited
            if input_grid[r, c] == 8 and not visited[r, c]:
                # Find the contiguous azure region
                azure_region = []
                get_azure_region(r, c, azure_region)

                # Find left-most and top-most pixels in the region
                leftmost_col = min(pixel[1] for pixel in azure_region)
                topmost_row = min(pixel[0] for pixel in azure_region)

                # Determine the corresponding pixels for trigger conditions
                leftmost_pixels = [(row, col) for row, col in azure_region if col == leftmost_col]
                topmost_pixels =  [(row, col) for row, col in azure_region if row == topmost_row]
                
                leftmost_pixel = min(leftmost_pixels) # in case of multiple left, take top one
                topmost_pixel = min(topmost_pixels)  # in case multiple top, take left one

                # Check trigger conditions
                trigger_above = (leftmost_pixel[0] > 0) and (input_grid[leftmost_pixel[0] - 1, leftmost_pixel[1]] == 0)
                trigger_left = (topmost_pixel[0] > 0) and  (input_grid[topmost_pixel[0], topmost_pixel[1] - 1] == 0)

                # Transform the entire region if triggered
                if trigger_above or trigger_left:
                    for row, col in azure_region:
                        output_grid[row, col] = 1

    return output_grid
```
